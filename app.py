import streamlit as st
from database.db import load_metrics
from components.kpi_cards import show_kpi_cards
from components.top_users import show_top_users
from components.user_details import show_user_details
from components.recent_events import show_recent_events

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

left, middle, right = st.columns([1, 1.3, 1.3])

with left:
    st.subheader("Risk Distribution")

with middle:
    st.subheader("Top 10 Risky Users")
    show_top_users(df)

with right:
    if st.session_state.get("selected_user"):
        show_user_details(df, st.session_state.selected_user)

st.divider()

st.subheader("Recent Authentication Events")
show_recent_events(st.session_state.get("selected_user"))

st.divider()

st.subheader("User Investigation")