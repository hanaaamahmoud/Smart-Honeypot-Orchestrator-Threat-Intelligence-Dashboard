# Pipeline Flow — Complete Reference

This document describes every stage of the ML pipeline, from raw
Elasticsearch events to the Backend handoff files consumed by the
dashboard.

It is the single source of truth for how data flows through the
service.

---

## End-to-End Overview
┌─────────────────────────────────────────────────────────────────┐
│ 1. Elasticsearch (honeypot-events index) │
│ 58,895 events · 26 fields per event │
│ ↓ │
│ 2. ElasticsearchReader (read-only) │
│ ↓ │
│ 3. Input Adapter (boundary) │
│ ↓ │
│ 4. Canonical Adapter (24-field contract) │
│ ↓ │
│ 5. Normalization │
│ ↓ │
│ 6. Session Reconstruction (group by session_id) │
│ ↓ │
│ 7. Feature Generation (48 features per session) │
│ ↓ │
│ 8. Feature Validation (order, count, types) │
│ ↓ │
│ 9. Frozen Scaler (transform only — no fit) │
│ ↓ │
│ 10. Frozen Centroid Assignment (nearest centroid) │
│ ↓ │
│ 11. Analytics Layers (8 independent layers) │
│ ↓ │
│ 12. Backend Handoff (JSON files) │
└─────────────────────────────────────────────────────────────────┘

text

---

## STEP 1 — Elasticsearch Source

**Location:** External (ELK stack)

- **Index:** `honeypot-events`
- **Fields:** 26 per event
- **Network:** `elk_elk-net`
- **URL inside container:** `http://elasticsearch:9200`

Example event:

