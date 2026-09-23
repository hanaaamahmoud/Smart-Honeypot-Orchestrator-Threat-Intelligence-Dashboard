from app.analytics.session_analytics import build_session_analytics
from app.analytics.session_boundary import (
    build_session_analytics_input,
)


def test_production_output_flows_into_session_analytics():
    production_results = [
        {
            "reconstructed_session_id": "session-001",
            "production_cluster_assignment": 12,
            "assignment_status": "EXISTING_PRODUCTION_CLUSTER",
            "feature_validation_status": "VALIDATED_48_FEATURES",
            "event_count": 4,
            "session_start": "2026-09-21T10:00:00Z",
            "session_end": "2026-09-21T10:01:00Z",
            "source": "honeypot",
        }
    ]

    analytics_input = build_session_analytics_input(
        production_results
    )

    analytics_results = build_session_analytics(
        analytics_input
    )

    assert len(analytics_results) == 1

    row = analytics_results[0]

    assert row["reconstructed_session_id"] == "session-001"
    assert row["production_cluster_assignment"] == (
        "EXISTING_PRODUCTION_CLUSTER"
    )
    assert row["assignment_status"] == (
        "EXISTING_PRODUCTION_CLUSTER"
    )
    assert row["feature_validation_status"] == (
        "VALIDATED_48_FEATURES"
    )

    assert row["event_count"] == 4
    assert row["source"] == "honeypot"


def test_production_result_is_not_modified_by_analytics_boundary():
    production_results = [
        {
            "reconstructed_session_id": "session-002",
            "production_cluster_assignment": 7,
            "assignment_status": "EXISTING_PRODUCTION_CLUSTER",
            "feature_validation_status": "VALIDATED_48_FEATURES",
        }
    ]

    original = [dict(row) for row in production_results]

    analytics_input = build_session_analytics_input(
        production_results
    )

    build_session_analytics(analytics_input)

    assert production_results == original
    assert production_results[0]["production_cluster_assignment"] == 7
