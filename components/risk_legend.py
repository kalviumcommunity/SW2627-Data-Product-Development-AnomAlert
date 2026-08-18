import streamlit as st

from components.badges import band_badge

# Mirrors scripts/compute_risk_scores.py's RISK_BAND_MAX exactly -- these are
# the actual thresholds used to assign risk_band, not placeholder numbers.
BANDS = [
    ("0 - 30", "Normal"),
    ("31 - 60", "Suspicious"),
    ("61 - 80", "High Risk"),
    ("81 - 100", "Critical"),
]


def show_risk_legend():
    with st.container(border=True):
        cols = st.columns([1.1] + [1] * len(BANDS))
        cols[0].markdown(
            '<span style="font-size:0.85rem;font-weight:700;color:var(--text-color);">Risk Score Range: 0 - 100</span>',
            unsafe_allow_html=True,
        )
        for col, (rng, band) in zip(cols[1:], BANDS):
            col.markdown(
                f'<span style="font-size:0.8rem;color:var(--secondary-text-color);margin-right:8px;">{rng}</span>{band_badge(band)}',
                unsafe_allow_html=True,
            )
