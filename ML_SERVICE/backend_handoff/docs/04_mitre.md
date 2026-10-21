# MITRE Analytics

MITRE ATT&CK distributions with tactics mapping.

| Item | Value |
|---|---|
| Data file | mitre_analytics.json |
| Schema | 04_mitre_analytics/schema.json |
| Endpoint | /api/ml/mitre |

## Data Keys

- `mitre_technique_distribution[]`
- `mitre_tactics_distribution[]`
- `attack_type_distribution[]`
- `attack_stage_distribution[]`
- `session_mitre_relationships[]`
- `mitre_activity_over_time[]`
- `summary`

## Technique Item

| Field | Type | Description |
|---|---|---|
| value | string | Technique ID (e.g. T1595) |
| count | int | Session count |
| percentage | float | Share |
| tactic | string | MITRE tactic (derived) |
| top_source_ips | array | Top 5 IPs for this technique |

## Tactic Item

`{"value": "Reconnaissance", "count": N, "percentage": F}`

## Relationship Item

`{"session_id": "...", "mitre_techniques": [], "attack_types": [], "attack_stages": []}`

## Activity Item

`{"date": "YYYY-MM-DD", "count": N}`

## Notes

- Techniques sorted by count descending.
- top_source_ips capped at 5 per technique.
- Tactic derived from official MITRE ATT&CK mapping.
- Empty MITRE values are not fabricated.
