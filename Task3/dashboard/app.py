import streamlit as st
import pandas as pd
import plotly.express as px
import time
import os

# ==========================================
# CONFIGURATION & SETUP
# ==========================================
# Page configuration MUST be the first Streamlit command
st.set_page_config(
    page_title="Smart Environment Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Update this path to point to where Task 2 saves the CSV
DATA_PATH = "../../Task2/python_logger/data/sensor_log.csv"

# ==========================================
# DATA LOADING
# ==========================================
@st.cache_data(ttl=2) # Cache data for 2 seconds to prevent excessive disk reads
def load_data():
    if not os.path.exists(DATA_PATH):
        return pd.DataFrame()
    
    try:
        df = pd.read_csv(DATA_PATH)
        # Ensure Timestamp is a datetime object
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# ==========================================
# UI COMPONENTS
# ==========================================
def render_header():
    st.title("🌍 Smart Environment Monitoring Dashboard")
    st.markdown("Real-time telemetry for Temperature, Ambient Light, and Motion Detection.")
    
    # Future Hook for Task 4 (Alerts)
    # This container will hold critical alerts later. 
    st.container(border=False) 

def render_kpis(df):
    if df.empty:
        st.warning("No data available to display KPIs.")
        return

    latest = df.iloc[-1]
    
    # Determine motion status text and color
    motion_val = latest['Motion']
    motion_text = "Motion Detected 🚨" if motion_val == 1 else "No Motion ✅"
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="🌡️ Current Temperature", value=f"{latest['Temperature']:.1f} °C")
    with col2:
        st.metric(label="☀️ Ambient Light", value=f"{latest['Light']:.1f} %")
    with col3:
        st.metric(label="🚶 Motion Status", value=motion_text)

def render_charts(df):
    if df.empty:
        return
        
    st.subheader("📈 Sensor Trends")
    col1, col2 = st.columns(2)
    
    with col1:
        fig_temp = px.line(df, x='Timestamp', y='Temperature', 
                           title='Temperature over Time',
                           color_discrete_sequence=['#FF4B4B'])
        fig_temp.update_layout(margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(fig_temp, use_container_width=True)
        
    with col2:
        fig_light = px.line(df, x='Timestamp', y='Light', 
                            title='Ambient Light over Time',
                            color_discrete_sequence=['#FFA500'])
        fig_light.update_layout(margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(fig_light, use_container_width=True)

def render_motion_and_stats(df):
    if df.empty:
        return
        
    st.subheader("📊 Analytics & Motion Log")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("**Dataset Overview**")
        st.write(f"**Total Records:** {len(df)}")
        st.write(f"**Avg Temperature:** {df['Temperature'].mean():.1f} °C")
        st.write(f"**Avg Light Level:** {df['Light'].mean():.1f} %")
        
        total_motion = df[df['Motion'] == 1].shape[0]
        st.write(f"**Total Motion Events:** {total_motion}")
        
    with col2:
        st.markdown("**Recent Motion Events**")
        motion_df = df[df['Motion'] == 1].sort_values(by='Timestamp', ascending=False)
        if motion_df.empty:
            st.info("No motion detected yet.")
        else:
            st.dataframe(motion_df[['Timestamp', 'Temperature', 'Light']], 
                         use_container_width=True, hide_index=True, height=200)

def render_raw_data(df):
    with st.expander("🔍 View Raw Sensor Data"):
        st.dataframe(df.sort_values(by='Timestamp', ascending=False), use_container_width=True)

# ==========================================
# MAIN APPLICATION LOGIC
# ==========================================
def main():
    # Sidebar Controls
    with st.sidebar:
        st.header("⚙️ Controls")
        auto_refresh = st.checkbox("Enable Live Auto-Refresh", value=False)
        st.markdown("---")
        st.markdown("**Project Info**")
        st.markdown("IoT Internship Project")
        st.markdown("Task 3: Dashboard")
        
        # Future Hook for Task 5
        # st.markdown("Deployment Status: Local") 

    # Load Data
    df = load_data()
    
    if df.empty:
        st.error(f"Cannot find data at `{DATA_PATH}`. Please ensure Task 2 is running and the path is correct.")
        return

    # Render UI
    render_header()
    render_kpis(df)
    st.divider()
    render_charts(df)
    st.divider()
    render_motion_and_stats(df)
    render_raw_data(df)

    # Auto-Refresh Logic (Production friendly standard approach)
    if auto_refresh:
        time.sleep(5) # Wait 5 seconds
        st.rerun()    # Rerun the script to fetch new data

if __name__ == "__main__":
    main()