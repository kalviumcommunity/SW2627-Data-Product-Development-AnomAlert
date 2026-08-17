import streamlit as st

# Mirrors scripts/compute_risk_scores.py's FACTORS exactly -- this is the
# actual formula being computed, not the PRD's original 6-factor version
# (deliberately extended to 8, equal-weighted; see that script's docstring
# for why).
FACTOR_LABELS = [
    "Failed Login Rate",
    "Multiple Countries",
    "MFA Bypass Rate",
    "Privilege Escalation",
    "Lateral Movement",
    "Off-Hours Login",
    "New Device Usage",
    "Data Volume Spike",
]
WEIGHT = 1 / len(FACTOR_LABELS)


def show_risk_formula():
    st.subheader("Risk Score Calculation (How it works)")
    st.caption("Risk Score is calculated using the weighted formula below")

    st.latex(r"\text{Risk Score} = \sum_{i=1}^{n} W_i \times S_i")

    st.markdown(
        f"""
- **Wᵢ** = weight of risk factor *i* (importance of the factor)
- **Sᵢ** = normalized score of risk factor *i* (0-100, based on observed behaviour)
- **n** = total number of risk factors ({len(FACTOR_LABELS)})
"""
    )

    weight_table = [
        {"Risk Factor": label, "Weight (Wᵢ)": f"{WEIGHT:.1%}"}
        for label in FACTOR_LABELS
    ]
    weight_table.append({"Risk Factor": "Total", "Weight (Wᵢ)": "100%"})
    st.table(weight_table)
