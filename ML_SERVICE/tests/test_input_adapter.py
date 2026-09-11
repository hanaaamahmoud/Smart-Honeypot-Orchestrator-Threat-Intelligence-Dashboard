"""
D5.3 — Input Adapter Validation Tests
"""

import pytest

from app.pipeline.input_adapter import adapt_input


def test_accepts_valid_payload():
    payload = {
        "events": []
    }

    result = adapt_input(payload)

    assert result == []


def test_accepts_valid_events():
    payload = {
        "events": [
            {
                "timestamp": "2026-01-01T10:00:00Z",
                "event_type": "auth",
            }
        ]
    }

    result = adapt_input(payload)

    assert isinstance(result, list)
    assert len(result) == 1


def test_rejects_non_dict_payload():
    with pytest.raises(
        TypeError,
        match="Input payload must be a dictionary",
    ):
        adapt_input([])


def test_rejects_missing_events():
    with pytest.raises(
        ValueError,
        match="must contain 'events'",
    ):
        adapt_input({})


def test_rejects_events_as_non_list():
    with pytest.raises(
        TypeError,
        match="'events' must be a list",
    ):
        adapt_input({
            "events": {}
        })


def test_rejects_events_as_none():
    with pytest.raises(
        TypeError,
        match="'events' must be a list",
    ):
        adapt_input({
            "events": None
        })


def test_preserves_normalization_boundary():
    payload = {
        "events": []
    }

    result = adapt_input(payload)

    assert isinstance(result, list)


def test_adapter_returns_normalized_event():
    payload = {
        "events": [
            {
                "timestamp": "2026-01-01T10:00:00Z",
                "event_type": "auth",
                "username": "root",
                "source_ip": "192.168.1.10",
            }
        ]
    }

    result = adapt_input(payload)

    assert len(result) == 1

    normalized_event = result[0]

    assert isinstance(normalized_event, dict)
    assert normalized_event["timestamp"] is not None
    assert normalized_event["event_type"] == "auth"
    assert normalized_event["username"] == "root"
    assert normalized_event["source_ip"] == "192.168.1.10"


def test_adapter_is_source_neutral():
    source_a = {
        "events": [
            {
                "timestamp": "2026-01-01T10:00:00Z",
                "event_type": "auth",
                "username": "root",
                "source_ip": "192.168.1.10",
            }
        ]
    }

    source_b = {
        "events": [
            {
                "timestamp": "2026-01-01T10:00:00Z",
                "event_type": "auth",
                "username": "root",
                "source_ip": "192.168.1.10",
            }
        ]
    }

    result_a = adapt_input(source_a)
    result_b = adapt_input(source_b)

    assert result_a == result_b
    assert isinstance(result_a, list)
    assert len(result_a) == 1


def test_adapter_does_not_mutate_payload():
    payload = {
        "events": [
            {
                "timestamp": "2026-01-01T10:00:00Z",
                "event_type": "auth",
                "username": "root",
                "source_ip": "192.168.1.10",
            }
        ]
    }

    original_payload = {
        "events": [
            {
                "timestamp": "2026-01-01T10:00:00Z",
                "event_type": "auth",
                "username": "root",
                "source_ip": "192.168.1.10",
            }
        ]
    }

    adapt_input(payload)

    assert payload == original_payload


def test_adapter_output_is_deterministic():
    payload = {
        "events": [
            {
                "timestamp": "2026-01-01T10:00:00Z",
                "event_type": "auth",
                "username": "root",
                "source_ip": "192.168.1.10",
            }
        ]
    }

    result_a = adapt_input(payload)
    result_b = adapt_input(payload)

    assert result_a == result_b
