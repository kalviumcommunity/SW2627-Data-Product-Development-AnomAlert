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


@st.cache_data
def load_sidebar_summary() -> dict:
    """Load overall summary statistics for the sidebar.

    Returns
    -------
    dict with keys:
        total_logins, success_rate, failed_logins, unique_devices, unique_countries
    """
    conn = sqlite3.connect(DB_NAME)
    query = """
        SELECT
          COUNT(*) as total_logins,
          SUM(CASE WHEN auth_result = 'Success' THEN 1 ELSE 0 END) as success_logins,
          SUM(CASE WHEN auth_result = 'Failure' THEN 1 ELSE 0 END) as failed_logins,
          COUNT(DISTINCT device_id) as unique_devices,
          COUNT(DISTINCT geo_country) as unique_countries
        FROM Raw_data
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    if df.empty or df.iloc[0]["total_logins"] == 0:
        return {
            "total_logins": 0,
            "success_rate": 0.0,
            "failed_logins": 0,
            "unique_devices": 0,
            "unique_countries": 0,
        }

    row = df.iloc[0]
    total = int(row["total_logins"])
    success = int(row["success_logins"] or 0)
    failed = int(row["failed_logins"] or 0)
    devices = int(row["unique_devices"] or 0)
    countries = int(row["unique_countries"] or 0)

    success_rate = (success * 100.0) / total if total > 0 else 0.0

    return {
        "total_logins": total,
        "success_rate": success_rate,
        "failed_logins": failed,
        "unique_devices": devices,
        "unique_countries": countries,
    }
