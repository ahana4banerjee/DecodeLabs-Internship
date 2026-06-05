import csv
import os
from datetime import datetime, timedelta

# File configurations
INPUT_FILE = 'raw_tinkercad_data.txt' 
OUTPUT_CSV = 'data/sensor_log.csv'

def process_tinkercad_data():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: Could not find '{INPUT_FILE}'. Please create it in this folder and paste your Tinkercad output.")
        return

    try:
        with open(INPUT_FILE, 'r') as file:
            raw_lines = file.readlines()
            
        os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
        
        with open(OUTPUT_CSV, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            # Updated header row matching the new schema
            writer.writerow(['Timestamp', 'Temperature', 'Light', 'Motion'])
            
            # Anchor timestamp calculations to the current real time
            current_time = datetime.now()
            processed_count = 0
            
            for line in raw_lines:
                line = line.strip()
                if line and "Error" not in line:
                    try:
                        temp, light, motion = line.split(',')
                        formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
                        
                        writer.writerow([formatted_time, temp, light, motion])
                        print(f"Processed: {formatted_time} -> Temp: {temp}°C, Light: {light}%, Motion: {motion}")
                        
                        # Increment time window by 5 seconds per record line
                        current_time += timedelta(seconds=5)
                        processed_count += 1
                    except ValueError:
                        print(f"Skipping malformed or incomplete row: {line}")
                        
        print(f"\nPipeline execution successful. Generated {processed_count} rows in '{OUTPUT_CSV}'.")
        
    except Exception as e:
        print(f"An unexpected error occurred during processing: {e}")

if __name__ == '__main__':
    process_tinkercad_data()