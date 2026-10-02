# Models — Frozen Production Artifacts

These files are the frozen ML model used by the service.
They are read-only and protected by SHA-256 verification.

NEVER modify, delete, or regenerate any file in this folder.

---

## Folder Contents

    models/
    |-- frozen_reference_sha256.json       SHA-256 manifest for all files
    `-- frozen_production_reference/       All model artifacts (21 files)

---

## What Each File Is

### frozen_reference_sha256.json (root of models/)

Checksums for every file in frozen_production_reference/.
Used at startup to verify integrity. If any checksum fails, the
service refuses to start.

### frozen_production_reference/standard_scaler_params.json

Frozen StandardScaler parameters: mean and scale for all 48 features.
Used to transform features before cluster assignment.
NEVER refit.

### frozen_production_reference/step7g_dbscan_behavioral_reference_centroids.csv

The 38 production centroids (one row per cluster).
Used for nearest-centroid assignment.
NEVER fit DBSCAN again.

### frozen_production_reference/step7g_production_config.json

Model configuration: DBSCAN parameters (eps=0.5, min_samples=20).

### frozen_production_reference/step7h_production_feature_schema.json

The 48-feature schema with exact order.
Must match FROZEN_FEATURE_ORDER in the pipeline.

### frozen_production_reference/cluster_behavior_mapping.json

Maps each cluster ID (0-37, -1) to its behavioral description.

### frozen_production_reference/step7d_*.csv / *.json

Reference tables from the original training run:
cluster sizes, behavioral signatures, top features, detailed profiles.

### frozen_production_reference/step7g_*.csv

Production-level reference data:
centroids, behavioral assignments, pipeline audit.

---

## How Code Uses These Files

All files are loaded by app/model_loader.py at service startup:

1. Verifies SHA-256 of every file
2. Loads scaler parameters
3. Loads centroids
4. Loads feature schema
5. Loads model configuration

See docs/ARCHITECTURE.md for the design rules.

---

## Verification

To verify integrity at any time:

    python -c "
    from app.model_loader import load_frozen_model
    load_frozen_model()
    print('All checksums verified')
    "

If a checksum fails, restore from Git:

    git checkout HEAD -- models/
