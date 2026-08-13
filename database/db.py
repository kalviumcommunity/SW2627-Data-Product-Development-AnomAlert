import sqlite3
import pandas as pd

DB_NAME = "AnomAlert.sqlite"

def load_metrics():
    conn = sqlite3.connect(DB_NAME)

    df = pd.read_sql_query(
        "SELECT * FROM metrics",
        conn
    )

    conn.close()

    return df