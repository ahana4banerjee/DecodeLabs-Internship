# 🌍 Smart Environment Monitoring & Alert System


## 📌 Project Overview

This repository contains the complete progression of an Electronics and Communication Engineering (ECE) IoT internship project. The objective was to design, simulate, and build a modular software architecture for a Smart Environment Monitoring Platform.

The project simulates an edge device capturing environmental telemetry (Temperature, Ambient Light, and Motion), builds a Python-based data ingestion pipeline, implements a background rule engine for alert generation, and visualizes the system state through a web dashboard.

The internship was structured into four individual tasks, each focusing on a different aspect of an IoT workflow. While every task can be executed and understood independently, Task 5 serves as the final integration stage, combining the functionalities developed in Tasks 2, 3, and 4 into a single unified application.

For detailed technical architecture and implementation notes, please see the [`PROJECT_REPORT.md`](PROJECT_REPORT.md).

---

## 🏗️ System Architecture Flow

The system follows a modular architecture that separates data collection, processing, and visualization, making it easier to extend and maintain.

```text
[Edge Devices]      [Data Layer]         [Logic Layer]          [Presentation Layer]

Tinkercad Sim  -->  sensor_log.csv  -->  Automation Engine  --> alerts_log.csv
(TMP36, LDR)        (Pandas/UTF-8)       (Python Worker)       (Alert Storage)
                                                  |
                                                  v
                                          Streamlit Dashboard
```

---

## 🛠️ Technology Stack

**Hardware Simulation:** Tinkercad, Arduino Uno, TMP36, Photoresistor (LDR), PIR Motion Sensor

**Backend Processing:** Python, Pandas

**Frontend Visualization:** Streamlit, Plotly Express

**Data Storage:** UTF-8 encoded CSV files

---

## 📂 Repository Structure & Task Progression

This project was developed incrementally, with each task building upon the previous one.

### Task 2: Sensor Data Simulation

Established the hardware foundation by simulating an Arduino Uno connected to a TMP36 temperature sensor, an LDR for ambient light, and a PIR motion sensor in Tinkercad.

Since browser-based simulators cannot directly write to local storage, a Python batch-processing script (`process_tinkercad.py`) was developed to process raw serial output, append timestamps, and generate a standardized `sensor_log.csv` file.

**Note:** For circuit diagrams and execution instructions, see [Task2/README.md](Task2/README.md).

---

### Task 3: IoT Monitoring Dashboard

Built the monitoring interface using Streamlit and Pandas.

This task focused on creating a responsive web application that reads `sensor_log.csv` and displays:

* Current sensor values
* Motion event history
* Interactive Plotly charts for temperature and ambient light trends

**Note:** For dashboard details and UI structure, see [Task3/README.md](Task3/README.md).

---

### Task 4: Automation Logic & Alert Engine

Extended the system with a rule-based automation layer.

A background Python worker (`automation.py`) continuously evaluates incoming sensor data against predefined conditions and generates Critical, Warning, and Information alerts.

Generated alerts are stored in `alerts_log.csv`, which is then used by the dashboard to display alert notifications.

**Note:** For rule definitions and implementation details, see [Task4/README.md](Task4/README.md).

---

### Task 5: Final System Integration

Integrated the previous components into a single application structure.

This phase included:

* Centralizing configuration values into `config.py`
* Creating shared data-loading utilities
* Improving error handling for file operations
* Organizing the dashboard into separate sections for Live Monitoring, Analytics, and Alert Management
* Preparing the project structure for future deployment

**Note:** For integration details and deployment notes, see [Task5/README.md](Task5/README.md).

---

## 🚀 Quick Start (Running the Final System)

Since all four tasks are part of the same project, it is recommended to create **one virtual environment at the repository root**, which can be reused across every task.

### 1. Clone the repository

```bash
git clone https://github.com/ahana4banerjee/DecodeLabs-Internship.git
cd DecodeLabs-Internship
```

### 2. Create a virtual environment (Recommended)

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

> This virtual environment is shared across all tasks in the repository.

### 4. Navigate to the integrated Task 5 application

```bash
cd Task5
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Start the Automation Engine (Terminal 1)

```bash
python app/automation/engine.py
```

### 7. Launch the Dashboard (Terminal 2)

```bash
cd app
streamlit run main_dashboard.py
```


---

## 💡 About This Project

This project was developed as part of my DecodeLabs IoT Internship and serves as the primary portfolio project for the internship.

It demonstrates concepts including:

* IoT hardware simulation
* Python data processing
* Sensor data pipelines
* Rule-based automation
* Dashboard development
* Modular software design

---

## 👨‍💻 Author

**Name:** Ahana Banerjee

**University:** JNTUH

**Degree:** B.Tech + M.Tech IDP in Electronics and Communication Engineering (ECE)
