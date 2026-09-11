"""
D2.7 — D2 Contract Tests

End-to-end contract tests for session reconstruction.
"""

from app.pipeline.session_reconstruction import (
    reconstruct_sessions,
)


def _sample_events():
    return [
        {
            "session_id": "session-B",
            "timestamp": "2026-01-01T11:05:00Z",
            "event_type": "command",
            "value": "ls",
        },
        {
            "session_id": "session-A",
            "timestamp": "2026-01-01T10:05:00Z",
            "event_type": "auth",
            "value": "success",
        },
        {
            "session_id": "session-A",
            "timestamp": "2026-01-01T10:00:00Z",
            "event_type": "auth",
            "value": "failed",
        },
        {
            "session_id": "session-B",
            "timestamp": "2026-01-01T11:00:00Z",
            "event_type": "command",
            "value": "whoami",
        },
    ]


def test_event_conservation():
    events = _sample_events()

    sessions = reconstruct_sessions(events)

    reconstructed_events = [
        event
        for session in sessions
        for event in session["events"]
    ]

    assert len(reconstructed_events) == 4


def test_session_id_conservation():
    events = _sample_events()

    input_session_ids = {
        event["session_id"]
        for event in events
    }

    sessions = reconstruct_sessions(events)

    output_session_ids = {
        session["session_id"]
        for session in sessions
    }

    assert output_session_ids == input_session_ids


def test_events_remain_inside_correct_session():
    events = _sample_events()

    sessions = reconstruct_sessions(events)

    for session in sessions:
        session_id = session["session_id"]

        for event in session["events"]:
            assert event["session_id"] == session_id


def test_chronological_ordering():
    events = _sample_events()

    sessions = reconstruct_sessions(events)

    for session in sessions:
        timestamps = [
            event["timestamp"]
            for event in session["events"]
        ]

        assert timestamps == sorted(timestamps)


def test_boundaries_match_events():
    events = _sample_events()

    sessions = reconstruct_sessions(events)

    for session in sessions:
        timestamps = [
            event["timestamp"]
            for event in session["events"]
        ]

        assert session["start_time"] == timestamps[0]
        assert session["end_time"] == timestamps[-1]


def test_event_count_matches_actual_events():
    events = _sample_events()

    sessions = reconstruct_sessions(events)

    for session in sessions:
        assert session["event_count"] == len(
            session["events"]
        )


def test_duration_matches_boundaries():
    events = _sample_events()

    sessions = reconstruct_sessions(events)

    session_a = next(
        session
        for session in sessions
        if session["session_id"] == "session-A"
    )

    session_b = next(
        session
        for session in sessions
        if session["session_id"] == "session-B"
    )

    assert session_a["duration_seconds"] == 300.0
    assert session_b["duration_seconds"] == 300.0


def test_reconstruction_is_deterministic():
    events = _sample_events()

    first = reconstruct_sessions(events)
    second = reconstruct_sessions(events)

    assert first == second


def test_unassigned_events_do_not_create_sessions():
    events = _sample_events()

    events.append(
        {
            "timestamp": "2026-01-01T12:00:00Z",
            "event_type": "unknown",
        }
    )

    sessions = reconstruct_sessions(events)

    session_ids = {
        session["session_id"]
        for session in sessions
    }

    assert session_ids == {
        "session-A",
        "session-B",
    }
