# dashboard_extension/updated_app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import time
import os

st.set_page_config(page_title="Smart Environment Dashboard", page_icon="🌍", layout="wide")

# Paths
SENSOR_DATA_PATH = "../../Task-2-Sensor-Simulation/python_logger/data/sensor_log.csv"
ALERTS_DATA_PATH = "../automation_engine/data/alerts_log.csv"

@st.cache_data(ttl=2)
def load_sensor_data():
    if os.path.exists(SENSOR_DATA_PATH):
        df = pd.read_csv(SENSOR_DATA_PATH)
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        return df
    return pd.DataFrame()

@st.cache_data(ttl=2)
def load_alerts_data():
    if os.path.exists(ALERTS_DATA_PATH):
        df = pd.read_csv(ALERTS_DATA_PATH)
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        return df
    return pd.DataFrame()

def render_alert_banners(df_alerts):
    """Displays the most recent active alert in a prominent banner."""
    if df_alerts.empty:
        st.success("✅ System Status: Normal. No active alerts.")
        return

    latest_alert = df_alerts.iloc[-1]
    
    # Calculate how old the alert is to decide if it's "Active" 
    # (For simulation, we will just show the latest one if it happened recently)
    msg = f"**{latest_alert['AlertType']}**: {latest_alert['Message']} ({latest_alert['SensorValues']})"
    
    if latest_alert['Severity'] == 'Critical':
        st.error(f"🚨 CRITICAL ALERT - {latest_alert['Timestamp']}\n\n{msg}")
    elif latest_alert['Severity'] == 'Warning':
        st.warning(f"⚠️ WARNING - {latest_alert['Timestamp']}\n\n{msg}")
    else:
        st.info(f"ℹ️ INFORMATION - {latest_alert['Timestamp']}\n\n{msg}")

def render_alert_dashboard(df_alerts):
    if df_alerts.empty:
        return

    st.divider()
    st.subheader("🔔 Alert Management System")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("**Alert Statistics**")
        st.write(f"**Total Alerts:** {len(df_alerts)}")
        
        crit_count = len(df_alerts[df_alerts['Severity'] == 'Critical'])
        warn_count = len(df_alerts[df_alerts['Severity'] == 'Warning'])
        info_count = len(df_alerts[df_alerts['Severity'] == 'Information'])
        
        st.markdown(f"🔴 **Critical:** {crit_count}")
        st.markdown(f"🟠 **Warning:** {warn_count}")
        st.markdown(f"🔵 **Information:** {info_count}")
        
    with col2:
        st.markdown("**Alert History**")
        
        # Color coding for the dataframe
        def highlight_severity(s):
            if s['Severity'] == 'Critical':
                return ['background-color: #ffcccc'] * len(s)
            elif s['Severity'] == 'Warning':
                return ['background-color: #fff0cc'] * len(s)
            return [''] * len(s)

        styled_df = df_alerts.sort_values(by='Timestamp', ascending=False).style.apply(highlight_severity, axis=1)
        st.dataframe(styled_df, use_container_width=True, hide_index=True, height=250)

# ==========================================
# REUSED TASK 3 COMPONENTS (Abbreviated for brevity, use your full Task 3 code here)
# ==========================================
def render_kpis(df):
    latest = df.iloc[-1]
    col1, col2, col3 = st.columns(3)
    col1.metric("🌡️ Current Temp", f"{latest['Temperature']:.1f} °C")
    col2.metric("☀️ Ambient Light", f"{latest['Light']:.1f} %")
    col3.metric("🚶 Motion", "Detected 🚨" if latest['Motion'] == 1 else "No Motion ✅")

def render_charts(df):
    col1, col2 = st.columns(2)
    fig_temp = px.line(df, x='Timestamp', y='Temperature', title='Temperature')
    col1.plotly_chart(fig_temp, use_container_width=True)
    fig_light = px.line(df, x='Timestamp', y='Light', title='Ambient Light')
    col2.plotly_chart(fig_light, use_container_width=True)

def main():
    with st.sidebar:
        st.header("⚙️ Controls")
        auto_refresh = st.checkbox("Enable Live Auto-Refresh", value=False)
    
    df_sensor = load_sensor_data()
    df_alerts = load_alerts_data()

    st.title("🌍 Smart Environment Monitoring Dashboard")
    
    # Task 4 Addition: Inject Banners here
    alert_container = st.container()
    with alert_container:
        render_alert_banners(df_alerts)
    
    if not df_sensor.empty:
        render_kpis(df_sensor)
        render_charts(df_sensor)
        
    # Task 4 Addition: Alert History
    render_alert_dashboard(df_alerts)

    if auto_refresh:
        time.sleep(5)
        st.rerun()

if __name__ == "__main__":
    main()