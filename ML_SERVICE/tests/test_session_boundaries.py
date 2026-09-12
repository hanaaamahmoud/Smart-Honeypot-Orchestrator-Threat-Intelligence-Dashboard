import pytest

from app.pipeline.session_boundaries import (
    calculate_session_boundaries,
)


def test_session_boundaries_are_calculated():
    events = [
        {
            "session_id": "session-001",
            "timestamp": "2026-01-01T10:00:00+00:00",
            "event": "login",
        },
        {
            "session_id": "session-001",
            "timestamp": "2026-01-01T10:00:05+00:00",
            "event": "command",
        },
        {
            "session_id": "session-001",
            "timestamp": "2026-01-01T10:00:12+00:00",
            "event": "logout",
        },
    ]

    result = calculate_session_boundaries(
        "session-001",
        events,
    )

    assert result["session_id"] == "session-001"
    assert result["event_count"] == 3
    assert result["start_time"] == "2026-01-01T10:00:00+00:00"
    assert result["end_time"] == "2026-01-01T10:00:12+00:00"
    assert result["duration_seconds"] == 12.0
    assert result["events"] == events


def test_single_event_has_zero_duration():
    events = [
        {
            "session_id": "session-001",
            "timestamp": "2026-01-01T10:00:00+00:00",
            "event": "login",
        }
    ]

    result = calculate_session_boundaries(
        "session-001",
        events,
    )

    assert result["event_count"] == 1
    assert result["start_time"] == result["end_time"]
    assert result["duration_seconds"] == 0.0


def test_events_are_not_mutated():
    events = [
        {
            "session_id": "session-001",
            "timestamp": "2026-01-01T10:00:00+00:00",
            "data": {"command": "ls"},
        },
        {
            "session_id": "session-001",
            "timestamp": "2026-01-01T10:00:10+00:00",
            "data": {"command": "whoami"},
        },
    ]

    original = [
        {
            "session_id": "session-001",
            "timestamp": "2026-01-01T10:00:00+00:00",
            "data": {"command": "ls"},
        },
        {
            "session_id": "session-001",
            "timestamp": "2026-01-01T10:00:10+00:00",
            "data": {"command": "whoami"},
        },
    ]

    calculate_session_boundaries(
        "session-001",
        events,
    )

    assert events == original


def test_empty_session_is_rejected():
    with pytest.raises(ValueError):
        calculate_session_boundaries(
            "session-001",
            [],
        )


def test_empty_session_id_is_rejected():
    events = [
        {
            "timestamp": "2026-01-01T10:00:00+00:00",
        }
    ]

    with pytest.raises(ValueError):
        calculate_session_boundaries(
            "",
            events,
        )


def test_invalid_timestamp_is_rejected():
    events = [
        {
            "session_id": "session-001",
            "timestamp": "not-a-valid-timestamp",
        }
    ]

    with pytest.raises(ValueError):
        calculate_session_boundaries(
            "session-001",
            events,
        )


def test_unordered_events_are_rejected():
    events = [
        {
            "session_id": "session-001",
            "timestamp": "2026-01-01T10:00:10+00:00",
        },
        {
            "session_id": "session-001",
            "timestamp": "2026-01-01T10:00:00+00:00",
        },
    ]

    with pytest.raises(ValueError):
        calculate_session_boundaries(
            "session-001",
            events,
        )
