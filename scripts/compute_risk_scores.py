"""Compute weighted risk scores for each user based on the 8 behavioral metrics in `metrics`.

Writes: metrics.risk_score, metrics.risk_band
"""

import sqlite3
import numpy as np

DB_PATH = "AnomAlert.sqlite"

# 8 behavioral metric factors engineered in `metrics` -> equal weight (1/8 = 12.5% each)
FACTORS = [
    ("failed_login_score",         1 / 8),
    ("distinct_geo_score",         1 / 8),
    ("mfa_bypass_score",           1 / 8),
    ("privilege_mismatch_score",   1 / 8),
    ("lateral_movement_score",     1 / 8),
    ("off_hours_score",            1 / 8),
    ("new_device_score",           1 / 8),
    ("data_volume_score",          1 / 8),
]
assert abs(sum(w for _, w in FACTORS) - 1.0) < 1e-9

# Risk band thresholds
RISK_BAND_MAX = [
    (30, "Normal"),
    (60, "Suspicious"),
    (80, "High Risk"),
]


def band_for(score: float) -> str:
    for upper, label in RISK_BAND_MAX:
        if score <= upper:
            return label
    return "Critical"


def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    score_cols = [f[0] for f in FACTORS]
    weights = np.array([f[1] for f in FACTORS])

    cur.execute(f"SELECT user_id, {', '.join(score_cols)} FROM metrics")
    fetched = cur.fetchall()
    user_ids = [row[0] for row in fetched]
    score_matrix = np.array([row[1:] for row in fetched], dtype=float)

    risk_scores = (score_matrix * weights).sum(axis=1)
    risk_bands = [band_for(s) for s in risk_scores]

    cur.execute("PRAGMA table_info(metrics)")
    existing_cols = [r[1] for r in cur.fetchall()]
    if "risk_score" not in existing_cols:
        cur.execute("ALTER TABLE metrics ADD COLUMN risk_score REAL")
    if "risk_band" not in existing_cols:
        cur.execute("ALTER TABLE metrics ADD COLUMN risk_band VARCHAR(16)")
    cur.executemany(
        "UPDATE metrics SET risk_score = ?, risk_band = ? WHERE user_id = ?",
        list(zip(risk_scores.tolist(), risk_bands, user_ids)),
    )
    conn.commit()

    cur.execute("SELECT risk_band, COUNT(*) FROM metrics GROUP BY risk_band ORDER BY MIN(risk_score)")
    print("band distribution:", cur.fetchall())
    cur.execute("SELECT user_id, risk_score, risk_band FROM metrics ORDER BY risk_score DESC LIMIT 5")
    print("top 5:", cur.fetchall())

    conn.close()


if __name__ == "__main__":
    main()
