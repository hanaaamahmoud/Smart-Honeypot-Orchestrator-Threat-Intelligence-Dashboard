# 📦 Temporal Analytics — Backend Handoff

## 🎯 What is this? (Simple)

Analysis of **"when did the attacks happen?"**
Groups the 11,879 sessions by calendar day.

**Use:** Timeline chart on the dashboard.

## 📊 The Story (Important)

The data has **2 separate time periods**:

### 🔵 Period 1 — HTTP/FTP Activity (2020)
- 26 days (Jan 22 → Feb 22, 2020)
- 216 sessions (1.82%)
- Source: tanner (HTTP) + dionaea (FTP)

### 🔴 Period 2 — SSH Attack Surge (2025)
- 3 days (Jun 9 → Jun 11, 2025)
- 11,663 sessions (98.18%)
- Source: cowrie (SSH)
- **Peak: Jun 10 (6,812 sessions)**

### ⚠️ Gap between periods:
- 1,932 days without activity (5 years)
- **This is expected** — the dataset covers two distinct periods

## 🎨 How to Display on Dashboard

### ⚠️ Warning: There's a 5-year gap

If you plot all days equally, the chart will show:
▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁
2020 2025

text
All activity on the right — hard to see details.

### ✅ Recommended Display Options:

**Option A: Show periods separately** (best)
[ Period 1: 2020 ] [ Period 2: 2025 ]
26 days 3 days

text

**Option B: Skip the gap**
Show only active days in sequence.

**Option C: Log scale**
Y-axis = log(sessions)

## 📐 Top-Level Schema

```json
{
  "contract_name": "TEMPORAL_ANALYTICS_HANDOFF",
  "contract_version": "1.0.0",
  "generated_at": "ISO-8601",
  "analytics_layer": "TEMPORAL_ANALYTICS",
  "trend_type": "DAILY",
  "summary": {
    "total_days": 29,
    "total_sessions": 11879,
    "total_events": 58820,
    "date_range": {"from": "...", "to": "..."},
    "total_active_periods": 2,
    "largest_gap_days": 1932,
    "avg_sessions_per_active_day": 409.62
  },
  "highlights": {
    "peak_day": {
      "trend_date": "2025-06-10",
      "session_count": 6812,
      "event_count": 31905
    }
  },
  "periods": [
    {
      "period_id": 1,
      "from": "2020-01-22",
      "to": "2020-02-22",
      "days": 26,
      "sessions": 216,
      "sessions_pct": 1.82,
      "events": 4072,
      "events_pct": 6.92,
      "peak_day": {"trend_date": "...", "session_count": N},
      "daily_trends": [
        {"trend_date": "...", "session_count": N, "event_count": N}
      ]
    }
  ],
  "trends": [
    {
      "trend_date": "YYYY-MM-DD",
      "session_count": N,
      "total_events": N,
      "avg_session_duration_seconds": F,
      "event_count": N,
      "unique_sessions": N,
      "trend_type": "DAILY"
    }
  ]
}
🎨 Dashboard Components
KPI Cards
text
┌─────────────────┬─────────────────┬─────────────────┐
│ 📅 29 Days      │ 📊 11,879       │ 📈 58,820       │
│ Active          │ Sessions        │ Events          │
├─────────────────┼─────────────────┼─────────────────┤
│ 🔥 Peak Day     │ 📆 2 Periods    │ ⚠️ Gap          │
│ Jun 10, 2025    │ Active          │ 1,932 days      │
│ 6,812 sessions  │                 │                 │
└─────────────────┴─────────────────┴─────────────────┘
Period Card
text
🔴 SSH Attack Surge
Jun 9 → Jun 11, 2025
3 days · 11,663 sessions (98.18%)
Peak: Jun 10 (6,812 sessions)
Line Chart
Use periods[].daily_trends to draw one chart per period — avoids the 5-year gap issue.

🔗 Suggested Endpoints
text
GET /api/ml/analytics/temporal
GET /api/ml/analytics/temporal/periods
GET /api/ml/analytics/temporal/periods/{period_id}
⚠️ Critical Rules
Rows sorted ascending by trend_date

trend_type is ALWAYS "DAILY"

One row per calendar day

total_events == event_count (both aggregates)

Date gaps are MEANINGFUL — don't interpolate

Use periods to display — don't plot the gap

Don't add MITRE breakdown — use mitre_trends for that

🔄 Refresh Cadence
Regenerated on each ML pipeline run

generated_at marks the last run

📞 Contact
ML Service Owner: (fill)

Backend Integration Lead: (fill)
