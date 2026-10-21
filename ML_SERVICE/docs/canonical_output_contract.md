# Canonical ML Service Output Contract

## Purpose

This document defines the canonical output contract returned by the
ML Service for processed reconstructed sessions.

The contract is the boundary between the ML Service and downstream
consumers such as the Backend, dashboard, analytics, or other pipeline
components.

The contract describes the output produced by the production
`/process` flow.

---

## Canonical Session Result

Each processed session is represented by the following JSON object:

```json
{
  "reconstructed_session_id": "session-001",
  "production_cluster_assignment": 15,
  "assignment_status": "EXISTING_PRODUCTION_CLUSTER",
  "feature_validation_status": "VALIDATED_48_FEATURES",
  "event_count": 5,
  "session_start": "2026-01-01T00:00:00Z",
  "session_end": "2026-01-01T00:05:00Z",
  "source": "ELASTICSEARCH",
  "protocol": "SSH",
  "honeypot": "cowrie"
}
```

The values above are examples only. They do not represent fixed
production values.

## Canonical Fields

### `reconstructed_session_id`

- **Type:** `string`
- **Required:** Yes
- **Meaning:**
  Stable identifier produced by session reconstruction.
  The identifier represents the reconstructed session processed by the
  ML pipeline.

### `production_cluster_assignment`

- **Type:** `integer | null`
- **Required:** Yes
- **Meaning:**
  The existing frozen production behavioral cluster assigned to the
  session.
  Production assignment uses the frozen behavioral reference and nearest
  behavioral centroid.
  The ML Service does not create a new production cluster.

### `assignment_status`

- **Type:** `string`
- **Required:** Yes
- **Current production value:** `EXISTING_PRODUCTION_CLUSTER`
- **Meaning:**
  Indicates the status of the production cluster assignment.

### `feature_validation_status`

- **Type:** `string`
- **Required:** Yes
- **Current production value:** `VALIDATED_48_FEATURES`
- **Meaning:**
  Indicates that the production behavioral feature vector passed the
  expected 48-feature contract before frozen-model assignment.

### `event_count`

- **Type:** `integer`
- **Required:** Yes
- **Meaning:**
  The actual number of events contained in the reconstructed session.
  The value is derived from:

  ```python
  len(session["events"])
  ```

  This field is a session-level metadata field.
  It must not contain a behavioral feature value, scaled value, distance,
  or model output.

### `session_start`

- **Type:** `string | null`
- **Required:** No
- **Meaning:**
  Start timestamp of the reconstructed session.

### `session_end`

- **Type:** `string | null`
- **Required:** No
- **Meaning:**
  End timestamp of the reconstructed session.

### `source`

- **Type:** `string | null`
- **Required:** No
- **Meaning:**
  Source/dataset provenance exposed by the canonical ML output.
  The canonical input field used by the ML data model is:

  ```
  source_dataset
  ```

  Therefore the output mapping is:

  ```
  source_dataset → source
  ```

  `runtime_source` is not implicitly merged into `source`.

### `protocol`

- **Type:** `string | null`
- **Required:** No
- **Meaning:**
  Protocol associated with the processed session.

### `honeypot`

- **Type:** `string | null`
- **Required:** No
- **Meaning:**
  Honeypot associated with the processed session.

---

## Exact Canonical Output Keys

The session result contains exactly these keys:

- `reconstructed_session_id`
- `production_cluster_assignment`
- `assignment_status`
- `feature_validation_status`
- `event_count`
- `session_start`
- `session_end`
- `source`
- `protocol`
- `honeypot`

Legacy/internal names must not be emitted as canonical output names.
Examples of internal/legacy input aliases include:

- `session_id`
- `cluster_id`
- `validation_status`

These may be accepted internally where explicitly supported by the
adapter, but they are not canonical session output field names.

---

## Production Assignment Semantics

The production ML Service uses frozen behavioral reference artifacts.

The production flow:

```
Input events
    ↓
Input normalization
    ↓
Session reconstruction
    ↓
48-feature generation
    ↓
Feature assembly / validation
    ↓
Frozen feature scaling
    ↓
Nearest frozen behavioral centroid
    ↓
Canonical session result
```

Production assignment does not perform:

- DBSCAN fitting
- retraining
- new cluster creation

The assigned cluster must correspond to an existing frozen production
behavioral cluster.

---

## Distance

The frozen assignment layer calculates the distance to the selected
behavioral centroid.

The current canonical session output does not expose that distance as
a public contract field.

Therefore:

```
nearest_behavioral_distance
```

is not part of the current canonical session JSON contract.

The distance may remain an internal assignment value unless a future
contract explicitly promotes it to a public field.

---

## JSON Requirements

The canonical result must be JSON serializable.

Special floating-point values such as:

- `NaN`
- `+Infinity`
- `-Infinity`

must not be emitted as invalid JSON values.

The output adapter sanitizes such values to:

```
null
```

where applicable.

---

## Contract Boundary

The canonical output contract is implemented across:

```
app/schemas.py
        ↕
app/output_adapter.py
        ↕
app/main.py
        ↕
/process
```

The test suite verifies the contract behavior.

The canonical contract is therefore documentation of the production
implementation, not an independent data format.

---

## Current Scope

This document defines the canonical session result returned by the
ML Service.

Analytics output is defined separately by the `AnalyticsResult`
contract and is not part of the canonical session result above.

---

## Contract Change Rule

Any future change to:

- field names
- field types
- required/optional status
- source mapping
- assignment semantics
- output structure

must be reflected consistently in:

- schemas
- output adapter
- production `/process` implementation
- tests
- documentation

The contract must not be changed by documentation alone.
