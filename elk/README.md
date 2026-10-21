# ELK Integration - Smart Honeypot Orchestrator & Threat Intelligence Dashboard

This directory contains the ELK stack configuration used to ingest, normalize, enrich, and visualize honeypot logs for the Smart Honeypot Orchestrator & Threat Intelligence Dashboard project.

---
## Overview

The ELK stack in this project is responsible for:

- Collecting logs from integrated honeypots
- Normalizing heterogeneous log formats into a strict unified 24-field schema
- Enriching public source IPs using GeoIP
- Indexing processed events into Elasticsearch
- Visualizing indexed events in Kibana

---
## Components

### Elasticsearch

Stores processed honeypot events in the `honeypot-events` index.

### Logstash

Reads honeypot logs, transforms them into a unified schema, enriches events, and sends them to Elasticsearch.

### Kibana

Provides visualization and exploration of ingested honeypot events.

---

## Directory Structure

```txt
elk/
├── docker-compose.yml
├── README.md
├── elasticsearch/
│   └── data/
├── logstash/
│   ├── pipeline/
│   │   └── logstash.conf
│   └── data/
└── logs/

## Current Data Sources

At the current stage, the ELK pipeline is configured to ingest logs from the following honeypots:

- Cowrie
- Dionaea
- Tanner

Tanner integration may require additional adjustment depending on deployment mode and log source availability.

---

## Expected Mounted Paths Inside Logstash

### Cowrie

```txt
/mnt/logs/cowrie/cowrie.json

### Dionaea

```txt
/mnt/logs/dionaea/dionaea.json

### Tanner

```txt
/mnt/logs/tanner/tanner.json

## Unified Event Schema

The Logstash pipeline produces a strict 24-field top-level schema for every event:

| # | Field |
|---|-------|
| 1 | timestamp |
| 2 | honeypot |
| 3 | protocol |
| 4 | source_ip |
| 5 | source_port |
| 6 | destination_ip |
| 7 | destination_port |
| 8 | session_id |
| 9 | username |
| 10 | password |
| 11 | user_attempt |
| 12 | pass_attempt |
| 13 | auth_attempt |
| 14 | anonymous |
| 15 | command_count |
| 16 | country |
| 17 | country_code |
| 18 | asn |
| 19 | ip_reputation |
| 20 | attack_type |
| 21 | mitre_technique |
| 22 | attack_stage |
| 23 | severity |
| 24 | source_dataset |

This schema ensures consistency across different honeypot log formats and simplifies downstream consumption by the backend and AI model.

---

## GeoIP Enrichment

For public IP addresses, Logstash attempts to enrich events with:

- `country`
- `country_code`
- `asn`

For private or local IP addresses, the pipeline assigns:

- `ip_reputation` = private
- `country` = Local
- `country_code` = LOCAL

---

## Running the ELK Stack

From the `elk/` directory, run:

```bash
docker compose up -d

To stop the stack:

```bash
docker compose down

## Accessing Services

| Service | URL |
|---------|-----|
| Elasticsearch | http://localhost:9200 |
| Kibana | http://localhost:5601 |

---

## Kibana Usage

1. Open Kibana at `http://localhost:5601`
2. Go to **Stack Management** then **Data Views**
3. Create a new Data View with the pattern `honeypot-events*`
4. Select `timestamp` as the time field
5. Open **Discover** to inspect ingested events

---

## Verifying Data Ingestion

Using curl:

```bash
curl http://localhost:9200/honeypot-events/_count?pretty

Using PowerShell:

```powershell
Invoke-RestMethod "http://localhost:9200/honeypot-events/_count?pretty"

A successful response will show a `count` greater than zero with `successful` shards.

---

## Important Notes

- `elasticsearch/data/` and `logstash/data/` are runtime folders and must not be committed to Git
- Live or real honeypot logs must not be committed unless fully sanitized
- If testing with static files, Logstash may require deleting `sincedb` files to reprocess previously read logs
- GeoIP enrichment applies to public IPs only; private IPs are handled by a dedicated private network detection logic in the pipeline
- The Elasticsearch disk watermark setting may need to be adjusted in low-disk environments using the cluster settings API

---

## Recommended Git Ignore Entries

Add the following to your `.gitignore`:

```gitignore
elk/elasticsearch/data/
elk/logstash/data/
elk/logs/cowrie/
elk/logs/dionaea/
elk/logs/tanner/

---
## Integration Status

### Completed

- Elasticsearch single-node setup with security disabled for local development
- Logstash file input pipeline for Cowrie, Dionaea, and Tanner
- Unified 24-field normalization schema via Ruby filters
- GeoIP enrichment for country and country code using MaxMind GeoLite2
- Private IP detection and fallback labeling
- Kibana service with Data View and Discover support
- Cowrie live log integration
- Dionaea log path preparation

### In Progress or Needs Further Validation

- Full ASN enrichment field validation
- Final Tanner log source identification and integration
- End-to-end live honeypot log streaming validation
- Backend API integration with the `honeypot-events` Elasticsearch index
- AI model input pipeline from Elasticsearch

---

## Purpose in the Project

This ELK stack forms the observability and threat intelligence backbone of the project. It transforms raw honeypot telemetry from multiple sources into a structured, normalized, and enriched event stream. The resulting data stored in Elasticsearch serves as the primary data source for both the backend API and the AI-based threat classification model.