# ML Service — Honeypot Threat Intelligence

Production ML microservice for the Smart Honeypot Orchestrator.
It reads honeypot events from Elasticsearch, runs a frozen ML pipeline,
and produces dashboard-ready analytics for the Backend team.

The service is read-only with respect to Elasticsearch and never
retrains the ML model. Every run produces the same output for the
same input.

---

## What This Folder Contains

`ML_SERVICE/` is the Python microservice that turns raw honeypot events
into behavioral analytics for the dashboard.

Input: Elasticsearch events (honeypot-events index)
Output: 7 analytics layers (JSON) + Backend handoff package

If you are a:

- Backend developer     → start with docs/INTEGRATION_GUIDE.md
- Frontend developer    → start with backend_handoff/frontend_guide/FRONTEND_HANDOFF.md
- ML engineer           → start with docs/PIPELINE_FLOW.md
- DevOps / deployer     → start with docs/RUNTIME_GUIDE.md
- Reviewer             → start with docs/ARCHITECTURE.md

---

## Quick Start

    # 1. Ensure the ELK network exists (created by the ELK stack)
    docker network ls | grep elk_elk-net

    # 2. Build and start the service
    docker compose up -d

    # 3. Verify
    curl http://localhost:8000/health
    curl http://localhost:8000/ready

Expected responses:

    {"status":"ok","service":"honeypot-ml-service"}
    {"status":"ready","ready":true,...}

Interactive API documentation: http://localhost:8000/docs

---

## Folder Map

Every folder and top-level file is described below. Anyone new to the
repository should be able to identify a file's purpose within seconds.

    ML_SERVICE/
    |
    |-- app/                    Source code — the entire service
    |   |-- ingestion/          Elasticsearch reader (read-only)
    |   |-- pipeline/           ML pipeline stages (features, sessions)
    |   |-- analytics/          7 analytics layers
    |   |-- analytics/contracts/ JSON contract schemas
    |   |-- model_loader.py     Frozen model and scaler loader
    |   |-- output_adapter.py   Canonical ML result formatter
    |   |-- config.py           Configuration (env-driven)
    |   |-- schemas.py          Pydantic models
    |   `-- main.py             FastAPI entry point (all routes)
    |
    |-- tests/                  Automated tests
    |   |-- unit/               Pure-function tests
    |   |-- contract/           Schema and contract tests
    |   `-- integration/        End-to-end tests
    |
    |-- models/                 Frozen production artifacts (read-only)
    |   `-- frozen_production_reference/
    |       |-- standard_scaler_params.json
    |       |-- step7g_dbscan_behavioral_reference_centroids.csv
    |       `-- (21 files protected by SHA-256)
    |
    |-- docs/                   Detailed documentation
    |   |-- PIPELINE_FLOW.md    Pipeline step-by-step reference
    |   |-- RUNTIME_GUIDE.md    How to run the pipeline
    |   |-- INTEGRATION_GUIDE.md How to wire ML <-> Backend
    |   |-- ARCHITECTURE.md     Design rules and integration models
    |   `-- canonical_output_contract.md  Canonical ML output spec
    |
    |-- backend_handoff/        Per-analytics docs and data (for Backend)
    |   |-- 01_cluster_analytics/
    |   |-- 02_temporal_analytics/
    |   |-- 03_session_analytics/
    |   |-- 04_mitre_analytics/
    |   |-- 05_mitre_statistics/
    |   |-- 06_mitre_trends/
    |   |-- 07_session_replay/
    |   |-- frontend_guide/     Frontend integration guide
    |   `-- ml_analytics_files/ Data files (gitignored)
    |
    |-- analytics_output/       Generated data (gitignored)
    |   |-- 00_ml_output_full.json
    |   |-- 02_cluster_analytics_enriched.json
    |   |-- 03_temporal_analytics.json
    |   |-- 04_session_analytics.json
    |   |-- 05_mitre_analytics_lite.json
    |   |-- 06_mitre_statistics.json
    |   |-- 07_mitre_trends.json
    |   |-- 08_session_replay_list.json
    |   `-- session_replay_details/   367 session files
    |
    |-- scripts/                Runtime and diagnostic tools
    |   |-- run_ml_pipeline.sh  Run pipeline end-to-end
    |   |-- package_handoff.sh  Package results into a ZIP
    |   |-- docker_preflight.sh Pre-deployment checks
    |   `-- diagnostics/        Data inspection tools
    |       |-- diagnose_pipeline.py
    |       |-- diagnose_random.py
    |       |-- diagnose_bad_sessions.py
    |       `-- diagnose_distance_breakdown.py
    |
    |-- Dockerfile              Container image definition
    |-- docker-compose.yml      Service, mounts, and network
    |-- requirements.txt        Python dependencies
    |-- pytest.ini              Test configuration
    |-- .env.example            Environment variables template
    |-- .dockerignore           Excluded from image build
    |-- .gitignore              Excluded from Git
    `-- README.md               This file

---

## Top-Level File Reference

| File | Purpose |
|---|---|
| Dockerfile | Container image definition (python:3.11-slim) |
| docker-compose.yml | Service definition, volume mounts, network |
| requirements.txt | Python dependencies |
| pytest.ini | Test framework configuration |
| .env.example | Environment variable template |
| .dockerignore | Files excluded from the Docker build |
| .gitignore | Files excluded from Git (data, backups) |
| README.md | Project overview (this file) |

---

## Where to Find What

Use this table to locate any topic in a few seconds.

