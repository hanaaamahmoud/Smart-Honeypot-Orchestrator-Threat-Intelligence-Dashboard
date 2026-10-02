# 📦 MITRE Statistics — Backend Handoff

## 🎯 What is this?

Flat statistic records across 5 dimensions:
OVERALL, CLUSTER, MITRE_TECHNIQUE, ATTACK_TYPE, ATTACK_STAGE.

## 📊 Data Snapshot

- Total sessions: 11,879
- Total events: 58,820
- Total rows: 49
- Rows by type:
  - OVERALL: 1
  - CLUSTER: 29
  - MITRE_TECHNIQUE: 6
  - ATTACK_TYPE: 7
  - ATTACK_STAGE: 6

## 🔗 Suggested Endpoints
GET /api/ml/analytics/mitre/statistics
GET /api/ml/analytics/mitre/statistics?type=OVERALL
GET /api/ml/analytics/mitre/statistics?type=MITRE_TECHNIQUE

text

## 📐 Record Schema

```json
{
  "statistic_type": "MITRE_TECHNIQUE",
  "statistic_key": "T1595",
  "rank": 1,
  "label": "T1595 — Active Scanning",
  "tactic": "Reconnaissance",
  "session_count": 11637,
  "event_count": 42810,
  "session_share_pct": 97.96,
  "mapped_mitre_sessions": 11637,
  "unmapped_mitre_sessions": 0,
  "mitre_technique": "T1595",
  "mitre_attack_name": "Active Scanning",
  "attack_type": "",
  "attack_stage": ""
}
Field notes
rank: position within its statistic_type (1-based, sorted by session_count DESC or cluster ID)

label: display-ready string

tactic: only populated for MITRE_TECHNIQUE

mapped_mitre_sessions / unmapped_mitre_sessions: only meaningful for OVERALL & CLUSTER

Non-applicable dimension fields are empty strings (never null)

🎨 Dashboard Usage
Cards
For OVERALL row → single summary card:

text
┌─────────────────────┐
│ OVERALL              │
│ 11,879 sessions      │
│ 58,820 events        │
│ 100% mapped          │
└─────────────────────┘
Tables
For each dimension → filter + sort by rank:

Techniques table (6 rows)

Clusters table (29 rows)

Attack types table (7 rows)

Attack stages table (6 rows)

⚠️ Rules
Rows are ordered within each statistic_type by rank

session_share_pct sums to ~100% within each dimension

mapped + unmapped = session_count for OVERALL & CLUSTER

Non-applicable fields are empty strings

