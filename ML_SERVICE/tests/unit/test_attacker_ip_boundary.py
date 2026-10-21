from app.analytics.attacker_ip_boundary import (
    build_attacker_ip_analytics_input,
)


def _record():
    return {
        "source_ip": "8.8.8.8",
        "ip_scope": "PUBLIC",
        "resolution_status": "RESOLVED",
        "location_source": "GEOIP",
        "dashboard_source": "ELK",
        "country": "US",
        "country_code": "US",
        "city": "Mountain View",
        "asn": 15169,
        "asn_org": "Google LLC",
        "production_cluster_assignment": 3,
        "reconstructed_session_id": "session-1",
    }


def test_boundary_accepts_production_results():
    result = build_attacker_ip_analytics_input(
        [_record()]
    )

    assert len(result) == 1
    assert result[0]["source_ip"] == "8.8.8.8"


def test_boundary_preserves_existing_enrichment():
    record = _record()

    result = build_attacker_ip_analytics_input(
        [record]
    )

    assert result[0]["country"] == "US"
    assert result[0]["country_code"] == "US"
    assert result[0]["city"] == "Mountain View"
    assert result[0]["asn"] == 15169


def test_boundary_preserves_ml_assignment():
    record = _record()

    result = build_attacker_ip_analytics_input(
        [record]
    )

    assert result[0]["production_cluster_assignment"] == 3


def test_boundary_does_not_modify_input():
    record = _record()
    original = record.copy()

    build_attacker_ip_analytics_input([record])

    assert record == original


def test_boundary_allows_missing_optional_geoip():
    record = {
        "source_ip": "10.0.0.5",
        "ip_scope": "PRIVATE",
        "resolution_status": "UNRESOLVED",
        "location_source": "NONE",
        "dashboard_source": "ELK",
    }

    result = build_attacker_ip_analytics_input([record])

    assert result[0]["source_ip"] == "10.0.0.5"
    assert result[0]["resolution_status"] == "UNRESOLVED"
