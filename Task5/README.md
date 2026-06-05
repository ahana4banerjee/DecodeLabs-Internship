# 🚀 Task 5: Final System Integration

## 📌 Module Overview
This directory contains the final, unified iteration of the Smart Environment Monitoring Platform. Task 5 focuses on transforming the standalone scripts from previous tasks into a cohesive, locally integrated application.

The architecture has been heavily refactored to support centralized configuration, shared data loading pipelines, and a polished, multi-tab Streamlit frontend.

## 🏗️ Engineering Enhancements
* **Centralized Configuration (`config.py`):** All file paths, API thresholds, and system settings are abstracted here, ensuring the system runs flawlessly and can be easily adjusted from a single file.
* **Shared Data Layer (`data_loader.py`):** Implemented a unified utility module with robust error handling (e.g., catching empty files or corrupted headers) that serves data to both the analytics and UI layers.
* **Decoupled Architecture:** The background automation daemon (`engine.py`) and the frontend dashboard (`main_dashboard.py`) remain completely decoupled, communicating statelessly via standardized CSV logs.
* **Tabbed UI:** The Streamlit dashboard has been upgraded to a tabbed layout, cleanly separating Live Telemetry, Historical Analytics, and Alert Management.

## 📂 Directory Structure
```text
Task5/
├── app/
│   ├── main_dashboard.py      # The primary Streamlit UI application
│   ├── automation/
│   │   └── engine.py          # The headless alerting daemon
│   ├── data/
│   │   ├── sensor_log.csv     # Telemetry datastore
│   │   └── alerts_log.csv     # Stateful alert datastore
│   └── utils/
│       ├── config.py          # Global settings and threshold limits
│       └── data_loader.py     # Fault-tolerant Pandas ingestion logic
├── assets/                    # Screenshots and architecture diagrams
├── requirements.txt           # Project dependencies
└── README.md                  # This document

```

## 💻 Local Execution Guide

To run the unified platform on your local machine, you must run the backend worker and the frontend UI concurrently.

### 1. Install Dependencies

Ensure your Python virtual environment is activated, then install the required packages:

```bash
pip install -r requirements.txt

```

### 2. Start the Automation Daemon

Open a terminal, navigate to the `Task5` root, and launch the engine:

```bash
python app/automation/engine.py

```

*Note: The engine will immediately begin polling `app/data/sensor_log.csv` and writing generated alerts to `alerts_log.csv`.*

### 3. Launch the Web Platform

Open a second terminal, navigate to the `Task5/app` directory, and start the Streamlit UI:

```bash
cd app
streamlit run main_dashboard.py

```

## 🔮 Future Scope

* Implementation of a NoSQL Cloud Database (MongoDB/Firebase) to replace flat CSV files.
* Integration of the Twilio API for external SMS alert routing.
* Containerization via Docker for seamless cloud deployment.