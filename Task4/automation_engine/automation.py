# automation_engine/automation.py

import pandas as pd
import time
import os
import csv
from alert_rules import evaluate_sensor_data

# Configurations
# Adjust SENSOR_DATA_PATH to point to your Task 2 output
SENSOR_DATA_PATH = '../../Task2/python_logger/data/sensor_log.csv'
ALERTS_DATA_PATH = 'data/alerts_log.csv'
POLL_INTERVAL = 5  # Seconds to wait between checks

def setup_alerts_csv():
    """Ensure the alerts CSV exists with the proper headers."""
    os.makedirs(os.path.dirname(ALERTS_DATA_PATH), exist_ok=True)
    if not os.path.isfile(ALERTS_DATA_PATH):
        with open(ALERTS_DATA_PATH, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Timestamp', 'AlertType', 'Severity', 'Message', 'SensorValues'])
        print(f"Initialized alerts log at {ALERTS_DATA_PATH}")

def get_last_processed_timestamp():
    """Reads the last timestamp from the alerts log to know where to resume."""
    if not os.path.isfile(ALERTS_DATA_PATH):
        return None
    try:
        df_alerts = pd.read_csv(ALERTS_DATA_PATH)
        if not df_alerts.empty:
            return df_alerts.iloc[-1]['Timestamp']
    except Exception:
        pass
    return None

def process_new_data():
    """Reads sensor data, finds new rows, evaluates rules, and writes alerts."""
    if not os.path.exists(SENSOR_DATA_PATH):
        print(f"Waiting for sensor data at {SENSOR_DATA_PATH}...")
        return

    try:
        df_sensor = pd.read_csv(SENSOR_DATA_PATH)
        last_ts = get_last_processed_timestamp()

        # Filter for only new rows
        if last_ts:
            # Ensure string comparison or convert both to datetime
            df_new = df_sensor[df_sensor['Timestamp'] > last_ts]
        else:
            df_new = df_sensor

        if df_new.empty:
            return # Nothing new to process

        new_alerts = []
        for index, row in df_new.iterrows():
            generated_alerts = evaluate_sensor_data(row)
            new_alerts.extend(generated_alerts)

        # Write new alerts to CSV
        if new_alerts:
            with open(ALERTS_DATA_PATH, mode='a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['Timestamp', 'AlertType', 'Severity', 'Message', 'SensorValues'])
                for alert in new_alerts:
                    writer.writerow(alert)
                    print(f"[{alert['Severity'].upper()}] {alert['AlertType']} at {alert['Timestamp']}")

    except Exception as e:
        print(f"Error processing data: {e}")

def main():
    print("🚀 Starting IoT Automation Engine...")
    setup_alerts_csv()
    
    try:
        while True:
            process_new_data()
            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        print("\nAutomation Engine stopped.")

if __name__ == "__main__":
    main()