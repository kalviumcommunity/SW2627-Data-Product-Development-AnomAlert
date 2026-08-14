import streamlit as st
from components.user_details import show_user_details


def show_top_users(df):
    top10 = df.sort_values("risk_score", ascending=False).head(10).reset_index(drop=True)

    if "selected_user" not in st.session_state:
        st.session_state.selected_user = None

    header = st.columns([1, 2, 2, 2, 2])
    header[0].markdown("**Rank**")
    header[1].markdown("**User ID**")
    header[2].markdown("**Risk Score**")
    header[3].markdown("**Risk Band**")
    header[4].markdown("**Action**")

    for i, row in top10.iterrows():
        c = st.columns([1, 2, 2, 2, 2])
        c[0].write(i + 1)
        c[1].write(row["user_id"])
        c[2].write(round(row["risk_score"], 1))
        c[3].write(row["risk_band"])
        if c[4].button("View", key=f"view_{row['user_id']}"):
            st.session_state.selected_user = row["user_id"]

    if st.session_state.selected_user:
        st.divider()
        show_user_details(df, st.session_state.selected_user)
