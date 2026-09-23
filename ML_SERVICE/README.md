# Honeypot ML Service

Production ML service for behavioral analytics of honeypot sessions.

The service processes normalized honeypot events, reconstructs sessions, generates a fixed 48-feature behavioral representation, and assigns each session to an existing production behavioral cluster.

## Purpose

This service is the ML component of the honeypot analytics pipeline:

```text
Honeypots
    ->
Logstash / Elasticsearch
    ->
ML Service
    ->
Backend
    ->
Dashboard
```

The ML service is responsible for behavioral feature generation and production cluster assignment. It does not retrain the model during production inference.

## Production ML Contract

The production service uses a frozen ML reference:

- Model reference: Frozen DBSCAN production reference
- Feature count: 48
- Assignment method: `nearest_behavioral_centroid`
- Retraining: Disabled
- DBSCAN fitting in production: Disabled
- New cluster creation: Disabled
- Cluster reassignment: Disabled
- IP-only inference: Disabled

All production predictions are based on the existing frozen behavioral reference.

## Frozen Production Reference

The frozen production artifacts are stored under:

`models/frozen_production_reference/`

These artifacts are part of the production ML contract and must be treated as immutable.

The SHA256 manifest:

`models/frozen_reference_sha256.json`

is used to verify the integrity of the frozen reference artifacts.

## Project Status

The ML service has been validated with:

- 48-feature contract tests
- Frozen model integrity verification
- Session conservation checks
- Cluster assignment checks
- Strict JSON output validation
- Docker-based end-to-end tests
- Full regression test suite

The current production container exposes the ML service on port `8000`.

Real Elasticsearch integration is intentionally handled in the next integration phase.

## Repository Structure

```text
app/                                  Production application code
models/frozen_production_reference/  Frozen ML artifacts
models/frozen_reference_sha256.json   Frozen artifact checksums
tests/                                Automated test suite
Dockerfile                            Production container definition
docker-compose.yml                    Local container orchestration
.env.example                          Example environment configuration
```

## Production Safety

The production ML service is designed as a frozen inference system.

No production retraining, DBSCAN fitting, or new cluster creation is allowed.

Changes to the frozen ML reference must be treated as a controlled model-version change rather than an inference-time operation.

## Docker Usage

### Build the service

```bash
docker compose build
```

### Start the service

```bash
docker compose up -d
```

### Check container status

```bash
docker compose ps
```

The ML service should be reported as healthy.

### Health check

```bash
curl http://localhost:8000/health
```

### Readiness check

```bash
curl http://localhost:8000/ready
```

### Stop the service

```bash
docker compose down
```

The service is exposed on:

`http://localhost:8000`

The frozen production ML artifacts are copied into the Docker image and loaded read-only at startup.

## API Documentation

The ML service exposes the following HTTP endpoints.

### GET `/health`

Returns the basic service health status.

Example:

```bash
curl http://localhost:8000/health
```

Example response:

```json
{
  "status": "ok",
  "service": "honeypot-ml-service"
}
```

### GET `/ready`

Checks whether the frozen production ML artifacts are loaded and ready for inference.

Example:

```bash
curl http://localhost:8000/ready
```

Example response:

```json
{
  "status": "ready",
  "ready": true,
  "model_loaded": true,
  "scaler_loaded": true,
  "feature_contract_loaded": true,
  "reference_clusters_loaded": true
}
```

### GET `/model`

Returns the production ML configuration and frozen-model status.

Example:

```bash
curl http://localhost:8000/model
```

The response includes:

- Model type
- Feature count
- Assignment method
- Production mode
- Retraining policy
- DBSCAN fitting policy
- New-cluster creation policy
- Model loading status

### GET `/analytics`

Returns the current analytics service status.

Example:

```bash
curl http://localhost:8000/analytics
```

Analytics integration is handled in a later production integration phase.

### POST `/process`

Processes honeypot events and assigns reconstructed sessions to existing frozen production behavioral clusters.

Processing flow:

```text
Input Events
    ->
Input Normalization
    ->
Session Reconstruction
    ->
48-Feature Generation
    ->
Frozen StandardScaler
    ->
Nearest Frozen Behavioral Centroid
    ->
Session Results
```

#### Request

