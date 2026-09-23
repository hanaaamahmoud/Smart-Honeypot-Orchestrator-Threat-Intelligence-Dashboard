import pytest

from app.analytics.session_analytics import build_session_analytics


def valid_record():
    return {
        "reconstructed_session_id": "session-001",
        "production_cluster_assignment": "EXISTING_PRODUCTION_CLUSTER",
        "assignment_status": "ASSIGNED",
        "feature_validation_status": "PASS",
        "event_count": 4,
        "session_start": "2026-09-21T10:00:00Z",
        "session_end": "2026-09-21T10:01:00Z",
        "source": "honeypot",
    }


def test_preserves_validated_session_assignment():
    record = valid_record()

    assert build_session_analytics([record]) == [record]


def test_one_output_row_per_session():
    first = valid_record()
    second = valid_record()
    second["reconstructed_session_id"] = "session-002"

    result = build_session_analytics([first, second])

    assert len(result) == 2
    assert [
        row["reconstructed_session_id"]
        for row in result
    ] == ["session-001", "session-002"]


def test_optional_fields_are_not_fabricated():
    record = {
        "reconstructed_session_id": "session-001",
        "production_cluster_assignment": "NOISE",
        "assignment_status": "ASSIGNED",
        "feature_validation_status": "PASS",
    }

    assert build_session_analytics([record]) == [record]


def test_missing_required_field_fails():
    record = valid_record()
    del record["reconstructed_session_id"]

    with pytest.raises(ValueError, match="Missing required"):
        build_session_analytics([record])


def test_null_required_field_fails():
    record = valid_record()
    record["feature_validation_status"] = None

    with pytest.raises(ValueError, match="cannot be null"):
        build_session_analytics([record])


def test_invalid_cluster_assignment_fails():
    record = valid_record()
    record["production_cluster_assignment"] = "NEW_CLUSTER"

    with pytest.raises(
        ValueError,
        match="production_cluster_assignment",
    ):
        build_session_analytics([record])


def test_input_is_not_mutated():
    record = valid_record()
    original = record.copy()

    build_session_analytics([record])

    assert record == original
