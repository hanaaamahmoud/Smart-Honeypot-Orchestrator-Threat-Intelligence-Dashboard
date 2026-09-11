import json

import pytest

from app.output_adapter import (
    adapt_analytics_result,
    adapt_session_result,
)


def test_adapt_session_result_returns_backend_contract():
    result = {
        "session_id": "session-001",
        "cluster_id": 12,
        "assignment_status": "EXISTING_PRODUCTION_CLUSTER",
        "validation_status": "VALIDATED_48_FEATURES",
        "event_count": 15,
        "protocol": "SSH",
        "honeypot": "cowrie",
    }

    adapted = adapt_session_result(result)

    assert adapted == {
        "session_id": "session-001",
        "cluster_id": 12,
        "assignment_status": "EXISTING_PRODUCTION_CLUSTER",
        "validation_status": "VALIDATED_48_FEATURES",
        "event_count": 15,
        "protocol": "SSH",
        "honeypot": "cowrie",
    }


def test_adapt_analytics_result_returns_backend_contract():
    result = {
        "cluster_id": 12,
        "session_count": 20,
        "event_count": 340,
        "top_commands": [],
        "attack_types": [],
        "mitre_techniques": [],
    }

    adapted = adapt_analytics_result(result)

    assert adapted == {
        "cluster_id": 12,
        "session_count": 20,
        "event_count": 340,
        "top_commands": [],
        "attack_types": [],
        "mitre_techniques": [],
    }


def test_adapt_session_result_does_not_modify_input():
    result = {
        "session_id": "session-002",
        "cluster_id": 5,
        "assignment_status": "EXISTING_PRODUCTION_CLUSTER",
        "validation_status": "VALIDATED_48_FEATURES",
        "event_count": 3,
        "protocol": "SSH",
        "honeypot": "cowrie",
    }

    original = result.copy()

    adapt_session_result(result)

    assert result == original


def test_adapt_analytics_result_does_not_modify_input():
    result = {
        "cluster_id": 5,
        "session_count": 2,
        "event_count": 10,
        "top_commands": ["ls"],
        "attack_types": ["brute_force"],
        "mitre_techniques": ["T1110"],
    }

    original = {
        "cluster_id": 5,
        "session_count": 2,
        "event_count": 10,
        "top_commands": ["ls"],
        "attack_types": ["brute_force"],
        "mitre_techniques": ["T1110"],
    }

    adapt_analytics_result(result)

    assert result == original


def test_adapt_session_result_sanitizes_special_float_values():
    result = {
        "session_id": "session-003",
        "cluster_id": float("nan"),
        "assignment_status": "EXISTING_PRODUCTION_CLUSTER",
        "validation_status": "VALIDATED_48_FEATURES",
        "event_count": 3,
        "protocol": float("inf"),
        "honeypot": float("-inf"),
    }

    adapted = adapt_session_result(result)

    assert adapted["cluster_id"] is None
    assert adapted["protocol"] is None
    assert adapted["honeypot"] is None


def test_adapt_analytics_result_sanitizes_special_float_values():
    result = {
        "cluster_id": 12,
        "session_count": float("nan"),
        "event_count": float("inf"),
        "top_commands": [],
        "attack_types": [],
        "mitre_techniques": [],
    }

    adapted = adapt_analytics_result(result)

    assert adapted["session_count"] is None
    assert adapted["event_count"] is None


def test_adapted_session_result_is_strict_json():
    result = {
        "session_id": "session-004",
        "cluster_id": float("nan"),
        "assignment_status": "EXISTING_PRODUCTION_CLUSTER",
        "validation_status": "VALIDATED_48_FEATURES",
        "event_count": 3,
        "protocol": float("inf"),
        "honeypot": float("-inf"),
    }

    adapted = adapt_session_result(result)

    payload = json.dumps(adapted, allow_nan=False)

    assert json.loads(payload)["cluster_id"] is None
    assert json.loads(payload)["protocol"] is None
    assert json.loads(payload)["honeypot"] is None


def test_adapted_analytics_result_is_strict_json():
    result = {
        "cluster_id": 12,
        "session_count": float("nan"),
        "event_count": float("inf"),
        "top_commands": [],
        "attack_types": [],
        "mitre_techniques": [],
    }

    adapted = adapt_analytics_result(result)

    payload = json.dumps(adapted, allow_nan=False)

    parsed = json.loads(payload)

    assert parsed["session_count"] is None
    assert parsed["event_count"] is None


