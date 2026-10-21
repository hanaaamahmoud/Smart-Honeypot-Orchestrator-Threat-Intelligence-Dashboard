# Architecture — Design Decisions & Rules

This document captures the design principles, integration models, and
golden rules that govern the ML service.

It is the reference for any change to the service, and the starting
point for onboarding new team members.

---

## 1. System Position

The ML service sits between Elasticsearch and the Backend:
Elasticsearch → ML Service → Backend → Frontend
(events) (analytics) (API) (dashboard)

text

It is one of several services. It is not responsible for:

- Ingesting events (that is the ELK stack)
- Serving the dashboard (that is the Backend + Frontend)
- Managing honeypots (that is the Orchestrator)

---

## 2. Design Principles

### 2.1 Read-Only Access to Elasticsearch

The ML service never writes to Elasticsearch. It reads events and
processes them in memory.

**Why:** Isolation. The ML service cannot corrupt the source of truth.

### 2.2 Frozen Model, No Retraining

The production model (DBSCAN + scaler + centroids) is frozen. The ML
service only:

- Scales features using the frozen scaler
- Finds the nearest frozen centroid
- Assigns existing cluster IDs

**Why:** Reproducibility. Every run produces the same result for the
same input.

### 2.3 No Fabrication

Missing fields remain missing. No default values, no inference, no
guessing.

**Why:** Trust. A dashboard that shows fabricated values is worse than
one that shows empty sections.

### 2.4 Source-Agnostic Pipeline

The pipeline accepts any input that matches the canonical event shape.
It is not tied to any specific honeypot.

**Why:** Portability. New honeypots can be added without touching the
ML service.

### 2.5 Independent Analytics Layers

Each analytics layer is independent. It consumes the ML output and
produces its own JSON. It does not depend on other analytics layers.

**Why:** Modularity. Any layer can be modified, removed, or added
without affecting the others.

---

## 3. Integration Models

Two integration models exist between the ML service and the Backend.
Both produce the same data shapes.

### 3.1 Model A — File-Based (Recommended)
ML Service → analytics_output/.json → package_handoff.sh → ZIP
↓
Backend reads files
↓
Backend exposes /api/ml/
↓
Frontend consumes

text

**Pros:**

- No Docker network dependency
- No ML service running requirement
- Simple, deterministic, easy to debug
- Ideal for handoff and offline analysis
- Works for any deployment topology

**Cons:**

- Data is not "live"; requires regeneration on new data
- Manual refresh step

**Best for:** This project's current phase, academic handoff,
offline analytics, reproducible reporting.

### 3.2 Model B — Live API (Pull)
Backend → HTTP GET → ML Service → JSON → Backend → Frontend

text

Endpoints:

- `GET /health`
- `GET /ready`
- `GET /model`
- `GET /analytics`
- `GET /session-replay`
- `GET /session-replay/{id}`
- `POST /process`

**Pros:**

- Always up to date
- No manual refresh
- Standard microservice architecture

**Cons:**

- Both services must share a Docker network (`elk_elk-net`)
- ML service must run continuously
- Slightly more complex to deploy

**Best for:** Production deployments with continuous ingestion.

### 3.3 Model C — Live Push (Not Implemented)

A hypothetical model where the ML service pushes results to the
Backend:
ML Service → HTTP POST → Backend /ml/events
↓
Backend stores in DB
↓
Frontend consumes

text

**Why it is not implemented:**

- Requires an agreed endpoint on the Backend
- Requires retry, idempotency, and failure handling on both sides
- Not required for the current use case (files + pull already work)
- Adds coupling with no clear benefit for this project

**Reserved for future:**

If the project needs real-time event-driven updates later, this model
can be added. The contract would be:

- `POST /ml/events` on the Backend
- Body: array of ML results (same shape as `00_ml_output_full.json`)
- Backend stores the results

No changes to the Frontend are required; only the delivery mechanism
changes.

---

## 4. Recommendation Matrix

| Requirement | Model A (Files) | Model B (Pull API) | Model C (Push) |
|---|---|---|---|
| Easy handoff | ✅✅✅ | ✅ | ⚠️ |
| No network setup | ✅✅✅ | ❌ | ❌ |
| Real-time data | ❌ | ✅✅✅ | ✅✅✅ |
| Reproducible offline | ✅✅✅ | ❌ | ❌ |
| Frontend unchanged | ✅ | ✅ | ✅ |
| Backend code unchanged | ✅ | ✅ | ❌ |
| No ML running required | ✅ | ❌ | ❌ |
| Tested & documented | ✅ | ✅ | ❌ |

**Recommendation for this project:**

Use **Model A** as the primary delivery mechanism. Keep **Model B**
available as a production deployment option. Reserve **Model C** for
future work only if real-time push becomes a hard requirement.

