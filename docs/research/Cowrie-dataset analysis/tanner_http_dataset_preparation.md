# Tanner HTTP Dataset Preparation

## Dataset Information

| Item | Value |
|------|-------|
| Honeypot | Tanner |
| Protocol | HTTP |
| Dataset Source | Sweetie Data (GitHub) |
| Raw Files | tanner_report.json.1.gz → tanner_report.json.30.gz |
| Total Records | 2,544 |
| Final Columns | 62 |
| Output | tanner_http_labeled.csv |

---

# Objective

The objective of this stage is to transform raw Tanner HTTP honeypot logs into a structured and labeled dataset suitable for Threat Intelligence analysis and Machine Learning.

The processing pipeline follows the same methodology used for the Cowrie SSH dataset to ensure compatibility between multiple honeypots.

---

# Processing Pipeline

```text
Raw Tanner Logs (.json.gz)

        │

        ▼
Download & Merge

        │

        ▼
JSON Parsing

        │

        ▼
Cleaning

        │

        ▼
Exploratory Data Analysis (EDA)

        │

        ▼
Attack Behavior Analysis

        │

        ▼
Attack Labeling

        │

        ▼
MITRE ATT&CK Mapping

        │

        ▼
Severity Assignment

        │

        ▼
Final Labeled Dataset
```

---

# Dataset Loading

The raw dataset consisted of 30 compressed JSON log files.

Each file was:

- Downloaded from GitHub
- Decompressed
- Parsed line-by-line
- Converted into Python dictionaries
- Combined into a single Pandas DataFrame

Final dataset:

- Records: **2,544**
- Columns: **58** (before labeling)

---

# Data Cleaning

The following preprocessing steps were performed:

- Converted timestamps to datetime format.
- Parsed nested JSON fields using `json_normalize`.
- Verified duplicate records.
- Checked missing values.
- Preserved raw HTTP request information.
- Removed encoding issues before exporting.

Results:

- Duplicate rows: **0**
- Unique attacker IPs: **566**
- Unique sessions: **30**

---

# Exploratory Data Analysis

The following analyses were performed:

- HTTP methods distribution
- Request path distribution
- Session statistics
- Attacker IP frequency
- User-Agent analysis
- Detection name distribution
- Temporal activity analysis

Key observations:

- GET requests dominate the dataset.
- Multiple automated scanners repeatedly target vulnerable paths.
- Large bursts of requests originate from the same IPs.
- Most attacks occur within very short time intervals.

---

# Attack Behavior Analysis

Several common web attack patterns were identified, including:

- PHPUnit Remote Code Execution
- ThinkPHP Exploitation
- phpMyAdmin Scanning
- Joomla Enumeration
- SQLite Enumeration
- HNAP Probing
- WebDAV Requests
- Environment File Exposure
- Command Execution Attempts
- Web Shell Access
- Generic Web Reconnaissance

Behavioral analysis was performed using:

- HTTP paths
- Request methods
- POST parameters
- User-Agent strings
- Request frequency

---

# Attack Labeling

A rule-based labeling engine was implemented.

Each request was assigned an attack category.

Final attack types include:

- Web Recon
- PHPUnit RCE
- ThinkPHP RCE
- phpMyAdmin Scan
- SQLite Scan
- Admin Panel Scan
- Configuration Scan
- HNAP Scan
- Solr Scan
- Web Shell
- Command Execution
- Payload Delivery
- File Upload
- WebDAV
- Joomla Scan
- Tomcat Scan
- .env Exposure
- Other

---

# MITRE ATT&CK Mapping

Detected attacks were mapped to MITRE ATT&CK techniques where applicable.

Examples:

| Attack Type | MITRE Technique |
|-------------|-----------------|
| PHPUnit RCE | T1190 |
| ThinkPHP RCE | T1190 |
| Web Shell | T1505.003 |
| Command Execution | T1059 |
| .env Exposure | T1552 |
| Web Recon | T1595 |

---

# Attack Stage

Each labeled attack was assigned to a high-level attack stage.

Examples:

- Reconnaissance
- Initial Access
- Persistence
- Execution
- Credential Access
- Unknown

---

# Severity Assignment

Each attack was assigned a severity level.

Levels:

- Low
- Medium
- High
- Critical

Severity is based on the potential impact of the observed behavior rather than HTTP response codes.

---

# Final Dataset

Final output:

```
tanner_http_labeled.csv
```

Dataset shape:

```
Rows    : 2544
Columns : 62
```

Additional enrichment columns:

- attack_type
- mitre_technique
- attack_stage
- severity

---

# Relationship with Cowrie Dataset

The Tanner dataset was intentionally processed using the same workflow as the Cowrie SSH dataset.

This ensures that both datasets share a unified structure before Feature Engineering.

Common stages:

- Cleaning
- Labeling
- MITRE Mapping
- Severity Assignment

This standardization will simplify the future integration of multiple honeypot datasets into a unified Machine Learning pipeline.

---

# Next Phase

The next stage is **Feature Engineering**.

During this phase, raw HTTP logs will be transformed into behavioral features suitable for Machine Learning.

Future enrichment will include:

- GeoIP
- ASN
- Country
- Threat Intelligence enrichment
- Session-level behavioral features

---

# Summary

The Tanner HTTP dataset has been successfully transformed from raw honeypot logs into a structured and labeled dataset.

The resulting dataset is suitable for:

- Threat Intelligence
- Dashboard visualization
- Attack behavior analysis
- Feature Engineering
- Machine Learning
- Cross-honeypot integration with Cowrie
