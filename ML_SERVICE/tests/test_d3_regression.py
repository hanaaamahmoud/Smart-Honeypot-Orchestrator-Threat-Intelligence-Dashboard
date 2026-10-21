"""
D3.9 — Full Feature Generation Regression

Final regression test for the D3 pipeline.
"""

from copy import deepcopy

from app.pipeline.session_reconstruction import (
    reconstruct_sessions,
)

from app.pipeline.feature_generation import (
    FROZEN_FEATURE_ORDER,
    assemble_48_features,
)

from app.pipeline.feature_validation import (
    validate_48_features,
)


def _sample_events():
    return [
        {
            "session_id": "session-B",
            "timestamp": "2026-01-01T11:05:00Z",
            "event_type": "command",
            "command": "ls",
            "destination": "10.0.0.2",
            "destination_port": 22,
            "source_ip": "192.168.1.20",
            "protocol": "tcp",
            "honeypot": "hp-02",
            "username": "root",
            "country": "Egypt",
            "country_code": "EG",
            "city": "Cairo",
        },
        {
            "session_id": "session-A",
            "timestamp": "2026-01-01T10:05:00Z",
            "event_type": "auth",
            "username": "admin",
            "destination": "10.0.0.1",
            "destination_port": 22,
            "source_ip": "192.168.1.10",
            "protocol": "tcp",
            "honeypot": "hp-01",
            "country": "Egypt",
            "country_code": "EG",
            "city": "Cairo",
        },
        {
            "session_id": "session-A",
            "timestamp": "2026-01-01T10:00:00Z",
            "event_type": "auth",
            "username": "root",
            "destination": "10.0.0.1",
            "destination_port": 22,
            "source_ip": "192.168.1.10",
            "protocol": "tcp",
            "honeypot": "hp-01",
            "country": "Egypt",
            "country_code": "EG",
            "city": "Cairo",
        },
    ]


def _build_final_feature_vector(session):
    """
    Build the final 48-feature vector using the
    actual D3 feature generators.
    """

    from app.pipeline.feature_generation_base import (
        generate_base_features,
    )

    from app.pipeline.feature_generation_diversity import (
        generate_diversity_features,
    )

    from app.pipeline.feature_generation_temporal import (
        generate_temporal_features,
    )

    from app.pipeline.feature_generation_density import (
        generate_density_features,
    )

    from app.pipeline.feature_generation_geo import (
        generate_geo_availability_features,
    )

    features = {}

    # D3.2
    features.update(
        generate_base_features(session)
    )

    # D3.3
    features.update(
        generate_diversity_features(session)
    )

    # D3.4
    features.update(
        generate_temporal_features(
            session
        )
    )

    # D3.5
    features.update(
        generate_density_features(
            session
        )
    )

    # D3.6
    features.update(
        generate_geo_availability_features(
            session
        )
    )

    # D3.7
    return assemble_48_features(features)


def test_d3_produces_exactly_48_features():

    sessions = reconstruct_sessions(
        _sample_events()
    )

    for session in sessions:

        features = _build_final_feature_vector(
            session
        )

        assert len(features) == 48


def test_d3_feature_names_are_exact():

    sessions = reconstruct_sessions(
        _sample_events()
    )

    for session in sessions:

        features = _build_final_feature_vector(
            session
        )

        assert set(features.keys()) == set(
            FROZEN_FEATURE_ORDER
        )


def test_d3_feature_order_is_frozen():

    sessions = reconstruct_sessions(
        _sample_events()
    )

    for session in sessions:

        features = _build_final_feature_vector(
            session
        )

        assert list(features.keys()) == (
            FROZEN_FEATURE_ORDER
        )


def test_d3_features_are_numeric_and_finite():

    sessions = reconstruct_sessions(
        _sample_events()
    )

    for session in sessions:

        features = _build_final_feature_vector(
            session
        )

        assert validate_48_features(
            features,
            FROZEN_FEATURE_ORDER,
        ) is True


def test_d3_session_ids_are_preserved():

    events = _sample_events()

    input_ids = {
        event["session_id"]
        for event in events
    }

    sessions = reconstruct_sessions(events)

    output_ids = {
        session["session_id"]
        for session in sessions
    }

    assert output_ids == input_ids


def test_d3_is_deterministic():

    events = _sample_events()

    sessions_1 = reconstruct_sessions(events)
    sessions_2 = reconstruct_sessions(events)

    result_1 = [
        _build_final_feature_vector(session)
        for session in sessions_1
    ]

    result_2 = [
        _build_final_feature_vector(session)
        for session in sessions_2
    ]

    assert result_1 == result_2


def test_d3_does_not_mutate_input():

    events = _sample_events()

    original = deepcopy(events)

    sessions = reconstruct_sessions(events)

    for session in sessions:
        _build_final_feature_vector(session)

    assert events == original


def test_each_session_has_48_features():

    sessions = reconstruct_sessions(
        _sample_events()
    )

    assert len(sessions) == 2

    for session in sessions:

        features = _build_final_feature_vector(
            session
        )

        assert len(features) == 48

        assert list(features.keys()) == (
            FROZEN_FEATURE_ORDER
        )
