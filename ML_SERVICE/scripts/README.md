# Scripts — ML Service Operations

Operational and diagnostic scripts.

---

## Runtime Scripts

| Script | Purpose | When to Run |
|---|---|---|
| refresh_all.sh | Full refresh in one command | When new data arrives |
| run_ml_pipeline.sh | Run the ML pipeline only | Pipeline stage |
| package_handoff.sh | Package results into a ZIP | After pipeline |
| docker_preflight.sh | Pre-deployment checks | Before compose up |

---

## Quick Start — New Data Arrives

    bash scripts/refresh_all.sh

This one command does everything:

1. Verifies Docker + Container
2. Verifies Elasticsearch connectivity
3. Runs the full pipeline
4. Packages the ZIP
5. Copies the ZIP to the Desktop

When it finishes, the ZIP is ready to send to the Backend team.

---

## Manual Steps (if refresh_all is not used)

    # 1. Run the pipeline
    bash scripts/run_ml_pipeline.sh

    # 2. Package the results
    bash scripts/package_handoff.sh

    # 3. Copy the ZIP
    docker cp honeypot-ml-service:/app/backend_handoff/ml_analytics_files.zip ~/Desktop/

---

## Diagnostic Tools (scripts/diagnostics/)

Read-only tools for inspecting the pipeline.

| Tool | Purpose | When to Use |
|---|---|---|
| diagnose_pipeline.py | Full pipeline inspection | Debug pipeline issues |
| diagnose_random.py | Random sample check | Verify random sessions |
| diagnose_bad_sessions.py | Find unusual sessions | Investigate outliers |
| diagnose_distance_breakdown.py | Feature-level analysis | Debug cluster distances |

---

## Notes

- All scripts are idempotent (safe to run multiple times).
- Scripts never modify source data.
- Scripts never retrain the model.
- Diagnostics are read-only.
