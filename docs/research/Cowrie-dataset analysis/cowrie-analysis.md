# Cowrie Dataset Analysis

## Dataset Information

| Item | Value |
|------|-------|
| Honeypot | Cowrie |
| Protocol | SSH |
| Dataset Type | Real Honeypot Logs |
| Log Format | NDJSON (JSON Lines) |
| Source | Cowrie Logs collected from T-Pot |
| Project Role | Primary SSH Dataset |

---

# Dataset Overview

Cowrie is an open-source medium-interaction SSH/Telnet honeypot that captures real attacker interactions.

The dataset records complete attacker sessions including:

- SSH connections
- Authentication attempts
- SSH fingerprints (HASSH)
- Executed commands
- Session metadata
- File uploads/downloads
- Session duration
- Source IP addresses

---

# Data Cleaning Workflow

The following preprocessing pipeline was applied before analysis.

| Step | Status |
|------|--------|
| Load & Merge JSON Files | Completed |
| JSON Parsing | Completed |
| Flatten Nested JSON | Completed |
| Extract Cowrie Events | Completed |
| Filter SSH Events Only | Completed |
| Remove Telnet Events | Completed |
| Remove Empty Columns | Completed |
| Remove Constant Columns | Completed |
| Timestamp Conversion | Completed |
| Missing Values Review | Completed |
| Duplicate Review | Completed |
| Session Validation | Completed |
| Event Sequence Validation | Completed |
| Data Type Validation | Completed |
| Export Clean Dataset | Completed |

---

# Cleaning Decisions

The following preprocessing decisions were intentionally applied:

- Only SSH events were retained.
- Telnet events were removed because they are outside the project scope.
- Empty columns (100% NULL) were removed.
- Constant columns with no analytical value were removed.
- Missing values were preserved when they were event-specific.
- Rare event-specific features were retained.
- Timestamp fields were converted into datetime format.
- Session integrity was verified.
- Duplicate records were reviewed before removal.
- Protocol values were propagated within each SSH session when required.

---

# Dataset Validation

| Validation | Result |
|------------|--------|
| JSON Parsing | Verified |
| Flattening | Verified |
| SSH Filtering | Verified |
| Missing Values Reviewed | Verified |
| Empty Columns Removed | Verified |
| Constant Columns Removed | Verified |
| Data Types Checked | Verified |
| Session Integrity Verified | Verified |
| Timestamp Ordering Verified | Verified |
| Event Sequence Verified | Verified |
| Duplicate Review | Verified |
| SSH Workflow Verified | Verified |

The dataset is considered clean and ready for feature engineering.

---

# Dataset Statistics

| Metric | Value |
|--------|-------|
| SSH Sessions | 11,663 |
| SSH Events | 55,434 |
| Sessions without Connect Event | 0 |
| Sessions without Closed Event | 0 |

---

# Dataset Profiling

The dataset profiling includes:

- Number of Records
- Number of Features
- Schema
- Data Types
- Missing Values
- Event Distribution
- Session Statistics
- Label Availability
- Log Format
- Dataset Use Case

The complete dataset schema is documented separately in:

- cowrie-schema.md

---

# Missing Values Analysis

Missing values were manually reviewed.

They correspond to event-specific fields rather than data quality problems.

No behavioral information was lost.

---

# Duplicate Analysis

Result:

- No fully duplicated records were found.

---

# Session Validation

Validation confirmed:

- Every session contains one Connect event.
- Every session contains one Closed event.
- Timestamp ordering is correct.
- Only SSH sessions remain after filtering.

---

# Event Types

The dataset contains seven primary SSH event types.

Detailed documentation is available in:

- cowrie-event-reference.md

---

# Behavioral Information

The dataset captures:

- Authentication attempts
- Successful logins
- Failed logins
- SSH fingerprints
- Executed commands
- Session duration
- Command sequences
- Username diversity
- Password diversity

These behaviors provide a strong foundation for attacker profiling.

---

# Suitability for Machine Learning

The dataset contains sufficient behavioral information for:

- Behavioral Clustering
- Attacker Profiling
- Session Analysis
- Threat Intelligence
- Anomaly Detection

Suitable for Behavioral Clustering:

YES

---

# Project Objectives Coverage

| Objective | Status |
|-----------|--------|
| SSH Honeypot | Covered |
| GeoIP Enrichment | Covered |
| Dashboard | Covered |
| Behavior Analysis | Covered |
| Attack Timeline | Covered |
| Top Countries | Covered |
| Top IPs | Covered |
| Top Commands | Covered |
| Threat Intelligence | Covered |
| Machine Learning | Covered |

---

# Strengths

- Real attacker interactions
- Complete SSH sessions
- Rich behavioral information
- SSH fingerprints (HASSH)
- Authentication events
- Command history
- GeoIP compatible
- Suitable for behavioral clustering

---

# Limitations

- SSH protocol only
- No HTTP attacks
- No FTP attacks
- No SMTP attacks
- Requires feature engineering before Machine Learning

---

# Feature Engineering

Behavioral features will be extracted in a separate stage.

The complete extraction plan is documented in:

- feature-engineering-plan.md

---

# Final Assessment

The Cowrie dataset satisfies all SSH-related requirements of the Smart Honeypot Orchestrator project.

It provides complete attacker sessions, authentication events, command execution logs, SSH fingerprints, and session metadata, making it an excellent foundation for attacker behavior analysis, threat intelligence, and unsupervised machine learning.
