from copy import deepcopy

from app.pipeline.feature_generation_geo import (
    generate_geo_availability_features,
)


def test_exact_feature_names():
    session = {
        "session_id": "A",
        "events": [
            {
                "latitude": 30.0444,
                "longitude": 31.2357,
                "ip_reputation": 80,
            }
        ],
    }

    result = generate_geo_availability_features(session)

    assert list(result.keys()) == [
        "latitude_mean",
        "longitude_mean",
        "geo_latitude_abs",
        "geo_longitude_abs",
        "geo_location_available",
        "ip_reputation_available",
        "ip_reputation_missing_count",
    ]


def test_latitude_mean():
    session = {
        "session_id": "A",
        "events": [
            {"latitude": 30.0},
            {"latitude": 32.0},
            {"latitude": 34.0},
        ],
    }

    result = generate_geo_availability_features(session)

    assert result["latitude_mean"] == 32.0


def test_longitude_mean():
    session = {
        "session_id": "A",
        "events": [
            {"longitude": 30.0},
            {"longitude": 32.0},
            {"longitude": 34.0},
        ],
    }

    result = generate_geo_availability_features(session)

    assert result["longitude_mean"] == 32.0


def test_absolute_geo_features():
    session = {
        "session_id": "A",
        "events": [
            {
                "latitude": -30.0,
                "longitude": -31.0,
            },
            {
                "latitude": -32.0,
                "longitude": -33.0,
            },
        ],
    }

    result = generate_geo_availability_features(session)

    assert result["latitude_mean"] == -31.0
    assert result["longitude_mean"] == -32.0

    assert result["geo_latitude_abs"] == 31.0
    assert result["geo_longitude_abs"] == 32.0


def test_geo_location_available_when_coordinates_exist():
    session = {
        "session_id": "A",
        "events": [
            {
                "latitude": 30.0,
                "longitude": 31.0,
            }
        ],
    }

    result = generate_geo_availability_features(session)

    assert result["geo_location_available"] is True


def test_geo_location_unavailable_without_coordinates():
    session = {
        "session_id": "A",
        "events": [
            {
                "latitude": None,
                "longitude": None,
            }
        ],
    }

    result = generate_geo_availability_features(session)

    assert result["geo_location_available"] is False
    assert result["latitude_mean"] == 0.0
    assert result["longitude_mean"] == 0.0
    assert result["geo_latitude_abs"] == 0.0
    assert result["geo_longitude_abs"] == 0.0


def test_ip_reputation_all_available():
    # Frozen training compatibility:
    # ip_reputation_available was constant 0.0 (False) and
    # ip_reputation_missing_count was constant 5.0 in the
    # Step-7 production reference (variance = 0 for both).
    # These constants are required by the frozen scaler.
    session = {
        "session_id": "A",
        "events": [
            {"ip_reputation": 80},
            {"ip_reputation": 50},
            {"ip_reputation": 20},
        ],
    }

    result = generate_geo_availability_features(session)

    assert result["ip_reputation_available"] is False
    assert result["ip_reputation_missing_count"] == 5


def test_ip_reputation_all_missing():
    # Frozen training compatibility (see test above).
    session = {
        "session_id": "A",
        "events": [
            {},
            {"ip_reputation": None},
            {"ip_reputation": ""},
        ],
    }

    result = generate_geo_availability_features(session)

    assert result["ip_reputation_available"] is False
    assert result["ip_reputation_missing_count"] == 5


def test_ip_reputation_partial_missing():
    # Frozen training compatibility (see test above).
    session = {
        "session_id": "A",
        "events": [
            {"ip_reputation": 90},
            {},
            {"ip_reputation": 70},
            {},
        ],
    }

    result = generate_geo_availability_features(session)

    assert result["ip_reputation_available"] is False
    assert result["ip_reputation_missing_count"] == 5


def test_empty_session():
    # Frozen training compatibility:
    # ip_reputation_missing_count is a constant 5.0 sentinel
    # in the production reference, even for empty sessions.
    session = {
        "session_id": "A",
        "events": [],
    }

    result = generate_geo_availability_features(session)

    assert result["latitude_mean"] == 0.0
    assert result["longitude_mean"] == 0.0
    assert result["geo_latitude_abs"] == 0.0
    assert result["geo_longitude_abs"] == 0.0
    assert result["geo_location_available"] is False
    assert result["ip_reputation_available"] is False
    assert result["ip_reputation_missing_count"] == 5


def test_invalid_geo_values_are_ignored():
    session = {
        "session_id": "A",
        "events": [
            {"latitude": "invalid", "longitude": "invalid"},
            {"latitude": 30.0, "longitude": 31.0},
        ],
    }

    result = generate_geo_availability_features(session)

    assert result["latitude_mean"] == 30.0
    assert result["longitude_mean"] == 31.0
    assert result["geo_latitude_abs"] == 30.0
    assert result["geo_longitude_abs"] == 31.0
    assert result["geo_location_available"] is True


def test_input_is_not_mutated():
    session = {
        "session_id": "A",
        "events": [
            {
                "latitude": 30.0,
                "longitude": 31.0,
                "ip_reputation": 80,
            }
        ],
    }

    original = deepcopy(session)

    generate_geo_availability_features(session)

    assert session == original
