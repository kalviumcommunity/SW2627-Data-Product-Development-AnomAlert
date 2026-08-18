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
    st.markdown('<div class="section-heading">Risk Score Calculation (How it works)</div>', unsafe_allow_html=True)

    formula_col, table_col = st.columns([1.4, 1])

    with formula_col:
        st.caption("Risk Score is calculated using the weighted and normalized formula")
        with st.container(border=True):
            st.latex(r"\text{Risk Score} = \sum_{i=1}^{n} W_i \times S_i")

        st.markdown(
            f"""
Where,
- **Wᵢ** = Weight of risk factor *i* (importance of the factor)
- **Sᵢ** = Normalized score of risk factor *i* (0-100, based on observed behaviour)
- **n** = Total number of risk factors ({len(FACTOR_LABELS)})
"""
        )

    with table_col:
        st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)
        weight_table = [
            {"Risk Factor": label, "Weight (Wᵢ)": f"{WEIGHT:.1%}"}
            for label in FACTOR_LABELS
        ]
        weight_table.append({"Risk Factor": "Total", "Weight (Wᵢ)": "100%"})
        st.dataframe(weight_table, use_container_width=True, hide_index=True)
