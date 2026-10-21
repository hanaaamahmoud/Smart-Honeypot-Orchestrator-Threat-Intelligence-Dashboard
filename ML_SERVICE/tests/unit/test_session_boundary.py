from app.analytics.session_boundary import (
    build_session_analytics_input,
)


def test_numeric_cluster_id_is_preserved():
    """
    session_boundary preserves the numeric cluster ID as-is.
    The assignment_status carries the semantic meaning.
    """
    production = {
        "reconstructed_session_id": "session-001",
        "production_cluster_assignment": 12,
        "assignment_status": "EXISTING_PRODUCTION_CLUSTER",
        "feature_validation_status": "VALIDATED_48_FEATURES",
        "event_count": 4,
    }

    original = production.copy()

    result = build_session_analytics_input([production])

    # The numeric cluster ID is preserved.
    assert result[0]["production_cluster_assignment"] == 12

    # The semantic status is preserved.
    assert result[0]["assignment_status"] == (
        "EXISTING_PRODUCTION_CLUSTER"
    )

    # Input is not mutated.
    assert production == original


def test_none_cluster_with_noise_status_is_preserved():
    """
    A None cluster ID with NOISE status is preserved.
    session_boundary does not fabricate cluster IDs.
    """
    production = {
        "reconstructed_session_id": "session-002",
        "production_cluster_assignment": None,
        "assignment_status": "NOISE",
        "feature_validation_status": "VALIDATED_48_FEATURES",
    }

    result = build_session_analytics_input([production])

    assert result[0]["production_cluster_assignment"] is None
    assert result[0]["assignment_status"] == "NOISE"


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
    assert result[0]["production_cluster_assignment"] == 7
    assert result[0]["event_count"] == 10
    assert result[0]["session_start"] == "2026-09-21T10:00:00Z"
    assert result[0]["session_end"] == "2026-09-21T10:05:00Z"
    assert result[0]["source"] == "honeypot"


def test_missing_required_fields_raise():
    """
    session_boundary requires certain fields.
    """
    import pytest

    # Missing production_cluster_assignment
    with pytest.raises(ValueError, match="production_cluster_assignment"):
        build_session_analytics_input([
            {
                "reconstructed_session_id": "s-1",
                "assignment_status": "EXISTING_PRODUCTION_CLUSTER",
            }
        ])

    # Missing assignment_status
    with pytest.raises(ValueError, match="assignment_status"):
        build_session_analytics_input([
            {
                "reconstructed_session_id": "s-1",
                "production_cluster_assignment": 5,
            }
        ])

    # Missing reconstructed_session_id
    with pytest.raises(ValueError, match="reconstructed_session_id"):
        build_session_analytics_input([
            {
                "production_cluster_assignment": 5,
                "assignment_status": "EXISTING_PRODUCTION_CLUSTER",
            }
        ])


def test_input_not_mutated():
    production = [
        {
            "reconstructed_session_id": "session-x",
            "production_cluster_assignment": 10,
            "assignment_status": "EXISTING_PRODUCTION_CLUSTER",
            "feature_validation_status": "VALIDATED_48_FEATURES",
        }
    ]

    original = [dict(r) for r in production]

    build_session_analytics_input(production)

    assert production == original