```json
{
  "timestamp": "2020-01-22T04:56:10.963441+00:00",
  "honeypot": "tanner",
  "protocol": "HTTP",
  "source_ip": "45.243.162.246",
  "source_port": 33815,
  "destination_ip": null,
  "destination_port": 80,
  "session_id": "ade88c93-30a2-4cd0-902c-9b7f99df6579",
  "username": null,
  "password": null,
  "user_attempt": 0,
  "pass_attempt": 0,
  "auth_attempt": 0,
  "anonymous": 0,
  "command_count": 0,
  "country": "Egypt",
  "country_code": "EG",
  "asn": 24863,
  "ip_reputation": "0",
  "attack_type": "HTTP Exploitation",
  "mitre_technique": "T1190",
  "attack_stage": "Initial Access",
  "severity": "Medium",
  "source_dataset": "tanner_http_labeled",
  "ip_reputation_score": 0.0,
  "ip_reputation_level": "clean"
}
STEP 2 — Elasticsearch Reader
File: app/ingestion/elasticsearch.py
Class: ElasticsearchReader

Responsibilities:

Connect to Elasticsearch using configured URL

Verify availability

Read events in controlled batches

Return only _source documents

Never writes, updates, or deletes

Rules:

Read-only by design

No ML logic

No normalization

Uses elasticsearch:9200 (not localhost)

Usage:

python
from app.ingestion.elasticsearch import ElasticsearchReader
from app.config import Settings

reader = ElasticsearchReader(
    Settings.ELASTICSEARCH_URL,
    Settings.ELASTICSEARCH_INDEX,
)

# Small read
events = reader.read_events(size=100)

# Full read (batched)
for batch in reader.read_events_in_batches(batch_size=5000):
    process(batch)
STEP 3 — Input Adapter
File: app/pipeline/input_adapter.py
Function: adapt_input(payload)

Purpose: Boundary between external payloads and the pipeline.

python
from app.pipeline.input_adapter import adapt_input

normalized = adapt_input({"events": events})
# Returns: list[dict]
No ML, no features, no clustering.

STEP 4 — Canonical Adapter
File: app/pipeline/canonical_adapter.py
Function: canonicalize_event(event)

Purpose: Map the raw event into the stable 24-field CanonicalEvent contract.

Canonical fields:

text
timestamp            honeypot            protocol
source_ip            source_port         destination_ip
destination_port     session_id          username
password             user_attempt        pass_attempt
auth_attempt         anonymous           command_count
country              country_code        asn
ip_reputation        attack_type         mitre_technique
attack_stage         severity            source_dataset
Missing optional fields are preserved as None. Nothing is fabricated.

The full raw event is preserved under event["raw"].

STEP 5 — Normalization
File: app/pipeline/normalization.py
Function: normalize_events(events)

Purpose: Convert each canonical event into a stable internal dict
used by the rest of the pipeline.

Resulting event shape (sample):

python
{
    "event_id": None,
    "timestamp": "2020-01-22T04:56:10.963441+00:00",
    "session_id": "ade88c93-...",
    "source_ip": "45.243.162.246",
    "destination": None,
    "destination_port": 80.0,
    "protocol": "HTTP",
    "username": None,
    "country": "Egypt",
    "country_code": "EG",
    "city": None,
    "latitude": None,
    "longitude": None,
    "honeypot": "tanner",
    "event_type": None,
    "command": None,
    "auth_attempt": 0.0,
    "user_attempt": 0.0,
    "pass_attempt": 0.0,
    "anonymous": 0.0,
    "command_count": 0.0,
    "source_port": 33815.0,
    "password": None,
    "raw": { ... full original event ... },
}
Events that are not dictionaries raise EventNormalizationError.

STEP 6 — Session Reconstruction
File: app/pipeline/session_reconstruction.py
Function: reconstruct_sessions(events)

Purpose: Group normalized events by session_id, sort each session
chronologically, and compute boundaries.

Output (per session):

python
{
    "session_id": "ade88c93-30a2-4cd0-902c-9b7f99df6579",
    "events": [ ... events ordered by timestamp ... ],
    "start_time": "2020-01-22T04:56:10.963441+00:00",
    "end_time":   "2020-01-23T02:27:45.625127+00:00",
    "duration_seconds": 77494.66,
}
Event conservation rule:

text
sum(len(session["events"]) for session in sessions) == len(input_events)
Events without a session_id are not assigned a fabricated ID.

STEP 7 — Feature Generation (48 Features)
Files:

text
app/pipeline/feature_generation_base.py        (7 features)
app/pipeline/feature_generation_diversity.py   (16 features)
app/pipeline/feature_generation_temporal.py    (10 features)
app/pipeline/feature_generation_density.py     (8 features)
app/pipeline/feature_generation_geo.py         (7 features)
app/pipeline/feature_generation.py             (assembly + validation)
The 48 features (exact order):

text
Base (7)
  event_count
  session_duration_seconds
  auth_attempt_total
  user_attempt_total
  pass_attempt_total
  command_count_total
  anonymous_event_count

Diversity (16)
  unique_destinations
  unique_destination_ports
  unique_source_ips
  unique_protocols
  unique_honeypots
  unique_usernames
  unique_countries
  unique_country_codes
  unique_cities
  destination_diversity
  destination_port_diversity
  protocol_diversity
  honeypot_diversity
  username_diversity
  geo_country_diversity
  geo_city_diversity

Temporal (10)
  inter_event_gap_mean
  inter_event_gap_min
  inter_event_gap_max
  session_duration_recomputed_seconds
  events_per_second
  auth_attempt_rate
  command_rate
  session_start_hour
  session_start_dayofweek
  session_start_dayofmonth

Density (8)
  session_duration_log1p
  event_count_log1p
  inter_event_gap_mean_log1p
  inter_event_gap_max_log1p
  event_density
  command_density
  auth_attempt_density
  credential_attempt_density

Geo (7)
  latitude_mean
  longitude_mean
  geo_latitude_abs
  geo_longitude_abs
  geo_location_available
  ip_reputation_available
  ip_reputation_missing_count
The order is frozen — it must match the training pipeline exactly.

STEP 8 — Feature Validation
File: app/pipeline/feature_validation.py
Function: validate_48_features(vector, order)

Checks:

Exactly 48 features

Names match the frozen order

All values are numeric and finite

No missing entries

If any check fails, an exception is raised before the model is called.

STEP 9 — Frozen Scaler
File: app/model_loader.py
Method: model.scale_features(vector)

Loads standard_scaler_params.json (frozen)

Applies transform() only

Never calls fit()

Never retrains

Output: 48 scaled values (same order).

STEP 10 — Frozen Centroid Assignment
File: app/model_loader.py
Method: model.nearest_centroid(scaled_features)

Logic:

Loads 38 behavioral centroids (frozen)

Finds nearest centroid using Euclidean distance

Returns (cluster_id, distance)

Rules:

No DBSCAN fitting

No new clusters

No reassignment

No retraining

STEP 11 — Analytics Layers (8 Layers)
Files:

text
app/analytics/cluster_analytics.py
app/analytics/temporal_analytics.py
app/analytics/session_analytics.py
app/analytics/mitre_analytics.py
app/analytics/mitre_statistics.py
app/analytics/mitre_trends.py
app/analytics/session_replay.py
app/analytics/attacker_ip_analytics.py    (deferred)
Each analytics layer:

Consumes the ML output directly

Does not rerun ML processing

Produces a clearly-defined JSON output

Is independent of the other layers

Details for each layer are documented in its README.md under
backend_handoff/.

STEP 12 — Backend Handoff
Script: package_handoff.sh
Output: backend_handoff/ml_analytics_files.zip

Contains:

text
ml_analytics_files/
├── cluster_analytics.json
├── temporal_analytics.json
├── session_analytics.json
├── mitre_analytics.json
├── mitre_statistics.json
├── mitre_trends.json
├── session_replay_list.json
├── session_replay_details/
└── README.md
The Backend team reads these files directly — no live ML calls needed.

Data Invariants
The pipeline guarantees the following:

Invariant	Enforced by
Event count preserved through sessions	session_reconstruction
48 features, exact order	feature_generation + feature_validation
No fabricated values	Every stage
No model retraining	model_loader
No new clusters	model_loader
Same scaler as training	standard_scaler_params.json
Where to Look Next
Run instructions: docs/RUNTIME_GUIDE.md

Environment wiring: docs/INTEGRATION_GUIDE.md

Design rules: docs/ARCHITECTURE.md
