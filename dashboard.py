import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

st.set_page_config(page_title="Emotion Dashboard", layout="wide")
st.title("Emotion-Aware Focus Tracker")

import requests

try:
    response = requests.get("http://localhost:8000/api/events")  # Your Flask API endpoint
    response.raise_for_status()
    data_json = response.json()
    df = pd.DataFrame(data_json["events"])  # Adjust based on your API response structure
except Exception as e:
    st.error(f"Failed to get data from backend: {e}")
    # Fallback: stub data or empty dataframe
    df = pd.DataFrame(columns=["timestamp", "emotion", "emotion_conf"])

st.subheader("Emotion Frequency")
st.bar_chart(df['emotion'].value_counts())

st.subheader("Focus Trends Over Time")
fig = px.line(df, x='timestamp', y='emotion_conf', color='emotion', title="Emotion Confidence Timeline")
st.plotly_chart(fig)