| Goal | File or folder |
|---|---|
| Understand the whole pipeline | docs/PIPELINE_FLOW.md |
| Run the pipeline | scripts/run_ml_pipeline.sh |
| Send results to Backend | scripts/package_handoff.sh |
| Integrate ML with Backend | docs/INTEGRATION_GUIDE.md |
| Know the design rules | docs/ARCHITECTURE.md |
| Field-level docs per analytics | backend_handoff/0X_*/README.md |
| JSON schemas | backend_handoff/0X_*/schema*.json |
| Frontend integration guide | backend_handoff/frontend_guide/FRONTEND_HANDOFF.md |
| API routes | app/main.py |
| Frozen model artifacts | models/frozen_production_reference/ |
| Run tests | python -m pytest tests/ |
| Inspect pipeline output | scripts/diagnostics/diagnose_pipeline.py |
| Check cluster distances | scripts/diagnostics/diagnose_distance_breakdown.py |
| Fix unusual sessions | scripts/diagnostics/diagnose_bad_sessions.py |
| Random sample inspection | scripts/diagnostics/diagnose_random.py |

---

## Pipeline Overview

    Elasticsearch (honeypot-events)
            |
            v
    ElasticsearchReader.read_events()              [app/ingestion/]
            |
            v
    Input Adapter  ->  Canonical Adapter           [app/pipeline/]
            |
            v
    Normalization  ->  Session Reconstruction
            |
            v
    48-Feature Generation + Validation
            |
            v
    Frozen Scaler  ->  Nearest Centroid
            |
            v
    Canonical ML Output                            [app/output_adapter.py]
            |
            v
    7 Analytics Layers                             [app/analytics/]
            |
            v
    Backend Handoff Package                        [scripts/package_handoff.sh]

Full reference: docs/PIPELINE_FLOW.md

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | /health | Liveness check |
| GET | /ready | Readiness (model loaded) |
| GET | /model | Model metadata |
| GET | /analytics | All analytics layers |
| GET | /session-replay | Session list (lightweight) |
| GET | /session-replay/{id} | Single session detail |
| POST | /process | Run pipeline on a custom payload |

Interactive docs: http://localhost:8000/docs

---

## Analytics Layers

| # | Layer | File | Purpose |
|---|---|---|---|
| 1 | Cluster Analytics | cluster_analytics.py | 29 clusters and behaviors |
| 2 | Temporal Analytics | temporal_analytics.py | Timeline and periods |
| 3 | Session Analytics | session_analytics.py | KPIs, alerts, distributions |
| 4 | MITRE Analytics | mitre_analytics.py | Techniques, tactics, top IPs |
| 5 | MITRE Statistics | mitre_statistics.py | Flat stats table (49 rows) |
| 6 | MITRE Trends | mitre_trends.py | Time-series per technique |
| 7 | Session Replay | session_replay.py | Narratives and event timeline |

Each layer is independent and consumes the ML output directly.
Field-level details: backend_handoff/0X_*/README.md

---

## Service Guarantees

This service is designed around strict invariants. Every change must
preserve them.

Read-only:
- Elasticsearch access is read-only
- Analytics layers never modify the ML output
- The Backend never writes back to the ML service

Frozen model:
- The scaler, centroids, and 48-feature contract are frozen
- No retraining, no DBSCAN fitting, no new clusters
- No cluster reassignment
- Assignment is nearest-centroid only

No fabrication:
- Missing values remain null
- No defaults, no inference, no guessing
- Every field either comes from the source data or is explicitly absent

These rules apply to every stage of the pipeline. Any change that would
violate them must be rejected or handled as a separate, explicit
extension of the contract.

The model artifacts live in models/frozen_production_reference/ and
are protected by SHA-256 verification (frozen_reference_sha256.json).

---

## Docker and Runtime

Start the service:

    docker compose up -d

Mounted folders (Host <-> Container):

    app/               <->  /app/app
    analytics/         <->  /app/analytics
    tests/             <->  /app/tests
    models/            <->  /app/models
    backend_handoff/   <->  /app/backend_handoff
    analytics_output/  <->  /app/analytics_output
    docs/              <->  /app/docs
    scripts/           <->  /app/scripts

After code changes:

    docker restart honeypot-ml-service

After docker-compose.yml or Dockerfile changes:

    docker compose down && docker compose up -d

Network: elk_elk-net (external, created by the ELK stack).

Full details: docs/RUNTIME_GUIDE.md

---

## Local Development

    # Activate virtual environment
    source .venv/bin/activate

    # Run all tests
    python -m pytest tests/ -q

    # Run pipeline manually
    bash scripts/run_ml_pipeline.sh

    # Package results for Backend
    bash scripts/package_handoff.sh

---

## Documentation Index

| Document | Description |
|---|---|
| docs/PIPELINE_FLOW.md | Every pipeline step from ES to Backend |
| docs/RUNTIME_GUIDE.md | How to run the pipeline and package results |
| docs/INTEGRATION_GUIDE.md | ELK <-> ML <-> Backend wiring (two modes) |
| docs/ARCHITECTURE.md | Design decisions and golden rules |
| docs/canonical_output_contract.md | Canonical ML output specification |
| backend_handoff/README.md | Backend handoff overview |
| backend_handoff/frontend_guide/FRONTEND_HANDOFF.md | Frontend integration guide |

---

## Requirements

- Docker 20+
- Docker network elk_elk-net (created by the ELK stack)
- Elasticsearch index honeypot-events (populated)
- Python 3.11+ (only for local development outside Docker)

---

## Related Repositories

| Repository | Purpose |
|---|---|
| Orchestrator | Deployment and honeypot management |
| Backend | Consumes ML analytics and serves the dashboard |
| ELK | Elasticsearch, Logstash, Kibana stack |
| honeypots | Cowrie, Tanner, Dionaea configurations |
