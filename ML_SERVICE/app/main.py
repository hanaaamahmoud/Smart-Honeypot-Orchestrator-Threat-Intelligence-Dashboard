"""
Production ML Service API.

Frozen production artifacts are loaded read-only at startup.
No DBSCAN fitting, retraining, or new cluster creation is allowed.

Analytics layers consume the validated ML Result Contract.
They do not rerun ML processing.
"""

from fastapi import FastAPI, HTTPException

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
from .analytics.mitre_analytics import (
    build_mitre_analytics,
)
from .analytics.mitre_statistics import (
    build_mitre_statistics,
)
from .analytics.mitre_trends import (
    build_mitre_trends,
)
from .analytics.session_replay import (
    build_session_replay,
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

_mitre_analytics = {}

_mitre_statistics = {}

_mitre_trends = {}

# Session Replay: kept as:
# - _session_replay_list:      lightweight list for the dashboard table
# - _session_replay_sessions:  dict {session_id: full_session} for on-demand detail
_session_replay_list = {}

_session_replay_sessions = {}


# ============================================================
# MITRE INPUT BUILDER
# ============================================================

def _build_mitre_input(sessions):
    """
    Build MITRE analytics input records from reconstructed sessions.

    MITRE fields (mitre_technique, attack_type, attack_stage, severity)
    are read from the raw payload of the first event in each session.

    Does NOT fabricate values.
    Skips sessions without a valid timestamp.
    """
    records = []

    for session in sessions:
        events = session.get("events") or []
        if not events:
            continue

        first = events[0]
        raw = first.get("raw")
        if not isinstance(raw, dict):
            raw = {}

        ts = session.get("start_time") or first.get("timestamp")
        if not ts:
            continue

        records.append({
            "timestamp": ts,
            "session_id": session.get("session_id"),
            "event_count": len(events),
            "mitre_technique": raw.get("mitre_technique"),
            "attack_type": raw.get("attack_type"),
            "attack_stage": raw.get("attack_stage"),
            "severity": raw.get("severity"),
            "source_ip": (
                first.get("source_ip")
                or raw.get("source_ip")
            ),
        })

    return records


# ============================================================
# SESSION REPLAY HELPERS
# ============================================================

def _replay_score(session_summary: dict) -> int:
    """
    Compute a replay-worthiness score for one session.

    Sessions with high score get a dedicated replay detail file
    on the frontend (marked with has_replay=true).
    """
    flags = session_summary.get("flags", {})
    creds = session_summary.get("credentials", {})
    cmds = session_summary.get("commands", {})

    score = 0
    if flags.get("has_commands_executed"):
        score += 100
    if flags.get("is_brute_force_candidate"):
        score += 50
    if flags.get("is_high_severity"):
        score += 80
    if flags.get("is_medium_or_higher_severity"):
        score += 20
    if flags.get("is_large_session"):
        score += 30
    if flags.get("is_multi_ip"):
        score += 15

    score += creds.get("auth_attempt_total", 0) * 2
    score += len(creds.get("unique_usernames", [])) * 5
    score += cmds.get("unique_commands_count", 0) * 10

    return score


_REPLAY_THRESHOLD = 30


def _build_replay_list_entry(session: dict, has_replay: bool) -> dict:
    """Build one lightweight list entry for the sessions table."""
    sm = session["summary"]
    return {
        "id": sm["reconstructed_session_id"],
        "events": sm["event_count"],
        "duration": sm["duration_seconds"],
        "honeypot": sm["context"].get("honeypot"),
        "protocol": sm["context"].get("protocol"),
        "country": sm["context"].get("country"),
        "attack": sm["classification"].get("attack_type"),
        "mitre": sm["classification"].get("mitre_technique"),
        "severity": sm["classification"].get("severity"),
        "flags": sm["flags"],
        "has_replay": has_replay,
    }


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

        "session_analytics": _session_analytics,
        "sessions_count": len(_session_analytics),

        "cluster_analytics": _cluster_analytics,

        "temporal_analytics": _temporal_analytics,

        "mitre_analytics": _mitre_analytics,

        "mitre_statistics": _mitre_statistics,

        "mitre_trends": _mitre_trends,
    }


# ============================================================
# SESSION REPLAY — LIST
# ============================================================

@app.get("/session-replay")
def session_replay_list():
    """
    Return the lightweight session replay list.

    Frontend uses this once at startup (with gzip -> ~1 MB network).
    Use query params for filtering if needed.
    """
    return _session_replay_list


