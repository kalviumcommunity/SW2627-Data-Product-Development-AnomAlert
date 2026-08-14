# AnomAlert

Detect what others miss.

---

## What It Is

AnomAlert is a cybersecurity data product that surfaces behavioral anomalies in enterprise authentication logs — brute-force attempts, impossible travel, privilege escalation, lateral movement, and more. It turns raw login events into a quantified Risk Score, giving security teams something they can act on.

---

## The Problem

Authentication logs are abundant. Insight is not.

Traditional SIEM tools surface events. AnomAlert surfaces *patterns* — the subtle behavioral signatures that appear before an account is compromised. No pre-labeled `is_malicious` flag. No cheating. Just signal engineered from the raw data itself.

---

## Dataset

**180,000 synthetic enterprise authentication events** — sourced from a research-grade Kaggle dataset and refined for this product.

→ [View on Kaggle](https://www.kaggle.com/datasets/danielpeng1995/synthetic-enterprise-auth-logs)

### Columns

| Column | Type | Description |
|---|---|---|
| `event_id` | INTEGER | Unique identifier for each authentication event |
| `timestamp` | VARCHAR | Time of the event (mm:ss within a ~1-hr window) |
| `user_id` | VARCHAR | User identifier (U0001–U0500) |
| `user_role` | VARCHAR | `standard` or `admin` |
| `src_host` | VARCHAR | Source workstation initiating the request |
| `src_subnet` | VARCHAR | Network subnet of the source host |
| `dst_host` | VARCHAR | Destination server or domain controller |
| `auth_protocol` | VARCHAR | `Kerberos` or `NTLM` |
| `logon_type` | VARCHAR | Interactive / Network / Service / Remote Interactive |
| `auth_result` | VARCHAR | `Success` or `Failure` |
| `client_ip` | VARCHAR | IP address of the authenticating client |
| `geo_country` | VARCHAR | Country inferred from client IP |
| `geo_city` | VARCHAR | City inferred from client IP |
| `device_id` | VARCHAR | Device fingerprint of the authenticating endpoint |
| `mfa_used` | BOOLEAN | Whether MFA was used |
| `session_id` | VARCHAR | Session grouping identifier |
| `session_duration_sec` | INTEGER | Duration of the authenticated session |
| `bytes_transferred` | INTEGER | Data volume transferred during the session |
| `failed_attempts_before_success` | INTEGER | Consecutive failures before a successful login |
| `is_off_hours` | BOOLEAN | Whether the event occurred outside business hours |
| `privilege_used` | VARCHAR | Privilege level exercised (`standard` or `admin`) |
| `anomaly_type` | VARCHAR | **Evaluation label only** — never read by scoring logic |

### What Was Removed

The original dataset included `is_domain_controller_target` and `is_malicious`. Both were dropped — the first was redundant, and the second is exactly the ground truth the scoring engine must derive on its own.

---

## Anomaly Injection

With labels stripped, the dataset was purely normal activity. To build and evaluate a detector, we needed ground truth — synthetic anomalies embedded directly into the data, tagged only for evaluation.

**`inject.sql`** injects 8 behavioral anomaly patterns (per PRD §7.4) into the `Raw_data` table. Each affected row receives an `anomaly_type` label. The scoring engine must never read this column.

### Injection Results

**180,000 total rows · 23,523 changed (13.07%) · 156,477 unchanged (86.93%)**

| Anomaly | Rows | % | What Changed |
|---|---:|---:|---|
| `brute_force` | 2,974 | 1.65% | `failed_attempts_before_success` → 8–20, `auth_result → Success` |
| `impossible_travel` | 2,971 | 1.65% | `geo_country` flipped to a different country from prior event |
| `off_hours_access` | 3,000 | 1.67% | `is_off_hours → 1` (standard users only) |
| `privilege_escalation` | 3,000 | 1.67% | `privilege_used → admin`, `dst_host → DC-01` (standard users only) |
| `new_device_login` | 2,972 | 1.65% | `device_id → NEWDEV-<uid>-<eid>` (globally unique) |
| `dormant_reactivation` | 2,988 | 1.66% | `anomaly_type` only *(approximation — no calendar date available)* |
| `data_volume_spike` | 2,972 | 1.65% | `bytes_transferred → 10× user's own average` (~27.9 MB vs ~2.7 MB normal) |
| `rapid_lateral_movement` | 2,646 | 1.47% | `dst_host → SRV-100…119` (many hosts within a session) |
| Normal | 156,477 | 86.93% | — |

**Columns never modified on any row:**
`event_id` · `timestamp` · `user_id` · `user_role` · `src_host` · `src_subnet` · `auth_protocol` · `logon_type` · `client_ip` · `geo_city` · `mfa_used` · `session_id` · `session_duration_sec`

> **Note on `dormant_reactivation`:** `Raw_data` has no calendar date field — `timestamp` covers only a ~1-hour `mm:ss` window. "30+ days of silence" cannot be reliably measured. The artificial `reactivation_gap` proxy was removed from the scoring engine to avoid baseline noise, leaving 8 active telemetry metrics.

> **Note on `rapid_lateral_movement`:** 2,646 rows tagged instead of the 3,000 target — limited by the finite pool of sessions with ≥3 events.

---

## Risk Scoring Pipeline

AnomAlert derives a continuous **Risk Score (0–100)** for each user across **8 normalized behavioral metrics** without ever reading the evaluation-only `anomaly_type` column.

### The 8 Behavioral Metrics

| # | Metric | Derivation | Anomaly Target | Weight |
|---|---|---|---|---:|
| 1 | `failed_login_rate` | $\sum \text{failures} / \text{total events}$ | `brute_force` | 12.5% (1/8) |
| 2 | `distinct_geo_count` | $\text{COUNT(DISTINCT geo\_country)}$ | `impossible_travel` | 12.5% (1/8) |
| 3 | `off_hours_ratio` | $\sum \text{is\_off\_hours} / \text{total events}$ | `off_hours_access` | 12.5% (1/8) |
| 4 | `privilege_mismatch_count` | $\sum (\text{privilege\_used} \neq \text{user\_role})$ | `privilege_escalation` | 12.5% (1/8) |
| 5 | `distinct_device_count` | $\text{COUNT(DISTINCT device\_id)}$ | `new_device_login` | 12.5% (1/8) |
| 6 | `bytes_spike_ratio` | $\max(\text{bytes}) / \text{avg}(\text{bytes})$ | `data_volume_spike` | 12.5% (1/8) |
| 7 | `lateral_movement_rate` | $\text{COUNT(DISTINCT dst\_host)} / \text{COUNT(DISTINCT session\_id)}$ | `rapid_lateral_movement` | 12.5% (1/8) |
| 8 | `mfa_bypass_rate` | $\sum (\text{mfa\_used} = 0) / \text{total events}$ | Credential / MFA posture | 12.5% (1/8) |

Each raw metric is min-max scaled to 0–100 ($s_i$), and the composite score is calculated as:
$$\text{Risk Score} = \sum_{i=1}^{8} \frac{1}{8} \times s_i$$

### Risk Band Classification

Continuous scores are categorized into 4 severity bands:

| Risk Band | Score Range | User Count | % of Users | Status |
|---|---|---:|---:|---|
| **Normal** | 0 – 30 | **483** | 96.99% | Baseline Activity |
| **Suspicious** | 31 – 60 | **12** | 2.41% | Elevated Monitoring |
| **High Risk** | 61 – 80 | **3** | 0.60% | Active Investigation (`U0162`, `U0405`, `U0267`) |
| **Critical** | 81 – 100 | **0** | 0.00% | Immediate Incident Response |
| **Total** | | **498** | **100.0%** | |

---

## Repository Structure

| File / Directory | Description |
|---|---|
| `AnomAlert.sqlite` | Primary SQLite database containing `Raw_data` (180,000 events) and `metrics` (498 user profiles) |
| `RawData.sql` | SQL dump of the raw dataset |
| `inject.sql` | Anomaly injection script (8 patterns, PRD §7.4) |
| `parameter.md` | Detailed column and parameter descriptions |
| `requirements.txt` | Pinned Python dependencies (`streamlit`, `pandas`, `numpy`, `plotly`) |
| `app.py` | Main Streamlit security monitoring dashboard |
| `database/db.py` | Data access layer for loading metrics and events |
| `components/` | Streamlit modular UI components (`kpi_cards`, `risk_distribution`, `top_users`, `user_details`) |
| `scripts/build_metrics.py` | Computes the 8 per-user behavioral metrics and min-max normalized scores |
| `scripts/compute_risk_scores.py` | Computes composite risk scores (1/8 equal weights) and assigns risk bands |
| `scripts/evaluate_detection.py` | Evaluates detection recall against ground-truth injected labels |

