from app.pipeline.session_reconstruction import (
    reconstruct_sessions,
)


def test_reconstructs_complete_sessions():
    events = [
        {
            "session_id": "B",
            "timestamp": "2026-01-01T11:05:00Z",
            "event": 2,
        },
        {
            "session_id": "A",
            "timestamp": "2026-01-01T10:05:00Z",
            "event": 3,
        },
        {
            "session_id": "A",
            "timestamp": "2026-01-01T10:00:00Z",
            "event": 1,
        },
        {
            "session_id": "B",
            "timestamp": "2026-01-01T11:00:00Z",
            "event": 1,
        },
    ]

    sessions = reconstruct_sessions(events)

    assert len(sessions) == 2
    assert sessions[0]["session_id"] == "A"
    assert sessions[1]["session_id"] == "B"


def test_events_are_chronologically_ordered():
    events = [
        {
            "session_id": "A",
            "timestamp": "2026-01-01T10:05:00Z",
            "event": 2,
        },
        {
            "session_id": "A",
            "timestamp": "2026-01-01T10:01:00Z",
            "event": 1,
        },
        {
            "session_id": "A",
            "timestamp": "2026-01-01T10:03:00Z",
            "event": 3,
        },
    ]

    sessions = reconstruct_sessions(events)

    ordered = sessions[0]["events"]

    assert [
        event["event"]
        for event in ordered
    ] == [1, 3, 2]


def test_session_boundaries_are_correct():
    events = [
        {
            "session_id": "A",
            "timestamp": "2026-01-01T10:10:00Z",
        },
        {
            "session_id": "A",
            "timestamp": "2026-01-01T10:00:00Z",
        },
    ]

    sessions = reconstruct_sessions(events)

    session = sessions[0]

    assert session["start_time"] == "2026-01-01T10:00:00Z"
    assert session["end_time"] == "2026-01-01T10:10:00Z"
    assert session["duration_seconds"] == 600.0
    assert session["event_count"] == 2


def test_single_event_session():
    events = [
        {
            "session_id": "A",
            "timestamp": "2026-01-01T10:00:00Z",
        }
    ]

    sessions = reconstruct_sessions(events)

    assert len(sessions) == 1
    assert sessions[0]["event_count"] == 1
    assert sessions[0]["duration_seconds"] == 0.0


def test_missing_session_id_is_not_fabricated():
    events = [
        {
            "timestamp": "2026-01-01T10:00:00Z",
            "event": 1,
        },
        {
            "session_id": "A",
            "timestamp": "2026-01-01T10:01:00Z",
            "event": 2,
        },
    ]

    sessions = reconstruct_sessions(events)

    assert len(sessions) == 1
    assert sessions[0]["session_id"] == "A"


def test_input_is_not_mutated():
    events = [
        {
            "session_id": "A",
            "timestamp": "2026-01-01T10:05:00Z",
            "nested": {"value": 1},
        },
        {
            "session_id": "A",
            "timestamp": "2026-01-01T10:00:00Z",
            "nested": {"value": 2},
        },
    ]

    original = [
        {
            "session_id": event["session_id"],
            "timestamp": event["timestamp"],
            "nested": dict(event["nested"]),
        }
        for event in events
    ]

    reconstruct_sessions(events)

    assert events == original


def test_reconstruction_is_deterministic():
    events = [
        {
            "session_id": "B",
            "timestamp": "2026-01-01T11:00:00Z",
            "event": 1,
        },
        {
            "session_id": "A",
            "timestamp": "2026-01-01T10:02:00Z",
            "event": 2,
        },
        {
            "session_id": "A",
            "timestamp": "2026-01-01T10:01:00Z",
            "event": 1,
        },
    ]

    first = reconstruct_sessions(events)
    second = reconstruct_sessions(events)

    assert first == second
