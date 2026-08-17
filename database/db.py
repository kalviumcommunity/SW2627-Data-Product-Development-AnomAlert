import sqlite3
import streamlit as st
import pandas as pd

DB_NAME = "AnomAlert.sqlite"


def load_metrics():
    conn = sqlite3.connect(DB_NAME)

    df = pd.read_sql_query(
        "SELECT * FROM metrics",
        conn
    )

    conn.close()

    if "risk_score" not in df.columns or "risk_band" not in df.columns:
        st.error(
            "metrics table is missing risk_score/risk_band. "
            "Run `python scripts/build_metrics.py` to rebuild it (this also "
            "runs the scoring step)."
        )
        st.stop()

    return df


def load_recent_events(limit: int = 10, user_id: str = None) -> pd.DataFrame:
    """Load recent authentication events from Raw_data.

    Parameters
    ----------
    limit : int
        Maximum number of rows to return (default 10).
    user_id : str or None
        If provided, filters events to only this user.

    Returns
    -------
    pd.DataFrame with columns:
        timestamp, user_id, logon_type, auth_result, device_id,
        geo_country, client_ip
    """
    conn = sqlite3.connect(DB_NAME)

    if user_id:
        query = """
            SELECT timestamp, user_id, logon_type, auth_result,
                   device_id, geo_country, client_ip
            FROM   Raw_data
            WHERE  user_id = ?
            ORDER  BY event_id DESC
            LIMIT  ?
        """
        df = pd.read_sql_query(query, conn, params=(user_id, limit))
    else:
        query = """
            SELECT timestamp, user_id, logon_type, auth_result,
                   device_id, geo_country, client_ip
            FROM   Raw_data
            ORDER  BY event_id DESC
            LIMIT  ?
        """
        df = pd.read_sql_query(query, conn, params=(limit,))

    conn.close()
    return df