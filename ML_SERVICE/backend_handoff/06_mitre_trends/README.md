
📦 MITRE Trends — Backend Handoff
🎯 What is this?
Time-series of MITRE dimensions over calendar days.

For each (day, dimension, value) produces session_count + event_count.

📊 Data Snapshot
Total records: 11,879

Total trend rows: 189

Unique dates: 29

By dimension (63 rows each):

MITRE_TECHNIQUE

ATTACK_TYPE

ATTACK_STAGE

🔗 Suggested Endpoints
text
GET /api/ml/analytics/mitre/trends
GET /api/ml/analytics/mitre/trends?dimension=MITRE_TECHNIQUE
GET /api/ml/analytics/mitre/trends?dimension=MITRE_TECHNIQUE&value=T1595
📐 Three Views Available
1. trends — flat list
json
{
  "trend_date": "2025-06-10",
  "trend_dimension": "MITRE_TECHNIQUE",
  "trend_value": "T1595",
  "session_count": 6789,
  "event_count": 31814
}
Use for: filtering, exporting, table views

2. series — chart-ready
json
{
  "MITRE_TECHNIQUE": {
    "T1595": [
      {"date": "2025-06-09", "session_count": 2319, "event_count": 10812},
      {"date": "2025-06-10", "session_count": 6789, "event_count": 31814},
      {"date": "2025-06-11", "session_count": 2521, "event_count": 12179}
    ]
  }
}
Use for: Multi-line chart directly into Recharts/Chart.js

3. top_values — legend
json
{
  "MITRE_TECHNIQUE": [
    {"value": "T1595", "total_sessions": 11637},
    {"value": "T1110", "total_sessions": 178}
  ]
}
Use for: chart legend + filter dropdowns

🎨 Dashboard Usage
text
┌─────────────────────────────────────────────┐
│ 📈 MITRE Techniques Over Time                │
├─────────────────────────────────────────────┤
│  Sessions                                    │
│  7000 ┤                ╱╲                    │
│  3500 ┤               ╱  ╲                   │
│  1000 ┤              ╱    ╲                  │
│   500 ┤ ▁▁▁▁▁▁▁▁▁▁▁╱      ╲▁▁               │
│     0 └─────────────────────────            │
│       Jan 2020       Jun 2025               │
│                                              │
│ ● T1595 (11,637)  ● T1110 (178)  ● T1190   │
└─────────────────────────────────────────────┘
Recommended chart: Multi-line, one line per trend_value, using series[dimension][value] directly.

Note: There's a 5-year gap (2020 / 2025). Use the temporal analytics active_periods for slicing if needed.

⚠️ Rules
series[dimension][value] is always sorted by date

top_values[dimension] capped at 10 values

Sessions without a valid dimension value are excluded

Empty series[dim][val] means no data for that value
