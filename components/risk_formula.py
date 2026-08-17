import streamlit as st

FACTOR_DEFINITIONS = [
    ("failed_login_score", "Failed Login Rate"),
    ("distinct_geo_score", "Multiple Countries"),
    ("mfa_bypass_score", "MFA Bypass Rate"),
    ("privilege_mismatch_score", "Privilege Escalation"),
    ("lateral_movement_score", "Lateral Movement"),
    ("off_hours_score", "Off-Hours Login"),
    ("new_device_score", "New Device Usage"),
    ("data_volume_score", "Data Volume Spike"),
]


def show_risk_formula(df=None):
    if df is not None:
        active_factors = [
            (col, label) for col, label in FACTOR_DEFINITIONS if col in df.columns
        ]
    else:
        active_factors = FACTOR_DEFINITIONS

    n = len(active_factors)
    weight = 1.0 / n if n > 0 else 0.0

    weight_table = [
        {"Risk Factor": label, "Weight (Wᵢ)": f"{weight * 100:.1f}%"}
        for _, label in active_factors
    ]
    weight_table.append({"Risk Factor": "Total", "Weight (Wᵢ)": "100%"})
    st.table(weight_table)