# ============================================================
# SESSION REPLAY — DETAIL
# ============================================================

@app.get("/session-replay/{session_id}")
def session_replay_detail(session_id: str):
    """
    Return the full replay (narrative + events) for one session.

    Only sessions with has_replay=true have a detail entry.
    """
    session = _session_replay_sessions.get(session_id)

    if session is None:
        raise HTTPException(
            status_code=404,
            detail=(
                f"No replay available for session {session_id}. "
                "This session has no detail record."
            ),
        )

    return session


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
    global _mitre_analytics
    global _mitre_statistics
    global _mitre_trends
    global _session_replay_list
    global _session_replay_sessions

    # 1. CANONICAL ADAPTER
    normalized_events = adapt_input(request.model_dump())

    # 2. SESSION RECONSTRUCTION
    sessions = reconstruct_sessions(normalized_events)

    results = []

    # 3. ML PROCESSING PER SESSION
    for session in sessions:
        feature_groups = {}

        feature_groups.update(generate_base_features(session))
        feature_groups.update(generate_diversity_features(session))
        feature_groups.update(generate_temporal_features(session))
        feature_groups.update(generate_density_features(session))
        feature_groups.update(generate_geo_availability_features(session))

        feature_vector = assemble_48_features(feature_groups)

        if _frozen_model is None:
            raise FrozenModelError(
                "Frozen production model is not loaded."
            )

        scaled_features = _frozen_model.scale_features(feature_vector)
        cluster_id, distance = _frozen_model.nearest_centroid(
            scaled_features
        )

        # 4. ML RESULT CONTRACT
        result = adapt_session_result({
            "reconstructed_session_id": session["session_id"],
            "production_cluster_assignment": cluster_id,
            "assignment_status": "EXISTING_PRODUCTION_CLUSTER",
            "feature_validation_status": "VALIDATED_48_FEATURES",
            "event_count": len(session["events"]),
            "session_start": session.get("start_time"),
            "session_end": session.get("end_time"),
            "source": session["events"][0].get("source"),
            "protocol": session["events"][0].get("protocol"),
            "honeypot": session["events"][0].get("honeypot"),
        })

        results.append(result)

    # 5. SESSION ANALYTICS
    analytics_input = build_session_analytics_input(results)
    _session_analytics = build_session_analytics(analytics_input)

    # 6. CLUSTER ANALYTICS
    _cluster_analytics = build_cluster_analytics(results)

    # 7. TEMPORAL ANALYTICS
    _temporal_analytics = build_temporal_analytics(results)

    # 8. MITRE ANALYTICS / STATISTICS / TRENDS
    mitre_input = _build_mitre_input(sessions)
    _mitre_analytics = build_mitre_analytics(mitre_input)
    _mitre_statistics = build_mitre_statistics(mitre_input)
    _mitre_trends = build_mitre_trends(mitre_input)

    # ========================================================
    # 9. SESSION REPLAY
    #
    # Build once from the normalized events.
    # Store two structures:
    #  - _session_replay_list     (lightweight, full list)
    #  - _session_replay_sessions (dict for on-demand detail)
    #
    # Only sessions with replay_score >= threshold are kept
    # in the sessions dict (details). All sessions appear in
    # the list (with has_replay flag).
    # ========================================================
    replay_result = build_session_replay(normalized_events)

    replay_worthy_sessions = {}
    replay_list_entries = []

    for s in replay_result["sessions"]:
        sid = s["reconstructed_session_id"]
        score = _replay_score(s["summary"])
        has_replay = score >= _REPLAY_THRESHOLD

        replay_list_entries.append(
            _build_replay_list_entry(s, has_replay=has_replay)
        )

        if has_replay:
            replay_worthy_sessions[sid] = s

    _session_replay_sessions = replay_worthy_sessions
    _session_replay_list = {
        "contract_name": "SESSION_REPLAY_LIST",
        "contract_version": "3.0.0",
        "total_sessions": replay_result["summary"]["total_sessions"],
        "replay_worthy_count": len(replay_worthy_sessions),
        "sessions": replay_list_entries,
    }

    # ========================================================
    # 10. FINAL RESPONSE
    # ========================================================

    return {
        "status": "ok",
        "sessions_processed": len(sessions),
        "results": results,
    }


# ============================================================
# MODULE EXPORT
# ============================================================

__all__ = [
    "app",
]
