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