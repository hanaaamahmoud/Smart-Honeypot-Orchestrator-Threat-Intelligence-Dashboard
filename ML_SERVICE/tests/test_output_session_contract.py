from app.schemas import SessionResult
import json


def test_session_result_contract_preserves_values():
    result = SessionResult(
        reconstructed_session_id="session-001",
        production_cluster_assignment=12,
        assignment_status="EXISTING_PRODUCTION_CLUSTER",
        feature_validation_status="VALIDATED_48_FEATURES",
        event_count=15,
        protocol="SSH",
        honeypot="cowrie",
    )

    assert result.reconstructed_session_id == "session-001"
    assert result.production_cluster_assignment == 12
    assert result.assignment_status == "EXISTING_PRODUCTION_CLUSTER"
    assert result.feature_validation_status == "VALIDATED_48_FEATURES"
    assert result.event_count == 15
    assert result.protocol == "SSH"
    assert result.honeypot == "cowrie"


def test_session_result_optional_values_can_be_null():
    result = SessionResult(
        reconstructed_session_id="session-002",
        production_cluster_assignment=None,
        assignment_status="EXISTING_PRODUCTION_CLUSTER",
        feature_validation_status="VALIDATED_48_FEATURES",
        event_count=1,
        protocol=None,
        honeypot=None,
    )

    assert result.reconstructed_session_id == "session-002"
    assert result.production_cluster_assignment is None
    assert result.protocol is None
    assert result.honeypot is None


def test_session_result_serializes_to_json():
    result = SessionResult(
        reconstructed_session_id="session-003",
        production_cluster_assignment=7,
        assignment_status="EXISTING_PRODUCTION_CLUSTER",
        feature_validation_status="VALIDATED_48_FEATURES",
        event_count=5,
        protocol="SSH",
        honeypot="cowrie",
    )

    payload = json.loads(result.model_dump_json())

    assert payload["reconstructed_session_id"] == "session-003"
    assert payload["production_cluster_assignment"] == 7
    assert payload["assignment_status"] == "EXISTING_PRODUCTION_CLUSTER"
    assert payload["feature_validation_status"] == "VALIDATED_48_FEATURES"
    assert payload["event_count"] == 5
    assert payload["protocol"] == "SSH"
    assert payload["honeypot"] == "cowrie"


def test_session_result_preserves_session_id_exactly():
    original_session_id = "session-original-123"

    result = SessionResult(
        reconstructed_session_id=original_session_id,
        production_cluster_assignment=12,
        assignment_status="EXISTING_PRODUCTION_CLUSTER",
        feature_validation_status="VALIDATED_48_FEATURES",
        event_count=15,
        protocol="SSH",
        honeypot="cowrie",
    )

    payload = json.loads(result.model_dump_json())

    assert payload["reconstructed_session_id"] == original_session_id


def test_session_result_preserves_cluster_and_assignment_status():
    result = SessionResult(
        reconstructed_session_id="session-004",
        production_cluster_assignment=12,
        assignment_status="EXISTING_PRODUCTION_CLUSTER",
        feature_validation_status="VALIDATED_48_FEATURES",
        event_count=15,
        protocol="SSH",
        honeypot="cowrie",
    )

    payload = json.loads(result.model_dump_json())

    assert payload["production_cluster_assignment"] == 12
    assert payload["assignment_status"] == "EXISTING_PRODUCTION_CLUSTER"


def test_session_result_preserves_validation_status_and_event_count():
    result = SessionResult(
        reconstructed_session_id="session-005",
        production_cluster_assignment=12,
        assignment_status="EXISTING_PRODUCTION_CLUSTER",
        feature_validation_status="VALIDATED_48_FEATURES",
        event_count=15,
        protocol="SSH",
        honeypot="cowrie",
    )

    payload = json.loads(result.model_dump_json())

    assert payload["feature_validation_status"] == "VALIDATED_48_FEATURES"
    assert payload["event_count"] == 15