def test_adapt_session_result_has_exact_backend_fields():
    result = {
        "session_id": "session-005",
        "cluster_id": 12,
        "assignment_status": "EXISTING_PRODUCTION_CLUSTER",
        "validation_status": "VALIDATED_48_FEATURES",
        "event_count": 15,
        "protocol": "SSH",
        "honeypot": "cowrie",
    }

    adapted = adapt_session_result(result)

    assert set(adapted.keys()) == {
        "session_id",
        "cluster_id",
        "assignment_status",
        "validation_status",
        "event_count",
        "protocol",
        "honeypot",
    }


def test_adapt_analytics_result_has_exact_backend_fields():
    result = {
        "cluster_id": 12,
        "session_count": 20,
        "event_count": 340,
        "top_commands": [],
        "attack_types": [],
        "mitre_techniques": [],
    }

    adapted = adapt_analytics_result(result)

    assert set(adapted.keys()) == {
        "cluster_id",
        "session_count",
        "event_count",
        "top_commands",
        "attack_types",
        "mitre_techniques",
    }


@pytest.mark.parametrize(
    "missing_field",
    [
        "session_id",
        "assignment_status",
        "validation_status",
    ],
)
def test_adapt_session_result_requires_mandatory_fields(missing_field):
    result = {
        "session_id": "session-required-001",
        "cluster_id": 12,
        "assignment_status": "EXISTING_PRODUCTION_CLUSTER",
        "validation_status": "VALIDATED_48_FEATURES",
        "event_count": 15,
        "protocol": "SSH",
        "honeypot": "cowrie",
    }

    del result[missing_field]

    with pytest.raises(KeyError):
        adapt_session_result(result)
def test_adapt_analytics_result_requires_cluster_id():
    result = {
        "session_count": 20,
        "event_count": 340,
        "top_commands": [],
        "attack_types": [],
        "mitre_techniques": [],
    }

    with pytest.raises(KeyError):
        adapt_analytics_result(result)
def test_adapt_session_result_preserves_session_and_cluster_identity():
    result = {
        "session_id": "session-identity-123",
        "cluster_id": 42,
        "assignment_status": "EXISTING_PRODUCTION_CLUSTER",
        "validation_status": "VALIDATED_48_FEATURES",
        "event_count": 15,
        "protocol": "SSH",
        "honeypot": "cowrie",
    }

    adapted = adapt_session_result(result)

    assert adapted["session_id"] == "session-identity-123"
    assert adapted["cluster_id"] == 42


def test_adapt_session_result_preserves_status_values():
    result = {
        "session_id": "session-status-123",
        "cluster_id": 42,
        "assignment_status": "EXISTING_PRODUCTION_CLUSTER",
        "validation_status": "VALIDATED_48_FEATURES",
        "event_count": 15,
        "protocol": "SSH",
        "honeypot": "cowrie",
    }

    adapted = adapt_session_result(result)

    assert adapted["assignment_status"] == "EXISTING_PRODUCTION_CLUSTER"
    assert adapted["validation_status"] == "VALIDATED_48_FEATURES"
def test_adapt_session_result_contains_no_non_finite_floats():
    result = {
        "session_id": "session-json-001",
        "cluster_id": float("nan"),
        "assignment_status": "EXISTING_PRODUCTION_CLUSTER",
        "validation_status": "VALIDATED_48_FEATURES",
        "event_count": float("inf"),
        "protocol": "SSH",
        "honeypot": "cowrie",
    }

    adapted = adapt_session_result(result)

    assert all(
        not (isinstance(value, float) and not __import__("math").isfinite(value))
        for value in adapted.values()
    )


def test_adapt_analytics_result_contains_no_non_finite_floats():
    result = {
        "cluster_id": 12,
        "session_count": float("nan"),
        "event_count": float("-inf"),
        "top_commands": [],
        "attack_types": [],
        "mitre_techniques": [],
    }

    adapted = adapt_analytics_result(result)

    assert all(
        not (isinstance(value, float) and not __import__("math").isfinite(value))
        for value in adapted.values()
    )
