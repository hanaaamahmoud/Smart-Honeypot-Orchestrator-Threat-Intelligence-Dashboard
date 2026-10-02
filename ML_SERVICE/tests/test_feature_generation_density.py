from copy import deepcopy

import pytest

from app.pipeline.feature_generation_density import (
    generate_density_features,
)


def _sample_session():
    """
    Sample session used across density tests.

    Base / temporal values:
        duration  = 180.0
        event_count = 4
        inter_event_gap_mean = 5.0
        inter_event_gap_max = 10.0

    Counter values:
        command_count_total  = 2
        auth_attempt_total   = 3
        user_attempt_total   = 2
        pass_attempt_total   = 1
        credential_attempt_total = 3
    """
    return {
        "session_id": "session-A",
        "duration_seconds": 180.0,
        "event_count": 4,
        "inter_event_gap_mean": 5.0,
        "inter_event_gap_max": 10.0,
        "command_count_total": 2,
        "auth_attempt_total": 3,
        "user_attempt_total": 2,
        "pass_attempt_total": 1,
        "events": [
            {"timestamp": "2026-01-01T10:00:00Z"},
            {"timestamp": "2026-01-01T10:01:00Z"},
            {"timestamp": "2026-01-01T10:02:00Z"},
            {"timestamp": "2026-01-01T10:03:00Z"},
        ],
    }


def test_exact_density_feature_names():
    result = generate_density_features(
        _sample_session()
    )

    assert list(result.keys()) == [
        "session_duration_log1p",
        "event_count_log1p",
        "inter_event_gap_mean_log1p",
        "inter_event_gap_max_log1p",
        "event_density",
        "command_density",
        "auth_attempt_density",
        "credential_attempt_density",
    ]


def test_session_duration_log1p():
    import math

    result = generate_density_features(
        _sample_session()
    )

    assert result["session_duration_log1p"] == pytest.approx(
        math.log1p(180.0)
    )


def test_event_count_log1p():
    import math

    result = generate_density_features(
        _sample_session()
    )

    assert result["event_count_log1p"] == pytest.approx(
        math.log1p(4.0)
    )


def test_inter_event_gap_log1p():
    import math

    result = generate_density_features(
        _sample_session()
    )

    assert result["inter_event_gap_mean_log1p"] == pytest.approx(
        math.log1p(5.0)
    )

    assert result["inter_event_gap_max_log1p"] == pytest.approx(
        math.log1p(10.0)
    )


def test_event_density():
    # Colab parity: event_density = event_count / duration
    result = generate_density_features(
        _sample_session()
    )

    assert result["event_density"] == pytest.approx(4.0 / 180.0)


def test_command_density():
    # Colab parity: command_density = command_count_total / event_count
    result = generate_density_features(
        _sample_session()
    )

    assert result["command_density"] == pytest.approx(2.0 / 4.0)


def test_auth_attempt_density():
    # Colab parity: auth_attempt_density = auth_attempt_total / event_count
    result = generate_density_features(
        _sample_session()
    )

    assert result["auth_attempt_density"] == pytest.approx(3.0 / 4.0)


def test_credential_attempt_density():
    # Colab parity:
    #   credential_attempt_density =
    #       (user_attempt_total + pass_attempt_total) / event_count
    result = generate_density_features(
        _sample_session()
    )

    # (2 + 1) / 4 = 0.75
    assert result["credential_attempt_density"] == pytest.approx(3.0 / 4.0)


def test_zero_duration_returns_zero_event_density():
    session = _sample_session()
    session["duration_seconds"] = 0.0

    result = generate_density_features(session)

    # Only event_density depends on duration.
    assert result["event_density"] == 0.0

    # Densities over event_count remain well-defined.
    assert result["command_density"] == pytest.approx(2.0 / 4.0)
    assert result["auth_attempt_density"] == pytest.approx(3.0 / 4.0)
    assert result["credential_attempt_density"] == pytest.approx(3.0 / 4.0)


def test_zero_event_count_returns_zero_densities():
    session = _sample_session()
    session["event_count"] = 0

    result = generate_density_features(session)

    assert result["command_density"] == 0.0
    assert result["auth_attempt_density"] == 0.0
    assert result["credential_attempt_density"] == 0.0


def test_empty_session_returns_zero():
    session = {
        "session_id": "A",
        "events": [],
    }

    result = generate_density_features(session)

    assert all(
        value == 0
        for value in result.values()
    )


def test_input_is_not_mutated():
    session = _sample_session()
    original = deepcopy(session)

    generate_density_features(session)

    assert session == original


def test_two_argument_form():
    """
    generate_density_features(base, temporal) must merge dicts
    without mutating either one.
    """
    base = {
        "event_count": 4,
        "command_count_total": 2,
        "auth_attempt_total": 3,
        "user_attempt_total": 2,
        "pass_attempt_total": 1,
    }
    temporal = {
        "session_duration_recomputed_seconds": 180.0,
        "inter_event_gap_mean": 5.0,
        "inter_event_gap_max": 10.0,
    }

    base_copy = deepcopy(base)
    temporal_copy = deepcopy(temporal)

    result = generate_density_features(base, temporal)

    assert base == base_copy
    assert temporal == temporal_copy

    assert result["event_density"] == pytest.approx(4.0 / 180.0)
    assert result["command_density"] == pytest.approx(2.0 / 4.0)