```json
{
  "events": [
    {
      "timestamp": "2025-01-01T00:00:00Z",
      "event_type": "auth",
      "source_ip": "10.0.0.1",
      "username": "admin",
      "session_id": "example-session"
    }
  ]
}
```

The `events` field contains the honeypot events submitted for processing.

#### Response

```json
{
  "status": "ok",
  "sessions_processed": 1,
  "results": [
    {
      "session_id": "example-session",
      "cluster_id": 0,
      "assignment_status": "EXISTING_PRODUCTION_CLUSTER",
      "validation_status": "VALIDATED_48_FEATURES",
      "event_count": 1,
      "protocol": null,
      "honeypot": null
    }
  ]
}
```

`cluster_id` identifies the existing frozen production behavioral cluster assigned to the session.

`assignment_status` confirms that the assignment uses an existing production cluster.

`validation_status` confirms validation against the 48-feature production contract.

The `/process` endpoint does not perform model training, DBSCAN fitting, or new cluster creation.

## Frozen ML Policy

The ML service operates as a frozen production inference system.

### Immutable Production Artifacts

The production ML reference is stored under:

`models/frozen_production_reference/`

These artifacts are read-only during inference and must not be modified by the running service.

### Production Restrictions

The following operations are explicitly disabled in production:

- Model retraining
- DBSCAN fitting
- New cluster creation
- Cluster reassignment
- IP-only inference

The service does not create or learn new behavioral clusters during inference.

### Feature Contract

Production inference uses exactly 48 behavioral features with a fixed feature order.

The feature contract is validated against the frozen production configuration, behavioral reference, and production feature schema before the model is used.

### Frozen Scaling

The service uses the frozen StandardScaler parameters stored in the production reference.

No scaler fitting is performed during inference.

### Cluster Assignment

Future sessions are assigned using:

`nearest_behavioral_centroid`

The assignment is made only against the existing frozen production behavioral centroids.

The production reference contains 38 non-noise clusters with cluster IDs `0..37`.

### Integrity Verification

Before loading the production model, the service verifies the SHA-256 values of the frozen production artifacts against:

`models/frozen_reference_sha256.json`

If a required artifact is missing or its SHA-256 value does not match the frozen manifest, the production model is rejected.

### Model Version Changes

Any change to the frozen production ML reference must be treated as a controlled model-version change.

It must not occur as part of normal runtime inference.

## Output Contract

The `/process` endpoint returns one result for each reconstructed session.

### Process Response

The top-level response contains:

- `status`: Processing status.
- `sessions_processed`: Number of reconstructed sessions processed.
- `results`: List of session-level ML results.

Example:

```json
{
  "status": "ok",
  "sessions_processed": 2,
  "results": [
    {
      "session_id": "session-a",
      "cluster_id": 12,
      "assignment_status": "EXISTING_PRODUCTION_CLUSTER",
      "validation_status": "VALIDATED_48_FEATURES",
      "event_count": 5,
      "protocol": "ssh",
      "honeypot": "cowrie"
    },
    {
      "session_id": "session-b",
      "cluster_id": 4,
      "assignment_status": "EXISTING_PRODUCTION_CLUSTER",
      "validation_status": "VALIDATED_48_FEATURES",
      "event_count": 3,
      "protocol": "http",
      "honeypot": "web"
    }
  ]
}
```

### Session Result Contract

Each item in `results` contains:

| Field | Description |
|---|---|
| `session_id` | Stable identifier of the reconstructed session. |
| `cluster_id` | Existing frozen production behavioral cluster assigned to the session. |
| `assignment_status` | Confirms assignment to an existing production cluster. |
| `validation_status` | Confirms validation against the 48-feature production contract. |
| `event_count` | Number of events belonging to the session. |
| `protocol` | Protocol associated with the session when available. |
| `honeypot` | Honeypot identifier when available. |

### Output Guarantees

The ML service guarantees that:

- Results are produced at session level.
- Each processed session has a corresponding result.
- Cluster assignment uses an existing frozen production cluster.
- Feature validation uses the fixed 48-feature contract.
- No new cluster is created during inference.
- The output is JSON-compatible.
- The output contract is validated by automated tests.

The output is designed to provide the Backend with the information required for downstream behavioral analytics and dashboard integration.