---

## 5. Data Flow Contract

Regardless of integration model, the following contract holds:

### 5.1 Input

Events must have at minimum:
timestamp, honeypot, protocol, source_ip, session_id

text

Optional fields (recommended for richer analytics):
country, country_code, asn, attack_type, mitre_technique,
attack_stage, severity, ...

text

Missing optional fields are preserved as `null` and never fabricated.

### 5.2 Output

Each analytics layer outputs a JSON object with:

- `contract_name` — stable identifier
- `contract_version` — semver
- `generated_at` — ISO-8601 timestamp
- `analytics_layer` — layer identifier
- `summary` — layer-specific summary object
- Layer-specific data array

The full field reference lives in `backend_handoff/*/README.md`.

### 5.3 Stability

Contract versions follow semantic versioning:

- **Patch** — documentation only
- **Minor** — new optional fields, additive
- **Major** — breaking change (rare)

---

## 6. Golden Rules

These rules apply to all changes.

### 6.1 Never Modify

- The frozen model (`models/frozen_production_reference/`)
- The scaler parameters (`standard_scaler_params.json`)
- The 48-feature order (`FROZEN_FEATURE_ORDER`)
- The canonical event schema (24 fields)
- The ML result contract

### 6.2 Never Allow

- Retraining
- DBSCAN fitting at runtime
- New cluster creation
- Cluster reassignment
- Fabrication of any kind (missing values stay missing)
- Write access to Elasticsearch

### 6.3 Always

- Backup before modifying pipeline files
- Run tests after every change
- Document contract changes
- Preserve backward compatibility when possible
- Keep data files out of Git

---

## 7. Folder Layout
ML_SERVICE/
├── app/ ← source code
│ ├── analytics/ ← 8 analytics layers + contracts
│ ├── pipeline/ ← ML pipeline stages
│ ├── ingestion/ ← Elasticsearch reader
│ ├── model_loader.py ← frozen model loader
│ ├── output_adapter.py ← canonical ML result
│ └── main.py ← FastAPI service
│
├── models/ ← frozen production artifacts (read-only)
│ └── frozen_production_reference/
│
├── tests/ ← unit + contract tests
│
├── docs/ ← this documentation
│
├── analytics_output/ ← generated files (gitignored)
│
├── backend_handoff/ ← package for backend (gitignored)
│
├── run_ml_pipeline.sh ← run the pipeline end-to-end
├── package_handoff.sh ← package results into a ZIP
├── Dockerfile
├── docker-compose.yml
└── README.md

text

---

## 8. Extension Points

The service is designed to be extended without breaking existing
functionality.

### 8.1 Adding a New Analytics Layer

1. Create `app/analytics/my_analytics.py`
2. Create `app/analytics/contracts/my_analytics_contract.json`
3. Create `tests/unit/test_my_analytics.py`
4. Create `tests/contract/test_my_analytics_contract.py`
5. Register in `app/main.py` (`/analytics` response and `/process`)
6. Document in `backend_handoff/08_my_analytics/`

The other layers remain unchanged.

### 8.2 Switching Integration Model

- Model A → Model B: no frontend change; only backend change
- Model B → Model A: same; revert to file-based reads
- Model A/B → Model C: add backend endpoint + ML client

### 8.3 Adding a New Data Source

If a new Elasticsearch index appears:

1. Add a `source` field to canonical events
2. Reader stays unchanged (still read-only)
3. No pipeline change required

If a new event format appears:

1. Add handling in `canonical_adapter.py`
2. Preserve unknown fields under `raw`
3. Tests ensure no regression

---

## 9. Failure Modes & Recovery

| Failure | Detection | Recovery |
|---|---|---|
| Elasticsearch unreachable | Reader raises | Check `docker ps`, network |
| Index empty | `count() == 0` | Confirm ingest, check index name |
| Feature validation failed | Exception raised | Inspect feature vector, restore backup |
| Model not loaded | Startup error | Check `models/` mounted |
| Contract mismatch | Tests fail | Restore contract, re-run pipeline |
| Stale JSON files | `generated_at` old | Re-run `run_ml_pipeline.sh` |

The ML service never silently falls back to defaults. All failures are
explicit.

---

## 10. What This Document Does Not Cover

- Detailed API shapes — see `docs/INTEGRATION_GUIDE.md`
- Pipeline steps — see `docs/PIPELINE_FLOW.md`
- Run instructions — see `docs/RUNTIME_GUIDE.md`
- Per-analytics field references — see `backend_handoff/*/README.md`

---

## 11. Change Log

| Date | Change |
|---|---|
| 2026-10-02 | Initial architecture document |

Future changes to architecture must be recorded here.
