# Backend Handoff — ML Analytics

Complete reference for the ML Service analytics handoff to the Backend
and Frontend teams.

This folder contains:

- Per-analytics JSON schemas for validation
- Per-analytics data files (gitignored — regenerated on each run)
- Packaged data files ready for serving (`ml_analytics_files/`)

This README is the single reference for integration. It covers all
seven analytics layers, the folder structure, the data contract, and
the frontend integration summary.

---

## Table of Contents

1. Folder Structure
2. Analytics Layers Overview
3. Data Contract (Common Structure)
4. Per-Layer Reference
5. Frontend Integration Summary
6. Global Rules for Backend
7. Refresh Workflow

---

## 1. Folder Structure

    backend_handoff/
    |
    |-- README.md                     This file
    |
    |-- 01_cluster_analytics/
    |   |-- schema.json               JSON schema for validation
    |   `-- cluster_analytics.json    Data (gitignored)
    |
    |-- 02_temporal_analytics/
    |   |-- schema.json
    |   `-- temporal_analytics.json
    |
    |-- 03_session_analytics/
    |   |-- schema.json
    |   `-- session_analytics.json
    |
    |-- 04_mitre_analytics/
    |   |-- schema.json
    |   |-- mitre_analytics.json
    |   |-- mitre_analytics_full.json
    |   `-- mitre_analytics_sessions.json
    |
    |-- 05_mitre_statistics/
    |   |-- schema.json
    |   `-- mitre_statistics.json
    |
    |-- 06_mitre_trends/
    |   |-- schema.json
    |   `-- mitre_trends.json
    |
    |-- 07_session_replay/
    |   |-- schema_list.json
    |   |-- schema_detail.json
    |   |-- session_replay_list.json
    |   `-- session_replay_details/   Individual session files
    |
    `-- ml_analytics_files/           Packaged data for Backend serving
        |-- README.md                 Data usage guide
        |-- cluster_analytics.json
        |-- temporal_analytics.json
        |-- session_analytics.json
        |-- mitre_analytics.json
        |-- mitre_statistics.json
        |-- mitre_trends.json
        |-- session_replay_list.json
        `-- session_replay_details/

Each analytics folder contains:

- schema.json — JSON schema for validation
- <name>.json — the actual data (gitignored — regenerated on each run)

The `ml_analytics_files/` folder is the packaged data folder.
Extract it from the delivered ZIP into your backend data directory.

---

## 2. Analytics Layers Overview

| # | Layer | Folder | Data File | Endpoint |
|---|---|---|---|---|
| 1 | Cluster Analytics | 01_cluster_analytics | cluster_analytics.json | /api/ml/clusters |
| 2 | Temporal Analytics | 02_temporal_analytics | temporal_analytics.json | /api/ml/temporal |
| 3 | Session Analytics | 03_session_analytics | session_analytics.json | /api/ml/sessions/summary |
| 4 | MITRE Analytics | 04_mitre_analytics | mitre_analytics.json | /api/ml/mitre |
| 5 | MITRE Statistics | 05_mitre_statistics | mitre_statistics.json | /api/ml/mitre/statistics |
| 6 | MITRE Trends | 06_mitre_trends | mitre_trends.json | /api/ml/mitre/trends |
| 7 | Session Replay | 07_session_replay | session_replay_list.json | /api/ml/session-replay |

Each layer is independent and consumes the ML output directly.

---

## 3. Data Contract (Common Structure)

Every analytics JSON file follows the same top-level structure:

    {
      "contract_name": "LAYER_NAME_HANDOFF",
      "contract_version": "x.y.z",
      "generated_at": "ISO-8601 timestamp",
      "source": "ML_SERVICE_FROZEN_PRODUCTION",
      "analytics_layer": "LAYER_NAME",
      "summary": { ... },
      "<data_key>": [ ... ]
    }

Required fields:
- contract_name — stable identifier for the layer
- contract_version — semantic version
- generated_at — ISO-8601 UTC timestamp
- source — always "ML_SERVICE_FROZEN_PRODUCTION"
- analytics_layer — layer identifier
- summary — layer-specific summary object

Layer-specific data keys are documented below.

---

## 4. Per-Layer Reference

### 4.1 Cluster Analytics

Data key: clusters[]

Each cluster object:

| Field | Type | Description |
|---|---|---|
| cluster_id | int | Production cluster ID |
| session_count | int | Sessions in this cluster |
| percentage | float | Share of total sessions |
| cluster_type | string | Behavioral type |
| activity_profile | string | Activity description |
| attacker_behavior | string | Attacker intent |
| confidence | enum | HIGH / MEDIUM / LOW |
| possible_attack_name | string | Optional, only when evidence supports |
| evidence_features | string[] | Defining features |
| top_honeypots | TopItem[] | Top honeypots |
| top_countries | TopItem[] | Top countries |
| top_protocols | TopItem[] | Top protocols |
| top_attack_types | TopItem[] | Top attack types |
| top_mitre_techniques | TopItem[] | Top MITRE techniques |
| top_attack_stages | TopItem[] | Top MITRE stages |
| top_severities | TopItem[] | Top severities |
| avg_event_count | float or null | Average events per session |
| avg_distance | float or null | Average distance to centroid |
| avg_session_duration | float or null | Average duration (seconds) |

TopItem shape:

    {"value": "...", "count": N, "percentage": F}

Notes:
- Clusters are sorted by session_count descending.
- Only clusters that received sessions are present.
- Missing clusters simply received no sessions in this run.

---

### 4.2 Temporal Analytics

Data keys: trends[], periods[], highlights, summary

Trend row:

| Field | Type | Description |
|---|---|---|
| trend_date | string | YYYY-MM-DD |
| session_count | int | Sessions on this day |
| total_events | int | Events on this day |
| event_count | int | Same as total_events |
| avg_session_duration_seconds | float | Average duration |
| unique_sessions | int | Distinct session count |
| trend_type | string | Always "DAILY" |

Period object:

| Field | Type | Description |
|---|---|---|
| period_id | int | 1-based period index |
| from | string | Start date |
| to | string | End date |
| days | int | Number of active days |
| sessions | int | Sessions in this period |
| sessions_pct | float | Share of total sessions |
| events | int | Events in this period |
| events_pct | float | Share of total events |
| peak_day | object | Peak session day within the period |
| daily_trends | array | Daily rows for this period only |

Notes:
- Rows are sorted ascending by trend_date.
- Date gaps between periods are meaningful — do not interpolate.
- Use periods[] for charting — one chart per period.
- trend_type is always "DAILY".

---

### 4.3 Session Analytics

Data keys: summary, distributions, critical_alerts, top_source_ips

Summary fields:

| Field | Type | Description |
|---|---|---|
| total_sessions | int | Total sessions |
| total_events | int | Total events |
| total_clusters_used | int | Distinct clusters |
| assigned_sessions | int | Sessions with a cluster |
| noise_sessions | int | Noise sessions |
| avg_events_per_session | float | Mean events |
| avg_session_duration_seconds | float | Mean duration |
| median_session_duration_seconds | float | Median duration |
| min_session_duration_seconds | float | Minimum duration |
| max_session_duration_seconds | float | Maximum duration |
| unique_source_ips | int | Distinct IPs |
| unique_countries | int | Distinct countries |
| percentiles | object | p50, p90, p95, p99 duration |

Distribution shape:

    "by_honeypot": [{"value": "...", "count": N, "percentage": F}]

Available distributions:
- by_honeypot, by_protocol, by_country
- by_attack_type, by_mitre_technique, by_attack_stage
- by_severity, by_cluster
- by_event_count_bucket, by_duration_bucket

Critical alert shape:

    {
      "session_id": "...",
      "severity": "Critical",
      "source_ip": "...",
      "country": "...",
      "attack_type": "...",
      "mitre_technique": "...",
      "attack_stage": "...",
      "honeypot": "...",
      "event_count": N,
      "cluster_id": N
    }

Top source IP shape:

    {"ip": "...", "session_count": N, "event_count": N}

Notes:
- critical_alerts is capped at 10; use critical_alerts_count for total.
- Empty arrays mean "no data", never null.
- Do not recompute values — serve as-is.

---

### 4.4 MITRE Analytics

Data keys: mitre_technique_distribution, mitre_tactics_distribution,
attack_type_distribution, attack_stage_distribution,
session_mitre_relationships, mitre_activity_over_time, summary

Technique item:

    {
      "value": "T1595",
      "count": N,
      "percentage": F,
      "tactic": "Reconnaissance",
      "top_source_ips": [{"ip": "...", "session_count": N}]
    }

Tactic item:

    {"value": "Reconnaissance", "count": N, "percentage": F}

Relationship item:

    {
      "session_id": "...",
      "mitre_techniques": ["T1595"],
      "attack_types": ["..."],
      "attack_stages": ["..."]
    }

Activity item:

    {"date": "YYYY-MM-DD", "count": N}

Notes:
- Techniques sorted by count descending.
- top_source_ips capped at 5 per technique.
- Tactic derived from official MITRE ATT&CK mapping.
- Empty MITRE values are not fabricated.

---

### 4.5 MITRE Statistics

Data key: statistics[]

Statistic record:

| Field | Type | Description |
|---|---|---|
| statistic_type | string | OVERALL, CLUSTER, MITRE_TECHNIQUE, ATTACK_TYPE, ATTACK_STAGE |
| statistic_key | string | Identifier within the type |
| rank | int | 1-based rank within the type |
| label | string | Display-ready string |
| tactic | string | Populated only for MITRE_TECHNIQUE |
| session_count | int | Sessions |
| event_count | int | Events |
| session_share_pct | float | Share of total sessions |
| mapped_mitre_sessions | int | Mapped count (OVERALL, CLUSTER) |
| unmapped_mitre_sessions | int | Unmapped count (OVERALL, CLUSTER) |
| mitre_technique | string | Empty unless applicable |
| mitre_attack_name | string | Empty unless applicable |
| attack_type | string | Empty unless applicable |
| attack_stage | string | Empty unless applicable |

Notes:
- Rows ordered within each statistic_type by rank.
- Non-applicable dimension fields are empty strings, not null.
- mapped + unmapped = session_count for OVERALL and CLUSTER.

---

### 4.6 MITRE Trends

Data keys: trends[], series, top_values, summary

Trend row:

    {
      "trend_date": "YYYY-MM-DD",
      "trend_dimension": "MITRE_TECHNIQUE",
      "trend_value": "T1595",
      "session_count": N,
      "event_count": N
    }

Series shape:

    "series": {
      "MITRE_TECHNIQUE": {
        "T1595": [
          {"date": "YYYY-MM-DD", "session_count": N, "event_count": N}
        ]
      }
    }

Top values shape:

    "top_values": {
      "MITRE_TECHNIQUE": [
        {"value": "T1595", "total_sessions": N}
      ]
    }

Trend dimensions:
- MITRE_TECHNIQUE
- ATTACK_TYPE
- ATTACK_STAGE

Notes:
- series[dimension][value] always sorted by date ascending.
- top_values[dimension] capped at 10 values.
- Empty dimension values are excluded.

---

### 4.7 Session Replay

Two files:

- session_replay_list.json — lightweight sessions list for the table
- session_replay_details/<session_id>.json — full replay for one session

List item:

    {
      "id": "...",
      "events": N,
      "duration": F,
      "honeypot": "...",
      "protocol": "...",
      "country": "...",
      "attack": "...",
      "mitre": "...",
      "severity": "...",
      "flags": { ... },
      "has_replay": true
    }

Flags:

| Flag | Meaning |
|---|---|
| is_suspicious | Any strong signal |
| is_brute_force_candidate | auth attempts > 3 or usernames > 3 |
| has_commands_executed | command_count > 0 |
| has_attack_classification | has attack_type or mitre_technique |
| is_large_session | events > 50 |
| is_long_running | duration > 3600s |
| is_multi_ip | > 5 source IPs |
| is_high_severity | severity in (High, Critical) |
| is_medium_or_higher_severity | severity in (Medium, High, Critical) |

Detail file:

    {
      "id": "...",
      "summary": { ... },
      "narrative": {
        "steps": [ ... ],
        "phases": [ ... ],
        "total_steps": N
      },
      "events": [ ... ]
    }

Narrative step:

    {
      "index": N,
      "offset_seconds": F,
      "phase": "connection|auth|command|activity|disconnect",
      "step_type": "...",
      "icon": "...",
      "title": "...",
      "details": [{"label": "...", "value": "..."}],
      "timestamp": "..."
    }

Notes:
- Only sessions with has_replay=true have a detail file.
- Load details on demand — never bulk.
- 404 for sessions without a detail file.

---

## 5. Frontend Integration Summary

The dashboard has six sections. Each section reads from the Backend
API only. The Frontend never reads the JSON files directly.

| Section | Backend Endpoint | Purpose |
|---|---|---|
| Overview | /api/ml/sessions/summary | KPI cards + distributions |
| Clusters | /api/ml/clusters | Cluster table + detail modal |
| MITRE | /api/ml/mitre | Techniques + tactics charts |
| Timeline | /api/ml/temporal | Daily timeline per period |
| Sessions | /api/ml/session-replay | Sessions table with filters |
| Session Replay | /api/ml/session-replay/{id} | Replay modal |

### Recommended Layout

- KPI cards row at the top
- Cluster distribution bar chart
- MITRE tactics pie chart
- Timeline line chart (one chart per period)
- Sessions table with [Replay] button
- Replay modal opens on button click

### Display Notes

- Use periods[] for the timeline — do not plot the whole range.
- Show only clusters present in the data.
- Empty arrays mean "no data", never null.
- possible_attack_name is optional per cluster.
- Session replay details load on demand.

---

## 6. Global Rules for Backend

- Do not modify cluster assignments on the Backend side.
- Do not create new clusters.
- Do not reassign sessions between clusters.
- Do not infer or fabricate missing fields.
- Do not treat empty arrays as null.
- Empty arrays mean "no data available".
- Optional fields may be absent (e.g., possible_attack_name).
- Serve values as-is — do not recompute.
- Analytics files are read-only from the Backend's perspective.

---

## 7. Refresh Workflow

When new events arrive in Elasticsearch:

    Step 1 — Run the ML pipeline
        bash scripts/run_ml_pipeline.sh

    Step 2 — Rebuild the handoff ZIP
        bash scripts/package_handoff.sh

    Step 3 — Deliver the new ZIP to the Backend team

    Step 4 — Backend replaces files and reloads

No code changes are needed. File names stay the same.

Full details: ../docs/RUNTIME_GUIDE.md

---

## Related Documentation

- Integration guide:  ../docs/INTEGRATION_GUIDE.md
- Pipeline flow:      ../docs/PIPELINE_FLOW.md
- Architecture:       ../docs/ARCHITECTURE.md
- Data usage guide:   ml_analytics_files/README.md
