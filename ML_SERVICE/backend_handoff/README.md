# Backend Handoff — ML Analytics

Analytics data and per-layer documentation for the Smart Honeypot
Threat Intelligence Dashboard.

---

## Folder Structure

    backend_handoff/
    |-- README.md                     This file
    |-- 01_cluster_analytics/         Cluster distribution + behaviors
    |-- 02_temporal_analytics/        Timeline + active periods
    |-- 03_session_analytics/         KPIs, alerts, distributions
    |-- 04_mitre_analytics/           Techniques, tactics, top IPs
    |-- 05_mitre_statistics/          Statistics table
    |-- 06_mitre_trends/              Time-series per technique
    |-- 07_session_replay/            Session list + replay details
    |-- frontend_guide/               Frontend integration guide
    `-- ml_analytics_files/           Packaged data files for serving

Each analytics folder (`01_*` through `07_*`) contains:

- `README.md`      Field reference and endpoint suggestions
- `schema.json`    JSON schema for validation

The `ml_analytics_files/` folder contains the actual JSON data to
serve from the Backend API. It is the folder to extract from the ZIP
that the ML Service owner delivers.

---

## Quick Start for Backend

1. Extract the delivered ZIP into a shared data directory:

       /backend/data/ml_analytics/

2. Load the JSON files at startup (see `ml_analytics_files/README.md`).

3. Expose the analytics via your Backend API:

       GET /api/ml/clusters
       GET /api/ml/temporal
       GET /api/ml/sessions/summary
       GET /api/ml/sessions/alerts
       GET /api/ml/mitre
       GET /api/ml/mitre/statistics
       GET /api/ml/mitre/trends
       GET /api/ml/session-replay
       GET /api/ml/session-replay/{id}

4. Frontend consumes the Backend API only.

Full integration details: `../docs/INTEGRATION_GUIDE.md`

---

## Analytics Layers

| # | Folder | Layer | Data File |
|---|---|---|---|
| 1 | 01_cluster_analytics | Cluster Analytics | cluster_analytics.json |
| 2 | 02_temporal_analytics | Temporal Analytics | temporal_analytics.json |
| 3 | 03_session_analytics | Session Analytics | session_analytics.json |
| 4 | 04_mitre_analytics | MITRE Analytics | mitre_analytics.json |
| 5 | 05_mitre_statistics | MITRE Statistics | mitre_statistics.json |
| 6 | 06_mitre_trends | MITRE Trends | mitre_trends.json |
| 7 | 07_session_replay | Session Replay | session_replay_list.json + session_replay_details/ |

Each folder's README explains the fields and suggests the corresponding
Backend endpoint.

---

## General Payload Contract

Every analytics JSON file follows this structure:

    {
      "contract_name": "...",
      "contract_version": "1.0.0",
      "generated_at": "ISO-8601 timestamp",
      "source": "ML_SERVICE_FROZEN_PRODUCTION",
      "analytics_layer": "LAYER_NAME",
      "summary": { ... },
      "<data_key>": [ ... ]
    }

Field-level details are documented in each folder's README.

---

## Global Rules

- Never modify cluster assignments on the Backend side.
- Never create new clusters.
- Never infer or fabricate missing fields.
- Empty arrays mean "no data", not "null".
- Optional fields may be absent (e.g., possible_attack_name).
- Re-fetch data only when the ML Service signals a new pipeline run.
- Analytics files are read-only from the Backend's perspective.

---

## Refresh Workflow

    ML Service runs pipeline
            |
            v
    Generates analytics_output/*.json
            |
            v
    Packages into backend_handoff/ml_analytics_files/
            |
            v
    Creates ml_analytics_files.zip
            |
            v
    Delivered to Backend team
            |
            v
    Backend extracts and reloads

See `../scripts/package_handoff.sh` for the packaging step.

---

## Related Documentation

- Integration guide:  ../docs/INTEGRATION_GUIDE.md
- Pipeline flow:      ../docs/PIPELINE_FLOW.md
- Architecture:       ../docs/ARCHITECTURE.md
- Frontend guide:     frontend_guide/FRONTEND_HANDOFF.md
- Data README:        ml_analytics_files/README.md
