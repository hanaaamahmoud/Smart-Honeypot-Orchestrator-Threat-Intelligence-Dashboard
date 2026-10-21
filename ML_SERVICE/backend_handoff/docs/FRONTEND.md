# Frontend Integration Guide

Dashboard layout and display rules.

The Frontend reads from the Backend API only. Never directly from JSON.

## Dashboard Sections

| Section | Endpoint | Purpose |
|---|---|---|
| Overview | /api/ml/sessions/summary | KPI cards + distributions |
| Clusters | /api/ml/clusters | Cluster table + detail modal |
| MITRE | /api/ml/mitre | Techniques + tactics charts |
| Timeline | /api/ml/temporal | Daily timeline per period |
| Sessions | /api/ml/session-replay | Sessions table + filters |
| Session Replay | /api/ml/session-replay/{id} | Replay modal |

## Recommended Layout

    Header: Title + Live Status + Last Update
    ─────────────────────────────────────────
    KPI Cards Row
    ─────────────────────────────────────────
    Cluster Bar Chart    |    MITRE Tactics Pie
    ─────────────────────────────────────────
    Timeline Line Chart (per period)
    ─────────────────────────────────────────
    Sessions Table with [Replay] button

## KPI Cards

| Card | Source |
|---|---|
| Total Sessions | sessions/summary |
| Total Events | sessions/summary |
| Unique Source IPs | sessions/summary |
| ML Clusters | clusters |
| Critical Alerts | sessions/summary |
| Peak Day | temporal |

## Charts

### Cluster Distribution (Bar)
- X: cluster_id, Y: session_count
- Tooltip: cluster_type + confidence

### MITRE Tactics (Pie)
- Source: mitre_tactics_distribution
- Sort by count descending

### Timeline (Line)
- One chart per active period
- X: trend_date, Y: session_count
- Use periods[].daily_trends — do not plot the gap

## Sessions Table

| Column | Source |
|---|---|
| Session ID | sessions[].id |
| Events | sessions[].events |
| Duration | sessions[].duration |
| Country | sessions[].country |
| Attack | sessions[].attack |
| Severity | sessions[].severity |
| Action | [Replay] or [Details] |

### Button Logic

    if has_replay == true:
        → [Replay] button (opens narrative modal)
    else:
        → [Details] button (opens summary only)

### Filters

| Filter | Field |
|---|---|
| Replay-Worthy | has_replay == true |
| High Severity | flags.is_high_severity |
| Brute Force | flags.is_brute_force_candidate |
| With Commands | flags.has_commands_executed |

## Session Replay Modal

Triggered by [Replay].

Contents:
- Header: session ID + close button
- Context: honeypot · protocol · country
- Classification: attack · MITRE · severity
- Flags: badges
- Timeline: narrative.steps (20 per page + Load more)
- Credentials + Commands if present

## Display Rules

- Use periods[] for timeline — never plot gaps.
- Show only clusters present in the data.
- Empty arrays mean "no data", never null.
- possible_attack_name is optional.
- Session replay details load on demand.

## Colors

| Element | Hex |
|---|---|
| Primary | #0EA5E9 |
| Critical | #DC2626 |
| High | #F97316 |
| Medium | #EAB308 |
| Low | #22C55E |
