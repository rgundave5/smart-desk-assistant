import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

st.set_page_config(page_title="Emotion Dashboard", layout="wide")
st.title("Emotion-Aware Focus Tracker")

conn = sqlite3.connect("/Users/prithikavenkatesh/smart-desk-assistant/app/tracker.db")
df = pd.read_sql_query("SELECT * FROM events", conn)

st.subheader("Emotion Frequency")
st.bar_chart(df['emotion'].value_counts())

st.subheader("Focus Trends Over Time")
fig = px.line(df, x='timestamp', y='emotion_conf', color='emotion', title="Emotion Confidence Timeline")
st.plotly_chart(fig)