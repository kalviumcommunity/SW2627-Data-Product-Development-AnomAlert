import streamlit as st
from database.db import load_metrics
from components.kpi_cards import show_kpi_cards

st.set_page_config(
    page_title="AnomAlert Dashboard",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ AnomAlert Dashboard")
st.caption("Real-Time Security Risk Monitoring")

st.divider()

df = load_metrics()

st.subheader("📊 Security Overview")
show_kpi_cards(df)

st.divider()

left, right = st.columns([1,1])

with left:
    st.subheader("Risk Distribution")

with right:
    st.subheader("Top 10 Risky Users")

st.divider()

st.subheader("Recent Authentication Events")

st.divider()

st.subheader("User Investigation")