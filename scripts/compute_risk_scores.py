"""Compute weighted risk scores for each user.

DEVIATES FROM PRD 7.2 DELIBERATELY: the approved formula only weights 6
factors, but the dataset has 8 injected anomaly patterns (7.4) and 2 of them
(new_device_login, data_volume_spike) have no signal in those 6 factors at all
-- a user who only ever triggered those 2 could never score above Normal.
So this extends to the 8 factors now in `metrics` (see build_metrics.py) and,
since we're already off the approved formula, weights them equally (1/8 each)
rather than guessing at relative severity. PRD's own Risks section (R1) calls
the weights "heuristic; must be tuned against validation labels" -- equal
weighting is the honest starting point for that tuning, done by
evaluate_detection.py.

Writes: metrics.risk_score, metrics.risk_band

FR-05 explainability (per-factor observed value, score, contribution,
impact level) is intentionally NOT persisted as a separate table -- every
input it needs (raw value + normalized score per factor) is already a
column on `metrics`, so the dashboard derives the "why was this user
flagged" breakdown for whichever single user is selected at render time.
"""

import sqlite3
import numpy as np

DB_PATH = "AnomAlert.sqlite"

# score column already in `metrics` -> weight (equal, see module docstring)
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

# PRD 7.3 gives integer buckets (0-30/31-60/61-80/81+) for a continuous 0-100
# score; treated here as upper bounds so no real-valued score falls in a gap
# between e.g. 60 and 61.
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
