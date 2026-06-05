import os

# Base directory resolving
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# File Paths
SENSOR_DATA_PATH = os.path.join(BASE_DIR, "data", "sensor_log.csv")
ALERTS_DATA_PATH = os.path.join(BASE_DIR, "data", "alerts_log.csv")

# Application Settings
REFRESH_RATE_SECONDS = 5
CRITICAL_TEMP_THRESHOLD = 35.0
LOW_LIGHT_THRESHOLD = 20.0