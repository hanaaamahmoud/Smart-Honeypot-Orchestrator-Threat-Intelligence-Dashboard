# Unified Multi-Honeypot Security Log Dataset

## 1. Overview

| Item | Details |
|---|---|
| Combined Protocols | SSH, HTTP, FTP |
| Source Files | `cowrie_ssh_preprocessed.csv`, `tanner_http_labeled.csv`, `dionaea_ftp_clean.csv`, `ftp_clean_final.csv` |
| Output File | `unified_security_events_clean_v1.csv` |
| Total Schema Columns | 24 Standardized Fields |

## 2. Schema Alignment

All source datasets were normalized into a single 24-column baseline:
`timestamp`, `honeypot`, `protocol`, `source_ip`, `source_port`, `destination_ip`, `destination_port`, `session_id`, `username`, `password`, `user_attempt`, `pass_attempt`, `auth_attempt`, `anonymous`, `command_count`, `country`, `country_code`, `asn`, `ip_reputation`, `attack_type`, `mitre_technique`, `attack_stage`, `severity`, `source_dataset`.

## 3. Merging & Final Processing

1. Schema force-alignment across all datasets.
2. Concatenation into a unified pandas dataframe.
3. Cross-dataset deduplication.
4. Comprehensive missing value and date-range validation.
