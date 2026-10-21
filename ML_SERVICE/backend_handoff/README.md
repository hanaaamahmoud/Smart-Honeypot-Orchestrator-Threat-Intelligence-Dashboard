# Backend Handoff — ML Analytics

Integration reference for the ML Service analytics.

---

## Quick Start

1. Extract the delivered ZIP to `/backend/data/ml_analytics/`
2. Load the JSON files at startup
3. Expose the endpoints listed below
4. Frontend reads from your API only

---

## Analytics Layers

| # | Layer | Data File | Endpoint | Details |
|---|---|---|---|---|
| 1 | Cluster | cluster_analytics.json | /api/ml/clusters | [doc](docs/01_cluster.md) |
| 2 | Temporal | temporal_analytics.json | /api/ml/temporal | [doc](docs/02_temporal.md) |
| 3 | Session | session_analytics.json | /api/ml/sessions/summary | [doc](docs/03_session.md) |
| 4 | MITRE | mitre_analytics.json | /api/ml/mitre | [doc](docs/04_mitre.md) |
| 5 | MITRE Stats | mitre_statistics.json | /api/ml/mitre/statistics | [doc](docs/05_mitre_stats.md) |
| 6 | MITRE Trends | mitre_trends.json | /api/ml/mitre/trends | [doc](docs/06_mitre_trends.md) |
| 7 | Session Replay | session_replay_list.json | /api/ml/session-replay | [doc](docs/07_replay.md) |

Frontend guide: [docs/FRONTEND.md](docs/FRONTEND.md)

---

## Common Data Contract

Every file follows the same top-level structure:

    {
      "contract_name": "...",
      "contract_version": "x.y.z",
      "generated_at": "ISO-8601",
      "source": "ML_SERVICE_FROZEN_PRODUCTION",
      "analytics_layer": "LAYER_NAME",
      "summary": { ... },
      "<data_key>": [ ... ]
    }

Full per-layer details: see the Details links above.

---

## Global Rules

- Do not modify cluster assignments on the Backend side
- Do not create new clusters or reassign sessions
- Do not infer or fabricate missing fields
- Empty arrays mean "no data", never null
- Optional fields may be absent
- Analytics files are read-only

---

## Refresh Workflow

    bash scripts/run_ml_pipeline.sh     # regenerate data
    bash scripts/package_handoff.sh     # rebuild the ZIP
    → send the new ZIP to the Backend team

No code changes needed. File names stay the same.

---

## Folder Structure

    backend_handoff/
    |-- README.md              This file
    |-- docs/                  Per-layer references
    |   |-- 01_cluster.md
    |   |-- 02_temporal.md
    |   |-- 03_session.md
    |   |-- 04_mitre.md
    |   |-- 05_mitre_stats.md
    |   |-- 06_mitre_trends.md
    |   |-- 07_replay.md
    |   `-- FRONTEND.md
    |-- 01_cluster_analytics/  Data + schema
    |-- 02_temporal_analytics/
    |-- 03_session_analytics/
    |-- 04_mitre_analytics/
    |-- 05_mitre_statistics/
    |-- 06_mitre_trends/
    `-- 07_session_replay/

---

## Related Documentation

- Integration guide:  ../docs/INTEGRATION_GUIDE.md
- Pipeline flow:      ../docs/PIPELINE_FLOW.md
- Architecture:       ../docs/ARCHITECTURE.md
