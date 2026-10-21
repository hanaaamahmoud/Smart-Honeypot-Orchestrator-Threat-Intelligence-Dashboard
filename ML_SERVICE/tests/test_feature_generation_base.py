from copy import deepcopy

from app.pipeline.feature_generation_base import (
    generate_base_features,
)


def _sample_session():
    """
    Sample session with explicit integer counters.

    Mirrors the Colab Step 5B-1 aggregation:
        auth_attempt_total    = sum(auth_attempt)
        user_attempt_total    = sum(user_attempt)
        pass_attempt_total    = sum(pass_attempt)
        command_count_total   = sum(command_count)
        anonymous_event_count = sum(anonymous)
    """
    return {
        "session_id": "session-A",
        "events": [
            {
                "session_id": "session-A",
                "timestamp": "2026-01-01T10:00:00Z",
                "event_type": "auth",
                "username": "root",
                "password": "bad-password",
                "auth_attempt": 1,
                "user_attempt": 1,
                "pass_attempt": 1,
                "anonymous": 0,
                "command_count": 0,
            },
            {
                "session_id": "session-A",
                "timestamp": "2026-01-01T10:01:00Z",
                "event_type": "auth",
                "username": "",
                "auth_attempt": 1,
                "user_attempt": 0,
                "pass_attempt": 0,
                "anonymous": 1,
                "command_count": 0,
            },
            {
                "session_id": "session-A",
                "timestamp": "2026-01-01T10:02:00Z",
                "event_type": "command",
                "username": "root",
                "command": "whoami",
                "auth_attempt": 0,
                "user_attempt": 0,
                "pass_attempt": 0,
                "anonymous": 0,
                "command_count": 1,
            },
            {
                "session_id": "session-A",
                "timestamp": "2026-01-01T10:03:00Z",
                "event_type": "network",
                "username": "anonymous",
                "auth_attempt": 0,
                "user_attempt": 0,
                "pass_attempt": 0,
                "anonymous": 1,
                "command_count": 0,
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
    # Colab parity:
    # auth_attempt_total    = sum(auth_attempt)
    # command_count_total   = sum(command_count)
    result = generate_base_features(
        _sample_session()
    )

    assert result["auth_attempt_total"] == 2   # 1 + 1 + 0 + 0
    assert result["command_count_total"] == 1  # 0 + 0 + 1 + 0


def test_user_and_password_attempt_counts():
    # Colab parity:
    # user_attempt_total = sum(user_attempt)
    # pass_attempt_total = sum(pass_attempt)
    result = generate_base_features(
        _sample_session()
    )

    assert result["user_attempt_total"] == 1   # 1 + 0 + 0 + 0
    assert result["pass_attempt_total"] == 1   # 1 + 0 + 0 + 0


def test_anonymous_event_count():
    # Colab parity:
    # anonymous_event_count = sum(anonymous)
    result = generate_base_features(
        _sample_session()
    )

    assert result["anonymous_event_count"] == 2  # 0 + 1 + 0 + 1


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


def test_missing_counters_default_to_zero():
    """
    If a session's events do not carry explicit counters,
    all sums should default to 0 — matching pandas semantics.
    """
    session = {
        "session_id": "no-counters",
        "events": [
            {
                "timestamp": "2026-01-01T10:00:00Z",
                "event_type": "auth",
                "username": "root",
            },
            {
                "timestamp": "2026-01-01T10:01:00Z",
                "event_type": "command",
                "command": "ls",
            },
        ],
        "duration_seconds": 60.0,
    }

    result = generate_base_features(session)

    assert result["event_count"] == 2
    assert result["auth_attempt_total"] == 0
    assert result["user_attempt_total"] == 0
    assert result["pass_attempt_total"] == 0
    assert result["command_count_total"] == 0
    assert result["anonymous_event_count"] == 0
