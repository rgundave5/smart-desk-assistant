import streamlit as st
import pandas as pd
import plotly.express as px
import requests

st.set_page_config(page_title="Emotion Dashboard", layout="wide")
st.title("Emotion-Aware Focus Tracker")

try:
    response = requests.get("http://localhost:5001/api/emotion-results")  # Flask backend URL and port
    response.raise_for_status()
    df = pd.DataFrame(response.json())
except Exception as e:
    st.error(f"Failed to get data from backend: {e}")
    df = pd.DataFrame(columns=["timestamp", "emotion", "emotion_conf", "productivity"])

st.subheader("Emotion Frequency")
st.bar_chart(df['emotion'].value_counts())

st.subheader("Focus Trends Over Time")
fig = px.line(df, x='timestamp', y='emotion_conf', color='productivity', title="Productivity Timeline")
st.plotly_chart(fig)