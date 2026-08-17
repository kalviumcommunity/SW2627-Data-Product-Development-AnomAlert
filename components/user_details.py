import streamlit as st

# 8 score columns in `metrics` -> (raw column, display label)
FACTORS = [
    ("failed_login_score", "failed_login_rate", "Failed Login Rate"),
    ("distinct_geo_score", "distinct_geo_count", "Multiple Countries"),
    ("mfa_bypass_score", "mfa_bypass_rate", "MFA Bypass Rate"),
    ("privilege_mismatch_score", "privilege_mismatch_count", "Privilege Escalation"),
    ("lateral_movement_score", "lateral_movement_rate", "Lateral Movement"),
    ("off_hours_score", "off_hours_ratio", "Off-Hours Login"),
    ("new_device_score", "distinct_device_count", "New Device Usage"),
    ("data_volume_score", "bytes_spike_ratio", "Data Volume Spike"),
]
WEIGHT = 1.0 / len(FACTORS)


def impact_level(normalized_score):
    if normalized_score >= 70:
        return "High"
    if normalized_score >= 40:
        return "Medium"
    return "Low"


def show_user_details(df, user_id):
    row = df[df["user_id"] == user_id].iloc[0]

    st.subheader(f"Why User Was Flagged? ({user_id})")
    st.metric("Total Risk Score", f"{row['risk_score']:.1f} / 100", row["risk_band"])

    records = [
        {
            "Risk Factor": label,
            "Observed Value": round(row[raw_col], 3),
            "Impact": impact_level(row[score_col]),
            "Contribution": round(WEIGHT * row[score_col], 1),
        }
        for score_col, raw_col, label in FACTORS
    ]
    st.table(records)
