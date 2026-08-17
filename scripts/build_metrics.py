"""Build the per-user `metrics` table from `Raw_data`.

Extends the PRD 7.1 6-metric set with 2 more (new_device_login, data_volume_spike)
to cover injected anomaly patterns (7.4).

Calls compute_risk_scores.main() at the end so metrics.risk_score/risk_band
always exist right after this script runs -- the dashboard (database/db.py)
reads them unconditionally, so a `metrics` table without them (e.g. someone
reruns just this script after a data change) would otherwise crash the UI
with a KeyError until compute_risk_scores.py was remembered and run too.
"""

import sqlite3

import compute_risk_scores

DB_PATH = "AnomAlert.sqlite"


def minmax(values):
    lo, hi = min(values), max(values)
    span = hi - lo
    if span == 0:
        return [0.0 for _ in values]
    return [(v - lo) / span for v in values]


def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # PRD 7.1's original 6
    cur.execute("""
    SELECT
      user_id,
      CAST(SUM(failed_attempts_before_success) AS REAL) / COUNT(*)              AS failed_login_rate,
      COUNT(DISTINCT geo_country)                                                AS distinct_geo_count,
      CAST(SUM(CASE WHEN mfa_used = 0 THEN 1 ELSE 0 END) AS REAL) / COUNT(*)     AS mfa_bypass_rate,
      SUM(CASE WHEN privilege_used != user_role THEN 1 ELSE 0 END)               AS privilege_mismatch_count,
      CAST(COUNT(DISTINCT dst_host) AS REAL) / COUNT(DISTINCT session_id)        AS lateral_movement_rate,
      CAST(SUM(is_off_hours) AS REAL) / COUNT(*)                                 AS off_hours_ratio
    FROM Raw_data
    GROUP BY user_id
    """)
    cols = [d[0] for d in cur.description]
    rows = {r[0]: dict(zip(cols, r)) for r in cur.fetchall()}

    # new_device_login signal: how many distinct devices this user has used
    cur.execute("SELECT user_id, COUNT(DISTINCT device_id) FROM Raw_data GROUP BY user_id")
    for uid, v in cur.fetchall():
        rows[uid]["distinct_device_count"] = v

    # data_volume_spike signal: peak session vs. this user's own average
    # (a raw bytes value doesn't indicate a spike; the ratio to their own
    # baseline does)
    cur.execute("SELECT user_id, MAX(bytes_transferred) * 1.0 / AVG(bytes_transferred) FROM Raw_data GROUP BY user_id")
    for uid, v in cur.fetchall():
        rows[uid]["bytes_spike_ratio"] = v

    rows = list(rows.values())

    score_components = {
        "failed_login_rate": "failed_login_score",
        "distinct_geo_count": "distinct_geo_score",
        "mfa_bypass_rate": "mfa_bypass_score",
        "privilege_mismatch_count": "privilege_mismatch_score",
        "lateral_movement_rate": "lateral_movement_score",
        "off_hours_ratio": "off_hours_score",
        "distinct_device_count": "new_device_score",
        "bytes_spike_ratio": "data_volume_score",
    }

    for comp, score_col in score_components.items():
        vals = [r[comp] for r in rows]
        norm = minmax(vals)
        for r, n in zip(rows, norm):
            r[score_col] = n * 100.0

    cur.execute("DROP TABLE IF EXISTS metrics")
    cur.execute("""
    CREATE TABLE metrics (
      user_id                     VARCHAR(32) PRIMARY KEY,
      failed_login_rate           REAL,
      distinct_geo_count          INTEGER,
      mfa_bypass_rate             REAL,
      privilege_mismatch_count    INTEGER,
      lateral_movement_rate       REAL,
      off_hours_ratio             REAL,
      distinct_device_count       INTEGER,
      bytes_spike_ratio           REAL,
      failed_login_score          REAL,
      distinct_geo_score          REAL,
      mfa_bypass_score            REAL,
      privilege_mismatch_score    REAL,
      lateral_movement_score      REAL,
      off_hours_score             REAL,
      new_device_score            REAL,
      data_volume_score           REAL
    )
    """)

    insert_cols = [
        "user_id", "failed_login_rate", "distinct_geo_count", "mfa_bypass_rate",
        "privilege_mismatch_count", "lateral_movement_rate", "off_hours_ratio",
        "distinct_device_count", "bytes_spike_ratio",
        "failed_login_score", "distinct_geo_score", "mfa_bypass_score",
        "privilege_mismatch_score", "lateral_movement_score", "off_hours_score",
        "new_device_score", "data_volume_score",
    ]
    placeholders = ",".join("?" for _ in insert_cols)
    cur.executemany(
        f"INSERT INTO metrics ({','.join(insert_cols)}) VALUES ({placeholders})",
        [tuple(r[c] for c in insert_cols) for r in rows],
    )

    conn.commit()
    cur.execute("SELECT COUNT(*) FROM metrics")
    print("metrics rows:", cur.fetchone()[0])
    conn.close()

    compute_risk_scores.main()


if __name__ == "__main__":
    main()
