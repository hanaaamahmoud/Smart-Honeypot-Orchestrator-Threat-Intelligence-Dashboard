from copy import deepcopy
from math import isfinite, log1p

import pytest

from app.pipeline.feature_generation_density import (
    generate_density_features,
)


def _sample_session():
    return {
        "session_id": "session-A",
        "events": [
            {"event": 1},
            {"event": 2},
            {"event": 3},
            {"event": 4},
        ],
        "event_count": 4,
        "duration_seconds": 10.0,
        "inter_event_gap_mean": 2.0,
        "inter_event_gap_max": 4.0,
        "command_count_total": 2,
        "auth_attempt_total": 3,
        "credential_attempt_total": 4,
    }


def test_exact_feature_names():

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


def test_log_features():

    result = generate_density_features(
        _sample_session()
    )

    assert result["session_duration_log1p"] == pytest.approx(
        log1p(10.0)
    )

    assert result["event_count_log1p"] == pytest.approx(
        log1p(4.0)
    )

    assert result["inter_event_gap_mean_log1p"] == pytest.approx(
        log1p(2.0)
    )

    assert result["inter_event_gap_max_log1p"] == pytest.approx(
        log1p(4.0)
    )


def test_event_density():

    result = generate_density_features(
        _sample_session()
    )

    assert result["event_density"] == pytest.approx(
        4.0 / 10.0
    )


def test_command_density():

    result = generate_density_features(
        _sample_session()
    )

    assert result["command_density"] == pytest.approx(
        2.0 / 10.0
    )


def test_auth_attempt_density():

    result = generate_density_features(
        _sample_session()
    )

    assert result["auth_attempt_density"] == pytest.approx(
        3.0 / 10.0
    )


def test_credential_attempt_density():

    result = generate_density_features(
        _sample_session()
    )

    assert result["credential_attempt_density"] == pytest.approx(
        4.0 / 10.0
    )


def test_zero_duration_returns_zero_density():

    session = _sample_session()
    session["duration_seconds"] = 0.0

    result = generate_density_features(session)

    assert result["event_density"] == 0.0
    assert result["command_density"] == 0.0
    assert result["auth_attempt_density"] == 0.0
    assert result["credential_attempt_density"] == 0.0


def test_zero_values_have_zero_log1p():

    session = {
        "session_id": "A",
        "events": [],
        "event_count": 0,
        "duration_seconds": 0.0,
        "inter_event_gap_mean": 0.0,
        "inter_event_gap_max": 0.0,
        "command_count_total": 0,
        "auth_attempt_total": 0,
        "credential_attempt_total": 0,
    }

    result = generate_density_features(session)

    assert result["session_duration_log1p"] == 0.0
    assert result["event_count_log1p"] == 0.0
    assert result["inter_event_gap_mean_log1p"] == 0.0
    assert result["inter_event_gap_max_log1p"] == 0.0


def test_all_outputs_are_finite():

    result = generate_density_features(
        _sample_session()
    )

    assert all(
        isfinite(value)
        for value in result.values()
    )


def test_all_outputs_are_numeric():

    result = generate_density_features(
        _sample_session()
    )

    assert all(
        isinstance(value, float)
        for value in result.values()
    )


def test_negative_log_input_is_rejected():

    session = _sample_session()
    session["event_count"] = -1

    with pytest.raises(ValueError):
        generate_density_features(session)


def test_negative_duration_is_rejected():

    session = _sample_session()
    session["duration_seconds"] = -1

    with pytest.raises(ValueError):
        generate_density_features(session)


def test_input_is_not_mutated():

    session = _sample_session()
    original = deepcopy(session)

    generate_density_features(session)

    assert session == original
