"""
D2.8 — Regression / Immutability Tests

Final regression gate before D3.

Guarantees:
- Input events are never mutated.
- Nested input structures are preserved.
- Reconstruction is deterministic.
- Session contract remains stable.
- Re-running reconstruction does not change the source data.
"""

from copy import deepcopy

from app.pipeline.session_reconstruction import (
    reconstruct_sessions,
)


def _regression_events():
    return [
        {
            "session_id": "session-002",
            "timestamp": "2026-01-01T12:05:00Z",
            "event_type": "command",
            "username": "admin",
            "metadata": {
                "source": "honeypot",
                "tags": ["ssh", "command"],
            },
        },
        {
            "session_id": "session-001",
            "timestamp": "2026-01-01T10:05:00Z",
            "event_type": "auth",
            "username": "root",
            "metadata": {
                "source": "honeypot",
                "tags": ["ssh"],
            },
        },
        {
            "session_id": "session-001",
            "timestamp": "2026-01-01T10:00:00Z",
            "event_type": "auth",
            "username": "root",
            "metadata": {
                "source": "honeypot",
                "tags": ["ssh"],
            },
        },
        {
            "session_id": "session-002",
            "timestamp": "2026-01-01T12:00:00Z",
            "event_type": "command",
            "username": "admin",
            "metadata": {
                "source": "honeypot",
                "tags": ["ssh"],
            },
        },
    ]


def test_input_events_are_immutable():
    events = _regression_events()
    original = deepcopy(events)

    reconstruct_sessions(events)

    assert events == original


def test_nested_input_data_is_immutable():
    events = _regression_events()
    original = deepcopy(events)

    reconstruct_sessions(events)

    assert events == original
    assert events[0]["metadata"]["tags"] == [
        "ssh",
        "command",
    ]


def test_input_order_is_not_modified():
    events = _regression_events()

    original_order = [
        (
            event["session_id"],
            event["timestamp"],
        )
        for event in events
    ]

    reconstruct_sessions(events)

    current_order = [
        (
            event["session_id"],
            event["timestamp"],
        )
        for event in events
    ]

    assert current_order == original_order


def test_repeated_execution_does_not_modify_input():
    events = _regression_events()
    original = deepcopy(events)

    first = reconstruct_sessions(events)
    second = reconstruct_sessions(events)

    assert first == second
    assert events == original


def test_session_contract_keys_are_stable():
    events = _regression_events()

    sessions = reconstruct_sessions(events)

    expected_keys = {
        "session_id",
        "events",
        "event_count",
        "start_time",
        "end_time",
        "duration_seconds",
    }

    for session in sessions:
        assert set(session.keys()) == expected_keys


def test_regression_session_counts():
    events = _regression_events()

    sessions = reconstruct_sessions(events)

    assert len(sessions) == 2

    assert sessions[0]["session_id"] == "session-001"
    assert sessions[1]["session_id"] == "session-002"


def test_regression_boundaries():
    events = _regression_events()

    sessions = reconstruct_sessions(events)

    session_001 = sessions[0]
    session_002 = sessions[1]

    assert session_001["start_time"] == (
        "2026-01-01T10:00:00Z"
    )

    assert session_001["end_time"] == (
        "2026-01-01T10:05:00Z"
    )

    assert session_001["duration_seconds"] == 300.0

    assert session_002["start_time"] == (
        "2026-01-01T12:00:00Z"
    )

    assert session_002["end_time"] == (
        "2026-01-01T12:05:00Z"
    )

    assert session_002["duration_seconds"] == 300.0


def test_no_behavioral_features_are_generated_in_d2():
    events = _regression_events()

    sessions = reconstruct_sessions(events)

    forbidden_feature_names = {
        "event_count_log1p",
        "events_per_second",
        "auth_attempt_rate",
        "command_rate",
        "destination_diversity",
        "protocol_diversity",
        "geo_country_diversity",
        "session_start_hour",
    }

    for session in sessions:
        assert forbidden_feature_names.isdisjoint(
            session.keys()
        )
