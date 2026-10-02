
📦 Backend Handoff Package
ML Service analytics handoff for the Smart Honeypot Threat Intelligence Dashboard.

📁 Structure
text
backend_handoff/
├── README.md                     ← this file
├── 01_cluster_analytics/         ✅ DONE
│   ├── README.md
│   ├── cluster_analytics.json
│   └── schema.json
├── 02_temporal_analytics/        ⏳ pending
├── 03_attacker_ip_analytics/     ⏳ pending
├── 04_mitre_analytics/           ⏳ pending
├── 05_mitre_statistics/          ⏳ pending
├── 06_mitre_trends/              ⏳ pending
├── 07_geoip_analytics/           ⏳ pending
├── 08_session_replay/            ⏳ pending
└── 09_session_analytics/         ⏳ pending
🎯 Quick Start for Backend
Each NN_* folder contains:

README.md — What the data is, endpoint suggestions, schema

<name>.json — The actual data to serve

schema.json — JSON schema for validation

📐 General Contract
All payloads follow this pattern:

json
{
  "contract_name": "...",
  "contract_version": "1.0.0",
  "generated_at": "ISO-8601",
  "source": "ML_SERVICE_FROZEN_PRODUCTION",
  "analytics_layer": "LAYER_NAME",
  "summary": { ... },
  "<data_key>": [ ... ]
}
⚠️ Global Rules
Never modify cluster assignments on the backend

Never create new clusters

Never infer missing fields

Empty arrays mean "no data", never null

Optional fields (like possible_attack_name) may be absent

Re-fetch data when ML service signals a new pipeline run

🔄 Refresh Workflow
text
ML Service runs pipeline
        ↓
Generates analytics_output/*.json
        ↓
Copies to backend_handoff/NN_*/
        ↓
Backend re-fetches from shared location
📞 Contact
ML Service Owner: (fill)

Backend Integration Lead: (fill)
