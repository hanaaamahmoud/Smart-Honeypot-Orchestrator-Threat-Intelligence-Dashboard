# Scripts — ML Service Operations

Operational scripts for running and inspecting the ML pipeline.

---

## Folder Layout

    scripts/
    |-- run_ml_pipeline.sh        Run the full pipeline end-to-end
    |-- package_handoff.sh        Package results into a ZIP
    |-- docker_preflight.sh       Pre-deployment checks
    `-- diagnostics/              Data inspection tools
        |-- diagnose_pipeline.py
        |-- diagnose_random.py
        |-- diagnose_bad_sessions.py
        `-- diagnose_distance_breakdown.py

---

## Runtime Scripts

### run_ml_pipeline.sh

Runs the ML pipeline end-to-end:

1. Reads all events from Elasticsearch
2. Reconstructs sessions
3. Generates 48 features per session
4. Assigns each session to a frozen cluster
5. Writes the ML output to analytics_output/

When to run:

- After Elasticsearch has new events
- After any change to pipeline code
- As part of a scheduled regeneration

Usage:

    bash scripts/run_ml_pipeline.sh

Output:

    analytics_output/00_ml_output_full.json
    analytics_output/00_ml_output_full.csv

Typical runtime: 1–2 minutes for ~59,000 events.

---

### package_handoff.sh

Packages the generated analytics into a ZIP for the Backend team.

1. Copies analytics files into backend_handoff/ml_analytics_files/
2. Renames them to stable filenames
3. Creates backend_handoff/ml_analytics_files.zip

When to run:

- After run_ml_pipeline.sh finishes
- Before delivering results to the Backend team

Usage:

    bash scripts/package_handoff.sh

Output:

    backend_handoff/ml_analytics_files.zip

---

### docker_preflight.sh

Pre-deployment sanity checks for the Docker environment.

Verifies:

- Docker daemon is running
- Network elk_elk-net exists
- Required volumes are present
- Container can reach Elasticsearch

When to run:

- Before docker compose up for the first time
- After infrastructure changes

Usage:

    bash scripts/docker_preflight.sh

---

## Diagnostic Tools

Located in scripts/diagnostics/. All tools are read-only.

### diagnose_pipeline.py

Inspects the pipeline output on a sample of events.

Shows:

- Session reconstruction stats
- Feature distribution
- Cluster assignment distribution
- Distance statistics

When to use: General pipeline health check.

Usage:

    python scripts/diagnostics/diagnose_pipeline.py

---

### diagnose_random.py

Runs the pipeline on a random sample of events.

Shows:

- Per-cluster session counts
- Distance statistics (min, median, p95, max)
- Comparison against training reference

When to use: Quick sanity check after code changes.

Usage:

    python scripts/diagnostics/diagnose_random.py

---

### diagnose_bad_sessions.py

Finds the sessions with the highest distance to their assigned centroid.

Shows:

- Top 5 worst sessions
- Their feature vectors
- Their assigned cluster and distance

When to use: When clusters look wrong or distances are unusually high.

Usage:

    python scripts/diagnostics/diagnose_bad_sessions.py

---

### diagnose_distance_breakdown.py

Breaks down the distance to the centroid by feature.

Shows:

- Feature-by-feature contribution to the total distance
- Top 15 contributing features
- Percentage contribution per feature

When to use: When a specific feature seems to be dominating distances.

Usage:

    python scripts/diagnostics/diagnose_distance_breakdown.py

---

## Typical Workflows

### Standard run (new data arrives)

    # 1. Run the pipeline
    bash scripts/run_ml_pipeline.sh

    # 2. Package results for Backend
    bash scripts/package_handoff.sh

    # 3. Send the ZIP to the Backend team

### First-time setup

    # 1. Verify Docker environment
    bash scripts/docker_preflight.sh

    # 2. Start the ML service
    docker compose up -d

    # 3. Run the pipeline
    bash scripts/run_ml_pipeline.sh

### Debugging

    # 1. General pipeline check
    python scripts/diagnostics/diagnose_pipeline.py

    # 2. Random sample check
    python scripts/diagnostics/diagnose_random.py

    # 3. If clusters look wrong
    python scripts/diagnostics/diagnose_bad_sessions.py

    # 4. If distances are unusually high
    python scripts/diagnostics/diagnose_distance_breakdown.py

---

## Notes

- All scripts are idempotent; running them twice is safe.
- Scripts never modify the source data.
- Scripts never retrain the model.
- Diagnostics are read-only.
- The pipeline runs inside the container by default when the service is up.
