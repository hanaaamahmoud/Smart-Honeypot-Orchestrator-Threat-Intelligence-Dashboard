# MITRE Statistics

Flat statistics table across 5 dimensions.

| Item | Value |
|---|---|
| Data file | mitre_statistics.json |
| Schema | 05_mitre_statistics/schema.json |
| Endpoint | /api/ml/mitre/statistics |

## Data Key: statistics[]

| Field | Type | Description |
|---|---|---|
| statistic_type | string | OVERALL, CLUSTER, MITRE_TECHNIQUE, ATTACK_TYPE, ATTACK_STAGE |
| statistic_key | string | Identifier |
| rank | int | 1-based rank within type |
| label | string | Display-ready string |
| tactic | string | Only for MITRE_TECHNIQUE |
| session_count | int | Sessions |
| event_count | int | Events |
| session_share_pct | float | Share of total sessions |
| mapped_mitre_sessions | int | Mapped (OVERALL, CLUSTER) |
| unmapped_mitre_sessions | int | Unmapped (OVERALL, CLUSTER) |
| mitre_technique | string | Empty unless applicable |
| mitre_attack_name | string | Empty unless applicable |
| attack_type | string | Empty unless applicable |
| attack_stage | string | Empty unless applicable |

## Notes

- Rows ordered within each statistic_type by rank.
- Non-applicable fields are empty strings, not null.
- mapped + unmapped = session_count for OVERALL and CLUSTER.
