## AnomAlert Metrics
# Overview

The AnomAlert metrics are per-user security measurements derived from authentication and behavioural data. They help identify unusual activities such as repeated failed logins, access from multiple locations, MFA bypasses, privilege mismatches, unusual login times, new devices, lateral movement, and abnormal data transfer.

These behavioural metrics are converted into risk scores, which are then combined to produce an overall risk_score and risk_band for each user.

1. failed_login_rate

Measures the proportion of authentication attempts that resulted in a failed login.

Purpose: Helps identify repeated or suspicious failed login activity, such as possible brute-force attempts.

2. distinct_geo_count

Measures the number of different countries from which a user's authentication activity was recorded.

Purpose: Helps identify unusual geographic activity, such as access from multiple countries.

3. mfa_bypass_rate

Measures the proportion of authentication events where Multi-Factor Authentication (MFA) was not used.

Purpose: Helps identify weak authentication behaviour or possible MFA bypass activity.

4. privilege_mismatch_count

Counts the number of events where the privilege used does not match the user's assigned role.

Purpose: Helps identify possible privilege escalation or unauthorized access.

5. lateral_movement_rate

Measures the extent to which a user accesses different destination hosts across their sessions.

Purpose: Helps identify rapid movement between systems, which may indicate lateral movement.

6. off_hours_ratio

Measures the proportion of authentication events that occurred outside normal working hours.

Purpose: Helps identify unusual login timing and potentially suspicious after-hours activity.

7. distinct_device_count

Measures the number of different devices associated with a user's authentication activity.

Purpose: Helps identify users accessing the system from multiple or unusual devices.

8. bytes_spike_ratio

Measures unusual increases in the amount of data transferred by a user.

Purpose: Helps identify abnormal data-transfer behaviour that may indicate suspicious activity.

Risk Score Metrics

The following metrics represent normalized scores derived from the behavioural metrics.

9. failed_login_score

Represents the normalized risk contribution of a user's failed login behaviour.

Purpose: Converts failed-login activity into a value that can contribute to the overall risk score.

10. distinct_geo_score

Represents the normalized risk contribution of unusual geographic activity.

Purpose: Converts geographic behaviour into a risk-scoring value.

11. mfa_bypass_score

Represents the normalized risk contribution of MFA bypass or non-use.

Purpose: Measures how much the user's MFA-related behaviour contributes to their overall risk.

12. privilege_mismatch_score

Represents the normalized risk contribution of privilege mismatches.

Purpose: Measures the risk associated with users using privileges that do not match their assigned role.

13. lateral_movement_score

Represents the normalized risk contribution of lateral movement behaviour.

Purpose: Measures the risk associated with accessing multiple systems or hosts.

14. off_hours_score

Represents the normalized risk contribution of authentication activity occurring outside normal hours.

Purpose: Measures the risk associated with unusual login timing.

15. new_device_score

Represents the normalized risk contribution of activity involving new or unusual devices.

Purpose: Helps identify potentially suspicious device usage.

16. data_volume_score

Represents the normalized risk contribution of abnormal data-transfer activity.

Purpose: Measures the risk associated with unusually high data volume.

# Final Risk Metrics
17. risk_score

Represents the user's overall security risk level, calculated using the individual normalized risk factors.

Purpose: Provides a single numerical value that summarizes the user's observed security risk.

18. risk_band

Represents the categorical risk classification assigned to a user based on their overall risk_score.

* The dashboard categorizes users into:
Normal — Low risk behaviour
Suspicious — Behaviour requiring attention
High Risk — Strong indicators of risky behaviour
Critical — Severe or highly suspicious behaviour requiring immediate investigation