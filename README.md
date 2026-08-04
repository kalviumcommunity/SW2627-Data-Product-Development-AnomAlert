# SW2627-Data-Product-Development-AnomAlert

## Overview

AnomAlert is a cybersecurity analytics system that detects suspicious user authentication behavior by analyzing login attempts, failed authentication patterns, and device access history. It helps security teams identify behavioral anomalies that may indicate an account is at risk of compromise.

## Problem Statement

Traditional security reports provide authentication logs and login statistics but fail to detect unusual user behavior that often precedes account compromise. AnomAlert addresses this gap by identifying anomalies and generating actionable security alerts.

## Dataset 

To improve the quality and scope of our analysis, we explored multiple cybersecurity datasets available on Kaggle and selected a more comprehensive authentication dataset. This dataset has been added to the repository and will serve as the primary dataset for further development and experimentation.

[Access the dataset](https://www.kaggle.com/datasets/danielpeng1995/synthetic-enterprise-auth-logs)

### About the Dataset

The dataset contains **180,000 synthetic enterprise authentication events** created for cybersecurity research, particularly for **lateral movement detection**.

It includes a wide variety of authentication scenarios, such as:

- Normal user authentication activity
- Benign first-time host connections
- Suspicious host transitions
- Access attempts to sensitive systems
- Labeled malicious authentication events

The dataset provides a realistic environment for evaluating different anomaly detection techniques and security analytics models.

### Dataset Refinement

The original dataset included `is_domain_controller_target` and `is_malicious` columns. We removed both, since they don't directly support the analysis we're building and `is_malicious` in particular acts as a ground-truth label we don't want the detection logic to depend on.

With those columns gone, the dataset now only reflects normal authentication activity — there's no signal in it that represents anomalous behavior. To address this, we plan to generate synthetic anomalous activity and add it into the same dataset, so it contains both normal and anomalous behavior to analyze.

### Planned Metric: Risk Score

Once the dataset includes anomalous activity, the next step is to engineer a **Risk Score** metric from the available authentication fields (login patterns, failed attempts, device/host access, etc.). This metric will let us quantify how anomalous a user's behavior is and flag accounts that show signs of compromise, without relying on a pre-labeled "malicious" flag.

