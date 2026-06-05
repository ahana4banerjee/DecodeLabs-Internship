import pandas as pd
import time
import os
import csv
import sys

# ==========================================
# PATH RESOLUTION (Critical for Task 5)
# ==========================================
# This ensures the script can find the 'utils' folder whether you run it 
# from the 'app' folder, the 'automation' folder, or the root 'Task5' folder.
current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.dirname(current_dir)
sys.path.append(app_dir)

from utils.config import (
    SENSOR_DATA_PATH, 
    ALERTS_DATA_PATH, 
    CRITICAL_TEMP_THRESHOLD, 
    LOW_LIGHT_THRESHOLD,
    REFRESH_RATE_SECONDS
)

# ==========================================
# ALERT BUSINESS LOGIC
# ==========================================
def evaluate_sensor_data(row):
    """Evaluates a single row of data against thresholds defined in config.py"""
    alerts = []
    
    timestamp = row['Timestamp']
    temp = float(row['Temperature'])
    light = float(row['Light'])
    motion = int(row['Motion'])
    
    sensor_values_str = f"Temp: {temp}°C, Light: {light}%, Motion: {motion}"

    # CRITICAL: High Temp + Motion
    if temp > CRITICAL_TEMP_THRESHOLD and motion == 1:
        alerts.append({
            'Timestamp': timestamp,
            'AlertType': 'Critical Environment',
            'Severity': 'Critical',
            'Message': 'High temperature and motion detected simultaneously.',
            'SensorValues': sensor_values_str
        })
        return alerts # Skip lesser alerts to prevent fatigue

    # WARNING: High Temp
    if temp > CRITICAL_TEMP_THRESHOLD:
        alerts.append({
            'Timestamp': timestamp,
            'AlertType': 'High Temperature',
            'Severity': 'Warning',
            'Message': f'Temperature exceeded {CRITICAL_TEMP_THRESHOLD}°C threshold.',
            'SensorValues': sensor_values_str
        })

    # WARNING: Low Light
    if light < LOW_LIGHT_THRESHOLD:
        alerts.append({
            'Timestamp': timestamp,
            'AlertType': 'Low Light',
            'Severity': 'Warning',
            'Message': f'Ambient light dropped below {LOW_LIGHT_THRESHOLD}% minimum.',
            'SensorValues': sensor_values_str
        })

    # INFO: Motion
    if motion == 1:
        alerts.append({
            'Timestamp': timestamp,
            'AlertType': 'Motion Detected',
            'Severity': 'Information',
            'Message': 'Motion event detected in monitored area.',
            'SensorValues': sensor_values_str
        })

    return alerts

# ==========================================
# AUTOMATION WORKER LOGIC
# ==========================================
def setup_alerts_csv():
    """Ensure the alerts CSV exists with proper UTF-8 encoding."""
    os.makedirs(os.path.dirname(ALERTS_DATA_PATH), exist_ok=True)
    if not os.path.isfile(ALERTS_DATA_PATH):
        with open(ALERTS_DATA_PATH, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Timestamp', 'AlertType', 'Severity', 'Message', 'SensorValues'])
        print(f"Initialized alerts log at {ALERTS_DATA_PATH}")

def get_last_processed_timestamp():
    if not os.path.isfile(ALERTS_DATA_PATH):
        return None
    try:
        df_alerts = pd.read_csv(ALERTS_DATA_PATH, encoding='utf-8')
        if not df_alerts.empty and 'Timestamp' in df_alerts.columns:
            return df_alerts.iloc[-1]['Timestamp']
    except Exception:
        pass
    return None

def process_new_data():
    if not os.path.exists(SENSOR_DATA_PATH):
        print(f"Waiting for sensor data at {SENSOR_DATA_PATH}...")
        return

    try:
        df_sensor = pd.read_csv(SENSOR_DATA_PATH, encoding='utf-8')
        if df_sensor.empty or 'Timestamp' not in df_sensor.columns:
            return

        last_ts = get_last_processed_timestamp()

        if last_ts:
            df_new = df_sensor[df_sensor['Timestamp'] > last_ts]
        else:
            df_new = df_sensor

        if df_new.empty:
            return 

        new_alerts = []
        for index, row in df_new.iterrows():
            generated_alerts = evaluate_sensor_data(row)
            new_alerts.extend(generated_alerts)

        if new_alerts:
            with open(ALERTS_DATA_PATH, mode='a', newline='', encoding='utf-8') as file:
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
            time.sleep(REFRESH_RATE_SECONDS)
    except KeyboardInterrupt:
        print("\nAutomation Engine stopped.")

if __name__ == "__main__":
    main()