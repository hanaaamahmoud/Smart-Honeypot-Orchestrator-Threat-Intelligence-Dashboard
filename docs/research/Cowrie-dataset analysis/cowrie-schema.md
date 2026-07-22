# Cowrie Dataset Schema

## Dataset Information

| Item | Value |
|------|-------|
| Honeypot | Cowrie |
| Protocol | SSH |
| Dataset | cowrie_ssh_preprocessed.csv |
| Total Columns | 73 |
| Log Format | CSV (preprocessed from NDJSON) |

---

# Purpose

This document describes the schema of the preprocessed Cowrie dataset used in the Smart Honeypot Orchestrator project.

For each field, the following information is documented:

- Data Type
- Description
- Project Usage
- Keep / Remove Decision

---

# Schema

| Column | Data Type | Description | Project Usage | Status |
|---------|-----------|-------------|---------------|--------|
| t-pot_hostname | Object | T-Pot host name | Environment metadata | Keep |
| t-pot_ip_ext | Object | External IP of the honeypot | Infrastructure information | Keep |
| t-pot_ip_int | Object | Internal IP of the honeypot | Infrastructure information | Keep |
| timestamp | Datetime | Event timestamp | Event ordering | Keep |
| @timestamp | Datetime | Original log timestamp | Time validation | Keep |
| message | Object | Human-readable event message | Event interpretation | Keep |
| eventid | Object | Event type identifier | Event classification | Keep |
| sensor | Object | Honeypot sensor ID | Sensor identification | Keep |
| host | Object | Host running Cowrie | Environment metadata | Keep |
| duration | Float | Session duration (seconds) | Behavioral analysis | Keep |
| src_ip | Object | Attacker source IP | Threat Intelligence | Keep |
| session | Object | Session identifier | Session reconstruction | Keep |

---

# GeoIP Fields

## External (Honeypot Location)

| Column | Data Type | Description | Status |
|---------|-----------|-------------|--------|
| geoip_ext.ip | Object | Honeypot public IP | Keep |
| geoip_ext.country_name | Object | Honeypot country | Keep |
| geoip_ext.country_code2 | Object | ISO country code | Keep |
| geoip_ext.country_code3 | Object | ISO country code | Keep |
| geoip_ext.city_name | Object | Honeypot city | Keep |
| geoip_ext.region_name | Object | Honeypot region | Keep |
| geoip_ext.region_code | Object | Region code | Keep |
| geoip_ext.continent_code | Object | Continent | Keep |
| geoip_ext.latitude | Float | Latitude | Keep |
| geoip_ext.longitude | Float | Longitude | Keep |
| geoip_ext.location.lat | Float | Latitude | Keep |
| geoip_ext.location.lon | Float | Longitude | Keep |
| geoip_ext.timezone | Object | Timezone | Keep |
| geoip_ext.postal_code | Integer | Postal code | Keep |
| geoip_ext.as_org | Object | ASN organization | Keep |
| geoip_ext.asn | Integer | ASN number | Keep |

---

## Attacker GeoIP

| Column | Data Type | Description | Status |
|---------|-----------|-------------|--------|
| geoip.ip | Object | Attacker IP | Keep |
| geoip.country_name | Object | Country | Keep |
| geoip.country_code2 | Object | ISO country code | Keep |
| geoip.country_code3 | Object | ISO country code | Keep |
| geoip.city_name | Object | City | Keep |
| geoip.region_name | Object | Region | Keep |
| geoip.region_code | Object | Region code | Keep |
| geoip.continent_code | Object | Continent | Keep |
| geoip.latitude | Float | Latitude | Keep |
| geoip.longitude | Float | Longitude | Keep |
| geoip.location.lat | Float | Latitude | Keep |
| geoip.location.lon | Float | Longitude | Keep |
| geoip.timezone | Object | Timezone | Keep |
| geoip.postal_code | Object | Postal code | Keep |
| geoip.as_org | Object | ASN organization | Keep |
| geoip.asn | Float | ASN number | Keep |
| geoip.dma_code | Float | DMA code (legacy) | Keep |

---

# Network Fields

| Column | Data Type | Description | Status |
|---------|-----------|-------------|--------|
| src_port | Float | Source port | Keep |
| dest_ip | Object | Destination IP | Keep |
| dest_port | Float | Destination port | Keep |
| protocol | Object | Network protocol | Keep |
| ip_rep | Object | IP reputation | Keep |

---

# Authentication Fields

| Column | Data Type | Description | Status |
|---------|-----------|-------------|--------|
| username | Object | Attempted username | Keep |
| password | Object | Attempted password | Keep |

---

# SSH Fingerprinting

| Column | Data Type | Description | Status |
|---------|-----------|-------------|--------|
| version | Object | SSH client version | Keep |
| hassh | Object | HASSH fingerprint | Keep |
| hasshAlgorithms | Object | HASSH algorithm string | Keep |
| kexAlgs | Object | Key exchange algorithms | Keep |
| keyAlgs | Object | Host key algorithms | Keep |
| macCS | Object | MAC algorithms | Keep |
| encCS | Object | Encryption algorithms | Keep |
| compCS | Object | Compression algorithms | Keep |
| langCS | Object | Language algorithms | Keep |

---

# Command Execution

| Column | Data Type | Description | Status |
|---------|-----------|-------------|--------|
| input | Object | Executed attacker command | Keep |

---

# File Transfer

| Column | Data Type | Description | Status |
|---------|-----------|-------------|--------|
| filename | Object | Uploaded/downloaded filename | Keep |
| outfile | Object | Output file | Keep |
| destfile | Object | Destination file | Keep |
| shasum | Object | File SHA hash | Keep |
| size | Float | File size | Keep |

---

# Additional Fields

| Column | Data Type | Description | Status |
|---------|-----------|-------------|--------|
| ttylog | Object | TTY session log | Keep |
| duplicate | Object | Duplicate indicator | Keep |
| arch | Object | File architecture | Keep |
| url | Object | Download URL | Keep |
| data | Object | Raw payload data | Keep |
| headers.content_length | Integer | Original log content length | Keep |

---

# Notes

- All retained fields correspond to valid Cowrie event types.
- Many fields contain NULL values because they are event-specific, not because of missing data.
- Sparse fields such as `filename`, `input`, `shasum`, and `url` were intentionally retained since they represent valuable attacker behavior.
- No behavioral fields were removed during preprocessing.
- This schema serves as the reference for the Feature Engineering stage.

---

# Schema Summary

| Category | Count |
|----------|------:|
| Infrastructure Fields | 3 |
| Timestamp Fields | 2 |
| Session & Event Fields | 6 |
| External GeoIP Fields | 15 |
| Attacker GeoIP Fields | 16 |
| Network Fields | 5 |
| Authentication Fields | 2 |
| SSH Fingerprinting Fields | 9 |
| Command Fields | 1 |
| File Transfer Fields | 5 |
| Additional Fields | 6 |

**Total Columns:** 73
