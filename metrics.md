## AnomAlert Metrics

# Overview

The AnomAlert metrics are per-user security measurements derived from authentication and behavioural data. They help identify unusual activities such as repeated failed logins, access from multiple locations, MFA bypasses, privilege mismatches, unusual login times, activity across multiple devices, lateral movement, and abnormal data-transfer behaviour.

These behavioural metrics are converted into normalized scores, which are then combined using equal weights to produce an overall `risk_score` and `risk_band` for each user.

---

## 1. failed_login_rate

Measures the total number of `failed_attempts_before_success` divided by the user's total number of event rows.

Because a single event can contain multiple failed attempts, this metric is not necessarily bounded between 0 and 1.

**Purpose:** Helps identify repeated or suspicious failed-login activity, such as possible brute-force attempts.

---

## 2. distinct_geo_count

Measures the number of different countries from which a user's authentication activity was recorded.

**Purpose:** Helps identify unusual geographic activity, such as access from multiple countries.

---

## 3. mfa_bypass_rate

Measures the proportion of authentication events where Multi-Factor Authentication (MFA) was not used.

**Purpose:** Helps identify weak authentication behaviour or possible MFA bypass activity.

---

## 4. privilege_mismatch_count

Counts the number of events where the privilege used does not match the user's assigned role.

**Purpose:** Helps identify possible privilege escalation or unauthorized access.

---

## 5. lateral_movement_rate

Measures the extent to which a user accesses different destination hosts across their sessions.

**Purpose:** Helps identify movement between multiple systems, which may indicate lateral movement.

---

## 6. off_hours_ratio

Measures the proportion of authentication events that occurred outside normal working hours.

**Purpose:** Helps identify unusual login timing and potentially suspicious after-hours activity.

---

## 7. distinct_device_count

Measures the number of different device IDs associated with a user's authentication activity.

**Purpose:** Helps identify users accessing the system from multiple devices.

---

## 8. bytes_spike_ratio

Measures the ratio of a user's maximum transferred bytes to their average transferred bytes.

**Purpose:** Helps identify within-user spikes or unusual variation in data-transfer activity.

---

# Risk Score Metrics

The following metrics are dataset-wide min-max normalized scores on a 0–100 scale. They are derived from the corresponding behavioural metrics.

Each score has an equal weight of 1/8 when calculating the final `risk_score`.

---

## 9. failed_login_score

Represents the dataset-wide min-max normalized value of `failed_login_rate` on a 0–100 scale.

**Purpose:** Represents the normalized level of failed-login behaviour for the user.

Its weighted contribution to the final risk score is:

`failed_login_score × 1/8`

---

## 10. distinct_geo_score

Represents the dataset-wide min-max normalized value of `distinct_geo_count` on a 0–100 scale.

**Purpose:** Represents the normalized level of geographic variation in the user's authentication activity.

Its weighted contribution to the final risk score is:

`distinct_geo_score × 1/8`

---

## 11. mfa_bypass_score

Represents the dataset-wide min-max normalized value of `mfa_bypass_rate` on a 0–100 scale.

**Purpose:** Represents the normalized level of MFA bypass or non-use behaviour.

Its weighted contribution to the final risk score is:

`mfa_bypass_score × 1/8`

---

## 12. privilege_mismatch_score

Represents the dataset-wide min-max normalized value of `privilege_mismatch_count` on a 0–100 scale.

**Purpose:** Represents the normalized level of privilege mismatch behaviour.

Its weighted contribution to the final risk score is:

`privilege_mismatch_score × 1/8`

---

## 13. lateral_movement_score

Represents the dataset-wide min-max normalized value of `lateral_movement_rate` on a 0–100 scale.

**Purpose:** Represents the normalized level of lateral movement behaviour.

Its weighted contribution to the final risk score is:

`lateral_movement_score × 1/8`

---

## 14. off_hours_score

Represents the dataset-wide min-max normalized value of `off_hours_ratio` on a 0–100 scale.

**Purpose:** Represents the normalized level of authentication activity occurring outside normal working hours.

Its weighted contribution to the final risk score is:

`off_hours_score × 1/8`

---

## 15. new_device_score

Represents the dataset-wide min-max normalized value of `distinct_device_count` on a 0–100 scale.

It measures the number of distinct device IDs associated with a user. It does not determine whether a device is newly observed, first-seen, recent, or unusual.

**Purpose:** Represents the normalized level of distinct-device activity.

Its weighted contribution to the final risk score is:

`new_device_score × 1/8`

---

## 16. data_volume_score

Represents the dataset-wide min-max normalized value of the ratio between a user's maximum transferred bytes and their average transferred bytes.

It measures within-user data-transfer spikiness rather than absolute high data volume.

**Purpose:** Represents the normalized level of variation in the user's data-transfer activity.

Its weighted contribution to the final risk score is:

`data_volume_score × 1/8`

---

# Final Risk Metrics

## 17. risk_score

Represents the user's overall security risk level, calculated from the eight normalized risk scores.

Each score contributes equally with a weight of 1/8.

Conceptually:

`risk_score = (failed_login_score + distinct_geo_score + mfa_bypass_score + privilege_mismatch_score + lateral_movement_score + off_hours_score + new_device_score + data_volume_score) / 8`

**Purpose:** Provides a single numerical value that summarizes the user's calculated security risk.

---

## 18. risk_band

Represents the categorical risk classification assigned to a user based on their overall `risk_score`.

**The dashboard categorizes users into:**

- **Normal** — Low-risk behaviour
- **Suspicious** — Behaviour requiring attention
- **High Risk** — Strong indicators of risky behaviour
- **Critical** — Severe or highly suspicious behaviour requiring immediate investigation