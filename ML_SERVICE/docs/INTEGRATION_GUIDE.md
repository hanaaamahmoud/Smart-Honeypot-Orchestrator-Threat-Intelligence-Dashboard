# Integration Guide — ML Service ↔ Backend

This document explains how the Backend team integrates ML analytics
into the dashboard.

Two integration modes are supported. The data shapes are **identical**
in both modes, so the Backend API and Frontend code do not change when
switching from one to the other.

---

## Two Integration Modes

| Mode | How it works | Data source |
|---|---|---|
| **A. File-Based** | Backend reads pre-generated JSON files | `ml_analytics_files.zip` |
| **B. Live API** | Backend queries the ML service over HTTP | `http://honeypot-ml-service:8000` |

The Backend is free to pick whichever fits the deployment. The same
JSON structures are served in both modes.

---

## Data Shape — Same in Both Modes

Every analytics layer produces one JSON object. Example for cluster
analytics:

```json
{
  "contract_name": "CLUSTER_ANALYTICS_HANDOFF",
  "contract_version": "1.0.0",
  "generated_at": "2026-10-02T...Z",
  "source": "ML_SERVICE_FROZEN_PRODUCTION",
  "analytics_layer": "CLUSTER_ANALYTICS",
  "summary": {
    "total_clusters": 29,
    "total_sessions": 11879,
    "noise_session_count": 0
  },
  "clusters": [ ... ]
}
The Backend maps each file (or endpoint) to a dashboard section. Full
field references are in backend_handoff/*/README.md.

Mode A — File-Based (Recommended for Handoff)
What the Backend receives
A single ZIP file:

text
ml_analytics_files.zip
└── ml_analytics_files/
    ├── cluster_analytics.json
    ├── temporal_analytics.json
    ├── session_analytics.json
    ├── mitre_analytics.json
    ├── mitre_statistics.json
    ├── mitre_trends.json
    ├── session_replay_list.json
    ├── session_replay_details/
    │   └── <session_id>.json
    └── README.md
How to use it
Step 1 — Extract the ZIP into a shared data directory.

text
/backend/data/ml_analytics/
├── cluster_analytics.json
├── temporal_analytics.json
├── ...
└── session_replay_details/
Step 2 — Load files at backend startup.

python
# backend/app/services/ml_analytics.py

import json
from pathlib import Path

DATA_DIR = Path("/backend/data/ml_analytics")

def load_analytics(name: str) -> dict:
    path = DATA_DIR / name
    return json.loads(path.read_text(encoding="utf-8"))

# Example usage
cluster_data = load_analytics("cluster_analytics.json")
Step 3 — Expose the data via Backend endpoints.

python
# backend/app/api/ml.py

from fastapi import APIRouter, HTTPException
from backend.app.services.ml_analytics import load_analytics

router = APIRouter(prefix="/api/ml")

@router.get("/clusters")
def get_clusters():
    return load_analytics("cluster_analytics.json")

@router.get("/temporal")
def get_temporal():
    return load_analytics("temporal_analytics.json")

@router.get("/session-replay")
def get_session_replay():
    return load_analytics("session_replay_list.json")

@router.get("/session-replay/{session_id}")
def get_session_replay_detail(session_id: str):
    path = DATA_DIR / "session_replay_details" / f"{session_id}.json"
    if not path.exists():
        raise HTTPException(404, "Session replay not found")
    return json.loads(path.read_text(encoding="utf-8"))
Step 4 — Frontend fetches from the Backend.

text
GET /api/ml/clusters
GET /api/ml/temporal
GET /api/ml/session-replay
GET /api/ml/session-replay/{id}
Refresh flow (new data)
text
1. ML service owner regenerates the ZIP
   (run_ml_pipeline.sh + package_handoff.sh)
2. Send the new ZIP to the Backend team
3. Backend replaces the files in /backend/data/ml_analytics/
4. Backend reloads (or restarts)
5. Frontend shows new data
No backend code changes required between refreshes.

Mode B — Live API (Future / Real-Time)
Use this mode when the ML service runs continuously alongside the
Backend.

Requirements
ELK stack running (elk_elk-net network)

ML service container running

Both services on the same Docker network (elk_elk-net)

Docker network
The ML service already declares elk_elk-net in its
docker-compose.yml. To attach the Backend:

yaml
# backend/docker-compose.yml

services:
  backend:
    build: .
    networks:
      - elk-net

networks:
  elk-net:
    external: true
    name: elk_elk-net
ML service endpoints
Method	Endpoint	Description
GET	/health	Liveness
GET	/ready	Readiness (model loaded)
GET	/model	Model metadata
GET	/analytics	All analytics layers (JSON)
GET	/session-replay	Sessions list
GET	/session-replay/{id}	Single session detail
POST	/process	Run pipeline on custom events
Example call from the Backend
python
import httpx

ML_SERVICE = "http://honeypot-ml-service:8000"

async def fetch_clusters():
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{ML_SERVICE}/analytics")
        r.raise_for_status()
        return r.json()["cluster_analytics"]
Same endpoints for the Frontend
The Backend still exposes the same routes to the Frontend:

text
GET /api/ml/clusters
GET /api/ml/temporal
GET /api/ml/session-replay
GET /api/ml/session-replay/{id}
Only the backend implementation changes: instead of reading a file, it
forwards the request to the ML service.

Switching Between Modes
text
        ┌─────────────────────────────────┐
        │   Frontend (unchanged)          │
        │   /api/ml/clusters              │
        │   /api/ml/session-replay        │
        └────────────────┬────────────────┘
                         │
        ┌────────────────▼────────────────┐
        │   Backend API (unchanged)       │
        └────────────────┬────────────────┘
                         │
        ┌────────────────┴────────────────┐
        │                                 │
   [Mode A]                          [Mode B]
   Read file                         HTTP call
   cluster_analytics.json            /analytics
        │                                 │
        ▼                                 ▼
   /backend/data/                    honeypot-ml-service:8000
Only the "how to get data" step changes. Everything downstream is
identical.

Endpoint Mapping — Frontend Perspective
Frontend call	Backend reads (Mode A)	Backend calls (Mode B)
/api/ml/clusters	cluster_analytics.json	GET /analytics → cluster_analytics
/api/ml/temporal	temporal_analytics.json	GET /analytics → temporal_analytics
/api/ml/sessions/summary	session_analytics.json	GET /analytics → session_analytics
/api/ml/mitre	mitre_analytics.json	GET /analytics → mitre_analytics
/api/ml/mitre/statistics	mitre_statistics.json	(in /analytics)
/api/ml/mitre/trends	mitre_trends.json	(in /analytics)
/api/ml/session-replay	session_replay_list.json	GET /session-replay
/api/ml/session-replay/{id}	session_replay_details/{id}.json	GET /session-replay/{id}
Which Mode to Use?
Factor	Mode A (Files)	Mode B (Live API)
Setup complexity	Low	Medium
Real-time data	No	Yes
Requires ML container	No	Yes
Backend code changes	None after setup	None after setup
Frontend changes	None	None
Delivery	ZIP	Docker network
Best for	Initial handoff	Production deployment
Recommendation:

Start with Mode A. When the team is ready for continuous operation,
switch to Mode B. The frontend contract does not change.

Delivery Checklist — Mode A
Send ml_analytics_files.zip to the Backend team.

Backend extracts to /backend/data/ml_analytics/.

Backend loads at startup.

Backend exposes /api/ml/* routes.

Frontend consumes the routes.

Deployment Checklist — Mode B
Confirm elk_elk-net network exists.

Deploy ML service:

text
docker compose -f ML_SERVICE/docker-compose.yml up -d
Verify:

text
curl http://honeypot-ml-service:8000/ready
Attach Backend to elk_elk-net.

Backend uses http://honeypot-ml-service:8000/....

Frontend consumes the same /api/ml/* routes.

Notes
JSON structures are identical between the two modes.

Switch at any time without changing the Backend or Frontend contracts.

All ML analytics are read-only. The Backend never modifies them.

The ML service is stateless from the Backend's point of view.

Related Documents
docs/PIPELINE_FLOW.md — Data pipeline reference

docs/RUNTIME_GUIDE.md — Run scripts and workflows

docs/ARCHITECTURE.md — Design rules

backend_handoff/*/README.md — Per-analytics field references
