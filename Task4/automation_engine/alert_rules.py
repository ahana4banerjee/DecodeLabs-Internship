# automation_engine/alert_rules.py

def evaluate_sensor_data(row):
    """
    Evaluates a single row of sensor data against defined automation rules.
    Returns a list of alert dictionaries (if any rules are triggered).
    """
    alerts = []
    
    timestamp = row['Timestamp']
    temp = float(row['Temperature'])
    light = float(row['Light'])
    motion = int(row['Motion'])
    
    sensor_values_str = f"Temp: {temp}°C, Light: {light}%, Motion: {motion}"

    # Rule 4: CRITICAL (Highest Priority)
    if temp > 35.0 and motion == 1:
        alerts.append({
            'Timestamp': timestamp,
            'AlertType': 'Critical Environment',
            'Severity': 'Critical',
            'Message': 'High temperature and motion detected simultaneously.',
            'SensorValues': sensor_values_str
        })
        # Skip individual temp/motion rules to avoid alert fatigue
        # Still check light level
        if light < 20.0:
            alerts.append({
                'Timestamp': timestamp,
                'AlertType': 'Low Light',
                'Severity': 'Warning',
                'Message': 'Ambient light dropped below minimum threshold.',
                'SensorValues': sensor_values_str
            })
        return alerts

    # Rule 1: High Temperature Warning
    if temp > 35.0:
        alerts.append({
            'Timestamp': timestamp,
            'AlertType': 'High Temperature',
            'Severity': 'Warning',
            'Message': 'Temperature exceeded 35°C threshold.',
            'SensorValues': sensor_values_str
        })

    # Rule 2: Low Light Warning
    if light < 20.0:
        alerts.append({
            'Timestamp': timestamp,
            'AlertType': 'Low Light',
            'Severity': 'Warning',
            'Message': 'Ambient light dropped below minimum threshold.',
            'SensorValues': sensor_values_str
        })

    # Rule 3: Motion Detected Info
    if motion == 1:
        alerts.append({
            'Timestamp': timestamp,
            'AlertType': 'Motion Detected',
            'Severity': 'Information',
            'Message': 'Motion event detected in monitored area.',
            'SensorValues': sensor_values_str
        })

    return alerts