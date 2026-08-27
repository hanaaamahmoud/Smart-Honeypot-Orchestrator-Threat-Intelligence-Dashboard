# FTP Datasets — Dionaea & T-Pot

## 1. Dataset Overview

| Item | Details |
|---|---|
| Honeypots | Dionaea & T-Pot FTP |
| Protocol | FTP (Port 21) |
| Environments | Dionaea SQLite & Raw JSON Events |
| Final Format | CSV |
| Datasets Produced | `ftp_clean_final.csv` & `dionaea_ftp_clean.csv` |
| Role | Primary FTP Command & Authentication Datasets |

## 2. Source Datasets

The FTP data pipeline ingests from two distinct honeypot logging mechanisms:
1. **Raw JSON Honeynet Events (`RawHoneynetEventsBatch-*.json`):** Captures high-level event sequences, FTP command execution details (`USER`, `PASS`, `AUTH`, `EPSV`, `QUIT`), and GeoIP enrichment.
2. **Dionaea SQLite Databases (`dionaea.sqlite.*`):** Captures relational login attempts, connecting attack IP addresses, and exact byte-encoded credential pairs.

## 3. Processing Performed

### Pipeline A: Dionaea JSON Event Extraction (`ftp_clean_final.csv`)
1. Decompressed raw JSON events and filtered for `ftpd` protocol logs.
2. Dropped constant, non-informative headers and reduced dataset dimensionality.
3. Rationalized and standardized GeoIP information and country codes.
4. Extracted command frequencies and created binary indicators (`has_USER`, `has_PASS`, `is_anonymous`).

### Pipeline B: Dionaea SQLite Credential Extraction (`dionaea_ftp_clean.csv`)
1. Connected to SQLite tables and merged `connections` with `logins` using connection IDs.
2. Resolved byte-encoding issues (`decode_bytes`) in raw usernames and passwords.
3. Extracted attack timestamps into granular time features (`hour`, `weekday`).
4. Sanitized missing values and dropped fully empty columns.

## 4. Important Information Retained

- Connection and session identifiers
- Remote attacker IP addresses and local destination ports
- Raw username and password combinations
- FTP command execution frequencies and flags
- Temporal attack attributes (timestamps, hour, weekday)
- GeoIP metadata and threat indicators

## 5. Validation

Both FTP pipelines were verified for:
- Correct relational joining across SQLite tables
- UTF-8 string decoding of binary credentials
- Duplicate record removal
- Standardized datetime conversion to UTC
- Accurate frequency counting of executed commands

## 6. Output Files

- `ftp_clean_final.csv`: Structured command sequence dataset.
- `dionaea_ftp_clean.csv`: Cleaned authentication & brute-force record dataset.

## 7. Machine Learning Readiness

Suitable for analyzing brute-force attempt frequencies, password spray patterns, and FTP command-based anomaly detection.
