-- Injects the 8 synthetic anomaly patterns (PRD section 7.4) into Raw_data,
-- tagging each affected row with anomaly_type for evaluation only (the
-- scoring engine must never read this column).
--
-- CAVEAT: dormant_reactivation is only approximated below. Raw_data has no
-- date field (timestamp is mm:ss within a single ~1hr window), so "30+ days
-- of silence" cannot be represented. The query instead picks the largest
-- event_id gaps per user as a time-order proxy -- flag this to the team.
ALTER TABLE Raw_data
ADD COLUMN anomaly_type VARCHAR(32);
-- 1. brute_force: repeated failures immediately preceding a success
UPDATE Raw_data
SET failed_attempts_before_success = 8 + ABS(RANDOM() % 13),
    -- 8-20
    auth_result = 'Success',
    anomaly_type = 'brute_force'
WHERE event_id IN (
        SELECT event_id
        FROM Raw_data
        WHERE anomaly_type IS NULL
        ORDER BY RANDOM()
        LIMIT 1500
    );
-- 2. impossible_travel: same user, two adjacent-in-time events, forced to
-- a country different from the immediately preceding one
WITH ordered AS (
    SELECT event_id,
        user_id,
        geo_country,
        LAG(geo_country) OVER (
            PARTITION BY user_id
            ORDER BY timestamp
        ) AS prev_country
    FROM Raw_data
    WHERE anomaly_type IS NULL
),
picked AS (
    SELECT event_id,
        prev_country
    FROM ordered
    WHERE prev_country IS NOT NULL
    ORDER BY RANDOM()
    LIMIT 1500
)
UPDATE Raw_data
SET geo_country = CASE
        WHEN picked.prev_country = 'US' THEN 'RU'
        ELSE 'US'
    END,
    anomaly_type = 'impossible_travel'
FROM picked
WHERE Raw_data.event_id = picked.event_id;
-- 3. off_hours_access: standard user forced into the 2-4am off-hours flag
UPDATE Raw_data
SET is_off_hours = 1,
    anomaly_type = 'off_hours_access'
WHERE event_id IN (
        SELECT event_id
        FROM Raw_data
        WHERE anomaly_type IS NULL
            AND user_role = 'standard'
        ORDER BY RANDOM()
        LIMIT 1500
    );
-- 4. privilege_escalation: standard-role user using admin privilege on a DC host
UPDATE Raw_data
SET privilege_used = 'admin',
    dst_host = 'DC-01',
    anomaly_type = 'privilege_escalation'
WHERE event_id IN (
        SELECT event_id
        FROM Raw_data
        WHERE anomaly_type IS NULL
            AND user_role = 'standard'
        ORDER BY RANDOM()
        LIMIT 1500
    );
-- 5. new_device_login: device_id guaranteed unique to this event/user (never seen before)
UPDATE Raw_data
SET device_id = 'NEWDEV-' || user_id || '-' || event_id,
    anomaly_type = 'new_device_login'
WHERE event_id IN (
        SELECT event_id
        FROM Raw_data
        WHERE anomaly_type IS NULL
        ORDER BY RANDOM()
        LIMIT 1500
    );
-- 6. dormant_reactivation (APPROXIMATION -- see caveat above):
-- events following the largest event_id gap for their user
WITH ordered AS (
    SELECT event_id,
        user_id,
        event_id - LAG(event_id) OVER (
            PARTITION BY user_id
            ORDER BY event_id
        ) AS gap
    FROM Raw_data
    WHERE anomaly_type IS NULL
),
picked AS (
    SELECT event_id
    FROM ordered
    WHERE gap IS NOT NULL
    ORDER BY gap DESC
    LIMIT 1500
)
UPDATE Raw_data
SET anomaly_type = 'dormant_reactivation'
WHERE event_id IN (
        SELECT event_id
        FROM picked
    );
-- 7. data_volume_spike: bytes_transferred forced to 10x that user's own average
WITH user_avg AS (
    SELECT user_id,
        AVG(bytes_transferred) AS avg_bytes
    FROM Raw_data
    GROUP BY user_id
),
picked AS (
    SELECT r.event_id,
        u.avg_bytes
    FROM Raw_data r
        JOIN user_avg u ON r.user_id = u.user_id
    WHERE r.anomaly_type IS NULL
    ORDER BY RANDOM()
    LIMIT 1500
)
UPDATE Raw_data
SET bytes_transferred = CAST(picked.avg_bytes * 10 AS INTEGER),
    anomaly_type = 'data_volume_spike'
FROM picked
WHERE Raw_data.event_id = picked.event_id;
-- 8. rapid_lateral_movement: rows within ~300 sessions forced onto many distinct hosts
WITH picked_sessions AS (
    SELECT session_id
    FROM Raw_data
    WHERE anomaly_type IS NULL
    GROUP BY session_id
    HAVING COUNT(*) >= 3
    ORDER BY RANDOM()
    LIMIT 300
), picked_rows AS (
    SELECT event_id,
        session_id,
        ROW_NUMBER() OVER (
            PARTITION BY session_id
            ORDER BY event_id
        ) AS rn
    FROM Raw_data
    WHERE session_id IN (
            SELECT session_id
            FROM picked_sessions
        )
)
UPDATE Raw_data
SET dst_host = 'SRV-' || (100 + (picked_rows.rn % 20)),
    anomaly_type = 'rapid_lateral_movement'
FROM picked_rows
WHERE Raw_data.event_id = picked_rows.event_id;