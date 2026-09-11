"""
Production ML Service API.

Frozen production artifacts are loaded read-only at startup.
No DBSCAN fitting, retraining, or new cluster creation is allowed.
"""

from fastapi import FastAPI

from .config import settings
from .model_loader import FrozenModelError, load_frozen_model
from .schemas import (
    HealthResponse,
    ReadinessResponse,
    ProcessRequest,
    ProcessResponse,
)
from .pipeline.input_adapter import adapt_input
from .pipeline.session_reconstruction import reconstruct_sessions
from .pipeline.feature_generation_base import generate_base_features
from .pipeline.feature_generation_diversity import generate_diversity_features
from .pipeline.feature_generation_temporal import generate_temporal_features
from .pipeline.feature_generation_density import generate_density_features
from .pipeline.feature_generation_geo import generate_geo_availability_features
from .pipeline.feature_generation import assemble_48_features
from .output_adapter import adapt_session_result


app = FastAPI(
    title="Honeypot ML Service",
    version="1.0.0",
)

_frozen_model = None
_model_load_error = None


@app.on_event("startup")
def load_production_model():
    global _frozen_model
    global _model_load_error

    try:
        _frozen_model = load_frozen_model()
        _model_load_error = None
    except Exception as exc:
        _frozen_model = None
        _model_load_error = str(exc)


@app.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(
        status="ok",
        service=settings.APP_NAME,
    )


@app.get("/ready")
def ready():
    loaded = _frozen_model is not None

    return {
        "status": "ready",
        "ready": loaded,
        "model_loaded": loaded,
        "scaler_loaded": loaded,
        "feature_contract_loaded": loaded,
        "reference_clusters_loaded": loaded,
    }


@app.get("/model")
def model_info():
    return {
        "model": "DBSCAN",
        "feature_count": settings.FEATURE_COUNT,
        "assignment_method": settings.ASSIGNMENT_METHOD,
        "mode": settings.PRODUCTION_MODE,
        "dbscan_fitting_allowed": False,
        "retraining_allowed": False,
        "new_cluster_creation_allowed": False,
        "model_loaded": _frozen_model is not None,
        "model_load_error": _model_load_error,
    }


@app.get("/analytics")
def analytics():
    return {
        "status": "not_initialized",
        "message": (
            "Analytics pipeline will be connected "
            "in a later production step."
        ),
    }


@app.post(
    "/process",
    response_model=ProcessResponse,
)
def process(request: ProcessRequest):
    normalized_events = adapt_input(
        request.model_dump()
    )

    sessions = reconstruct_sessions(
        normalized_events
    )

    results = []

    for session in sessions:
        feature_groups = {}

        feature_groups.update(
            generate_base_features(session)
        )
        feature_groups.update(
            generate_diversity_features(session)
        )
        feature_groups.update(
            generate_temporal_features(session)
        )
        feature_groups.update(
            generate_density_features(session)
        )
        feature_groups.update(
            generate_geo_availability_features(session)
        )

        feature_vector = assemble_48_features(
            feature_groups
        )

        if _frozen_model is None:
            raise FrozenModelError(
                "Frozen production model is not loaded."
            )

        scaled_features = _frozen_model.scale_features(
            feature_vector
        )

        cluster_id, distance = _frozen_model.nearest_centroid(
            scaled_features
        )

        results.append(
            adapt_session_result(
                {
                    "session_id": session["session_id"],
                    "cluster_id": cluster_id,
                    "assignment_status": "EXISTING_PRODUCTION_CLUSTER",
                    "validation_status": "VALIDATED_48_FEATURES",
                    "event_count": len(session["events"]),
                    "protocol": session["events"][0].get("protocol"),
                    "honeypot": session["events"][0].get("honeypot"),
                }
            )
        )

    return {
        "status": "ok",
        "sessions_processed": len(sessions),
        "results": results,
    }
