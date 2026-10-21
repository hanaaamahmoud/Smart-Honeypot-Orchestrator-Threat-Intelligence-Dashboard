import json
import urllib.request


REQUIRED_RESULT_FIELDS = {
    "reconstructed_session_id",
    "production_cluster_assignment",
    "assignment_status",
    "feature_validation_status",
    "event_count",
    "session_start",
    "session_end",
    "source",
    "protocol",
    "honeypot",
}

LEGACY_RESULT_FIELDS = {
    "session_id",
    "cluster_id",
    "cluster",
    "behavior",
    "source_dataset",
    "start_time",
    "end_time",
}


def post_process(payload):
    request = urllib.request.Request(
        "http://localhost:8000/process",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(request) as response:
        return json.loads(response.read().decode("utf-8"))


def test_process_runs_full_frozen_pipeline():
    payload = {
        "events": [
            {
                "timestamp": "2025-01-01T00:00:00Z",
                "event_type": "auth",
                "source_ip": "10.0.0.1",
                "username": "admin",
                "session_id": "session-a",
            },
            {
                "timestamp": "2025-01-01T00:00:05Z",
                "event_type": "command",
                "source_ip": "10.0.0.1",
                "username": "admin",
                "command": "whoami",
                "session_id": "session-a",
            },
            {
                "timestamp": "2025-01-01T00:01:00Z",
                "event_type": "auth",
                "source_ip": "10.0.0.2",
                "username": "root",
                "session_id": "session-b",
            },
        ]
    }

    result = post_process(payload)

    assert result["status"] == "ok"
    assert result["sessions_processed"] == 2
    assert len(result["results"]) == 2

    for item in result["results"]:
        assert item["production_cluster_assignment"] is not None
        assert item["assignment_status"] == "EXISTING_PRODUCTION_CLUSTER"
        assert item["feature_validation_status"] == "VALIDATED_48_FEATURES"

    assert [item["reconstructed_session_id"] for item in result["results"]] == [
        "session-a",
        "session-b",
    ]


def test_process_response_has_exact_canonical_fields():
    payload = {
        "events": [
            {
                "timestamp": "2025-01-01T00:00:00Z",
                "event_type": "auth",
                "source_ip": "10.0.0.1",
                "username": "admin",
                "session_id": "session-contract-001",
                "protocol": "SSH",
                "honeypot": "cowrie",
            },
            {
                "timestamp": "2025-01-01T00:00:05Z",
                "event_type": "command",
                "source_ip": "10.0.0.1",
                "username": "admin",
                "command": "whoami",
                "session_id": "session-contract-001",
                "protocol": "SSH",
                "honeypot": "cowrie",
            },
        ]
    }

    result = post_process(payload)

    assert result["status"] == "ok"
    assert result["sessions_processed"] == 1

    item = result["results"][0]

    assert set(item.keys()) == REQUIRED_RESULT_FIELDS
    assert not set(item.keys()).intersection(LEGACY_RESULT_FIELDS)


def test_process_response_has_correct_field_types():
    payload = {
        "events": [
            {
                "timestamp": "2025-01-01T00:00:00Z",
                "event_type": "auth",
                "source_ip": "10.0.0.1",
                "username": "admin",
                "session_id": "session-types-001",
                "protocol": "SSH",
                "honeypot": "cowrie",
            },
            {
                "timestamp": "2025-01-01T00:00:05Z",
                "event_type": "command",
                "source_ip": "10.0.0.1",
                "username": "admin",
                "command": "whoami",
                "session_id": "session-types-001",
                "protocol": "SSH",
                "honeypot": "cowrie",
            },
        ]
    }

    result = post_process(payload)
    item = result["results"][0]

    assert isinstance(item["reconstructed_session_id"], str)
    assert isinstance(item["production_cluster_assignment"], int)
    assert isinstance(item["assignment_status"], str)
    assert isinstance(item["feature_validation_status"], str)
    assert isinstance(item["event_count"], int)

    assert item["session_start"] is None or isinstance(
        item["session_start"],
        str,
    )
    assert item["session_end"] is None or isinstance(
        item["session_end"],
        str,
    )
    assert item["source"] is None or isinstance(item["source"], str)
    assert item["protocol"] is None or isinstance(item["protocol"], str)
    assert item["honeypot"] is None or isinstance(item["honeypot"], str)


def test_process_response_allows_none_for_optional_fields():
    payload = {
        "events": [
            {
                "timestamp": "2025-01-01T00:00:00Z",
                "event_type": "auth",
                "source_ip": "10.0.0.1",
                "username": "admin",
                "session_id": "session-optional-001",
            },
            {
                "timestamp": "2025-01-01T00:00:05Z",
                "event_type": "command",
                "source_ip": "10.0.0.1",
                "username": "admin",
                "command": "whoami",
                "session_id": "session-optional-001",
            },
        ]
    }

    result = post_process(payload)
    item = result["results"][0]

    assert item["source"] is None
    assert item["protocol"] is None
    assert item["honeypot"] is None


def test_process_response_preserves_backend_session_contract():
    payload = {
        "events": [
            {
                "timestamp": "2025-01-01T00:00:00Z",
                "event_type": "auth",
                "source_ip": "10.0.0.1",
                "username": "admin",
                "session_id": "session-contract-001",
                "protocol": "SSH",
                "honeypot": "cowrie",
            },
            {
                "timestamp": "2025-01-01T00:00:05Z",
                "event_type": "command",
                "source_ip": "10.0.0.1",
                "username": "admin",
                "command": "whoami",
                "session_id": "session-contract-001",
                "protocol": "SSH",
                "honeypot": "cowrie",
            },
        ]
    }

    result = post_process(payload)

    assert result["status"] == "ok"
    assert result["sessions_processed"] == 1

    item = result["results"][0]

    assert set(item.keys()) == REQUIRED_RESULT_FIELDS

    assert item["reconstructed_session_id"] == "session-contract-001"
    assert item["production_cluster_assignment"] is not None
    assert item["assignment_status"] == "EXISTING_PRODUCTION_CLUSTER"
    assert item["feature_validation_status"] == "VALIDATED_48_FEATURES"
    assert item["event_count"] == 2

    assert item["source"] is None
    assert item["protocol"] == "SSH"
    assert item["honeypot"] == "cowrie"


def test_process_response_is_strict_json():
    payload = {
        "events": [
            {
                "timestamp": "2025-01-01T00:00:00Z",
                "event_type": "auth",
                "source_ip": "10.0.0.1",
                "username": "admin",
                "session_id": "session-json-001",
            },
            {
                "timestamp": "2025-01-01T00:00:05Z",
                "event_type": "command",
                "source_ip": "10.0.0.1",
                "username": "admin",
                "command": "whoami",
                "session_id": "session-json-001",
            },
        ]
    }

    result = post_process(payload)

    strict_payload = json.dumps(
        result,
        allow_nan=False,
    )

    parsed = json.loads(strict_payload)

    assert parsed["status"] == "ok"
    assert parsed["sessions_processed"] == 1
    assert (
        parsed["results"][0]["reconstructed_session_id"]
        == "session-json-001"
    )
def test_process_assignment_status_is_existing_production_cluster():
    payload = {
        "events": [
            {
                "timestamp": "2025-01-01T00:00:00Z",
                "event_type": "auth",
                "source_ip": "10.0.0.1",
                "username": "admin",
                "session_id": "session-assignment-001",
            },
            {
                "timestamp": "2025-01-01T00:00:05Z",
                "event_type": "command",
                "source_ip": "10.0.0.1",
                "username": "admin",
                "command": "whoami",
                "session_id": "session-assignment-001",
            },
        ]
    }

    result = post_process(payload)

    assert result["status"] == "ok"
    assert result["sessions_processed"] == 1

    item = result["results"][0]

    assert item["assignment_status"] == "EXISTING_PRODUCTION_CLUSTER"
    assert item["production_cluster_assignment"] is not None
def test_process_feature_validation_status():
    payload = {
        "events": [
            {
                "timestamp": "2025-01-01T00:00:00Z",
                "event_type": "auth",
                "source_ip": "10.0.0.1",
                "username": "admin",
                "session_id": "session-validation-001",
            },
            {
                "timestamp": "2025-01-01T00:00:05Z",
                "event_type": "command",
                "source_ip": "10.0.0.1",
                "username": "admin",
                "command": "whoami",
                "session_id": "session-validation-001",
            },
        ]
    }

    request = urllib.request.Request(
        "http://localhost:8000/process",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(request) as response:
        result = json.loads(response.read().decode("utf-8"))

    assert result["status"] == "ok"
    assert result["sessions_processed"] == 1

    item = result["results"][0]

    assert item["feature_validation_status"] == (
        "VALIDATED_48_FEATURES"
    )


def test_process_does_not_fabricate_optional_values():
    payload = {
        "events": [
            {
                "timestamp": "2025-01-01T00:00:00Z",
                "event_type": "auth",
                "source_ip": "10.0.0.1",
                "username": "admin",
                "session_id": "session-no-fabrication-001",
            },
            {
                "timestamp": "2025-01-01T00:00:05Z",
                "event_type": "command",
                "source_ip": "10.0.0.1",
                "username": "admin",
                "command": "whoami",
                "session_id": "session-no-fabrication-001",
            },
        ]
    }

    request = urllib.request.Request(
        "http://localhost:8000/process",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(request) as response:
        result = json.loads(response.read().decode("utf-8"))

    assert result["status"] == "ok"

    item = result["results"][0]

    # These fields were not supplied by the input events.
    # The service must not invent values for them.
    assert item["source"] is None
    assert item["protocol"] is None
    assert item["honeypot"] is None


def test_process_response_is_strict_json_d15():
    payload = {
        "events": [
            {
                "timestamp": "2025-01-01T00:00:00Z",
                "event_type": "auth",
                "source_ip": "10.0.0.1",
                "username": "admin",
                "session_id": "session-strict-json-001",
            },
            {
                "timestamp": "2025-01-01T00:00:05Z",
                "event_type": "command",
                "source_ip": "10.0.0.1",
                "username": "admin",
                "command": "whoami",
                "session_id": "session-strict-json-001",
            },
        ]
    }

    request = urllib.request.Request(
        "http://localhost:8000/process",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(request) as response:
        raw_response = response.read().decode("utf-8")

    result = json.loads(raw_response)

    strict_payload = json.dumps(
        result,
        allow_nan=False,
    )

    parsed = json.loads(strict_payload)

    assert parsed["status"] == "ok"
    assert parsed["sessions_processed"] == 1
    assert len(parsed["results"]) == 1


def test_process_metadata_consistency_d15():
    payload = {
        "events": [
            {
                "timestamp": "2025-01-01T00:00:00Z",
                "event_type": "auth",
                "source_ip": "10.0.0.1",
                "username": "admin",
                "session_id": "session-metadata-001",
            },
            {
                "timestamp": "2025-01-01T00:00:05Z",
                "event_type": "command",
                "source_ip": "10.0.0.1",
                "username": "admin",
                "command": "whoami",
                "session_id": "session-metadata-001",
            },
        ]
    }

    request = urllib.request.Request(
        "http://localhost:8000/process",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(request) as response:
        result = json.loads(response.read().decode("utf-8"))

    assert result["status"] == "ok"
    assert result["sessions_processed"] == len(
        result["results"]
    )

    for item in result["results"]:
        assert item["assignment_status"] == (
            "EXISTING_PRODUCTION_CLUSTER"
        )

        assert item["feature_validation_status"] == (
            "VALIDATED_48_FEATURES"
        )

        assert item["event_count"] == 2

        assert item["session_start"] == (
            "2025-01-01T00:00:00+00:00"
        )

        assert item["session_end"] == (
            "2025-01-01T00:00:05+00:00"
        )

        assert item["reconstructed_session_id"] == (
            "session-metadata-001"
        )
