import streamlit as st
import plotly.express as px
import time
from utils.data_loader import load_sensor_data, load_alerts_data
from utils.config import REFRESH_RATE_SECONDS

st.set_page_config(page_title="IoT Environment Platform", page_icon="🌍", layout="wide")

def render_health_sidebar(df_sensor, df_alerts):
    with st.sidebar:
        st.header("⚙️ System Status")
        st.success("🟢 Platform Online")
        st.divider()
        st.markdown("**System Health**")
        st.write(f"**Records Processed:** {len(df_sensor)}")
        st.write(f"**Alerts Generated:** {len(df_alerts)}")
        
        last_update = "No data"
        if not df_sensor.empty:
            last_update = df_sensor['Timestamp'].iloc[-1].strftime('%H:%M:%S')
        st.write(f"**Last Sync:** {last_update}")
        
        st.divider()
        return st.checkbox("Enable Live Auto-Refresh", value=False)

def tab_monitoring(df_sensor, df_alerts):
    st.subheader("Live Telemetry")
    
    # Render Active Alert Banner
    if not df_alerts.empty:
        latest = df_alerts.iloc[-1]
        msg = f"**{latest['AlertType']}**: {latest['Message']}"
        if latest['Severity'] == 'Critical':
            st.error(f"🚨 CRITICAL - {latest['Timestamp']} | {msg}")
        elif latest['Severity'] == 'Warning':
            st.warning(f"⚠️ WARNING - {latest['Timestamp']} | {msg}")

    # Render KPIs
    if not df_sensor.empty:
        latest_sensor = df_sensor.iloc[-1]
        col1, col2, col3 = st.columns(3)
        col1.metric("🌡️ Temperature", f"{latest_sensor['Temperature']:.1f} °C")
        col2.metric("☀️ Light Level", f"{latest_sensor['Light']:.1f} %")
        motion_status = "Detected 🚨" if latest_sensor['Motion'] == 1 else "Clear ✅"
        col3.metric("🚶 Motion Status", motion_status)
        
        # Quick Trend Charts
        c1, c2 = st.columns(2)
        c1.plotly_chart(px.line(df_sensor.tail(50), x='Timestamp', y='Temperature', title='Recent Temperature'), use_container_width=True)
        c2.plotly_chart(px.line(df_sensor.tail(50), x='Timestamp', y='Light', title='Recent Light Level'), use_container_width=True)
    else:
        st.info("Awaiting sensor telemetry...")

def tab_analytics(df_sensor):
    st.subheader("Historical Analytics")
    if df_sensor.empty:
        st.warning("Insufficient data for analytics.")
        return

    # Aggregate Data
    df_sensor['Date'] = df_sensor['Timestamp'].dt.date
    daily_avg = df_sensor.groupby('Date')[['Temperature', 'Light']].mean().reset_index()
    motion_counts = df_sensor.groupby('Date')['Motion'].sum().reset_index()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Daily Average Metrics**")
        st.dataframe(daily_avg.style.format({"Temperature": "{:.2f}", "Light": "{:.2f}"}), use_container_width=True, hide_index=True)
    with col2:
        st.markdown("**Motion Detection Frequency**")
        fig = px.bar(motion_counts, x='Date', y='Motion', title="Motion Events per Day", color_discrete_sequence=['#8A2BE2'])
        st.plotly_chart(fig, use_container_width=True)

def tab_alerts(df_alerts):
    st.subheader("Alert Management")
    if df_alerts.empty:
        st.success("No alerts generated yet.")
        return

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("**Severity Breakdown**")
        severity_counts = df_alerts['Severity'].value_counts().reset_index()
        fig = px.pie(severity_counts, values='count', names='Severity', 
                     color='Severity', color_discrete_map={'Critical':'red', 'Warning':'orange', 'Information':'blue'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("**Alert History**")
        st.dataframe(df_alerts.sort_values(by='Timestamp', ascending=False), use_container_width=True, hide_index=True)

def main():
    st.title("🌍 Smart Environment Monitoring Platform")
    
    df_sensor = load_sensor_data()
    df_alerts = load_alerts_data()
    
    auto_refresh = render_health_sidebar(df_sensor, df_alerts)
    
    # Unified UI Tabs
    tab1, tab2, tab3 = st.tabs(["📡 Live Monitoring", "📊 Analytics", "🔔 Alert Management"])
    
    with tab1:
        tab_monitoring(df_sensor, df_alerts)
    with tab2:
        tab_analytics(df_sensor)
    with tab3:
        tab_alerts(df_alerts)

    if auto_refresh:
        time.sleep(REFRESH_RATE_SECONDS)
        st.rerun()

if __name__ == "__main__":
    main()