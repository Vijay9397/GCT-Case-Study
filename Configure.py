import os
import time
import boto3
import hashlib

# ======= CONFIGURATION =======
BUCKET_NAME = 'co2-plant-raw-data'
LOCAL_ROOT = r'C:\Users\vijay\Desktop\GCT Project\raw'
UPLOAD_INTERVAL_SECONDS = 60
# =============================

s3 = boto3.client('s3')

# Memory store of uploaded file hashes
uploaded_hashes = set()

def file_hash(path):
    try:
        with open(path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception as e:
        print(f"❌ Could not hash file {path}: {e}")
        return None

def upload_new_files():
    for root, _, files in os.walk(LOCAL_ROOT):
        for file in files:
            # Only upload .json files
            if not file.lower().endswith('.json'):
                continue

            full_path = os.path.join(root, file)
            file_id = file_hash(full_path)
            if file_id is None or file_id in uploaded_hashes:
                continue

            # S3 key
            rel_path = os.path.relpath(full_path, LOCAL_ROOT).replace("\\", "/")
            s3_key = f'raw/{rel_path}'

            try:
                print(f"📤 Uploading: {full_path} ➜ s3://{BUCKET_NAME}/{s3_key}")
                s3.upload_file(full_path, BUCKET_NAME, s3_key)
                uploaded_hashes.add(file_id)
            except Exception as e:
                print(f"❌ Upload failed for {full_path}: {e}")

def run_scheduler():
    print("📡 Auto-upload started. Watching folder for new .json files...")
    while True:
        try:
            upload_new_files()
            time.sleep(UPLOAD_INTERVAL_SECONDS)
        except KeyboardInterrupt:
            print("\n🛑 Upload stopped by user.")
            break

if __name__ == '__main__':
    run_scheduler()
