import streamlit as st
from database.db import load_metrics
from components.kpi_cards import show_kpi_cards
from components.top_users import show_top_users
from components.user_details import show_user_details
from components.risk_formula import show_risk_formula
from components.risk_distribution import show_risk_distribution
from components.recent_events import show_recent_events
from components.filters import filters, apply_filters
from components.sidebar import show_sidebar

st.set_page_config(
    page_title="AnomAlert Dashboard",
    page_icon="🛡️",
    layout="wide"
)

st.markdown("""
<style>

/* Filter Bar */

.filter-bar{
    background:#FFFFFF;
    border:1px solid #E5E7EB;
    border-radius:14px;
    padding:18px 20px 6px;
    margin-bottom:20px;
}

.filter-bar [data-testid="stSelectbox"] label,
.filter-bar [data-testid="stTextInput"] label{
    font-size:13px;
    font-weight:600;
    color:#374151;
}

</style>
""", unsafe_allow_html=True)

show_sidebar()

st.title("🛡️ AnomAlert Dashboard")
st.caption("Real-Time Security Risk Monitoring")

st.divider()

df = load_metrics()

st.subheader("📊 Security Overview")
show_kpi_cards(df)

selections = filters(df)
df = apply_filters(df, selections)

st.divider()

left, middle, right = st.columns([1, 1.3, 1.3])

with left:
    st.subheader("Risk Distribution")
    show_risk_distribution(df)

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

show_risk_formula()

st.divider()

st.subheader("User Investigation")

all_users = sorted(df["user_id"].dropna().unique().tolist())
searched_user = st.selectbox(
    "Search or select a user to investigate",
    options=[""] + all_users,
    format_func=lambda x: "Type or select a User ID..." if x == "" else x,
)

if searched_user:
    st.session_state.selected_user = searched_user
    show_user_details(df, searched_user)