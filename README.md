# 🌍 Smart Environment Monitoring & Alert System

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.36.0-red)
![Pandas](https://img.shields.io/badge/Pandas-Data_Processing-150458)
![IoT](https://img.shields.io/badge/IoT-Simulation-00979D)

## 📌 Project Overview
This repository contains the complete progression of an Electronics and Communication Engineering (ECE) IoT internship project. The objective was to design, simulate, and build a decoupled software architecture for a **Smart Environment Monitoring Platform**.

The project simulates an edge-device capturing telemetry (Temperature, Ambient Light, and Motion), builds a robust Python data ingestion pipeline, implements an autonomous background rule engine for alert generation, and visualizes the system state using a modern web dashboard. 

*For detailed technical architecture and formal implementation notes, please see the [Project Report](./PROJECT_REPORT.md).*

---

## 🏗️ System Architecture Flow
The system utilizes a decoupled, asynchronous architecture to prevent data bottlenecks and ensure the frontend UI never blocks the backend rule engine.

```text
[Edge Devices]      [Data Layer]         [Logic Layer]          [Presentation Layer]
Tinkercad Sim  -->  sensor_log.csv  -->  Automation Daemon  --> alerts_log.csv
(TMP36, LDR)        (Pandas/UTF-8)       (Python Worker)        (State Storage)
                                                  |
                                                  v
                                          Streamlit Dashboard (Unified UI)

```

---

## 🛠️ Technology Stack

* **Hardware Simulation:** Tinkercad, Arduino Uno, TMP36, Photoresistor (LDR), PIR Motion Sensor.
* **Backend Processing:** Python, Pandas.
* **Frontend Visualization:** Streamlit, Plotly Express.
* **Data Storage:** Standardized UTF-8 CSV Flat Files.

---

## 📂 Repository Structure & Task Progression

This project was developed using an iterative, agile-style progression. Below is a detailed breakdown of each phase of the project build.

### Task 2: Sensor Data Simulation

Established the hardware foundation by simulating an Arduino Uno connected to a TMP36 temperature sensor, an LDR for ambient light, and a PIR motion sensor within Tinkercad. Because web-based simulators cannot natively write to local storage, a custom Python batch-processing script (`process_tinkercad.py`) was engineered to ingest raw serial output, append accurate timestamps, and format the data into a standardized `sensor_log.csv` pipeline.

> **Note:** For more task-specific details, circuit diagrams, and execution instructions, please read: [`Task2/README.md`](https://github.com/ahana4banerjee/DecodeLabs-Internship/Task2/README.md)

### Task 3: IoT Monitoring Dashboard

Built the initial presentation layer using Streamlit and Pandas. This task focused on creating a responsive web application that continuously reads the `sensor_log.csv` file without locking the filesystem. It features top-level KPI metric cards for current sensor states, a dynamic motion event log, and interactive Plotly time-series charts to visualize temperature and light trends over time.

> **Note:** For more task-specific details and UI architecture, please read: [`Task3/README.md`](https://github.com/ahana4banerjee/DecodeLabs-Internship/Task3/README.md)

### Task 4: Automation Logic & Alert Engine

Transitioned the project from a passive dashboard to an active, intelligent monitoring system. Engineered a headless, continuously polling Python daemon (`automation.py`) that acts as a background worker. It evaluates incoming telemetry against hierarchical business rules to prevent alert fatigue, generating Critical, Warning, and Info alerts. These states are saved to `alerts_log.csv`, which the dashboard then reads to inject real-time, color-coded UI banners.

> **Note:** For more task-specific details and rule definitions, please read: [`Task4/README.md`](https://github.com/ahana4banerjee/DecodeLabs-Internship/Task4/README.md)
### Task 5: Final System Integration

The final production-ready deliverable. Refactored the entire codebase to implement a professional microservices folder structure. This included abstracting hardcoded variables into a centralized `config.py` file, building shared, fault-tolerant Pandas data-loading utilities, and redesigning the Streamlit interface into a clean, multi-tab layout (Live Monitoring, Analytics, Alert Management) suitable for cloud deployment.

> **Note:** For more task-specific details and deployment strategies, please read: [`Task5/README.md`](https://github.com/ahana4banerjee/DecodeLabs-Internship/Task5/README.md)
---

## 🚀 Quick Start (Running the Final System)

To evaluate the final integrated platform, navigate to the **Task 5** directory.

1. **Clone the repository:**
```bash
git clone https://github.com/ahana4banerjee/DecodeLabs-Internship.git
cd DecodeLabs-Internship/Task5
```


2. **Install dependencies:**
```bash
pip install -r requirements.txt

```


3. **Start the Automation Daemon (Terminal 1):**
```bash
python app/automation/engine.py

```


4. **Launch the Dashboard (Terminal 2):**
```bash
cd app
streamlit run main_dashboard.py

```



---

## 💡 Note: This is part of my DecodeLabs Internship as IoT Intern

This comprehensive project was architected and developed from the ground up as the core portfolio deliverable for my IoT internship, demonstrating proficiency in data pipelines, decoupled system architecture, and full-stack Python development.

---

## 👨‍💻 Author

* **Name:** Ahana Banerjee
* **College / University:** JNTUH
* **Degree:** B. Tech + M. Tech IDP in ECE, 4th Year
```
