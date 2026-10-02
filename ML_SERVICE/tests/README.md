# Tests — ML Service

Automated tests for the ML Service.

---

## How to Run

From the ML_SERVICE/ folder:

    # All tests
    python -m pytest tests/ -q

    # A specific folder
    python -m pytest tests/unit/ -q
    python -m pytest tests/contract/ -q
    python -m pytest tests/integration/ -q

    # A single file
    python -m pytest tests/unit/test_mitre_analytics.py -v

    # Verbose with details
    python -m pytest tests/ -v

---

## Test Organization

The tests folder uses three naming patterns:

### 1. Folders (organized by type)

| Folder | Purpose |
|---|---|
| tests/unit/ | Pure-function tests (fast, no dependencies) |
| tests/contract/ | Contract/schema validation tests |
| tests/integration/ | End-to-end tests (may require Elasticsearch) |

### 2. Files with milestone prefixes (L2, L3, D2, D3, D4)

These files correspond to the project's development milestones:

| Prefix | Meaning |
|---|---|
| D2 | Session reconstruction stages |
| D3 | Feature generation stages |
| D4 | Feature assembly and validation |
| L2 | Canonical adapter and normalization |
| L3 | Integration and API contracts |

### 3. Files with subject names

These files test a specific feature or component.

---

## Test Files Reference

### Unit-level tests (root of tests/)

| File | What it tests |
|---|---|
| test_health.py | Health and readiness endpoints |
| test_input_adapter.py | Input adapter boundary |
| test_output_adapter.py | Canonical ML output |
| test_feature_contract.py | Feature contract definition |
| test_feature_generation_base.py | Base feature generation (7 features) |
| test_feature_generation_density.py | Density features (8 features) |
| test_feature_generation_diversity.py | Diversity features (16 features) |
| test_feature_generation_geo.py | Geo features (7 features) |
| test_feature_generation_temporal.py | Temporal features (10 features) |
| test_geoip_input_contract.py | GeoIP input contract |
| test_process_integration.py | Process endpoint behavior |
| test_output_analytics_contract.py | Analytics output contract |
| test_output_session_contract.py | Session output contract |
| test_session_boundaries.py | Session start/end calculation |
| test_session_contract.py | Session data contract |
| test_session_grouping.py | Session grouping by ID |
| test_session_id_policy.py | Session ID policy |
| test_session_ordering.py | Session event ordering |
| test_session_reconstruction.py | Full session reconstruction |
| test_event_conservation_unassigned.py | Events without session_id |
| test_d16_real_process_verification.py | Full process verification |
| test_d2_contract.py | D2 contract |
| test_d2_regression.py | D2 regression tests |
| test_d3_7_feature_assembly.py | D3.7 feature assembly |
| test_d3_8_feature_validation.py | D3.8 feature validation |
| test_d3_regression.py | D3 regression |
| test_d4_feature_validation.py | D4 feature validation |
| test_d4_integration.py | D4 integration |
| test_l3d_gate.py | L3 gate (canonical output) |
| test_l3f_process_api_contract.py | L3-F process API contract |

### Contract tests (tests/contract/)

| File | What it tests |
|---|---|
| test_attacker_ip_analytics_contract.py | Attacker IP contract |
| test_cluster_analytics_contract.py | Cluster analytics contract |
| test_mitre_analytics_contract.py | MITRE analytics contract |
| test_mitre_statistics_contract.py | MITRE statistics contract |
| test_mitre_trends_contract.py | MITRE trends contract |
| test_session_analytics_contract.py | Session analytics contract |
| test_session_replay_contract.py | Session replay contract |
| test_temporal_analytics_contract.py | Temporal analytics contract |

### Unit tests (tests/unit/)

| File | What it tests |
|---|---|
| test_canonical_adapter.py | Canonical adapter logic |
| test_cluster_analytics.py | Cluster analytics logic |
| test_elasticsearch_reader.py | Elasticsearch reader |
| test_mitre_analytics.py | MITRE analytics logic |
| test_mitre_statistics.py | MITRE statistics logic |
| test_mitre_trends.py | MITRE trends logic |
| test_session_analytics.py | Session analytics logic |
| test_session_boundary.py | Session boundary logic |
| test_session_replay.py | Session replay logic |
| test_temporal_analytics.py | Temporal analytics logic |

### Integration tests (tests/integration/)

| File | What it tests |
|---|---|
| test_l210_real_elk_frozen_pipeline.py | Real ELK frozen pipeline |
| test_l29_pipeline_compatibility.py | Pipeline compatibility |
| test_real_elk_canonical.py | Real ELK canonical adapter |
| test_session_analytics_integration.py | Session analytics integration |
| test_session_analytics_runtime.py | Session analytics runtime |

---

## Test Coverage Summary

The test suite covers:

- Elasticsearch reader (read-only, batched)
- Input adapter and canonical adapter
- Normalization pipeline
- Session reconstruction (grouping, ordering, boundaries)
- 48-feature generation (all 5 groups)
- Feature assembly and validation
- Frozen model loading and scaling
- Nearest centroid assignment
- Canonical ML output
- All analytics layers (cluster, temporal, session, MITRE x3, replay)
- API endpoints (health, ready, process, analytics, session-replay)
- Contract schemas for every analytics layer

Target: All tests must pass before any commit.

---

## Adding a New Test

When adding a new analytics layer:

1. Add unit tests in tests/unit/test_<name>.py
2. Add contract tests in tests/contract/test_<name>_contract.py
3. Run python -m pytest tests/ -q
4. Ensure all tests pass before commit

When modifying existing code:

1. Run the relevant test file first
2. If behavior changed intentionally, update the test
3. If behavior changed accidentally, fix the code
4. Run the full suite before commit

---

## Notes

- Tests are read-only with respect to source data
- Tests do not write to Elasticsearch
- Integration tests may need the ML container to be running
- Contract tests validate JSON schemas only
- All tests are deterministic (no random seeds)
