# Docs — ML Service Documentation

All documentation for the ML Service.

---

## Files

| File | Purpose |
|---|---|
| PIPELINE_FLOW.md | Every pipeline step from Elasticsearch to Backend |
| RUNTIME_GUIDE.md | How to run the pipeline and package results |
| INTEGRATION_GUIDE.md | How to integrate the ML Service with the Backend (two modes) |
| ARCHITECTURE.md | Design rules, integration models, golden rules |
| ML_SERVICE_REFERENCE.md | Full reference for the ML service |
| canonical_output_contract.md | Canonical ML output specification |

---

## Quick Descriptions

### PIPELINE_FLOW.md

Step-by-step reference for all 12 pipeline stages:
Elasticsearch → Reader → Canonical → Normalization → Sessions →
Features → Validation → Scaler → Centroid → Output → Analytics → Backend.

### RUNTIME_GUIDE.md

How to run:
- scripts/run_ml_pipeline.sh
- scripts/package_handoff.sh

Includes refresh flow, verification, and troubleshooting.

### INTEGRATION_GUIDE.md

Two integration modes for the Backend:
- Mode A — File-based (recommended for handoff)
- Mode B — Live API (for production)

Both modes use the same data shape.

### ARCHITECTURE.md

Design principles, integration models, golden rules, extension points.

### ML_SERVICE_REFERENCE.md

Full internal reference for the ML service.

### canonical_output_contract.md

The canonical ML output contract (fields, types, guarantees).

---

## Related Documentation

- Main README: ../README.md
- Backend handoff docs: ../backend_handoff/
- Frontend guide: ../backend_handoff/frontend_guide/FRONTEND_HANDOFF.md
- Tests reference: ../tests/README.md
- Scripts reference: ../scripts/README.md
- Models reference: ../models/README.md
