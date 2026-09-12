from app.pipeline.session_contract import SessionContract


def test_session_contract_shape():
    session: SessionContract = {
        "session_id": "session-001",
        "events": [
            {
                "session_id": "session-001",
                "timestamp": "2026-01-01T10:00:00Z",
            }
        ],
        "event_count": 1,
        "start_time": "2026-01-01T10:00:00Z",
        "end_time": "2026-01-01T10:00:00Z",
        "duration_seconds": 0.0,
    }

    assert isinstance(session["session_id"], str)
    assert isinstance(session["events"], list)
    assert isinstance(session["event_count"], int)
    assert isinstance(session["start_time"], str)
    assert isinstance(session["end_time"], str)
    assert isinstance(session["duration_seconds"], float)
