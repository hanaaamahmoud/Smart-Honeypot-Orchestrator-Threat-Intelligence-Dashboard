# HTTP Dataset — Tanner

## 1. Dataset Overview

| Item | Details |
|---|---|
| Honeypot | Tanner |
| Protocol | HTTP |
| Original Format | JSON.gz |
| Final Format | CSV |
| Dataset Produced | `tanner_http_labeled.csv` |
| Role | Labeled HTTP Threat & Attack Classifier Dataset |

## 2. Source Dataset

Extracted from raw compressed Tanner honeypot events (`JSON.gz`). Tanner acts as an emulation service that evaluates incoming HTTP requests and responses, assessing payload intent and maliciousness.
https://github.com/0xsha/sweetie-data/tree/master/tanner/log

## 3. Processing Performed

1. Decompressed raw `JSON.gz` logs and extracted nested request payloads.
2. Parsed HTTP peer IP addresses, ports, headers, and request session UUIDs.
3. Standardized timestamps to UTC ISO formats.
4. Mapped threat payloads to attack categories (e.g., LFI, SQLi, XSS, Cmd Injection).
5. Enriched logs with MITRE ATT&CK techniques, Cyber Kill Chain stages, and severity scores.
6. Handled missing request fields and removed exact duplicate logs.

## 4. Important Information Retained

- Attacker IP address and session UUID
- Full request paths, HTTP methods, and user agents
- Attack classification types (`attack_type`)
- Enriched threat intelligence (MITRE Technique, Kill Chain Stage, Severity)
- Request execution timestamps

## 5. Validation

- Payload extraction integrity check
- Consistency validation across MITRE ATT&CK labels
- Timestamp ordering and format conversion
- Null and duplicate record filtering

## 6. Output File

- `tanner_http_labeled.csv`: Fully labeled HTTP attack dataset with MITRE ATT&CK mappings.

## 7. Machine Learning Readiness

Ideal for multi-class payload classification, threat severity estimation, and automated web attack pattern profiling.
