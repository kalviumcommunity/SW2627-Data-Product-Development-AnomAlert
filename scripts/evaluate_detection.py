"""Evaluate risk_band against injected anomaly_type labels (PRD Section 8 / AC-3).

For each of the 8 injected patterns: recall = fraction of users who have at
least one event of that pattern whose risk_band ended up above "Normal".

False-positive rate is also reported (fraction of users with ZERO injected
anomalies who still got flagged) but is only meaningful if such users exist.
"""

import sqlite3

DB_PATH = "AnomAlert.sqlite"


def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT user_id, risk_band FROM metrics")
    band_by_user = dict(cur.fetchall())

    cur.execute("SELECT DISTINCT anomaly_type FROM Raw_data WHERE anomaly_type IS NOT NULL")
    patterns = [r[0] for r in cur.fetchall()]

    print(f"{'pattern':<24}{'users_with_pattern':>20}{'flagged':>10}{'recall':>10}")
    for pattern in sorted(patterns):
        cur.execute(
            "SELECT DISTINCT user_id FROM Raw_data WHERE anomaly_type = ?", (pattern,)
        )
        users = [r[0] for r in cur.fetchall()]
        flagged = sum(1 for u in users if band_by_user.get(u) != "Normal")
        recall = flagged / len(users) if users else float("nan")
        print(f"{pattern:<24}{len(users):>20}{flagged:>10}{recall:>10.1%}")

    cur.execute("SELECT COUNT(DISTINCT user_id) FROM Raw_data WHERE anomaly_type IS NOT NULL")
    n_touched = cur.fetchone()[0]
    cur.execute("SELECT COUNT(DISTINCT user_id) FROM Raw_data")
    n_total = cur.fetchone()[0]
    n_clean = n_total - n_touched
    print(f"\nusers with zero injected anomalies (true negatives available): {n_clean} / {n_total}")
    if n_clean:
        cur.execute(
            f"""SELECT user_id FROM Raw_data
                GROUP BY user_id
                HAVING SUM(CASE WHEN anomaly_type IS NOT NULL THEN 1 ELSE 0 END) = 0"""
        )
        clean_users = [r[0] for r in cur.fetchall()]
        false_positives = sum(1 for u in clean_users if band_by_user.get(u) != "Normal")
        print(f"false-positive rate: {false_positives}/{n_clean} = {false_positives / n_clean:.1%}")
    else:
        print("false-positive rate: UNDEFINED -- every user has at least one injected anomaly, "
              "so there is no clean control group to measure false positives against.")

    conn.close()


if __name__ == "__main__":
    main()
