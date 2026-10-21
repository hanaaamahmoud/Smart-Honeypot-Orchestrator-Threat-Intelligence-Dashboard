import json
from pathlib import Path

import pytest

from app.analytics.attacker_ip_analytics import (
    build_attacker_ip_analytics,
    validate_attacker_ip_record,
)


CONTRACT_PATH = (
    Path(__file__).resolve().parents[2]
    / "app"
    / "analytics"
    / "contracts"
    / "attacker_ip_analytics_contract.json"
)


@pytest.fixture
def contract():
    with CONTRACT_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


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
    }


def test_contract_identity(contract):
    assert contract["name"] == "ATTACKER_IP_ANALYTICS_CONTRACT"
    assert contract["version"] == "1.0.0"
    assert contract["status"] == "ACTIVE"


def test_contract_required_fields(contract):
    required = set(
        contract["required_input_fields"]
    )

    assert {
        "source_ip",
        "ip_scope",
        "resolution_status",
        "location_source",
        "dashboard_source",
    }.issubset(required)


def test_contract_output_grain(contract):
    assert contract["output"]["grain"] == "ATTACKER_IP"


def test_contract_is_independent(contract):
    independence = contract["independence"]

    assert independence[
        "depends_on_session_analytics"
    ] is False

    assert independence[
        "depends_on_cluster_analytics"
    ] is False

    assert independence[
        "consumes_production_ml_output_directly"
    ] is True


def test_contract_forbids_external_enrichment(contract):
    rules = contract["transformation"]["rules"]

    assert "Do not perform GeoIP lookup." in rules
    assert "Do not call external providers." in rules


def test_valid_record_matches_contract():
    result = validate_attacker_ip_record(_record())

    assert result["valid"] is True


def test_unresolved_geoip_is_valid():
    record = _record()

    record["resolution_status"] = "UNRESOLVED"
    record.pop("country")
    record.pop("country_code")
    record.pop("city")
    record.pop("asn")
    record.pop("asn_org")

    result = build_attacker_ip_analytics([record])

    assert result["analytics_layer"] == (
        "ATTACKER_IP_ANALYTICS"
    )
    assert result["unresolved_source_ips"] == 1
