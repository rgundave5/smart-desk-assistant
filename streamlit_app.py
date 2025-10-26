import streamlit as st
from data import fetch_events
from charts import plot_emotion_freq, plot_focus_trends

st.title("Emotion-Aware Focus Tracker")

df = fetch_events()

plot_emotion_freq(df)
plot_focus_trends(df)
