# ML Service — Honeypot Threat Intelligence

Production ML microservice for the Smart Honeypot Orchestrator.
Reads events from Elasticsearch, runs the frozen production ML pipeline,
and produces dashboard-ready analytics.

---

## Quick Start

```bash
# 1. Ensure ELK network exists
docker network ls | grep elk_elk-net

# 2. Start the service
docker compose up -d

# 3. Verify
curl http://localhost:8000/health
curl http://localhost:8000/ready
Expected: {"status":"ok"} and {"ready":true}.

What It Does
text
Elasticsearch  →  ML Pipeline  →  8 Analytics  →  Backend Handoff
   (events)       (48 features)    (JSON files)      (dashboard)
Reads events from Elasticsearch (honeypot-events index)

Reconstructs sessions from raw events

Generates 48 behavioral features per session

Assigns each session to a production cluster (frozen model)

Produces 8 analytics layers for the dashboard

Packages everything for the Backend team

Folder Map
Folder	Purpose
app/	Source code (pipeline + analytics + API)
app/pipeline/	ML pipeline stages (features, sessions)
app/analytics/	8 analytics layers + contracts
app/analytics/contracts/	JSON contract schemas
models/	Frozen production model artifacts (read-only)
tests/	Unit + contract tests
docs/	Detailed documentation (see below)
analytics_output/	Generated JSON files (gitignored)
backend_handoff/	Package for Backend team (gitignored)
run_ml_pipeline.sh	Run the full pipeline end-to-end
package_handoff.sh	Package results into a ZIP for Backend
Documentation
Document	Description
docs/PIPELINE_FLOW.md	Every pipeline step from ES to Backend
docs/RUNTIME_GUIDE.md	How to run the pipeline + package results
docs/INTEGRATION_GUIDE.md	ELK ↔ ML ↔ Backend wiring
docs/ARCHITECTURE.md	Design decisions + golden rules
API Endpoints
Method	Endpoint	Description
GET	/health	Health check
GET	/ready	Readiness (model loaded?)
GET	/model	Model metadata
GET	/analytics	All 6 analytics layers
GET	/session-replay	Session list (paginated)
GET	/session-replay/{id}	Single session detail
POST	/process	Run pipeline on custom payload
Full API docs: http://localhost:8000/docs (Swagger UI).

Frozen Model Rules
This service never modifies the ML model:

❌ No retraining

❌ No DBSCAN fitting

❌ No new cluster creation

❌ No cluster reassignment

✅ Read-only Elasticsearch access

✅ Frozen scaler + frozen centroids only

✅ Nearest-centroid assignment only

The model artifacts live in models/frozen_production_reference/
and are protected by SHA-256 verification.

Analytics Layers
#	Layer	Output
1	Cluster Analytics	29 clusters + behaviors
2	Temporal Analytics	Timeline + periods
3	Session Analytics	KPIs + alerts + distributions
4	MITRE Analytics	Techniques + tactics + top IPs
5	MITRE Statistics	Flat stats table (49 rows)
6	MITRE Trends	Time-series per technique
7	Session Replay	Session narratives + events
8	Attacker IP Analytics	(deferred — needs public IPs)
Each layer is independent and consumes the ML output directly.

Requirements
Docker 20+

Docker network elk_elk-net (created by the ELK stack)

Elasticsearch index honeypot-events (populated)

Python 3.11+ (only for local dev outside Docker)

Local Development
bash
# Activate virtual environment
source .venv/bin/activate

# Run tests
python -m pytest tests/ -q

# Run the pipeline manually
bash run_ml_pipeline.sh

# Package results for Backend
bash package_handoff.sh
Related Repositories
Orchestrator — deployment & honeypot management

Backend — consumes ML analytics + serves the dashboard

ELK — Elasticsearch, Logstash, Kibana stack

honeypots — Cowrie, Tanner, Dionaea configurations

Contact
ML Service Owner: Hanaa

Backend Integration Lead: (fill)

Frontend Lead: (fill)
