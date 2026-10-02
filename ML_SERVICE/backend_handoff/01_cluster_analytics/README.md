# 📦 Cluster Analytics — Backend Handoff

## 🎯 What is this?

ML-driven behavioral cluster analytics for the Smart Honeypot dashboard.
Each cluster = a distinct attacker behavior group discovered by the
frozen production DBSCAN model.

## 📁 Files in this folder
01_cluster_analytics/
├── README.md ← this file
├── cluster_analytics.json ← the data
└── schema.json ← JSON schema for validation

text

## 🔗 Suggested Endpoints
GET /api/ml/analytics/clusters
GET /api/ml/analytics/clusters/{cluster_id}

text

## 📊 Source

- Pipeline: Elasticsearch → ML Service → cluster analytics
- Model: Frozen production DBSCAN (38 behavioral clusters + noise)
- Input: 11,879 sessions from ES index `honeypot-events`
- Output: 29 clusters (assigned by nearest frozen centroid)

### ⚠️ Why 29 clusters, not 38?

The frozen model contains 38 behavioral centroids. In this run, only
29 received sessions. The other 9 (4, 5, 7, 11, 14, 16, 21, 22, 29)
had no sessions closer to them than to other centroids.

This is expected behavior. The dashboard should display only the
clusters that actually received sessions.

When new data arrives that matches those missing clusters, they will
appear automatically. No code change is needed.

## 📐 Top-Level Schema

```json
{
  "contract_name": "CLUSTER_ANALYTICS_HANDOFF",
  "contract_version": "1.0.0",
  "generated_at": "2026-10-02T...Z",
  "source": "ML_SERVICE_FROZEN_PRODUCTION",
  "model_status": "FROZEN_PRODUCTION_REFERENCE",
  "analytics_layer": "CLUSTER_ANALYTICS",
  "summary": {
    "total_clusters": 29,
    "total_sessions": 11879,
    "noise_session_count": 0
  },
  "clusters": [ ... ]
}
📐 Cluster Object Fields
Field	Type	Required	Description
cluster_id	int	✅	Production cluster ID
session_count	int	✅	Sessions in this cluster
percentage	float	✅	Share of total sessions
cluster_type	string	✅	Behavioral type
activity_profile	string	✅	Activity description
attacker_behavior	string	✅	Attacker intent
confidence	enum	✅	HIGH / MEDIUM / LOW
possible_attack_name	string	❌	Only when evidence supports
evidence_features	string[]	✅	Defining features
top_honeypots	TopItem[]	✅	Top 5 honeypots
top_countries	TopItem[]	✅	Top 5 countries
top_protocols	TopItem[]	✅	Top 5 protocols
top_attack_types	TopItem[]	✅	Top 5 attack types
top_mitre_techniques	TopItem[]	✅	Top 5 MITRE techniques
top_attack_stages	TopItem[]	✅	Top 5 MITRE stages
top_severities	TopItem[]	✅	Top 5 severities
avg_event_count	float	null	✅	Avg events/session
avg_distance	float	null	✅	Avg distance to centroid
avg_session_duration	float	null	✅	Avg duration (seconds)
📐 TopItem Schema
json
{
  "value": "cowrie",
  "count": 1536,
  "percentage": 99.29
}
Up to 5 items per top_* array

Sorted descending by count

Empty array [] means "no data", never null

🎨 Dashboard Usage
Overview Table
Columns: ID · Sessions · % · Type · Confidence · Top Honeypot · Top Country

Detail Page (per cluster)
Header: cluster_id, session_count, percentage

Behavior card: cluster_type + activity_profile + attacker_behavior

Evidence card: evidence_features

Distribution cards: honeypots, countries, protocols, attacks, MITRE, stages, severities

Stats: avg_event_count, avg_distance, avg_session_duration

Filters
By cluster_type

By confidence

By possible_attack_name presence

⚠️ Critical Rules for Backend
DO NOT reassign clusters on the backend side

DO NOT create new clusters

DO NOT change cluster_id values

DO NOT infer missing fields

Empty top_* arrays mean "no data available"

possible_attack_name is optional — many clusters don't have one

noise_session_count = DBSCAN noise (-1) sessions

If a cluster is absent from clusters, it simply received no sessions

🔄 Refresh Cadence
Regenerated on each ML pipeline run

generated_at marks the last run

Backend should re-fetch when ML service signals a new run

📞 Contact
ML Service Owner: (fill)

Backend Integration Lead: (fill)
