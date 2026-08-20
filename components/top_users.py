import streamlit as st

from components.badges import band_badge


def show_top_users(df):
    top10 = df.sort_values("risk_score", ascending=False).head(10).reset_index(drop=True)

    if top10.empty:
        st.caption("No users match the current filters.")
        return

    if not st.session_state.get("selected_user"):
        st.session_state.selected_user = top10.iloc[0]["user_id"]  # default: top-ranked user

    col_ratios = [0.6, 1.5, 1.0, 1.5, 1.3]
    header = st.columns(col_ratios)
    for col, text in zip(header, ["Rank", "User ID", "Score", "Risk Band", "Action"]):
        col.markdown(f'<span class="col-label" style="font-size:0.8rem;font-weight:700;color:var(--secondary-text-color);">{text}</span>', unsafe_allow_html=True)

    st.markdown('<hr style="margin:6px 0 8px 0;">', unsafe_allow_html=True)

    for i, row in top10.iterrows():
        c = st.columns(col_ratios)
        c[0].markdown(f'<span class="col-label"><b>{i + 1}</b></span>', unsafe_allow_html=True)
        c[1].markdown(f'<span class="col-label">{row["user_id"]}</span>', unsafe_allow_html=True)
        c[2].markdown(f'<span class="col-label"><b>{row["risk_score"]:.0f}</b></span>', unsafe_allow_html=True)
        c[3].markdown(band_badge(row["risk_band"]), unsafe_allow_html=True)
        if c[4].button("View", key=f"view_{row['user_id']}", use_container_width=True):
            st.session_state.selected_user = row["user_id"]
