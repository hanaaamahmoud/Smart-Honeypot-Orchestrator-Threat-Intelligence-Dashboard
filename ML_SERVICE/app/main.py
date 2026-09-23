"""
Production ML Service API.

Frozen production artifacts are loaded read-only at startup.
No DBSCAN fitting, retraining, or new cluster creation is allowed.

Analytics layers consume the validated ML Result Contract.
They do not rerun ML processing.
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
from .pipeline.feature_generation_diversity import (
    generate_diversity_features,
)
from .pipeline.feature_generation_temporal import (
    generate_temporal_features,
)
from .pipeline.feature_generation_density import (
    generate_density_features,
)
from .pipeline.feature_generation_geo import (
    generate_geo_availability_features,
)
from .pipeline.feature_generation import assemble_48_features

from .output_adapter import adapt_session_result

from .analytics.session_boundary import (
    build_session_analytics_input,
)
from .analytics.session_analytics import (
    build_session_analytics,
)
from .analytics.cluster_analytics import (
    build_cluster_analytics,
)
from .analytics.temporal_analytics import (
    build_temporal_analytics,
)


app = FastAPI(
    title="Honeypot ML Service",
    version="1.0.0",
)


# ============================================================
# FROZEN PRODUCTION MODEL
# ============================================================

_frozen_model = None
_model_load_error = None


# ============================================================
# ANALYTICS STATE
# ============================================================

_session_analytics = []

_cluster_analytics = {}

_temporal_analytics = []


# ============================================================
# STARTUP
# ============================================================

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


# ============================================================
# HEALTH
# ============================================================

@app.get(
    "/health",
    response_model=HealthResponse,
)
def health():
    return HealthResponse(
        status="ok",
        service=settings.APP_NAME,
    )


# ============================================================
# READINESS
# ============================================================

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


# ============================================================
# MODEL INFORMATION
# ============================================================

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


# ============================================================
# ANALYTICS
# ============================================================

@app.get("/analytics")
def analytics():
    return {
        "status": "ok",
        "layer": "DASHBOARD_ANALYTICS",

        # ----------------------------------------------------
        # SESSION ANALYTICS
        # ----------------------------------------------------
        "session_analytics": _session_analytics,
        "sessions_count": len(_session_analytics),

        # ----------------------------------------------------
        # CLUSTER ANALYTICS
        # ----------------------------------------------------
        "cluster_analytics": _cluster_analytics,

        # ----------------------------------------------------
        # TEMPORAL ANALYTICS
        # ----------------------------------------------------
        "temporal_analytics": _temporal_analytics,
    }


# ============================================================
# PROCESS
# ============================================================

@app.post(
    "/process",
    response_model=ProcessResponse,
)
def process(request: ProcessRequest):
    global _session_analytics
    global _cluster_analytics
    global _temporal_analytics

    # ========================================================
    # 1. CANONICAL ADAPTER
    # ========================================================

    normalized_events = adapt_input(
        request.model_dump()
    )

    # ========================================================
    # 2. SESSION RECONSTRUCTION
    # ========================================================

    sessions = reconstruct_sessions(
        normalized_events
    )

    results = []

    # ========================================================
    # 3. ML PROCESSING PER SESSION
    # ========================================================

    for session in sessions:

        feature_groups = {}

        # ----------------------------------------------------
        # Base features
        # ----------------------------------------------------

        feature_groups.update(
            generate_base_features(session)
        )

        # ----------------------------------------------------
        # Diversity features
        # ----------------------------------------------------

        feature_groups.update(
            generate_diversity_features(session)
        )

        # ----------------------------------------------------
        # Temporal feature generation
        # ----------------------------------------------------

        feature_groups.update(
            generate_temporal_features(session)
        )

        # ----------------------------------------------------
        # Density features
        # ----------------------------------------------------

        feature_groups.update(
            generate_density_features(session)
        )

        # ----------------------------------------------------
        # Geo availability features
        # ----------------------------------------------------

        feature_groups.update(
            generate_geo_availability_features(session)
        )

        # ----------------------------------------------------
        # Assemble validated 48-feature vector
        # ----------------------------------------------------

        feature_vector = assemble_48_features(
            feature_groups
        )

        # ----------------------------------------------------
        # Frozen model must already be loaded
        # ----------------------------------------------------

        if _frozen_model is None:
            raise FrozenModelError(
                "Frozen production model is not loaded."
            )

        # ----------------------------------------------------
        # Frozen scaler
        # ----------------------------------------------------

        scaled_features = _frozen_model.scale_features(
            feature_vector
        )

        # ----------------------------------------------------
        # Production assignment
        #
        # IMPORTANT:
        # This is the frozen production assignment.
        # Analytics layers must not modify it.
        # ----------------------------------------------------

        cluster_id, distance = (
            _frozen_model.nearest_centroid(
                scaled_features
            )
        )

        # ====================================================
        # 4. ML RESULT CONTRACT
        # ====================================================

        result = adapt_session_result(
            {
                "reconstructed_session_id": (
                    session["session_id"]
                ),

                "production_cluster_assignment": (
                    cluster_id
                ),

                "assignment_status": (
                    "EXISTING_PRODUCTION_CLUSTER"
                ),

                "feature_validation_status": (
                    "VALIDATED_48_FEATURES"
                ),

                "event_count": len(
                    session["events"]
                ),

                "session_start": session.get(
                    "start_time"
                ),

                "session_end": session.get(
                    "end_time"
                ),

                # Source is optional.
                # Do not fabricate it.
                "source": session["events"][0].get(
                    "source"
                ),

                "protocol": session["events"][0].get(
                    "protocol"
                ),

                "honeypot": session["events"][0].get(
                    "honeypot"
                ),
            }
        )

        results.append(result)

    # ========================================================
    # 5. SESSION ANALYTICS
    #
    # Consumes ML Result Contract.
    # Does not rerun ML.
    # ========================================================

    analytics_input = build_session_analytics_input(
        results
    )

    _session_analytics = build_session_analytics(
        analytics_input
    )

    # ========================================================
    # 6. CLUSTER ANALYTICS
    #
    # Consumes existing production cluster assignments.
    # Does not refit DBSCAN.
    # Does not create clusters.
    # Does not modify assignments.
    # ========================================================

    _cluster_analytics = build_cluster_analytics(
        results
    )

    # ========================================================
    # 7. TEMPORAL ANALYTICS
    #
    # Consumes ML session-result records directly.
    #
    # It uses:
    #   reconstructed_session_id
    #   event_count
    #   session_start
    #   session_end
    #
    # It does NOT:
    #   - rerun session reconstruction
    #   - rerun feature generation
    #   - rerun clustering
    #   - modify ML assignments
    #   - perform external enrichment
    # ========================================================

    _temporal_analytics = build_temporal_analytics(
        results
    )

    # ========================================================
    # 8. FINAL RESPONSE
    # ========================================================

    return {
        "status": "ok",
        "sessions_processed": len(
            sessions
        ),
        "results": results,
    }


# ============================================================
# MODULE EXPORT
# ============================================================

__all__ = [
    "app",
]
