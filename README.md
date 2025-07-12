# 🌿 GCT Sensor Data Processing Pipeline

This project simulates, collects, stores, and analyzes plant-related environmental sensor data using a combination of **Node-RED**, **AWS S3**, and **AWS Lambda**. It is part of the GCT (Green Carbon Technology) project, aimed at building a modular and scalable IoT analytics system.

---

## 📌 Features

- ⚙️ **Simulated Sensor Data**: Generates synthetic readings for pH, temperature, humidity, CO2, and more.
- 📁 **Local Archival**: Stores raw data files in a time-based folder hierarchy on a Windows machine.
- ☁️ **Cloud Upload**: Automatically pushes raw `.json` files to AWS S3 in real-time.
- 🧠 **Lambda-Driven Processing**: Triggers AWS Lambda to analyze sensor statistics and detect threshold violations.
- 📊 **Structured Summary Output**: Saves mean, standard deviation, and alert flags to a second processed-data S3 bucket.

---

## 🧱 Architecture Overview

```plaintext
Node-RED (sensor generator)
     ├── Write to local path: C:/Users/vijay/Desktop/GCT Project/raw/...
     └── Upload to AWS S3 → co2-plant-raw-data (via msg.filename)

AWS S3
     ├── Bucket 1: co2-plant-raw-data
     └── Bucket 2: co2-plant-processed-data

AWS Lambda (triggered by ObjectCreated in raw bucket)
     └── Reads JSON → Computes mean/stddev → Detects threshold violations → Writes summary JSON to processed bucket
