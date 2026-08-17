"""US-301 – Recent Authentication Events component.

Uses only native Streamlit primitives so it adapts automatically to
whatever theme the user has set — no hardcoded colours or CSS.

Timestamp note
--------------
The Raw_data `timestamp` column stores a within-session offset in
MM:SS.f format (e.g. "59:13.0"). The dataset has no calendar date
field — the README explicitly states the column covers "only a ~1-hr
mm:ss window". Displaying it as-is IS the real data; no transformation
is applied. The column is labelled "Time (MM:SS)" so users understand
the format.

Events are ordered by `event_id DESC` (the sequential primary key) so
the most recently inserted rows appear first — this is the correct
chronological ordering for this dataset.
"""

import streamlit as st
import pandas as pd
from database.db import load_recent_events

# Number of rows shown in collapsed vs expanded view
LIMIT_DEFAULT  = 10
LIMIT_EXPANDED = 100


def _format_events(df: pd.DataFrame) -> pd.DataFrame:
    """Rename and select columns for clean display."""
    return df.rename(columns={
        "timestamp":   "Time (MM:SS)",
        "user_id":     "User ID",
        "logon_type":  "Event Type",
        "auth_result": "Result",
        "device_id":   "Device",
        "geo_country": "Location",
        "client_ip":   "IP Address",
    })[["Time (MM:SS)", "User ID", "Event Type", "Result", "Device", "Location", "IP Address"]]


def show_recent_events(selected_user: str = None) -> None:
    """Render the Recent Authentication Events section (US-301).

    Parameters
    ----------
    selected_user : str or None
        Currently selected user from the Top 10 Risky Users table.
        When set, a filter checkbox lets the analyst scope the table
        to only that user's events.
    """

    # ── session state defaults ────────────────────────────────────────────────
    if "rae_expanded" not in st.session_state:
        st.session_state.rae_expanded = False
    if "rae_filter_user" not in st.session_state:
        st.session_state.rae_filter_user = False

    # ── per-user filter checkbox (only when a user is selected) ──────────────
    if selected_user:
        st.session_state.rae_filter_user = st.checkbox(
            f"🔍 Filter by selected user ({selected_user})",
            value=st.session_state.rae_filter_user,
            key="rae_filter_checkbox",
        )

    # ── resolve query parameters ──────────────────────────────────────────────
    limit = LIMIT_EXPANDED if st.session_state.rae_expanded else LIMIT_DEFAULT
    user_filter = (
        selected_user
        if (selected_user and st.session_state.rae_filter_user)
        else None
    )

    events_df = load_recent_events(limit=limit, user_id=user_filter)

    # ── display ───────────────────────────────────────────────────────────────
    if events_df.empty:
        st.info("No authentication events found for the selected filter.")
        return

    st.caption(
        "⏱ Time column shows the within-session offset (MM:SS) "
        "from the raw dataset — no calendar date is stored in Raw_data."
    )

    st.dataframe(
        _format_events(events_df),
        use_container_width=True,
        hide_index=True,
    )

    # ── View All / Show Less toggle ───────────────────────────────────────────
    btn_label = "⬆ Show Less" if st.session_state.rae_expanded else "View All Events →"
    if st.button(btn_label, key="rae_toggle_btn"):
        st.session_state.rae_expanded = not st.session_state.rae_expanded
        st.rerun()
