from copy import deepcopy

from app.pipeline.feature_generation_base import (
    generate_base_features,
)


def _sample_session():
    return {
        "session_id": "session-A",
        "events": [
            {
                "session_id": "session-A",
                "timestamp": "2026-01-01T10:00:00Z",
                "event_type": "auth",
                "username": "root",
                "password": "bad-password",
            },
            {
                "session_id": "session-A",
                "timestamp": "2026-01-01T10:01:00Z",
                "event_type": "auth",
                "username": "",
            },
            {
                "session_id": "session-A",
                "timestamp": "2026-01-01T10:02:00Z",
                "event_type": "command",
                "username": "root",
                "command": "whoami",
            },
            {
                "session_id": "session-A",
                "timestamp": "2026-01-01T10:03:00Z",
                "event_type": "network",
                "username": "anonymous",
            },
        ],
        "event_count": 4,
        "start_time": "2026-01-01T10:00:00Z",
        "end_time": "2026-01-01T10:03:00Z",
        "duration_seconds": 180.0,
    }


def test_base_feature_names():
    result = generate_base_features(
        _sample_session()
    )

    assert set(result.keys()) == {
        "event_count",
        "session_duration_seconds",
        "auth_attempt_total",
        "user_attempt_total",
        "pass_attempt_total",
        "command_count_total",
        "anonymous_event_count",
    }


def test_event_count():
    result = generate_base_features(
        _sample_session()
    )

    assert result["event_count"] == 4


def test_session_duration():
    result = generate_base_features(
        _sample_session()
    )

    assert result["session_duration_seconds"] == 180.0


def test_auth_and_command_counts():
    result = generate_base_features(
        _sample_session()
    )

    assert result["auth_attempt_total"] == 2
    assert result["command_count_total"] == 1


def test_user_and_password_attempt_counts():
    result = generate_base_features(
        _sample_session()
    )

    assert result["user_attempt_total"] == 1
    assert result["pass_attempt_total"] == 1


def test_anonymous_event_count():
    result = generate_base_features(
        _sample_session()
    )

    assert result["anonymous_event_count"] == 2


def test_input_is_not_mutated():
    session = _sample_session()
    original = deepcopy(session)

    generate_base_features(session)

    assert session == original


def test_empty_session():
    session = {
        "session_id": "empty",
        "events": [],
        "duration_seconds": 0.0,
    }

    result = generate_base_features(session)

    assert result["event_count"] == 0
    assert result["session_duration_seconds"] == 0.0
    assert result["auth_attempt_total"] == 0
    assert result["user_attempt_total"] == 0
    assert result["pass_attempt_total"] == 0
    assert result["command_count_total"] == 0
    assert result["anonymous_event_count"] == 0
