from copy import deepcopy

import pytest

from app.pipeline.session_ordering import order_session_events


def test_events_are_sorted_chronologically():
    grouped = {
        "session-001": [
            {
                "session_id": "session-001",
                "timestamp": "2026-01-01T10:05:00Z",
                "event": "third",
            },
            {
                "session_id": "session-001",
                "timestamp": "2026-01-01T10:01:00Z",
                "event": "first",
            },
            {
                "session_id": "session-001",
                "timestamp": "2026-01-01T10:03:00Z",
                "event": "second",
            },
        ]
    }

    ordered = order_session_events(grouped)

    assert [
        event["event"]
        for event in ordered["session-001"]
    ] == ["first", "second", "third"]


def test_each_session_is_ordered_independently():
    grouped = {
        "session-001": [
            {
                "session_id": "session-001",
                "timestamp": "2026-01-01T10:05:00Z",
            },
            {
                "session_id": "session-001",
                "timestamp": "2026-01-01T10:01:00Z",
            },
        ],
        "session-002": [
            {
                "session_id": "session-002",
                "timestamp": "2026-01-01T09:05:00Z",
            },
            {
                "session_id": "session-002",
                "timestamp": "2026-01-01T09:01:00Z",
            },
        ],
    }

    ordered = order_session_events(grouped)

    assert [
        event["timestamp"]
        for event in ordered["session-001"]
    ] == [
        "2026-01-01T10:01:00Z",
        "2026-01-01T10:05:00Z",
    ]

    assert [
        event["timestamp"]
        for event in ordered["session-002"]
    ] == [
        "2026-01-01T09:01:00Z",
        "2026-01-01T09:05:00Z",
    ]


def test_equal_timestamps_preserve_original_order():
    grouped = {
        "session-001": [
            {
                "session_id": "session-001",
                "timestamp": "2026-01-01T10:00:00Z",
                "event": "first",
            },
            {
                "session_id": "session-001",
                "timestamp": "2026-01-01T10:00:00Z",
                "event": "second",
            },
            {
                "session_id": "session-001",
                "timestamp": "2026-01-01T10:00:00Z",
                "event": "third",
            },
        ]
    }

    ordered = order_session_events(grouped)

    assert [
        event["event"]
        for event in ordered["session-001"]
    ] == ["first", "second", "third"]


def test_event_count_is_preserved():
    grouped = {
        "session-001": [
            {
                "session_id": "session-001",
                "timestamp": "2026-01-01T10:03:00Z",
            },
            {
                "session_id": "session-001",
                "timestamp": "2026-01-01T10:01:00Z",
            },
            {
                "session_id": "session-001",
                "timestamp": "2026-01-01T10:02:00Z",
            },
        ]
    }

    ordered = order_session_events(grouped)

    assert len(ordered["session-001"]) == len(
        grouped["session-001"]
    )


def test_session_ids_are_preserved():
    grouped = {
        "session-abc": [
            {
                "session_id": "session-abc",
                "timestamp": "2026-01-01T10:02:00Z",
            },
            {
                "session_id": "session-abc",
                "timestamp": "2026-01-01T10:01:00Z",
            },
        ]
    }

    ordered = order_session_events(grouped)

    assert list(ordered.keys()) == ["session-abc"]

    assert all(
        event["session_id"] == "session-abc"
        for event in ordered["session-abc"]
    )


def test_input_is_not_mutated():
    grouped = {
        "session-001": [
            {
                "session_id": "session-001",
                "timestamp": "2026-01-01T10:05:00Z",
                "event": "late",
            },
            {
                "session_id": "session-001",
                "timestamp": "2026-01-01T10:01:00Z",
                "event": "early",
            },
        ]
    }

    original = deepcopy(grouped)

    ordered = order_session_events(grouped)

    assert grouped == original
    assert ordered is not grouped
    assert ordered["session-001"] is not grouped["session-001"]


def test_invalid_timestamp_is_rejected():
    grouped = {
        "session-001": [
            {
                "session_id": "session-001",
                "timestamp": "not-a-valid-timestamp",
            }
        ]
    }

    with pytest.raises(ValueError):
        order_session_events(grouped)
