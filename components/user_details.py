import streamlit as st

from components.badges import band_badge, impact_badge

# score column in `metrics` -> (raw column, display label, formatter)
# mirrors scripts/compute_risk_scores.py's FACTORS (equal 1/9 weight each,
# deliberately deviates from PRD 7.2's fixed 6-weight formula -- see that
# script's docstring for why)
FACTORS = [
    ("failed_login_score", "failed_login_rate", "Failed Login Rate", lambda v: f"{v:.0%} of attempts failed"),
    ("distinct_geo_score", "distinct_geo_count", "Multiple Countries", lambda v: f"{int(v)} countries accessed"),
    ("mfa_bypass_score", "mfa_bypass_rate", "MFA Bypass Rate", lambda v: f"{v:.0%} of logins without MFA"),
    ("privilege_mismatch_score", "privilege_mismatch_count", "Privilege Escalation", lambda v: f"{int(v)} privilege mismatches"),
    ("lateral_movement_score", "lateral_movement_rate", "Lateral Movement", lambda v: f"{v:.2f} hosts/session"),
    ("off_hours_score", "off_hours_ratio", "Off-Hours Login", lambda v: f"{v:.0%} of logins off-hours"),
    ("new_device_score", "distinct_device_count", "New Device Usage", lambda v: f"{int(v)} distinct devices"),
    ("data_volume_score", "bytes_spike_ratio", "Data Volume Spike", lambda v: f"{v:.1f}x baseline volume"),
]
WEIGHT = 1 / len(FACTORS)


def impact_level(normalized_score):
    if normalized_score >= 70:
        return "High"
    if normalized_score >= 40:
        return "Medium"
    return "Low"


def show_user_details(df, user_id):
    matches = df[df["user_id"] == user_id]
    if matches.empty:
        st.info(f"No data for user {user_id} in the current filter selection.")
        return
    row = matches.iloc[0]

    st.markdown(f'<div class="section-heading">Why User Was Flagged? ({user_id})</div>', unsafe_allow_html=True)

    header_left, header_right = st.columns([2, 1])
    with header_left:
        st.markdown(
            f"""
            <div style="display:flex;align-items:center;gap:12px;">
              <div style="width:40px;height:40px;border-radius:50%;background:rgba(128,128,128,0.15);
                          display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                     stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>
                </svg>
              </div>
              <div>
                <div style="font-size:0.75rem;color:var(--secondary-text-color);">User ID</div>
                <div style="font-weight:700;color:var(--text-color);">{user_id}</div>
              </div>
              <div style="margin-left:6px;">{band_badge(row['risk_band'])}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with header_right:
        st.markdown(
            f"""
            <div style="text-align:right;">
              <div style="font-size:0.75rem;color:var(--secondary-text-color);">Risk Score</div>
              <div style="font-size:1.6rem;font-weight:700;color:var(--text-color);">{row['risk_score']:.0f}<span style="font-size:0.9rem;color:var(--secondary-text-color);"> / 100</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)

    col_ratios = [1.6, 2.2, 0.9, 0.8]
    head = st.columns(col_ratios)
    for col, text in zip(head, ["Risk Factor", "Observed Behaviour", "Impact", "Score"]):
        col.markdown(f'<span class="col-label" style="font-size:0.78rem;font-weight:700;color:var(--secondary-text-color);">{text}</span>', unsafe_allow_html=True)
    st.markdown('<hr style="margin:4px 0 6px 0;">', unsafe_allow_html=True)

    for score_col, raw_col, label, fmt in FACTORS:
        level = impact_level(row[score_col])
        c = st.columns(col_ratios)
        c[0].markdown(f"**{label}**")
        c[1].write(fmt(row[raw_col]))
        c[2].markdown(impact_badge(level), unsafe_allow_html=True)
        c[3].markdown(f'<span class="col-label">{WEIGHT * row[score_col]:.0f}</span>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="display:flex;justify-content:space-between;align-items:center;
                    margin-top:14px;padding-top:12px;border-top:1px solid rgba(128,128,128,0.2);">
          <span style="font-weight:700;color:var(--text-color);">Total Risk Score</span>
          <span style="font-weight:700;font-size:1.1rem;color:var(--text-color);">{row['risk_score']:.0f} / 100</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
