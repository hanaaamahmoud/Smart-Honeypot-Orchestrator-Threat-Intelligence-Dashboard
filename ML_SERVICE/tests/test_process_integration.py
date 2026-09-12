import json
import urllib.request


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

    request = urllib.request.Request(
        "http://localhost:8000/process",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(request) as response:
        result = json.loads(response.read().decode("utf-8"))

    assert result["status"] == "ok"
    assert result["sessions_processed"] == 2
    assert len(result["results"]) == 2

    for item in result["results"]:
        assert item["cluster_id"] is not None
        assert item["assignment_status"] == "EXISTING_PRODUCTION_CLUSTER"
        assert item["validation_status"] == "VALIDATED_48_FEATURES"

    assert [item["session_id"] for item in result["results"]] == [
        "session-a",
        "session-b",
    ]
def test_process_response_preserves_backend_session_contract():
    payload = {
        "events": [
            {
                "timestamp": "2025-01-01T00:00:00Z",
                "event_type": "auth",
                "source_ip": "10.0.0.1",
                "username": "admin",
                "session_id": "session-contract-001",
            },
            {
                "timestamp": "2025-01-01T00:00:05Z",
                "event_type": "command",
                "source_ip": "10.0.0.1",
                "username": "admin",
                "command": "whoami",
                "session_id": "session-contract-001",
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

    assert set(item.keys()) == {
        "session_id",
        "cluster_id",
        "assignment_status",
        "validation_status",
        "event_count",
        "protocol",
        "honeypot",
    }

    assert item["session_id"] == "session-contract-001"
    assert item["cluster_id"] is not None
    assert item["assignment_status"] == "EXISTING_PRODUCTION_CLUSTER"
    assert item["validation_status"] == "VALIDATED_48_FEATURES"
    assert item["event_count"] == 2
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
    assert parsed["results"][0]["session_id"] == "session-json-001"
