import streamlit as st
import sqlite3
import pandas as pd
import altair as alt  # <--- Make sure altair is imported

st.set_page_config(page_title="AIoT Triage Dashboard", layout="wide", page_icon="🤖")

st.title("🏭 Smart Factory Edge AIoT Triage Dashboard")
st.markdown("Real-time industrial telemetry monitoring powered by **Local Ollama (Phi-3)** and SQLite (Zero API Keys / 100% Offline).")

DB_NAME = "factory.db"

def load_data():
    try:
        conn = sqlite3.connect(DB_NAME)
        df = pd.read_sql("SELECT * FROM telemetry ORDER BY id DESC LIMIT 100", conn)
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()

# Sidebar controls
st.sidebar.header("Control Panel")
if st.sidebar.button("🔄 Refresh Data"):
    st.rerun()

df = load_data()

if not df.empty:
    col1, col2, col3 = st.columns(3)
    total_events = len(df)
    warnings = len(df[df['status'] == 'WARNING'])
    
    col1.metric("Total Telemetry Logs", total_events)
    col2.metric("Warnings / Anomalies", warnings, delta_color="inverse")
    col3.metric("System Status", "🟢 Operational (Offline)" if warnings < 10 else "🟠 High Alert")

    st.subheader("📊 Recent Telemetry Streams & AI Triage Events")
    st.dataframe(df, use_container_width=True)

    # Clean continuous time-series chart using Altair
    st.subheader("🌡️ Temperature Trends Across Fleet")
    try:
        # Ensure timestamp is parsed as datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        chart = alt.Chart(df).mark_line(point=True, strokeWidth=2).encode(
            x=alt.X('timestamp:T', title='Time'),
            y=alt.Y('temperature_celsius:Q', title='Temperature (°C)'),
            color=alt.Color('device_id:N', title='Device ID'),
            tooltip=['timestamp', 'device_id', 'temperature_celsius', 'vibration_g', 'status']
        ).properties(
            height=400
        ).interactive()
        
        st.altair_chart(chart, use_container_width=True)
    except Exception as e:
        st.warning(f"Could not render chart: {e}")
else:
    st.info("Waiting for data... Make sure `simulator.py` is running!")
