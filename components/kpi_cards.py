import streamlit as st

def show_kpi_cards(df):

    total_users = len(df)

    total_alerts = len(df[df["failed_login_score"] > 0])

    high_risk = len(df[df["failed_login_score"] >= 70])   # Temporary

    critical = len(df[df["failed_login_score"] >= 90])    # Temporary

    average_risk = round(df["failed_login_score"].mean(), 2)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("👤 Total Users", total_users)

    with col2:
        st.metric("🚨 Total Alerts", total_alerts)

    with col3:
        st.metric("⚠️ High Risk", high_risk)

    with col4:
        st.metric("🔴 Critical", critical)

    with col5:
        st.metric("⭐ Avg Risk", average_risk)