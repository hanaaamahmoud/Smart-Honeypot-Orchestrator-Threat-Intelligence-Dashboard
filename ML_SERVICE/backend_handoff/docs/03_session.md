# Session Analytics

KPI cards, distributions, and critical alerts at the session level.

| Item | Value |
|---|---|
| Data file | session_analytics.json |
| Schema | 03_session_analytics/schema.json |
| Endpoint | /api/ml/sessions/summary |

## Data Keys

- `summary` — KPI fields
- `distributions` — 10 distribution arrays
- `critical_alerts[]` — up to 10 high/critical sessions
- `top_source_ips[]` — top 10 attackers

## Summary Fields

| Field | Type | Description |
|---|---|---|
| total_sessions | int | Total sessions |
| total_events | int | Total events |
| total_clusters_used | int | Distinct clusters |
| assigned_sessions | int | Sessions with cluster |
| noise_sessions | int | Noise sessions |
| avg_events_per_session | float | Mean events |
| avg_session_duration_seconds | float | Mean duration |
| median_session_duration_seconds | float | Median duration |
| min_session_duration_seconds | float | Min duration |
| max_session_duration_seconds | float | Max duration |
| unique_source_ips | int | Distinct IPs |
| unique_countries | int | Distinct countries |
| percentiles | object | p50, p90, p95, p99 |

## Distribution Shape

`[{"value": "...", "count": N, "percentage": F}]`

## Available Distributions

- by_honeypot, by_protocol, by_country
- by_attack_type, by_mitre_technique, by_attack_stage
- by_severity, by_cluster
- by_event_count_bucket, by_duration_bucket

## Critical Alert

session_id, severity, source_ip, country, attack_type,
mitre_technique, attack_stage, honeypot, event_count, cluster_id

## Top Source IP

`{"ip": "...", "session_count": N, "event_count": N}`

## Notes

- critical_alerts capped at 10; use critical_alerts_count for total.
- Empty arrays mean "no data", never null.
