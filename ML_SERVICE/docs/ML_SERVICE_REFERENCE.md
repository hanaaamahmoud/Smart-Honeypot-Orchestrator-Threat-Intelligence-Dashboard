# ML Service — Complete Reference Guide

> This document explains the ML Service architecture, pipeline, 
> file structure, and analytics layer. It works with any dataset 
> (not specific to any single run).

---

# PART A — ARCHITECTURE

## A.1 High-Level View
┌───────────────────────────────────────────────────────────┐
│ Data Source │
│ (Honeypots → Logstash → Elasticsearch, OR CSV Bulk) │
└───────────────────────────────────────────────────────────┘
↓
┌───────────────────────────────────────────────────────────┐
│ Elasticsearch │
│ Index: <your-index> │
│ Documents: N (any number) │
└───────────────────────────────────────────────────────────┘
↓ Docker Network: elk_elk-net
┌───────────────────────────────────────────────────────────┐
│ ML Service Container (honeypot-ml-service) │
│ │
│ 1. Reader → 2. Adapter → 3. Normalization │
│ 4. Sessions → 5. Features → 6. Validation │
│ 7. Scaler → 8. Centroid → 9. ML Output │
│ 10. Analytics │
└───────────────────────────────────────────────────────────┘
↓
┌───────────────────────────────────────────────────────────┐
│ Backend + Dashboard │
└───────────────────────────────────────────────────────────┘

text

---

## A.2 How ML Talks to Elasticsearch

