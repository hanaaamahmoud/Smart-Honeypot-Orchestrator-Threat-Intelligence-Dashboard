from app.main import load_production_model, process
from app.schemas import ProcessRequest


def test_process_runtime_wires_session_analytics():
    load_production_model()

    request = ProcessRequest(
        events=[
            {
                "timestamp": "2025-01-01T00:00:00Z",
                "event_type": "auth",
                "source_ip": "10.0.0.1",
                "username": "admin",
                "session_id": "runtime-session-001",
                "protocol": "SSH",
                "honeypot": "cowrie",
            },
            {
                "timestamp": "2025-01-01T00:00:05Z",
                "event_type": "command",
                "source_ip": "10.0.0.1",
                "username": "admin",
                "command": "whoami",
                "session_id": "runtime-session-001",
                "protocol": "SSH",
                "honeypot": "cowrie",
            },
        ]
    )

    response = process(request)

    assert response["status"] == "ok"
    assert response["sessions_processed"] == 1
    assert len(response["results"]) == 1

    result = response["results"][0]

    assert result["reconstructed_session_id"] == "runtime-session-001"
    assert isinstance(result["production_cluster_assignment"], int)
    assert result["assignment_status"] == "EXISTING_PRODUCTION_CLUSTER"
    assert result["feature_validation_status"] == "VALIDATED_48_FEATURES"
    assert result["event_count"] == 2
    assert result["protocol"] == "SSH"
    assert result["honeypot"] == "cowrie"
