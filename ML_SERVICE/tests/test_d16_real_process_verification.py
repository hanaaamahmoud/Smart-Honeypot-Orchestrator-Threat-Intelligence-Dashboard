import json
import urllib.request


def test_real_process_verification():
    payload = {
        "events": [
            {
                "timestamp": "2025-01-01T00:00:00Z",
                "event_type": "auth",
                "source_ip": "10.0.0.10",
                "username": "admin",
                "session_id": "real-session-001",
                "protocol": "SSH",
                "honeypot": "cowrie",
            },
            {
                "timestamp": "2025-01-01T00:00:05Z",
                "event_type": "command",
                "source_ip": "10.0.0.10",
                "username": "admin",
                "command": "whoami",
                "session_id": "real-session-001",
                "protocol": "SSH",
                "honeypot": "cowrie",
            },
            {
                "timestamp": "2025-01-01T00:00:12Z",
                "event_type": "command",
                "source_ip": "10.0.0.10",
                "username": "admin",
                "command": "uname -a",
                "session_id": "real-session-001",
                "protocol": "SSH",
                "honeypot": "cowrie",
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

    assert result["status"] == "ok"
    assert result["sessions_processed"] == 1
    assert len(result["results"]) == 1

    item = result["results"][0]

    assert item["reconstructed_session_id"] == "real-session-001"
    assert item["event_count"] == 3

    assert item["production_cluster_assignment"] is not None
    assert item["assignment_status"] == "EXISTING_PRODUCTION_CLUSTER"

    assert item["feature_validation_status"] == "VALIDATED_48_FEATURES"

    assert item["source"] is None
    assert item["protocol"] == "SSH"
    assert item["honeypot"] == "cowrie"

    assert item["session_start"] is not None
    assert item["session_end"] is not None
