# Runtime Guide — Running the Pipeline

This document explains how to run the ML pipeline end-to-end and how
to package the results for the Backend team.

It covers both the automated scripts and the manual steps, so anyone
can run the service without prior context.

---

## Overview

The ML Service exposes two runtime entry points:

| Script | Purpose |
|---|---|
| `run_ml_pipeline.sh` | Run the full pipeline and produce all analytics files |
| `package_handoff.sh` | Package results into a ZIP for the Backend team |

Both scripts run **inside the container** by default, but work equally
well on a host machine with the Python environment configured.

---

## Prerequisites

Before running:

1. **Elasticsearch is reachable** at `http://elasticsearch:9200`
2. **Index `honeypot-events` exists** and contains events
3. **The container is running** (`docker ps | grep honeypot-ml-service`)
4. **The Docker network `elk_elk-net` is up**

Quick sanity check:

```bash
docker exec honeypot-ml-service python -c "
from app.ingestion.elasticsearch import ElasticsearchReader
from app.config import Settings
r = ElasticsearchReader(Settings.ELASTICSEARCH_URL, Settings.ELASTICSEARCH_INDEX)
print('index:', r.index)
print('count:', r.count())
"
Expected:

text
index: honeypot-events
count: <N>
Script 1 — run_ml_pipeline.sh
What it does
Connects to Elasticsearch

Reads all events

Reconstructs sessions

Generates 48 features per session

Assigns each session to a production cluster (frozen model)

Writes the ML output to analytics_output/00_ml_output_full.json

When to use it
After Elasticsearch has new events

After any change to the pipeline code

As part of the scheduled regeneration

How to run
Inside the container:

bash
docker exec -it honeypot-ml-service bash
cd /app
bash run_ml_pipeline.sh
On the host (with venv activated):

bash
cd ML_SERVICE
source .venv/bin/activate
bash run_ml_pipeline.sh
Output
text
analytics_output/
├── 00_ml_output_full.json          ← all sessions + cluster assignments
└── 00_ml_output_full.csv           ← same data in CSV
Expected log lines
text
[1/6] Reading from Elasticsearch...
   Events: <N>
[2/6] Running pipeline + analytics...
   Events loaded: <N>
   Processed: <M> sessions
   Clusters: <K>
[3/6] Full pipeline done
✅ PIPELINE RUN COMPLETE
How long it takes
~1–2 minutes for ~59,000 events on a standard machine.

Script 2 — package_handoff.sh
What it does
Reads all analytics files from analytics_output/

Copies them into backend_handoff/ml_analytics_files/

Renames them to stable filenames (no version prefixes)

Creates ml_analytics_files.zip

When to use it
After run_ml_pipeline.sh finishes

Before delivering results to the Backend team

Whenever the pipeline output changes

How to run
Inside the container:

bash
docker exec -it honeypot-ml-service bash
cd /app
bash package_handoff.sh
On the host:

bash
cd ML_SERVICE
bash package_handoff.sh
Output
text
backend_handoff/
└── ml_analytics_files/
    ├── cluster_analytics.json
    ├── temporal_analytics.json
    ├── session_analytics.json
    ├── mitre_analytics.json
    ├── mitre_statistics.json
    ├── mitre_trends.json
    ├── session_replay_list.json
    ├── session_replay_details/
    └── README.md

backend_handoff/ml_analytics_files.zip   ← ready to send
Expected log lines
text
📦 PACKAGING ML ANALYTICS HANDOFF
[1/4] Copying files...
   ✅ Files copied
[2/4] Creating ZIP...
   ✅ ZIP created
[3/4] Verifying...
[4/4] Summary
✅ HANDOFF PACKAGE READY
Full Workflow — New Data Arrives
This is the standard flow whenever Elasticsearch receives new events:

text
Step 1 — Ingest
    Elasticsearch already has the new events
        ↓
Step 2 — Run pipeline
    bash run_ml_pipeline.sh
        ↓
Step 3 — Package results
    bash package_handoff.sh
        ↓
Step 4 — Deliver
    Send backend_handoff/ml_analytics_files.zip
    to the Backend team
No rebuild is required. No restart is required for data-only updates.

Full Workflow — Code Changes
When the code changes (analytics logic, pipeline steps, API):

text
Step 1 — Edit code
    (files under app/)
        ↓
Step 2 — Restart container (to reload FastAPI)
    docker restart honeypot-ml-service
        ↓
Step 3 — Run pipeline
    bash run_ml_pipeline.sh
        ↓
Step 4 — Package
    bash package_handoff.sh
Only a restart is needed — no rebuild — because app/ is mounted.

When a rebuild is required
A rebuild is needed only when any of these change:

Dockerfile

requirements.txt

docker-compose.yml

In those cases:

bash
docker compose down
docker compose up -d --build
Delivering to the Backend Team
The Backend team receives:

Item	Description
ml_analytics_files.zip	All analytics JSON files
backend_handoff/README.md	Overview
docs/PIPELINE_FLOW.md	Data flow reference
docs/INTEGRATION_GUIDE.md	Wiring instructions
Delivery channels:

Shared drive

Git branch (data-only, not merged to main)

Direct transfer

Never commit the JSON files to Git — they are gitignored.

Verifying the Output
After running the pipeline, verify the results:

bash
python3 -c "
import json
d = json.load(open('analytics_output/02_cluster_analytics_enriched.json'))
print('Total clusters:', d['summary']['total_clusters'])
print('Total sessions:', d['summary']['total_sessions'])
print('Noise sessions:', d['summary']['noise_session_count'])
"
Expected (with the current production dataset):

text
Total clusters: 29
Total sessions: 11879
Noise sessions: 0
Common Failures
Symptom	Cause	Fix
Elasticsearch is unavailable	Wrong URL, container down	Check docker ps and ES health
count = 0	Index empty	Confirm data was ingested
KeyError: 'clusters'	Old file format	Re-run run_ml_pipeline.sh
Container not visible	Name mismatch	docker ps -a
session_mitre_relationships missing	Old pipeline run	Re-run pipeline
Automation Notes
The two scripts are idempotent:

Running run_ml_pipeline.sh again overwrites the previous output.

Running package_handoff.sh again replaces the ZIP.

This makes them safe to use in cron jobs or CI pipelines.

Example cron entry to regenerate every night:

cron
0 2 * * * cd /app && bash run_ml_pipeline.sh && bash package_handoff.sh
What to Look at Next
Data flow details: docs/PIPELINE_FLOW.md

Environment wiring: docs/INTEGRATION_GUIDE.md

Design rules: docs/ARCHITECTURE.md
