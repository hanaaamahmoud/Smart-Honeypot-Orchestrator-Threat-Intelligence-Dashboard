# 📦 Session Analytics — Backend Handoff

## 🎯 What is this? (Simple)

Session-level analytics for the Smart Honeypot dashboard.
Answers the question: **"What happened at the session level?"**

Provides:
- KPI cards (summary numbers)
- Distributions (honeypots, countries, attacks, MITRE, etc.)
- Critical alerts (top sessions by severity)
- Top attackers (by session count)

## 📁 Files
03_session_analytics/
├── README.md
├── session_analytics.json
└── schema.json

text

## 📊 Source

- Pipeline: Elasticsearch → ML Service → session analytics
- Input: 11,879 sessions (ML output)
- All values are derived from the frozen production pipeline

## 🔗 Suggested Endpoints
GET /api/ml/analytics/sessions/summary
GET /api/ml/analytics/sessions/distributions
GET /api/ml/analytics/sessions/alerts
GET /api/ml/analytics/sessions/top-attackers

text

## 📐 Top-Level Schema

```json
{
  "contract_name": "SESSION_ANALYTICS_HANDOFF",
  "contract_version": "2.0.0",
  "generated_at": "ISO-8601",
  "source": "ML_SERVICE_FROZEN_PRODUCTION",
  "analytics_layer": "SESSION_ANALYTICS",
  "session_count": 11879,
  "summary": { ... },
  "distributions": { ... },
  "critical_alerts": [ ... ],
  "critical_alerts_count": 8,
  "top_source_ips": [ ... ]
}
📐 Summary Fields (KPI Cards)
Field	Type	Description
total_sessions	int	Total sessions analyzed
total_events	int	Total events across sessions
total_clusters_used	int	Distinct clusters in use
assigned_sessions	int	Sessions assigned to a cluster
noise_sessions	int	Sessions classified as noise
avg_events_per_session	float	Mean events per session
avg_session_duration_seconds	float	Mean session duration
median_session_duration_seconds	float	Median session duration
min_session_duration_seconds	float	Minimum session duration
max_session_duration_seconds	float	Maximum session duration
unique_source_ips	int	Distinct attacker IPs
unique_countries	int	Distinct source countries
percentiles	object	p50, p90, p95, p99 duration percentiles
📐 Distributions
All distributions follow the same shape:

json
"by_honeypot": [
  {"value": "cowrie", "count": 11663, "percentage": 98.18},
  ...
]
Available distributions:

by_honeypot (top 10)

by_protocol (top 10)

by_country (top 10)

by_attack_type (top 10)

by_mitre_technique (top 10)

by_attack_stage (top 10)

by_severity (top 10)

by_cluster (top 40)

by_event_count_bucket (fixed buckets: 1, 2-3, 4-5, 6-10, 11-50, 51-100, 100+)

by_duration_bucket (fixed buckets: < 1s, 1-10s, 10s-1m, 1m-1h, 1h-1d, > 1d)

📐 Critical Alerts
Only sessions with severity in (Critical, High) — up to 10 rows.

json
{
  "session_id": "...",
  "severity": "Critical",
  "source_ip": "192.42.116.216",
  "country": "The Netherlands",
  "attack_type": "C2 Activity",
  "mitre_technique": "T1090",
  "attack_stage": "Command and Control",
  "honeypot": "cowrie",
  "event_count": 6,
  "cluster_id": 9
}
Field critical_alerts_count shows the total (may be > 10).

📐 Top Source IPs
Top 10 attacker IPs by session count:

json
{
  "ip": "173.231.185.164",
  "session_count": 1389,
  "event_count": 4155
}
🎨 Dashboard Components
1. KPI Cards Row
text
┌────────────┬────────────┬────────────┬────────────┐
│ 11,879     │ 58,820     │ 4.95       │ 568        │
│ Sessions   │ Events     │ Avg Ev/Ses │ Unique IPs │
├────────────┼────────────┼────────────┼────────────┤
│ 206.65s    │ 2.09s      │ 47         │ 29         │
│ Avg Dur    │ Median Dur │ Countries  │ Clusters   │
└────────────┴────────────┴────────────┴────────────┘
2. 🚨 Critical Alerts Panel
Card list with severity badge + attack + IP + country + MITRE.

3. Distributions (Charts)
Pie: honeypot, protocol, severity

Bar: countries, attack_type, mitre

Histogram: event_count_bucket, duration_bucket

Table: clusters, top attackers

4. Duration Percentiles
Small card: p50 / p90 / p95 / p99

⚠️ Critical Rules
total_events == sum of event_count across sessions

assigned_sessions + noise_sessions == total_sessions

All distributions sorted descending by count

Percentages are rounded to 2 decimals

Empty distributions = [] (never null)

critical_alerts capped at 10 — use critical_alerts_count for total

Do NOT recompute or infer values — serve as-is

🔄 Refresh Cadence
Regenerated on each ML pipeline run

generated_at marks the last run

📞 Contact
ML Service Owner: (fill)

Backend Integration Lead: (fill)
