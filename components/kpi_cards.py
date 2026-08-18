import streamlit as st

# Lucide-style stroke icons (24x24, currentColor), matching sidebar.py's set.
ICONS = {
    "users": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
    "bell": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/></svg>',
    "trending-up": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>',
    "shield-alert": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>',
    "gauge": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20a8 8 0 1 0 0-16 8 8 0 0 0 0 16Z"/><path d="M12 12 16 8"/><path d="M12 12v.01"/></svg>',
}


def _card(icon_key, label, value, caption):
    st.markdown(
        f"""
        <div class="stat-card">
          <div class="stat-icon">{ICONS[icon_key]}</div>
          <div>
            <div class="stat-label">{label}</div>
            <div class="stat-value">{value}</div>
            <div class="stat-caption">{caption}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_kpi_cards(df):
    total_users = len(df)
    high_risk = int((df["risk_band"] == "High Risk").sum())
    critical = int((df["risk_band"] == "Critical").sum())
    total_alerts = int((df["risk_band"] != "Normal").sum())
    average_risk = round(df["risk_score"].mean(), 1)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        with st.container(border=True):
            _card("users", "Total Users", f"{total_users:,}", "All monitored users")

    with col2:
        with st.container(border=True):
            _card("bell", "Total Alerts", f"{total_alerts:,}", "Generated in selected period")

    with col3:
        with st.container(border=True):
            _card("trending-up", "High Risk Users", f"{high_risk:,}", "Users in high risk")

    with col4:
        with st.container(border=True):
            _card("shield-alert", "Critical Risk Users", f"{critical:,}", "Users in critical risk")

    with col5:
        with st.container(border=True):
            _card("gauge", "Avg Risk Score", f"{average_risk}", "Average across all users")
