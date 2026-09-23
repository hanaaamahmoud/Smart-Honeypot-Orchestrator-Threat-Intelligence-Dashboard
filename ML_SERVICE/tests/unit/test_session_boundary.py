from app.analytics.session_boundary import (
    build_session_analytics_input,
)


def test_numeric_production_cluster_is_translated_for_analytics():
    production = {
        "reconstructed_session_id": "session-001",
        "production_cluster_assignment": 12,
        "assignment_status": "EXISTING_PRODUCTION_CLUSTER",
        "feature_validation_status": "VALIDATED_48_FEATURES",
        "event_count": 4,
    }

    original = production.copy()

    result = build_session_analytics_input([production])

    assert result[0]["production_cluster_assignment"] == (
        "EXISTING_PRODUCTION_CLUSTER"
    )

    assert production == original


def test_missing_production_cluster_becomes_noise_for_analytics():
    production = {
        "reconstructed_session_id": "session-002",
        "production_cluster_assignment": None,
        "assignment_status": "NOISE",
        "feature_validation_status": "VALIDATED_48_FEATURES",
    }

    result = build_session_analytics_input([production])

    assert result[0]["production_cluster_assignment"] == "NOISE"


def test_all_other_production_fields_are_preserved():
    production = {
        "reconstructed_session_id": "session-003",
        "production_cluster_assignment": 7,
        "assignment_status": "EXISTING_PRODUCTION_CLUSTER",
        "feature_validation_status": "VALIDATED_48_FEATURES",
        "event_count": 10,
        "session_start": "2026-09-21T10:00:00Z",
        "session_end": "2026-09-21T10:05:00Z",
        "source": "honeypot",
    }

    result = build_session_analytics_input([production])

    assert result[0]["reconstructed_session_id"] == "session-003"
    assert result[0]["event_count"] == 10
    assert result[0]["session_start"] == (
        "2026-09-21T10:00:00Z"
    )
    assert result[0]["session_end"] == (
        "2026-09-21T10:05:00Z"
    )
    assert result[0]["source"] == "honeypot"
