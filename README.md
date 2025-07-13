# 🌿 GCT Case Study – CO₂ Plant Data Pipeline (By Vijay)

## 👋 Introduction

This project is part of the GCT Case Study Challenge, where I’ve built a fully functional data pipeline that simulates a CO₂ capturing plant's sensor system. My goal was to ingest real-time data, structure it in the cloud, and automatically process it — using only AWS free-tier tools.

This README documents my process, tools, and how the system works end-to-end.

---

## 🧪 Project Summary

- **Sensor Simulation**: 8 virtual sensors generate data every 10 seconds.
- **Data Format**: NDJSON (each line = one reading).
- **Storage**: Every 1 minute, a file containing 6 readings is created.
- **Upload**: Each file is saved to both local disk and S3 using Node-RED.
- **Trigger**: AWS Lambda processes every new file uploaded to S3.
- **Output**: A summary file with stats and alerts is saved to a second S3 bucket.
- **Dashboard**: Data visualized using AWS Glue, Athena, and QuickSight.

---

## 🔧 Tools I Used

| Tool            | Why I Used It                         |
| --------------- | ------------------------------------- |
| **Node-RED**    | To generate and send JSON sensor data |
| **AWS S3**      | For cloud storage (raw + processed)   |
| **AWS Lambda**  | For automatic processing + alerting   |
| **AWS Glue**    | Crawling processed data               |
| **AWS Athena**  | Querying processed data               |
| **QuickSight**  | Dashboard visualization               |
| **Python 3.12** | Lambda runtime and scripting          |

---

## 📁 Folder Structure in S3

### Input: `co2-plant-raw-data`

```
raw/
  └── Year YYYY/
      └── Month MM/
          └── Day DD/
              └── HH/
                  └── sensor_HHMM.json
```

Each JSON file contains 6 lines like this:

```json
{"timestamp":"...","pH":"7.5",...,"co2":"410.0"}
```

---

### Output: `co2-plant-processed-data`

```
processed/
  └── sensor_HHMM_summary.json
```

Each summary file looks like this:

```json
{
  "source_file": "raw/Year.../sensor_0832.json",
  "summary": {
    "pH": {"mean": 7.2, "std_dev": 0.4},
    "temperature": {"mean": 25.3, "std_dev": 1.8}
  },
  "alert_flags": [
    "⚠️ ALERT: pH = 5.8 at 2025-07-12T08:13:40Z"
  ]
}
```

---

## ⚙️ Lambda: What It Does

Whenever a file is uploaded to `raw/` in S3:

1. **Reads** the file line by line.
2. **Parses** each reading.
3. **Calculates** mean and standard deviation for each sensor.
4. **Checks** if any value crosses alert thresholds.
5. **Saves** a summary file in `co2-plant-processed-data`.

Thresholds for alerts:

| Sensor        | Rule                  |
| ------------- | --------------------- |
| `pH`          | `< 6.0 or > 8.5`      |
| `temperature` | `< 5°C or > 40°C`     |
| `pressure`    | `< 1 bar or > 10 bar` |
| `co2`         | `< 300 or > 1000 ppm` |

---

## 🧠 What I Learned

- Working with AWS Lambda triggers and permissions (IAM).
- Handling race conditions in S3 file availability.
- Structuring data in the cloud for long-term storage and scalability.
- Debugging tricky JSON issues with newline-delimited formats.
- Using Glue + Athena to power dashboard queries.
- Creating QuickSight visuals directly from Lambda output.

---

## 🚧 Improvements I’m Planning

- Add unit tests for the Lambda function.
- Push alerts to a dashboard or SNS topic.
- Automatically visualize processed stats in Grafana or QuickSight.
- Replace hardcoded alert rules with config stored in S3 or DynamoDB.

---

## 📂 Repository Structure (Suggested)

```
📁 node-red/
  └── gct-flow.json                              ← Node-RED flow export
📁 lambda/
  └── lambda_function.py                         ← Processing script
📁 samples/
  └── sensor_sample.json                         ← Sample input file
📁 screenshots/
  └── *.png                                      ← Visual evidence (Node-RED UI, Glue, Athena, QuickSight)
📄 README.md                                     ← This file   
📄 Case Study Data & Process Analytics.pdf       ← This file 
📄 Vijay_Presentation.pptx                       ← This file
```

---

## 🤝 About Me

Hi! I’m Vijay. This case study was a great hands-on experience where I learned to think like a systems integrator — working with real-time data, serverless compute, and cloud architecture, all from the ground up.

If you’re reviewing this repo, feel free to reach out. Feedback is welcome!

