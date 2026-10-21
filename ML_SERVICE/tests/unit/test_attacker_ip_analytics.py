import pytest

from app.analytics.attacker_ip_analytics import (
    ATTACKER_IP_FIELDS,
    build_attacker_ip_analytics,
    summarize_location_source,
    summarize_resolution_status,
    validate_attacker_ip_record,
)


def _base_record(**overrides):
    record = {
        "source_ip": "203.0.113.10",
        "event_count": "100",
        "unique_sessions": "10",
        "unique_destinations": "2",
        "unique_destination_ports": "1",
        "unique_protocols": "1",
        "unique_honeypots": "1",
        "unique_usernames": "5",
        "unique_countries": "1",
        "unique_country_codes": "1",
        "unique_geoip_countries": "1",
        "unique_geoip_cities": "1",
        "auth_attempt_total": "20",
        "user_attempt_total": "20",
        "pass_attempt_total": "20",
        "command_count_total": "3",
        "anonymous_total": "0",
        "first_seen": "2026-08-10T00:00:00Z",
        "last_seen": "2026-08-10T01:00:00Z",
        "dominant_attack_type": "ssh_bruteforce",
        "dominant_protocol": "SSH",
        "dominant_honeypot": "cowrie",
        "ip_scope": "PUBLIC",
        "resolution_status": "RESOLVED_GEOIP",
        "location_source": "GeoLite2",
        "country": "United States",
        "country_code": "US",
        "city": "Secaucus",
        "latitude": "40.7908",
        "longitude": "-74.056",
        "asn": "32475",
        "asn_org": "Internap Holding LLC",
        "dashboard_source": "Step8C2",
    }

    record.update(overrides)
    return record


def test_attacker_ip_contract_has_33_fields():
    assert len(ATTACKER_IP_FIELDS) == 33


def test_attacker_ip_contract_field_names():
    assert "source_ip" in ATTACKER_IP_FIELDS
    assert "ip_scope" in ATTACKER_IP_FIELDS
    assert "resolution_status" in ATTACKER_IP_FIELDS
    assert "location_source" in ATTACKER_IP_FIELDS
    assert "country" in ATTACKER_IP_FIELDS
    assert "country_code" in ATTACKER_IP_FIELDS
    assert "city" in ATTACKER_IP_FIELDS
    assert "asn" in ATTACKER_IP_FIELDS
    assert "asn_org" in ATTACKER_IP_FIELDS


def test_valid_attacker_ip_record():
    result = validate_attacker_ip_record(_base_record())

    assert result["valid"] is True
    assert result["source_ip"] == "203.0.113.10"
    assert result["ip_scope"] == "PUBLIC"
    assert result["resolution_status"] == "RESOLVED_GEOIP"
    assert result["location_source"] == "GeoLite2"


def test_unresolved_geoip_is_valid():
    record = _base_record(
        resolution_status="UNRESOLVED",
        location_source="GeoLite2_NO_MATCH",
        country="",
        country_code="",
        city="",
        latitude="",
        longitude="",
        asn="",
        asn_org="",
    )

    result = validate_attacker_ip_record(record)

    assert result["valid"] is True
    assert result["resolution_status"] == "UNRESOLVED"
    assert result["location_source"] == "GeoLite2_NO_MATCH"


def test_missing_optional_geoip_is_valid():
    record = _base_record(
        country="",
        country_code="",
        city="",
        latitude="",
        longitude="",
        asn="",
        asn_org="",
    )

    result = validate_attacker_ip_record(record)

    assert result["valid"] is True
    assert result["source_ip"] == "203.0.113.10"


def test_missing_source_ip_fails():
    record = _base_record(source_ip="")

    with pytest.raises(ValueError):
        validate_attacker_ip_record(record)


def test_missing_resolution_status_fails():
    record = _base_record(
        resolution_status="",
    )

    with pytest.raises(ValueError):
        validate_attacker_ip_record(record)


def test_attacker_ip_analytics_consumes_existing_values():
    records = [
        _base_record(
            source_ip="203.0.113.10",
            country="United States",
            country_code="US",
            city="Secaucus",
            asn="32475",
        ),
        _base_record(
            source_ip="203.0.113.77",
            country="Hong Kong",
            country_code="HK",
            city="Hong Kong",
            asn="45102",
            resolution_status="RESOLVED_GEOIP_EXTERNAL",
        ),
        _base_record(
            source_ip="192.0.2.44",
            country="",
            country_code="",
            city="",
            asn="",
            asn_org="",
            resolution_status="UNRESOLVED",
            location_source="GeoLite2_NO_MATCH",
        ),
    ]

    result = build_attacker_ip_analytics(records)

    assert result["analytics_layer"] == "ATTACKER_IP_ANALYTICS"
    assert result["row_count"] == 3
    assert result["unique_source_ips"] == 3

    assert result["public_source_ips"] == 3
    assert result["resolved_source_ips"] == 2
    assert result["unresolved_source_ips"] == 1

    assert result["country_diversity"] == 2
    assert result["country_code_diversity"] == 2
    assert result["city_diversity"] == 2
    assert result["asn_diversity"] == 2

    assert result["geoip_resolved_ratio"] == pytest.approx(2 / 3)


def test_resolution_status_summary():
    records = [
        _base_record(
            resolution_status="RESOLVED_GEOIP",
        ),
        _base_record(
            source_ip="203.0.113.77",
            resolution_status="RESOLVED_GEOIP_EXTERNAL",
        ),
        _base_record(
            source_ip="192.0.2.44",
            resolution_status="UNRESOLVED",
        ),
    ]

    result = summarize_resolution_status(records)

    assert result == {
        "RESOLVED_GEOIP": 1,
        "RESOLVED_GEOIP_EXTERNAL": 1,
        "UNRESOLVED": 1,
    }


def test_location_source_summary():
    records = [
        _base_record(location_source="GeoLite2"),
        _base_record(
            source_ip="203.0.113.77",
            location_source="GeoLite2",
        ),
        _base_record(
            source_ip="192.0.2.44",
            location_source="GeoLite2_NO_MATCH",
        ),
    ]

    result = summarize_location_source(records)

    assert result == {
        "GeoLite2": 2,
        "GeoLite2_NO_MATCH": 1,
    }


def test_empty_input():
    result = build_attacker_ip_analytics([])

    assert result["analytics_layer"] == "ATTACKER_IP_ANALYTICS"
    assert result["row_count"] == 0
    assert result["unique_source_ips"] == 0
    assert result["resolved_source_ips"] == 0
    assert result["unresolved_source_ips"] == 0
    assert result["geoip_resolved_ratio"] == 0.0
