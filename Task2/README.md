# Task 2: Sensor Data Simulation

## 📌 Overview
This repository contains the implementation for **Task 2** of the Smart Environment Monitoring and Alert System. The goal of this phase is to establish a reliable, simulated data pipeline that generates realistic environmental metrics (Temperature, Ambient Light, and Motion). 

This decoupled architecture separates the hardware simulation from the software pipeline, allowing downstream applications (like dashboards and automation engines) to ingest standard CSV data without relying on a live microcontroller connection.

## 🏗️ System Architecture
1. **Hardware Simulation:** Arduino Uno running in Tinkercad.
2. **Sensors:** TMP36 (Temperature), Photoresistor (Ambient Light), PIR (Motion).
3. **Data Extraction:** Serial output captured via batch processing.
4. **Data Ingestion:** Python script validates, timestamps, and formats the raw serial string.
5. **Storage:** Standardized `sensor_log.csv` ready for Pandas/Streamlit integration.

## 📂 Folder Structure
```text
Task2/
├── arduino_simulation/
│   └── sensor_read.ino           # C++ firmware for microcontroller simulation
├── python_logger/
│   ├── raw_tinkercad_data.txt    # Input buffer for raw serial data
│   ├── process_tinkercad.py      # Data processing pipeline script
│   └── data/                     
│       └── sensor_log.csv        # Final output dataset
└── README.md

```

## 🔌 Circuit Design & Wiring

The simulation utilizes the following connections on the Arduino Uno:

* **Analog Pin A0:** TMP36 Temperature Sensor (Vout)
* **Analog Pin A1:** Photoresistor / LDR (Voltage Divider configuration with 10kΩ resistor)
* **Digital Pin 2:** PIR Motion Sensor (Signal)

### Simulation Screenshot

>![Tinkercad Circuit Diagram](<assets/Screenshot 2026-06-05 225954.png>)

## 🚀 Execution Guide

### Step 1: Generate Simulated Data

1. Open the circuit in [Tinkercad](https://www.tinkercad.com/).
2. Paste the code from `arduino_sim/sensor_read.ino` into the code editor.
3. Click **Start Simulation** and open the **Serial Monitor**.
4. Interact with the sensor sliders (Temperature, Light) and trigger the PIR sensor to generate variable data.

### Step 2: Extract Data

1. Once sufficient data is generated, stop the simulation.
2. Highlight and copy all output from the Tinkercad Serial Monitor.
3. Paste the contents into `python_logger/raw_tinkercad_data.txt`.

> *Place a screenshot of your Tinkercad Serial Monitor output here.*

### Step 3: Run the Python Data Pipeline

Ensure you have Python 3.x installed. Navigate to the `python_logger` directory and execute the processing script:

```bash
cd python_logger
python process_tinkercad.py

```

The script will read the raw text, calculate sequential timestamps anchored to the current system time, and generate a structured CSV file.

### Step 4: Verify Output

Check the `python_logger/data/` directory for the `sensor_log.csv` file.

> *Place a screenshot of your terminal showing the successful execution of the Python script here.*

## 📊 Expected Data Format (`sensor_log.csv`)

```csv
Timestamp,Temperature,Light,Motion
2026-06-05 22:40:00,24.15,12.0,0
2026-06-05 22:40:05,24.15,85.0,1
2026-06-05 22:40:10,28.40,82.0,0

```

## ⏭️ Next Steps

This generated CSV will serve as the foundational data source for **Task 3 (Streamlit IoT Dashboard)** and **Task 4 (Automation Logic)**.
