import streamlit as st
from database.db import load_metrics
from components.kpi_cards import show_kpi_cards
from components.top_users import show_top_users
from components.user_details import show_user_details
from components.risk_formula import show_risk_formula
from components.risk_distribution import show_risk_distribution
from components.recent_events import show_recent_events
from components.risk_legend import show_risk_legend
from components.filters import filters, apply_filters
from components.sidebar import show_sidebar

st.set_page_config(
    page_title="AnomAlert Dashboard",
    page_icon="🛡️",
    layout="wide"
)

st.markdown("""
<style>

/* Section heading -- plain bold text, no default Streamlit top margin so it
   sits flush with the top of its bordered container. */
.section-heading{
    font-size:1.05rem;
    font-weight:700;
    color:var(--text-color);
    margin:0 0 14px 0;
}

/* KPI stat cards */
.stat-card{
    display:flex;
    align-items:flex-start;
    gap:14px;
}
.stat-icon{
    width:44px;
    height:44px;
    border-radius:10px;
    background:rgba(128,128,128,0.08);
    display:flex;
    align-items:center;
    justify-content:center;
    color:var(--text-color);
    flex-shrink:0;
}
.stat-label{
    font-size:0.85rem;
    font-weight:600;
    color:var(--text-color);
    margin:2px 0 0 0;
}
.stat-value{
    font-size:1.7rem;
    font-weight:700;
    color:var(--text-color);
    margin:6px 0 2px 0;
    line-height:1.1;
}
.stat-caption{
    font-size:0.78rem;
    color:var(--secondary-text-color);
    margin:0;
}

/* Table-style column headers/cells: truncate instead of breaking mid-word
   when a narrow column (e.g. sidebar expanded, smaller viewport) can't fit
   the label at full width. */
.col-label{
    display:block;
    white-space:nowrap;
    overflow:hidden;
    text-overflow:ellipsis;
}

/* Filter bar: bold, dark labels on the selectboxes/text input */
.st-key-filter_bar [data-testid="stSelectbox"] label,
.st-key-filter_bar [data-testid="stTextInput"] label{
    font-size:13px;
    font-weight:600;
    color:var(--text-color);
}

</style>
""", unsafe_allow_html=True)

show_sidebar()

df = load_metrics()

show_kpi_cards(df)

with st.container(key="filter_bar", border=True):
    selections = filters(df)
df = apply_filters(df, selections)

left, middle, right = st.columns([1, 1.3, 1.3])

with left:
    with st.container(border=True):
        st.markdown('<div class="section-heading">Risk Score Distribution</div>', unsafe_allow_html=True)
        show_risk_distribution(df)

with middle:
    with st.container(border=True):
        st.markdown('<div class="section-heading">Top 10 Risky Users</div>', unsafe_allow_html=True)
        show_top_users(df)

with right:
    if st.session_state.get("selected_user"):
        with st.container(border=True):
            show_user_details(df, st.session_state.selected_user)

with st.container(border=True):
    st.markdown('<div class="section-heading">Recent Authentication Events</div>', unsafe_allow_html=True)
    show_recent_events(st.session_state.get("selected_user"))

with st.container(border=True):
    show_risk_formula()

show_risk_legend()