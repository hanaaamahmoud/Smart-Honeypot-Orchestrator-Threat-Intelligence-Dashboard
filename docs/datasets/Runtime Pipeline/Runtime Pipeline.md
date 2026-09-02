
# Step 9 — Production New-Log Inference & Runtime Pipeline

## 1. Overview
Step 9 is the production inference stage of the project. The main goal is to process new security logs using the same approved behavioral feature pipeline and frozen DBSCAN production reference from Step 7, without retraining the model.

Step 9 is designed to prepare the system for real new-log inference while preserving the integrity of the previous production stages.


## 2. Production Architecture
The production pipeline follows this execution flow:

```text
New Logs ➔ Parsing & Normalization ➔ Session Reconstruction ➔ 48 Behavioral Features ➔ Feature Validation ➔ Frozen DBSCAN Assignment ➔ Production Output ➔ Dashboard / Analytics Handoff

```

### Stage Responsibilities

* **Step 7:** Provides the immutable ML production reference and the 48 behavioral features.
* **Step 8:** Provides the dashboard and analytics layer.
* **Step 9:** Processes new logs and performs production inference without retraining.


## 3. Production Governance

The following rules are strictly enforced throughout Step 9:

* **No DBSCAN Retraining:** Prohibits retraining on new logs.
* **Frozen Parameters:** No modification of `eps` or `min_samples`.
* **No Cluster Creation:** Prohibits creating new clusters during inference.
* **Immutable Features:** No modification or reordering of the 48 behavioral features.
* **No Label Leakage:** Prohibits attack-label leakage into behavioral features.
* **Protected Artifacts:** No modification of previous Step 7 or Step 8 artifacts.
* **Strict Data Integrity:** No fabrication or assumption of missing values.
* **No Unsupported Matching:** Prohibits fuzzy matching or unsupported IP-only inference.

*These rules ensure that production inference remains consistent with the approved ML reference.*



## 4. Step 9A — Production Reference & Assignment Gate

Step 9A validates and discovers the frozen production reference from Step 7.

### Process Workflow

1. Verifying the existence and integrity of the Step 7 archive.
2. Extracting the approved production reference.
3. Discovering model, preprocessing, scaler, and feature artifacts.
4. Validating the 48-feature contract.
5. Recording model configuration and production metadata.
6. Creating production assignment governance and readiness gates.

### Production DBSCAN Reference Configuration

| Parameter | Value |
| --- | --- |
| **Algorithm** | DBSCAN |
| **eps** | `0.5` |
| **min_samples** | `20` |
| **Reference Clusters** | `38` |
| **Reference Noise Sessions** | `1676` |
| **Behavioral Features** | `48` |
| **Execution Mode** | `FROZEN_PRODUCTION_REFERENCE` |

*The generated manifests and audit files document the approved production reference.*


## 5. Step 9B — New Log Parsing & Normalization

Step 9B defines the contract for processing new raw security logs.

### Supported Honeypot Sources

* `COWRIE`
* `SNARE_TANNER`
* `DIONAEA`

### Normalization Scope

The normalization process standardizes:

* Field names
* Data types
* Timestamps
* Session identifiers
* Network information
* Event information

### Canonical Event Structure

```json
[
  "event_id",
  "timestamp",
  "source",
  "reconstructed_session_id",
  "src_ip",
  "dst_ip",
  "src_port",
  "dst_port",
  "protocol",
  "event_type",
  "command",
  "payload",
  "username",
  "password",
  "file_name",
  "file_hash"
]

```

> **Note:** Missing values are preserved as `null` when information is unavailable instead of being fabricated.

---

## 6. Step 9C — Production Feature Generation

Step 9C defines how the approved 48 behavioral features are generated from normalized new events.

### Feature Contract Rules

* **Session-Level Processing:** Operates strictly on session granularity.
* **Primary Key:** Uses `reconstructed_session_id` as the main session identifier.
* **Feature Count:** Generates exactly 48 behavioral features.
* **Consistency:** Maintains feature ordering and representation identical to Step 7.

### Excluded Fields (Anti-Leakage Policy)

The following fields are explicitly excluded from feature generation:

