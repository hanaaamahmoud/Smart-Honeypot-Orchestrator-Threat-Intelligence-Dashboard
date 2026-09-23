import pytest

from app.analytics.cluster_analytics import (
    NOISE_CLUSTER_ID,
    build_cluster_analytics,
)


def valid_record(
    session_id="session-001",
    cluster_id=0,
):
    return {
        "reconstructed_session_id": session_id,
        "production_cluster_assignment": cluster_id,
        "assignment_status": "EXISTING_PRODUCTION_CLUSTER",
        "nearest_behavioral_cluster": cluster_id,
        "nearest_behavioral_distance": 0.42,
        "event_count": 4,
        "session_start": "2026-09-21T10:00:00Z",
        "session_end": "2026-09-21T10:01:00Z",
        "protocol": "ssh",
        "honeypot": "cowrie",
        "source": "honeypot",
        "source_ip": "172.22.0.1",
    }


def test_empty_input_returns_valid_zero_state():
    assert build_cluster_analytics([]) == {
        "analytics_layer": "CLUSTER_ANALYTICS",
        "cluster_count": 0,
        "session_count": 0,
        "noise_session_count": 0,
        "clusters": [],
    }


def test_builds_cluster_counts():
    records = [
        valid_record("session-001", 0),
        valid_record("session-002", 0),
        valid_record("session-003", 1),
    ]

    result = build_cluster_analytics(records)

    assert result["analytics_layer"] == "CLUSTER_ANALYTICS"
    assert result["cluster_count"] == 2
    assert result["session_count"] == 3
    assert result["noise_session_count"] == 0

    assert result["clusters"] == [
        {
            "cluster_id": 0,
            "session_count": 2,
            "percentage": pytest.approx(66.6666666667),
        },
        {
            "cluster_id": 1,
            "session_count": 1,
            "percentage": pytest.approx(33.3333333333),
        },
    ]


def test_noise_is_counted_separately():
    records = [
        valid_record("session-001", 0),
        valid_record("session-002", NOISE_CLUSTER_ID),
        valid_record("session-003", NOISE_CLUSTER_ID),
        valid_record("session-004", 2),
    ]

    result = build_cluster_analytics(records)

    assert result["cluster_count"] == 2
    assert result["session_count"] == 4
    assert result["noise_session_count"] == 2

    assert result["clusters"] == [
        {
            "cluster_id": 0,
            "session_count": 1,
            "percentage": pytest.approx(25.0),
        },
        {
            "cluster_id": 2,
            "session_count": 1,
            "percentage": pytest.approx(25.0),
        },
    ]


def test_noise_is_not_returned_as_behavioral_cluster():
    records = [
        valid_record("session-001", NOISE_CLUSTER_ID),
    ]

    result = build_cluster_analytics(records)

    assert result["cluster_count"] == 0
    assert result["noise_session_count"] == 1
    assert result["clusters"] == []


def test_optional_fields_are_not_required():
    record = {
        "reconstructed_session_id": "session-001",
        "production_cluster_assignment": 3,
        "assignment_status": "EXISTING_PRODUCTION_CLUSTER",
    }

    result = build_cluster_analytics([record])

    assert result["session_count"] == 1
    assert result["cluster_count"] == 1
    assert result["clusters"][0]["cluster_id"] == 3


def test_missing_required_field_fails():
    record = valid_record()

    del record["reconstructed_session_id"]

    with pytest.raises(ValueError, match="Missing required"):
        build_cluster_analytics([record])


def test_null_required_field_fails():
    record = valid_record()

    record["assignment_status"] = None

    with pytest.raises(ValueError, match="cannot be null"):
        build_cluster_analytics([record])


def test_invalid_cluster_assignment_fails():
    record = valid_record()

    record["production_cluster_assignment"] = "NEW_CLUSTER"

    with pytest.raises(
        ValueError,
        match="production_cluster_assignment must be an integer",
    ):
        build_cluster_analytics([record])


def test_duplicate_session_id_fails():
    first = valid_record("session-001", 0)
    second = valid_record("session-001", 1)

    with pytest.raises(
        ValueError,
        match="Duplicate reconstructed_session_id",
    ):
        build_cluster_analytics([first, second])


def test_input_is_not_mutated():
    record = valid_record()
    original = record.copy()

    build_cluster_analytics([record])

    assert record == original


def test_production_assignment_is_not_changed_by_nearest_behavioral_cluster():
    record = valid_record(
        session_id="session-001",
        cluster_id=NOISE_CLUSTER_ID,
    )

    record["nearest_behavioral_cluster"] = 35

    result = build_cluster_analytics([record])

    assert result["noise_session_count"] == 1
    assert result["cluster_count"] == 0
    assert result["clusters"] == []
