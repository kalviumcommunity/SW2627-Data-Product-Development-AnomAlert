import streamlit as st


def filters(df):
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1.4])

    with col1:
        risk_band_options = ["All"]
        if "risk_band" in df.columns:
            risk_band_options += sorted(df["risk_band"].dropna().unique().tolist())
        risk_band = st.selectbox("Risk Band", risk_band_options, key="filter_risk_band")

    with col2:
        # No user_role column in the data yet -- hardcoded options, decorative
        # until a real role column exists to filter on.
        user_role = st.selectbox("User Role", ["All", "Admin", "User"], key="filter_user_role")

    with col3:
        # No country column in the data yet -- decorative until it exists.
        country = st.selectbox("Country", ["All"], key="filter_country")

    with col4:
        # No timestamp column in the data yet -- decorative until it exists.
        time_range = st.selectbox(
            "Time Range",
            ["🕐 Last 24 Hours", "🕐 Last 7 Days", "🕐 Last 30 Days", "🕐 All Time"],
            key="filter_time_range",
        )

    with col5:
        search_user = st.text_input(
            "Search User",
            placeholder="Search by User ID",
            key="filter_search_user",
        ).strip()

    return {
        "risk_band": risk_band,
        "user_role": user_role,
        "country": country,
        "time_range": time_range,
        "search_user": search_user,
    }


def apply_filters(df, selections):
    filtered = df.copy()

    if "risk_band" in df.columns and selections["risk_band"] != "All":
        filtered = filtered[filtered["risk_band"] == selections["risk_band"]]

    if "user_id" in df.columns and selections["search_user"]:
        filtered = filtered[
            filtered["user_id"].astype(str).str.contains(selections["search_user"], case=False, na=False)
        ]

    # user_role / country / time_range have no backing columns yet, so they're
    # visual-only for now -- selecting them won't change the filtered data.

    return filtered