### Connection
- **URL:** `http://elasticsearch:9200` (Docker DNS)
- **Not:** `http://localhost:9200` (won't work inside container)
- **Index:** configurable via `ELASTICSEARCH_INDEX` env var
- **Client:** `elasticsearch-py` v8.x

### Why Docker DNS?
ML Container and ES Container are on the same Docker network
`elk_elk-net`. Docker resolves `elasticsearch` → container IP automatically.

### Read-Only Principle
The ML Service **never writes** to Elasticsearch.
No `index`, `update`, `delete`, or `bulk` operations.

---

# PART B — FILE-BY-FILE GUIDE

Each stage below shows:
- **File** — where the code lives
- **Class/Function** — what to call
- **Input** — what it expects
- **Output** — what it returns
- **Why** — its role in the pipeline

---

## B.1 — Elasticsearch Reader

**File:** `app/ingestion/elasticsearch.py`  
**Class:** `ElasticsearchReader`

**Purpose:**  
Read-only reader for raw events from Elasticsearch.

**Constructor:**
```python
reader = ElasticsearchReader(
    url="http://elasticsearch:9200",
    index="<your-index>",
    timeout=10,
)
Methods:

Method	Input	Output
health()	—	dict (cluster info)
count()	—	int (documents in index)
read_events(size=100)	size: int	list[dict]
read_events_in_batches(batch_size=500)	batch_size: int	Iterator[list[dict]]
Output example:

python
{
    "timestamp": "2025-01-01T00:00:00Z",
    "honeypot": "cowrie",
    "protocol": "SSH",
    "source_ip": "1.2.3.4",
    ...
}
Rules:

✅ Read-only

❌ No ML logic inside

❌ No hardcoded URL (use settings)

B.2 — Input Adapter
File: app/pipeline/input_adapter.py
Function: adapt_input()

Purpose:
Boundary between external input and internal pipeline.

Signature:

python
def adapt_input(payload: dict) -> list[dict]:
    ...
Input:

python
{"events": [event1, event2, ...]}
Output:

python
[normalized_event1, normalized_event2, ...]
Why it exists:
The pipeline always expects {"events": [...]} shape,
regardless of source. This adapter enforces the boundary.

Rules:

✅ Wraps payload

❌ No feature generation

B.3 — Normalization
File: app/pipeline/normalization.py
Function: normalize_events()

Purpose:
Convert raw events (any format) into Canonical Events.

Input: raw events (list[dict])
Output: canonical events with fixed field names

Canonical fields (17):

text
event_id, timestamp, session_id, source_ip, destination,
destination_port, protocol, username, country, country_code,
city, latitude, longitude, honeypot, event_type, command, raw
Why:
The rest of the pipeline should not care whether the event
came from Cowrie, Tanner, Dionaea, or a CSV file.

Rules:

✅ Deterministic mapping

✅ Preserve raw event under raw key

❌ No data fabrication (nulls stay null)

B.4 — Session Reconstruction
File: app/pipeline/session_reconstruction.py
Function: reconstruct_sessions()

Purpose:
Group individual events into logical sessions by session_id.

Input: canonical events
Output: list of session objects

Session schema:

python
{
    "session_id": "abc123",
    "events": [event1, event2, ...],
    "event_count": 5,
    "start_time": "2025-01-01T00:00:00Z",
    "end_time": "2025-01-01T00:05:00Z",
    "duration_seconds": 300,
}
Helper modules:

File	Role
session_grouping.py	Group by session_id
session_boundaries.py	Compute start/end/duration
session_ordering.py	Sort events chronologically
session_contract.py	Session schema definition
session_id_policy.py	How to handle missing session_id
Rules:

✅ Events without session_id are NOT assigned a fake one

❌ No session fabrication

B.5 — Feature Generation (48 features)
File: app/pipeline/feature_generation.py
Function: assemble_48_features()

Purpose:
Convert each session into a 48-dimensional feature vector
that matches the frozen production model contract.

Feature groups:

File	Feature Group
feature_generation_base.py	Event counts, durations
feature_generation_diversity.py	Unique values (IPs, protocols, ...)
feature_generation_temporal.py	Hour, day, gaps
feature_generation_density.py	Rates and densities
feature_generation_geo.py	Geo availability flags
Combined call:

python
fg = {}
fg.update(generate_base_features(session))
fg.update(generate_diversity_features(session))
fg.update(generate_temporal_features(session))
fg.update(generate_density_features(session))
fg.update(generate_geo_availability_features(session))

features = assemble_48_features(fg)
# → dict with exactly 48 keys
Rules:

✅ Exactly 48 features

✅ Exact names and order (see feature_contract.py)

❌ No extra or missing features

B.6 — Feature Validation
File: app/pipeline/feature_validation.py
Functions: validate_48_features(), validate_48_feature_vector()

Purpose:
Safety gate before ML. Reject invalid feature vectors.

Rejects:

Wrong count (47, 49, ...)

Wrong names

Wrong order

Missing / unexpected features

NaN / Inf

Non-numeric values

Boolean values

Accepts:

Exactly 48 features

Numeric + finite

Rule:
The pipeline should never reach the scaler with invalid features.

B.7 — Frozen Scaler
File: app/model_loader.py
Method: FrozenModel.scale_features()

Purpose:
Apply the frozen StandardScaler (trained offline) to the 48 features.

Input: feature dict (48 values)
Output: scaled feature array

Artifact:

text
models/frozen_production_reference/standard_scaler_params.json
Rules:

✅ transform() only

❌ Never fit() on new data

❌ Never retrain

B.8 — Frozen Centroid Assignment
File: app/pipeline/frozen_assignment.py + app/model_loader.py
Method: FrozenModel.nearest_centroid()

Purpose:
Assign each session to the closest frozen behavioral cluster.

Input: scaled features
Output: (cluster_id, distance)

Artifact:

text
models/frozen_production_reference/step7g_dbscan_behavioral_reference_centroids.csv
38 behavioral clusters (IDs 0-37)

1 noise cluster (ID -1)

Assignment:

text
nearest_behavioral_centroid
Rules:

✅ Nearest centroid only

❌ No DBSCAN fitting

❌ No new clusters

❌ No cluster reassignment

B.9 — Canonical ML Output
File: app/output_adapter.py
Function: adapt_session_result()

Purpose:
Format the internal ML result into a stable, Backend-friendly contract.

Input:

python
{
    "reconstructed_session_id": "...",
    "production_cluster_assignment": int,
    "assignment_status": "EXISTING_PRODUCTION_CLUSTER",
    "feature_validation_status": "VALIDATED_48_FEATURES",
    "event_count": int,
    "session_start": str,
    "session_end": str,
    "source": str | None,
    "protocol": str | None,
    "honeypot": str | None,
}
Output:

python
{
    "session_id": "...",
    "cluster_id": int,
    "assignment_status": "EXISTING_PRODUCTION_CLUSTER",
    "validation_status": "VALIDATED_48_FEATURES",
    "event_count": int,
    "protocol": str | None,
    "honeypot": str | None,
}
Why:
The Backend should never see scaler, centroids, or 48 features.
Only this canonical contract.

PART C — ANALYTICS LAYER
After ML Output, the analytics layer produces Dashboard-ready data.

C.1 Analytics Modules
File	Purpose
app/analytics/session_analytics.py	Per-session statistics
app/analytics/session_boundary.py	Prepare session input
app/analytics/cluster_analytics.py	Per-cluster aggregation
app/analytics/attacker_ip_analytics.py	Per-attacker-IP analytics
app/analytics/attacker_ip_boundary.py	Prepare IP input
app/analytics/temporal_analytics.py	Time-based trends
app/analytics/analytics.py	Boundary / entry point
app/analytics/cluster_behavior_api.py	Cluster behavior labels
app/analytics/cluster_behavior_mapping.py	Cluster → behavior map
C.2 Analytics Contracts
Contract	File
Session Analytics	app/analytics/contracts/session_analytics_contract.json
Cluster Analytics	app/analytics/contracts/cluster_analytics_contract.json
Attacker IP Analytics	app/analytics/contracts/attacker_ip_analytics_contract.json
Temporal Analytics	app/analytics/contracts/temporal_analytics_contract.json
Analytics Availability	app/analytics/contracts/analytics_availability.json
C.3 How Analytics Connect to Pipeline
text
ML Output (Canonical)
        ↓
   ┌────┴────┬─────────┬──────────┐
   ↓         ↓         ↓          ↓
Session   Cluster   Attacker   Temporal
Analytics Analytics IP Analytics Analytics
   ↓         ↓         ↓          ↓
   └────┬────┴─────────┴──────────┘
        ↓
   Dashboard Ready
Key rule:
Analytics do NOT call the ML pipeline.
They consume the ML Output only.

C.4 Session Analytics Output
Input: list of canonical ML outputs
Output:

python
[
    {
        "reconstructed_session_id": "...",
        "production_cluster_assignment": "EXISTING_PRODUCTION_CLUSTER",
        "assignment_status": "...",
        "feature_validation_status": "...",
        "event_count": int,
        "session_start": str | None,
        "session_end": str | None,
        "source": str | None,
    },
    ...
]
C.5 Cluster Analytics Output
Input: list of canonical ML outputs
Output:

python
{
    "analytics_layer": "CLUSTER_ANALYTICS",
    "cluster_count": 38,
    "session_count": N,
    "noise_session_count": M,
    "clusters": [
        {
            "cluster_id": 0,
            "session_count": int,
            "percentage": float,
            "cluster_type": "...",
            "attacker_behavior": "...",
            ...
        },
        ...
    ]
}
C.6 Attacker IP Analytics Output
Input: list of canonical ML outputs
Output: dict keyed by source_ip with per-IP metrics.

C.7 Temporal Analytics Output
Input: list of canonical ML outputs
Output: time-bucketed aggregations (hourly / daily).

PART D — CONFIGURATION
D.1 Environment Variables
text
ML_SERVICE_NAME          = honeypot-ml-service
ML_SERVICE_HOST          = 0.0.0.0
ML_SERVICE_PORT          = 8000
ELASTICSEARCH_URL        = http://elasticsearch:9200
ELASTICSEARCH_INDEX      = <your-index>
BACKEND_URL              = http://backend:8001
ML_PRODUCTION_MODE       = FROZEN_PRODUCTION_REFERENCE
D.2 Docker Network
Network: elk_elk-net

Containers on it: honeypot-ml-service, elasticsearch

D.3 Volume Mounts
Host → Container:

text
ML_SERVICE/app        → /app/app
ML_SERVICE/models     → /app/models
ML_SERVICE/tests      → /app/tests
ML_SERVICE/analytics  → /app/analytics
ML_SERVICE/pytest.ini → /app/pytest.ini
Changes on Host appear instantly in Container (and vice versa).

PART E — HOW TO RUN
E.1 Enter the Container
bash
docker exec -it honeypot-ml-service bash
E.2 Quick ES Check
bash
python -c "
import urllib.request
print(urllib.request.urlopen('http://elasticsearch:9200/<your-index>/_count').read().decode())
"
E.3 Run the Full Pipeline
python
from app.ingestion.elasticsearch import ElasticsearchReader
from app.pipeline.input_adapter import adapt_input
from app.pipeline.session_reconstruction import reconstruct_sessions
from app.pipeline.feature_generation import assemble_48_features
from app.pipeline.feature_generation_base import generate_base_features
from app.pipeline.feature_generation_diversity import generate_diversity_features
from app.pipeline.feature_generation_temporal import generate_temporal_features
from app.pipeline.feature_generation_density import generate_density_features
from app.pipeline.feature_generation_geo import generate_geo_availability_features
from app.model_loader import load_frozen_model
from app.output_adapter import adapt_session_result

# 1. Read
reader = ElasticsearchReader("http://elasticsearch:9200", "<your-index>")
events = reader.read_events(size=1000)  # or reader.count()

# 2. Adapter + Normalization
normalized = adapt_input({"events": events})

# 3. Sessions
sessions = reconstruct_sessions(normalized)

# 4. Feature + Scale + Assign
model = load_frozen_model()
results = []
for session in sessions:
    fg = {}
    fg.update(generate_base_features(session))
    fg.update(generate_diversity_features(session))
    fg.update(generate_temporal_features(session))
    fg.update(generate_density_features(session))
    fg.update(generate_geo_availability_features(session))
    features = assemble_48_features(fg)

    scaled = model.scale_features(features)
    cluster_id, distance = model.nearest_centroid(scaled)

    results.append(adapt_session_result({
        "reconstructed_session_id": session["session_id"],
        "production_cluster_assignment": cluster_id,
        "assignment_status": "EXISTING_PRODUCTION_CLUSTER",
        "feature_validation_status": "VALIDATED_48_FEATURES",
        "event_count": len(session["events"]),
        "session_start": session.get("start_time"),
        "session_end": session.get("end_time"),
    }))
PART F — API ENDPOINTS
Method	Endpoint	Purpose
GET	/health	Service status
GET	/ready	Model readiness
GET	/model	Model metadata
POST	/process	Run full pipeline
GET	/analytics	Current analytics state
PART G — TROUBLESHOOTING
Error	Cause	Fix
NameResolutionError	ML not on elk_elk-net	Check docker-compose.yml networks
media_type_header_exception	elasticsearch-py v9	Use v8 (>=8.0.0,<9.0.0)
index_not_found_exception	Wrong index name	Check ELASTICSEARCH_INDEX
date_time_parse_exception	Bad timestamp format	Must be ISO 8601 (T separator)
Empty events	ES empty or bad query	Check reader.count()
PART H — RULES (ALWAYS ENFORCED)
Allowed
✅ Read from Elasticsearch

✅ Transform using frozen scaler/centroids

✅ Assign to existing clusters

✅ Consume ML output in analytics

Forbidden
❌ Write / update / delete in ES

❌ Fit scaler on new data

❌ Retrain DBSCAN

❌ Create new clusters

❌ Reassign clusters

❌ Use localhost:9200 inside container

❌ Use elasticsearch-py v9

Document Version: 1.0.0
Last Updated: 2026-10-01
