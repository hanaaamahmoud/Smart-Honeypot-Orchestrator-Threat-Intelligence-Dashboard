# Temporal Analytics

Daily timeline of sessions. Identifies active periods and gaps.

| Item | Value |
|---|---|
| Data file | temporal_analytics.json |
| Schema | 02_temporal_analytics/schema.json |
| Endpoint | /api/ml/temporal |

## Data Keys

- `trends[]` — one row per calendar day
- `periods[]` — one entry per active period
- `highlights` — peak day
- `summary` — totals

## Trend Row

| Field | Type | Description |
|---|---|---|
| trend_date | string | YYYY-MM-DD |
| session_count | int | Sessions on this day |
| total_events | int | Events on this day |
| event_count | int | Same as total_events |
| avg_session_duration_seconds | float | Average duration |
| unique_sessions | int | Distinct sessions |
| trend_type | string | Always "DAILY" |

## Period Object

| Field | Type | Description |
|---|---|---|
| period_id | int | 1-based index |
| from, to | string | Start and end dates |
| days | int | Active days in period |
| sessions | int | Sessions in period |
| sessions_pct | float | Share of total |
| events | int | Events in period |
| events_pct | float | Share of total events |
| peak_day | object | Peak session day |
| daily_trends | array | Daily rows for the period |

## Notes

- Rows sorted ascending by trend_date.
- Date gaps between periods are meaningful — do not interpolate.
- Use periods[] for one chart per period.
