# MITRE Trends

Time-series for MITRE dimensions over calendar days.

| Item | Value |
|---|---|
| Data file | mitre_trends.json |
| Schema | 06_mitre_trends/schema.json |
| Endpoint | /api/ml/mitre/trends |

## Data Keys

- `trends[]` — flat rows
- `series` — chart-ready per dimension/value
- `top_values` — legend values
- `summary`

## Trend Row

| Field | Type | Description |
|---|---|---|
| trend_date | string | YYYY-MM-DD |
| trend_dimension | string | MITRE_TECHNIQUE, ATTACK_TYPE, ATTACK_STAGE |
| trend_value | string | Technique ID or value |
| session_count | int | Sessions |
| event_count | int | Events |

## Series Shape

    "series": {
      "MITRE_TECHNIQUE": {
        "T1595": [
          {"date": "YYYY-MM-DD", "session_count": N, "event_count": N}
        ]
      }
    }

## Top Values Shape

    "top_values": {
      "MITRE_TECHNIQUE": [
        {"value": "T1595", "total_sessions": N}
      ]
    }

## Notes

- series[dimension][value] sorted by date ascending.
- top_values[dimension] capped at 10 values.
- Empty dimension values are excluded.
