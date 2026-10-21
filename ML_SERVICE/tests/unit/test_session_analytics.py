"""Unit tests for session_analytics adapter."""

import pytest

from app.analytics.session_analytics import (
    ALLOWED_ASSIGNMENT_STATUS,
    NOISE_CLUSTER_ID,
    OUTPUT_FIELDS,
    REQUIRED_FIELDS,
    build_session_analytics,
)


def valid_record(**overrides):
    record = {
        "reconstructed_session_id": "session-001",
        "production_cluster_assignment": 5,
        "assignment_status": "EXISTING_PRODUCTION_CLUSTER",
        "feature_validation_status": "VALIDATED_48_FEATURES",
        "event_count": 4,
        "session_start": "2026-09-21T10:00:00Z",
        "session_end": "2026-09-21T10:01:00Z",
        "distance": 0.42,
        "honeypot": "cowrie",
        "protocol": "SSH",
        "source_ip": "1.2.3.4",
        "country": "Egypt",
        "attack_type": "SSH Connection Probe",
        "mitre_technique": "T1595",
        "attack_stage": "Reconnaissance",
        "severity": "Low",
    }
    record.update(overrides)
    return record


# ---------------------------------------------------------------
# Basic behavior
# ---------------------------------------------------------------

def test_single_valid_record():
    record = valid_record()
    result = build_session_analytics([record])
    assert len(result) == 1
    assert result[0]["reconstructed_session_id"] == "session-001"
    assert result[0]["production_cluster_assignment"] == 5
    assert result[0]["assignment_status"] == "EXISTING_PRODUCTION_CLUSTER"


def test_one_output_row_per_session():
    records = [
        valid_record(reconstructed_session_id="s-1"),
        valid_record(reconstructed_session_id="s-2", production_cluster_assignment=10),
        valid_record(reconstructed_session_id="s-3", production_cluster_assignment=NOISE_CLUSTER_ID, assignment_status="NOISE"),
    ]
    result = build_session_analytics(records)
    assert len(result) == 3
    assert [r["reconstructed_session_id"] for r in result] == ["s-1", "s-2", "s-3"]


def test_empty_input_returns_empty_list():
    assert build_session_analytics([]) == []


# ---------------------------------------------------------------
# Noise handling
# ---------------------------------------------------------------

def test_noise_cluster_is_valid():
    record = valid_record(
        production_cluster_assignment=NOISE_CLUSTER_ID,
        assignment_status="NOISE",
    )
    result = build_session_analytics([record])
    assert result[0]["production_cluster_assignment"] == -1
    assert result[0]["assignment_status"] == "NOISE"


# ---------------------------------------------------------------
# Optional fields
# ---------------------------------------------------------------

def test_optional_fields_are_preserved_when_present():
    record = valid_record()
    result = build_session_analytics([record])
    assert result[0]["honeypot"] == "cowrie"
    assert result[0]["mitre_technique"] == "T1595"


def test_optional_fields_are_not_fabricated():
    record = {
        "reconstructed_session_id": "s-1",
        "production_cluster_assignment": 5,
        "assignment_status": "EXISTING_PRODUCTION_CLUSTER",
        "feature_validation_status": "VALIDATED_48_FEATURES",
    }
    result = build_session_analytics([record])
    assert "honeypot" not in result[0]
    assert "event_count" not in result[0]


# ---------------------------------------------------------------
# Validation failures
# ---------------------------------------------------------------

def test_missing_required_field_fails():
    record = valid_record()
    del record["reconstructed_session_id"]
    with pytest.raises(ValueError, match="Missing required"):
        build_session_analytics([record])


def test_null_required_field_fails():
    record = valid_record(feature_validation_status=None)
    with pytest.raises(ValueError, match="cannot be null"):
        build_session_analytics([record])


def test_non_integer_cluster_fails():
    record = valid_record(production_cluster_assignment="EXISTING_PRODUCTION_CLUSTER")
    with pytest.raises(ValueError, match="must be an integer"):
        build_session_analytics([record])


def test_bool_cluster_fails():
    record = valid_record(production_cluster_assignment=True)
    with pytest.raises(ValueError, match="must be an integer"):
        build_session_analytics([record])


def test_invalid_assignment_status_fails():
    record = valid_record(assignment_status="NEW_CLUSTER")
    with pytest.raises(ValueError, match="assignment_status"):
        build_session_analytics([record])


def test_empty_session_id_fails():
    record = valid_record(reconstructed_session_id="   ")
    with pytest.raises(ValueError, match="non-empty string"):
        build_session_analytics([record])


# ---------------------------------------------------------------
# Immutability
# ---------------------------------------------------------------

def test_input_is_not_mutated():
    record = valid_record()
    original = dict(record)
    build_session_analytics([record])
    assert record == original


def test_output_is_a_copy():
    record = valid_record()
    result = build_session_analytics([record])
    result[0]["honeypot"] = "MODIFIED"
    assert record["honeypot"] == "cowrie"


# ---------------------------------------------------------------
# Schema
# ---------------------------------------------------------------

def test_output_contains_required_fields():
    result = build_session_analytics([valid_record()])
    for field in REQUIRED_FIELDS:
        assert field in result[0]
