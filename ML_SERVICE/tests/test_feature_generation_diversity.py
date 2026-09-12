from copy import deepcopy

from app.pipeline.feature_generation_diversity import (
    generate_diversity_features,
)


def _sample_session():
    return {
        "session_id": "session-A",
        "events": [
            {
                "destination": "10.0.0.1",
                "destination_port": 22,
                "source_ip": "192.168.1.10",
                "protocol": "tcp",
                "honeypot": "hp-01",
                "username": "root",
                "country": "Egypt",
                "country_code": "EG",
                "city": "Cairo",
            },
            {
                "destination": "10.0.0.1",
                "destination_port": 22,
                "source_ip": "192.168.1.10",
                "protocol": "tcp",
                "honeypot": "hp-01",
                "username": "root",
                "country": "Egypt",
                "country_code": "EG",
                "city": "Cairo",
            },
            {
                "destination": "10.0.0.2",
                "destination_port": 80,
                "source_ip": "192.168.1.11",
                "protocol": "http",
                "honeypot": "hp-02",
                "username": "admin",
                "country": "USA",
                "country_code": "US",
                "city": "New York",
            },
        ],
    }


def test_exact_diversity_feature_names():
    result = generate_diversity_features(
        _sample_session()
    )

    assert list(result.keys()) == [
        "unique_destinations",
        "unique_destination_ports",
        "unique_source_ips",
        "unique_protocols",
        "unique_honeypots",
        "unique_usernames",
        "unique_countries",
        "unique_country_codes",
        "unique_cities",
        "destination_diversity",
        "destination_port_diversity",
        "protocol_diversity",
        "honeypot_diversity",
        "username_diversity",
        "geo_country_diversity",
        "geo_city_diversity",
    ]


def test_unique_destinations():
    result = generate_diversity_features(
        _sample_session()
    )

    assert result["unique_destinations"] == 2


def test_unique_destination_ports():
    result = generate_diversity_features(
        _sample_session()
    )

    assert result["unique_destination_ports"] == 2


def test_unique_source_ips():
    result = generate_diversity_features(
        _sample_session()
    )

    assert result["unique_source_ips"] == 2


def test_unique_protocols():
    result = generate_diversity_features(
        _sample_session()
    )

    assert result["unique_protocols"] == 2


def test_unique_honeypots():
    result = generate_diversity_features(
        _sample_session()
    )

    assert result["unique_honeypots"] == 2


def test_unique_usernames():
    result = generate_diversity_features(
        _sample_session()
    )

    assert result["unique_usernames"] == 2


def test_unique_geo_fields():
    result = generate_diversity_features(
        _sample_session()
    )

    assert result["unique_countries"] == 2
    assert result["unique_country_codes"] == 2
    assert result["unique_cities"] == 2


def test_diversity_features():
    result = generate_diversity_features(
        _sample_session()
    )

    assert result["destination_diversity"] == 2 / 3
    assert result["destination_port_diversity"] == 2 / 3
    assert result["protocol_diversity"] == 2 / 3
    assert result["honeypot_diversity"] == 2 / 3
    assert result["username_diversity"] == 2 / 3
    assert result["geo_country_diversity"] == 2 / 3
    assert result["geo_city_diversity"] == 2 / 3


def test_duplicate_values_do_not_increase_cardinality():
    session = {
        "session_id": "A",
        "events": [
            {"destination": "1.1.1.1"},
            {"destination": "1.1.1.1"},
            {"destination": "1.1.1.1"},
        ],
    }

    result = generate_diversity_features(session)

    assert result["unique_destinations"] == 1


def test_duplicate_values_do_not_increase_diversity():
    session = {
        "session_id": "A",
        "events": [
            {"destination": "1.1.1.1"},
            {"destination": "1.1.1.1"},
            {"destination": "1.1.1.1"},
        ],
    }

    result = generate_diversity_features(session)

    assert result["destination_diversity"] == 1 / 3


def test_missing_values_are_not_counted():
    session = {
        "session_id": "A",
        "events": [
            {"destination": None},
            {"destination": ""},
            {"destination": "1.1.1.1"},
        ],
    }

    result = generate_diversity_features(session)

    assert result["unique_destinations"] == 1
    assert result["destination_diversity"] == 1 / 3


def test_empty_session_returns_zero():
    session = {
        "session_id": "A",
        "events": [],
    }

    result = generate_diversity_features(session)

    assert all(
        value == 0
        for value in result.values()
    )


def test_input_is_not_mutated():
    session = _sample_session()
    original = deepcopy(session)

    generate_diversity_features(session)

    assert session == original
