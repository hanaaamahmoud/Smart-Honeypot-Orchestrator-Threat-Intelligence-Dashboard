# Scripts — ML Service Operations

Operational and diagnostic scripts.

---

## Runtime Scripts

| Script | Purpose | When to Run |
|---|---|---|
| run_ml_pipeline.sh | Run the full ML pipeline end-to-end | When new data in ES |
| package_handoff.sh | Package results into a ZIP | After pipeline run |
| docker_preflight.sh | Pre-deployment checks | Before docker compose up |

### Typical Workflow

    # 1. Run pipeline
    bash scripts/run_ml_pipeline.sh

    # 2. Package for Backend
    bash scripts/package_handoff.sh

    # 3. Send the ZIP to the Backend team

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
