# Data Preprocessing & Integration Documentation

This folder documents the initial extraction, cleaning, schema standardization, and merging procedures performed on the raw honeypot security logs before downstream analysis.

## Pipeline Overview

| Document | Source Honeypots | Protocol | Key Actions | Primary Output File |
|---|---|---|---|---|
| [`ssh-dataset.md`](./ssh-dataset.md) | Cowrie | SSH | Event extraction, JSON flattening, session validation | `cowrie_ssh_clean_final.csv` |
| [`ftp-dataset.md`](./ftp-dataset.md) | Dionaea & T-Pot | FTP | SQLite decoding, command frequency extraction, GeoIP mapping | `ftp_clean_final.csv`, `dionaea_ftp_clean.csv` |
| [`http-dataset.md`](./http-dataset.md) | Tanner | HTTP | JSON parsing, payload extraction, MITRE ATT&CK mapping | `tanner_http_labeled.csv` |
| [`unified-dataset.md`](./unified-dataset.md) | All Honeypots | Multi-Protocol | Schema alignment (24 columns), dataset concatenation, deduplication | `unified_security_events_clean_v1.csv` |

## Data Flow Diagram

```text
[ Raw Cowrie SSH ] ------> ssh-dataset.md ------\
[ Raw Dionaea FTP ] -----\                      |
                          +--> ftp-dataset.md --+--> unified-dataset.md --> unified_security_events_clean_v1.csv
[ Raw T-Pot FTP ] -------/                      |
[ Raw Tanner HTTP ] -----> http-dataset.md -----/
