# 📦 MITRE Analytics — Backend Handoff

## 🎯 What is this? (Simple)

MITRE ATT&CK oriented analytics of the ML session data.

Answers: **"What kinds of attacks are happening, and how dangerous are they?"**

## 📊 The Story

The data shows:

- **97.96%** of sessions are **Reconnaissance** (T1595) — scanning, not real attacks
- **1.50%** are **Credential Access** (T1110) — brute force attempts
- **0.25%** are **Initial Access** (T1190) — exploitation
- **0.22%** are **Discovery** (T1046) — network scanning
- **0.04%** are **Defense Evasion** (T1078) — compromised accounts
- **0.03%** are **Command and Control** (T1090) — active C2 channels 🚨

## 🔗 Suggested Endpoints
GET /api/ml/analytics/mitre
GET /api/ml/analytics/mitre/techniques
GET /api/ml/analytics/mitre/tactics
GET /api/ml/analytics/mitre/activity

text

## 📐 Top-Level Schema

```json
{
  "contract_name": "MITRE_ANALYTICS_HANDOFF",
  "contract_version": "2.0.0",
  "generated_at": "ISO-8601",
  "source": "ML_SERVICE_FROZEN_PRODUCTION",
  "analytics_layer": "MITRE_ANALYTICS",
  "mitre_technique_distribution": [...],
  "mitre_tactics_distribution": [...],
  "attack_type_distribution": [...],
  "attack_stage_distribution": [...],
  "session_mitre_relationships": [...],
  "mitre_activity_over_time": [...],
  "summary": {...}
}
📐 Main Sections
1. mitre_technique_distribution
json
{
  "value": "T1595",
  "count": 11637,
  "percentage": 97.96,
  "tactic": "Reconnaissance",
  "top_source_ips": [
    {"ip": "173.231.185.164", "session_count": 1389}
  ]
}
2. mitre_tactics_distribution
json
{
  "value": "Reconnaissance",
  "count": 11637,
  "percentage": 97.96
}
3. attack_type_distribution
json
{
  "value": "SSH Connection Probe",
  "count": 11629,
  "percentage": 97.9
}
4. attack_stage_distribution
json
{
  "value": "Reconnaissance",
  "count": 11637,
  "percentage": 97.96
}
5. session_mitre_relationships
json
{
  "session_id": "...",
  "mitre_techniques": ["T1595"],
  "attack_types": ["SSH Connection Probe"],
  "attack_stages": ["Reconnaissance"]
}
6. mitre_activity_over_time
json
{"date": "2025-06-10", "count": 6812}
7. summary
json
{
  "total_records": 11879,
  "records_with_mitre": 11879,
  "unique_techniques": 6,
  "unique_tactics": 6,
  "unique_attack_types": 7,
  "unique_attack_stages": 6
}
🎨 Dashboard Components
KPI Cards
text
┌─────────────────┬─────────────────┬─────────────────┐
│ 6               │ 6               │ 7               │
│ Techniques      │ Tactics         │ Attack Types    │
├─────────────────┼─────────────────┼─────────────────┤
│ 11,879          │ 100%            │ 8               │
│ Sessions        │ MITRE Coverage  │ Critical Alerts │
└─────────────────┴─────────────────┴─────────────────┘
Techniques Table
Technique	Tactic	Sessions	%	Top IP
T1595	Reconnaissance	11,637	97.96%	173.231.185.164
T1110	Credential Access	178	1.50%	51.15.151.235
T1190	Initial Access	30	0.25%	49.37.130.19
T1046	Discovery	26	0.22%	64.62.156.112
T1078	Defense Evasion	5	0.04%	142.44.212.226
T1090	Command & Control	3	0.03%	192.42.116.216
Tactics Bar Chart
Show the tactics distribution — clear dominance of Reconnaissance.

Activity Chart
Daily line chart. Note the same 2020/2025 gap as temporal — use active_periods from temporal_analytics for display.

⚠️ Critical Rules
Techniques sorted descending by count

top_source_ips capped at 5 per technique

Tactic derived from official MITRE ATT&CK mapping

Empty MITRE values are NOT fabricated

session_mitre_relationships only contains sessions with valid MITRE

Serve values as-is — do not recompute

🔄 Refresh Cadence
Regenerated on each ML pipeline run

generated_at marks the last run

📞 Contact
ML Service Owner: (fill)

Backend Integration Lead: (fill)


## Files in this folder

| File | Size | Purpose |
|---|---|---|
| mitre_analytics.json | Small (~15 KB) | USE THIS for the Dashboard |
| mitre_analytics_sessions.json | Large (~2.6 MB) | Full session-level relationships |
| mitre_analytics_full.json | Large (~2.6 MB) | Everything combined |
| schema.json | Tiny | JSON schema |

## Which file should the Frontend use?

For the Dashboard UI: mitre_analytics.json (small)

It contains:
- Technique distribution with tactics + top IPs
- Tactics distribution
- Attack type distribution
- Attack stage distribution
- Activity over time
- Summary
- session_mitre_relationships_count (just a number)

For drilling into a specific session: mitre_analytics_sessions.json
Load only when the user clicks a session.