* `attack_type`
* `mitre_technique`
* `attack_stage`
* `session_mitre_status`
* `dbscan_cluster`
* `cluster_id`
* `cluster_label`
* `cluster_derived_features`

---

## 7. Step 9D — Feature Validation & Assignment Preparation

Before inference, generated feature vectors are validated against the frozen Step 7 feature contract.

### Validation Checks

* Feature count verification
* Feature name verification
* Feature order verification
* Data type validation
* Infinite-value checks
* Label leakage checks
* Scaling consistency checks

### Quarantined / Rejected Conditions

Invalid feature vectors containing any of the following are rejected or quarantined:

* Missing required features
* Incorrect dimensions
* Invalid values
* Label leakage
* Fabricated information

*Only validated feature vectors proceed to the production assignment stage.*

---

## 8. Step 9E — Frozen DBSCAN Production Assignment

Step 9E provides the production inference gate for the frozen DBSCAN reference.

### Production Configuration

* **Algorithm:** DBSCAN (`eps=0.5`, `min_samples=20`)
* **Reference Clusters:** 38
* **Reference Noise Sessions:** 1676
* **Features:** 48 behavioral features

### Execution Constraints

The production assignment process may process new logs, but it must **NOT**:

* Retrain DBSCAN
* Change model parameters
* Create new clusters
* Modify Step 7 artifacts
* Modify Step 8 artifacts

*When no real new logs are provided, execution remains in a readiness state without generating fabricated assignments.*

---

## 9. Step 9F — Production Assignment Output

Step 9F defines the structure of the production inference output at the session level using `reconstructed_session_id`.

### Allowed Assignment Results

* `EXISTING_PRODUCTION_CLUSTER`
* `NOISE`

### Output Schema

| Field Type | Field Name |
| --- | --- |
| **Required** | `reconstructed_session_id` |
| **Required** | `production_cluster_assignment` |
| **Required** | `assignment_status` |
| **Required** | `feature_validation_status` |
| **Optional** | `event_count` |
| **Optional** | `session_start` |
| **Optional** | `session_end` |
| **Optional** | `source` |

> **Note:** New or fabricated clusters are strictly not permitted.

---

## 10. Step 9G — Analytics & Dashboard Handoff

Step 9G defines how production inference results are passed to the Step 8 analytics and dashboard layer.

### Supported Analytics Layers

1. `SESSION_ANALYTICS`
2. `CLUSTER_ANALYTICS`
3. `GEOIP_ANALYTICS`
4. `ATTACKER_IP_ANALYTICS`
5. `MITRE_ANALYTICS`
6. `TEMPORAL_TRENDS`
7. `MITRE_TRENDS`
8. `MITRE_STATISTICS`
9. `SESSION_REPLAY`

### Empty Data Policy

When no new logs are available, the system validates the handoff contract but **must not** generate artificial:

* Sessions
* Cluster assignments
* MITRE information
* GeoIP information
* Dashboard records

*Existing Step 8 data remains protected from modification.*

---

## 11. Step 9H — End-to-End Production Readiness

The final stage prepares the system for complete new-log processing.

### End-to-End Pipeline

```text
New Logs ➔ Parsing ➔ Normalization ➔ Session Reconstruction ➔ Feature Generation ➔ Feature Validation ➔ Frozen DBSCAN Assignment ➔ Output ➔ Dashboard Handoff

```

The pipeline stops safely when real new logs are not available. This allows the production environment to be prepared without performing unauthorized inference or generating artificial data.

---

## 12. Final Result

Step 9 establishes a controlled production inference pipeline for processing future security logs.

### Key Pipeline Guarantees

* **No Retraining:** Preserves existing model weights and configurations.
* **Frozen DBSCAN Reference:** Maintains consistent clustering baseline.
* **48-Feature Consistency:** Ensures exact feature parity with Step 7.
* **Zero Label Leakage:** Strict exclusion of target/analytical labels during feature extraction.
* **No Fabricated Data:** Preserves missing values as `null`.
* **No New Clusters:** Out-of-distribution inputs default to `NOISE`.
* **Artifact Protection:** Leaves Step 7 and Step 8 files untouched.
* **Validated Outputs & Handoff:** Fully compatible with Step 8 dashboard requirements.

