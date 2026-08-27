# SSH Dataset — Cowrie

## Dataset Overview

| Item | Details |
|---|---|
| Honeypot | Cowrie |
| Protocol | SSH |
| Environment | T-Pot |
| Dataset Type | Real Honeypot Logs |
| Original Format | NDJSON / JSON Lines |
| Final Format | CSV / JSON |
| Role | Primary SSH Dataset |



## Source

The dataset originated from raw nested JSON logs collected from
Cowrie SSH honeypots deployed in a T-Pot environment.

The raw logs contained SSH connections, authentication attempts,
SSH fingerprints, executed commands, file activity, session
metadata, source IP addresses, and GeoIP information.


## Processing & Cleaning

The raw logs were processed in the SSH preprocessing notebook.

Main steps:

- Loaded and merged the raw JSON files.
- Parsed and flattened nested JSON structures.
- Extracted Cowrie events.
- Isolated SSH events.
- Removed Telnet and unrelated protocol events.
- Removed completely empty columns.
- Removed constant columns with no analytical value.
- Converted timestamps to datetime.
- Reviewed missing values.
- Reviewed duplicate records.
- Validated sessions and event sequences.
- Validated data types.
- Exported the cleaned dataset.

Event-specific missing values and rare behavioral fields were
preserved when they contained useful information.



## Final Dataset

| Metric | Value |
|---|---:|
| SSH Sessions | 11,663 |
| SSH Events | 55,434 |
| Sessions without Connect Event | 0 |
| Sessions without Closed Event | 0 |
| Duplicate Records | 0 |

The resulting dataset preserves important attacker behavior,
including:

- Authentication attempts
- Usernames and passwords
- Successful and failed logins
- SSH client versions
- HASSH fingerprints
- Executed commands
- File uploads/downloads
- File hashes
- Session duration
- Source IP addresses
- GeoIP information



## Validation

The final dataset was checked for:

- Parsing integrity
- SSH protocol isolation
- Missing values
- Duplicate records
- Data types
- Timestamp ordering
- Session integrity
- Event sequence integrity

Validation confirmed that the retained SSH sessions contain the
expected connection and closure events and that their timestamps
are correctly ordered.



## Output

The cleaned SSH dataset produced by this processing stage is:

`cowrie_ssh_clean_final.csv`

This file represents the **clean SSH source dataset before the
Unified Security Events merge**.



## Purpose

The dataset provides the SSH component of the project and will be
used for:

- Session analysis
- Attacker behavior analysis
- Threat intelligence
- Behavioral feature engineering
- Machine Learning

Further feature engineering and integration are performed after
the individual protocol datasets have been cleaned and validated.

