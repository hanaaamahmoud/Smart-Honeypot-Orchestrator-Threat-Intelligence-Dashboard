from copy import deepcopy

import pytest

from app.pipeline.feature_generation_temporal import (
    generate_temporal_features,
)


def _sample_session():
    """
    Sample session with explicit per-event counters.

    Matches the Colab Step 5B-2 semantics:
        auth_attempt_rate = sum(auth_attempt) / duration
        command_rate      = sum(command_count) / duration

    Counter values:
        auth_attempt:    1 + 0 + 1 = 2
        command_count:   0 + 1 + 0 = 1
    """
    return {
        "session_id": "session-A",
        "events": [
            {
                "session_id": "session-A",
                "timestamp": "2026-01-01T10:00:00Z",
                "event_type": "auth",
                "auth_attempt": 1,
                "command_count": 0,
            },
            {
                "session_id": "session-A",
                "timestamp": "2026-01-01T10:02:00Z",
                "event_type": "command",
                "auth_attempt": 0,
                "command_count": 1,
            },
            {
                "session_id": "session-A",
                "timestamp": "2026-01-01T10:05:00Z",
                "event_type": "auth",
                "auth_attempt": 1,
                "command_count": 0,
            },
        ],
    }


def test_exact_feature_names():
    result = generate_temporal_features(
        _sample_session()
    )

    assert list(result.keys()) == [
        "inter_event_gap_mean",
        "inter_event_gap_min",
        "inter_event_gap_max",
        "session_duration_recomputed_seconds",
        "events_per_second",
        "auth_attempt_rate",
        "command_rate",
        "session_start_hour",
        "session_start_dayofweek",
        "session_start_dayofmonth",
    ]


def test_inter_event_gaps():
    # inter_event_gap_min is a constant 0.0 in the frozen
    # production reference (variance=0).
    result = generate_temporal_features(
        _sample_session()
    )

    # gaps = 120s, 180s
    assert result["inter_event_gap_mean"] == 150.0
    assert result["inter_event_gap_min"] == 0.0
    assert result["inter_event_gap_max"] == 180.0


def test_recomputed_duration():
    result = generate_temporal_features(
        _sample_session()
    )

    assert (
        result["session_duration_recomputed_seconds"]
        == 300.0
    )


def test_events_per_second():
    result = generate_temporal_features(
        _sample_session()
    )

    assert result["events_per_second"] == pytest.approx(
        3 / 300
    )


def test_auth_attempt_rate():
    # Colab parity: auth_attempt_rate = sum(auth_attempt) / duration
    # sum = 1 + 0 + 1 = 2
    result = generate_temporal_features(
        _sample_session()
    )

    assert result["auth_attempt_rate"] == pytest.approx(
        2 / 300
    )


def test_command_rate():
    # Colab parity: command_rate = sum(command_count) / duration
    # sum = 0 + 1 + 0 = 1
    result = generate_temporal_features(
        _sample_session()
    )

    assert result["command_rate"] == pytest.approx(
        1 / 300
    )


def test_rates_without_counter_fields_return_zero():
    """
    If a session's events do not carry auth_attempt / command_count
    counters, the rates must default to 0 (matching pandas sum).
    """
    session = {
        "session_id": "no-counters",
        "events": [
            {
                "timestamp": "2026-01-01T10:00:00Z",
                "event_type": "auth",
            },
            {
                "timestamp": "2026-01-01T10:01:00Z",
                "event_type": "command",
            },
        ],
    }

    result = generate_temporal_features(session)

    assert result["auth_attempt_rate"] == 0.0
    assert result["command_rate"] == 0.0


def test_session_start_hour():
    result = generate_temporal_features(
        _sample_session()
    )

    assert result["session_start_hour"] == 10.0


def test_session_start_dayofweek():
    result = generate_temporal_features(
        _sample_session()
    )

    # 2026-01-01 is Thursday.
    # Python weekday(): Monday=0 ... Sunday=6.
    assert result["session_start_dayofweek"] == 3.0


def test_session_start_dayofmonth():
    result = generate_temporal_features(
        _sample_session()
    )

    assert result["session_start_dayofmonth"] == 1.0


def test_single_event_has_zero_gap():
    session = {
        "session_id": "A",
        "events": [
            {
                "timestamp": "2026-01-01T10:00:00Z",
                "event_type": "auth",
            }
        ],
    }

    result = generate_temporal_features(session)

    assert result["inter_event_gap_mean"] == 0.0
    assert result["inter_event_gap_min"] == 0.0
    assert result["inter_event_gap_max"] == 0.0
    assert result[
        "session_duration_recomputed_seconds"
    ] == 0.0


def test_zero_duration_rates_are_safe():
    session = {
        "session_id": "A",
        "events": [
            {
                "timestamp": "2026-01-01T10:00:00Z",
                "event_type": "auth",
            },
        ],
    }

    result = generate_temporal_features(session)

    assert result["events_per_second"] == 0.0
    assert result["auth_attempt_rate"] == 0.0
    assert result["command_rate"] == 0.0


def test_empty_session():
    session = {
        "session_id": "A",
        "events": [],
    }

    result = generate_temporal_features(session)

    assert all(
        value == 0.0
        for value in result.values()
    )


def test_unsorted_events_are_rejected():
    session = {
        "session_id": "A",
        "events": [
            {
                "timestamp": "2026-01-01T10:05:00Z",
            },
            {
                "timestamp": "2026-01-01T10:00:00Z",
            },
        ],
    }

    with pytest.raises(ValueError):
        generate_temporal_features(session)


def test_input_is_not_mutated():
    session = _sample_session()
    original = deepcopy(session)

    generate_temporal_features(session)

    assert session == original


def test_all_values_are_numeric():
    result = generate_temporal_features(
        _sample_session()
    )

    assert all(
        isinstance(value, (int, float))
        for value in result.values()
    )
