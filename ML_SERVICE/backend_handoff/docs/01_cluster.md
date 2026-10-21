# Cluster Analytics

Behavioral cluster analytics from the frozen production DBSCAN model.

| Item | Value |
|---|---|
| Data file | cluster_analytics.json |
| Schema | 01_cluster_analytics/schema.json |
| Endpoint | /api/ml/clusters |

## Data Key: clusters[]

| Field | Type | Description |
|---|---|---|
| cluster_id | int | Production cluster ID |
| session_count | int | Sessions in this cluster |
| percentage | float | Share of total sessions |
| cluster_type | string | Behavioral type |
| activity_profile | string | Activity description |
| attacker_behavior | string | Attacker intent |
| confidence | enum | HIGH / MEDIUM / LOW |
| possible_attack_name | string | Optional |
| evidence_features | string[] | Defining features |
| top_honeypots | TopItem[] | Top honeypots |
| top_countries | TopItem[] | Top countries |
| top_protocols | TopItem[] | Top protocols |
| top_attack_types | TopItem[] | Top attack types |
| top_mitre_techniques | TopItem[] | Top MITRE techniques |
| top_attack_stages | TopItem[] | Top MITRE stages |
| top_severities | TopItem[] | Top severities |
| avg_event_count | float or null | Average events per session |
| avg_distance | float or null | Average distance to centroid |
| avg_session_duration | float or null | Average duration (s) |

TopItem: `{"value": "...", "count": N, "percentage": F}`

## Notes

- Clusters sorted by session_count descending.
- Only clusters that received sessions are present.
- Missing clusters received no sessions in this run.
