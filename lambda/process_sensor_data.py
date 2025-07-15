import boto3
import json
import statistics

s3 = boto3.client('s3')
PROCESSED_BUCKET = 'co2-plant-processed-data'

# Define out-of-range rules (optional: customize thresholds)
ALERT_RULES = {
    "pH": lambda v: float(v) < 6.0 or float(v) > 8.5,
    "temperature": lambda v: float(v) > 40 or float(v) < 5,
    "pressure": lambda v: float(v) < 1 or float(v) > 10,
    "co2": lambda v: float(v) > 1000 or float(v) < 300
    # You can add more as needed
}

def lambda_handler(event, context):
    # Extract bucket and object key
    try:
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
    except Exception as e:
        print(f" Error reading event: {e}")
        return {"status": "error", "message": str(e)}

    print(f" Processing file: s3://{bucket}/{key}")

    # Read and parse file from S3
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        content = response['Body'].read().decode('utf-8')
        lines = content.strip().splitlines()
        readings = [json.loads(line) for line in lines]
    except Exception as e:
        print(f" Error reading file: {e}")
        return {"status": "error", "message": str(e)}

    # Sensors to process
    sensors = ["pH", "conductivity", "pressure", "temperature", "fillLevel", "flow", "humidity", "co2"]

    stats = {}
    alerts = []

    # Process each sensor
    for sensor in sensors:
        try:
            values = [float(r[sensor]) for r in readings if sensor in r]
            if not values:
                continue

            mean = round(statistics.mean(values), 2)
            stddev = round(statistics.stdev(values), 2) if len(values) > 1 else 0

            stats[sensor] = {
                "mean": mean,
                "std_dev": stddev
            }
        except Exception as e:
            print(f" Skipping sensor {sensor}: {e}")

    # Check for out-of-range alerts
    for reading in readings:
        for sensor, rule in ALERT_RULES.items():
            if sensor in reading:
                value = float(reading[sensor])
                if rule(value):
                    alerts.append(f" ALERT: {sensor} = {value} at {reading.get('timestamp')}")

    # Print summary
    print("\n Aggregated Sensor Stats:")
    for sensor, result in stats.items():
        print(f"  {sensor} → mean: {result['mean']}, std_dev: {result['std_dev']}")

    # Print alerts
    if alerts:
        print("\n🚨 Alerts Detected:")
        for alert in alerts:
            print(alert)
    else:
        print("\n✅ No alerts found.")

    # Save processed summary to new bucket
    output_filename = key.split("/")[-1].replace(".json", "_summary.json")
    output_key = f"processed/{output_filename}"

    summary_output = {
        "source_file": key,
        "summary": stats,
        "alert_flags": alerts
    }

    try:
        s3.put_object(
            Bucket=PROCESSED_BUCKET,
            Key=output_key,
            Body=json.dumps(summary_output),
            ContentType='application/json'
        )
        print(f"\n Processed summary saved to: s3://{PROCESSED_BUCKET}/{output_key}")
    except Exception as e:
        print(f" Failed to write processed summary: {e}")


    return {
        "status": "success",
        "summary": stats,
        "alerts": alerts
    }