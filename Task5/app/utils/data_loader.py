import pandas as pd
import os
import streamlit as st
from utils.config import SENSOR_DATA_PATH, ALERTS_DATA_PATH

@st.cache_data(ttl=2)
def load_sensor_data():
    if not os.path.exists(SENSOR_DATA_PATH):
        return pd.DataFrame()
    try:
        df = pd.read_csv(SENSOR_DATA_PATH, encoding='utf-8')
        if df.empty or 'Timestamp' not in df.columns:
            return pd.DataFrame()
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        return df
    except Exception:
        return pd.DataFrame()

@st.cache_data(ttl=2)
def load_alerts_data():
    if not os.path.exists(ALERTS_DATA_PATH):
        return pd.DataFrame()
    try:
        df = pd.read_csv(ALERTS_DATA_PATH, encoding='utf-8')
        if df.empty or 'Timestamp' not in df.columns:
            return pd.DataFrame()
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        return df
    except Exception:
        return pd.DataFrame()