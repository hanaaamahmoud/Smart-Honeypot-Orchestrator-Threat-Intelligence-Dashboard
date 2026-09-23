import json
from pathlib import Path

from app.analytics.cluster_analytics import (
    NOISE_CLUSTER_ID,
    OPTIONAL_FIELDS,
    OUTPUT_FIELDS,
    REQUIRED_FIELDS,
)


CONTRACT_PATH = (
    Path(__file__).parents[2]
    / "app"
    / "analytics"
    / "contracts"
    / "cluster_analytics_contract.json"
)


def load_contract():
    return json.loads(
        CONTRACT_PATH.read_text(encoding="utf-8")
    )


def test_contract_exists_and_is_valid_json():
    contract = load_contract()

    assert contract["name"] == "CLUSTER_ANALYTICS_CONTRACT"
    assert contract["version"] == "1.0.0"
    assert contract["status"] == "ACTIVE"


def test_contract_required_fields_match_implementation():
    contract = load_contract()

    assert tuple(
        contract["required_input_fields"]
    ) == REQUIRED_FIELDS


def test_contract_optional_fields_match_implementation():
    contract = load_contract()

    assert tuple(
        contract["optional_input_fields"]
    ) == OPTIONAL_FIELDS


def test_contract_output_fields_match_implementation():
    contract = load_contract()

    assert tuple(
        contract["output"]["required_fields"]
    ) == OUTPUT_FIELDS


def test_contract_output_grain_is_cluster():
    contract = load_contract()

    assert contract["output"]["grain"] == "CLUSTER"
    assert (
        contract["output"]["analytics_layer_value"]
        == "CLUSTER_ANALYTICS"
    )


def test_contract_noise_semantics_match_implementation():
    contract = load_contract()

    assert (
        contract["production_cluster_semantics"]["noise_cluster_id"]
        == NOISE_CLUSTER_ID
    )

    assert (
        contract["production_cluster_semantics"]
        ["noise_is_valid_production_assignment"]
        is True
    )


def test_contract_percentage_rule():
    contract = load_contract()

    percentage_rule = contract["percentage_rule"]

    assert percentage_rule["denominator"] == "total_input_sessions"
    assert (
        percentage_rule["formula"]
        == "cluster_session_count / total_input_sessions * 100"
    )
    assert percentage_rule["empty_input_percentage"] == 0.0


def test_contract_geoip_is_optional():
    contract = load_contract()

    geoip = contract["geoip_behavior"]

    assert geoip["required"] is False
    assert geoip["dependency"] is False
    assert geoip["lookup_performed"] is False
    assert geoip["external_provider_called"] is False
    assert geoip["missing_geoip_blocks_cluster_analytics"] is False


def test_contract_has_production_assignment_boundaries():
    contract = load_contract()

    rules = contract["transformation"]["rules"]

    assert "Do not refit DBSCAN." in rules
    assert "Do not retrain the model." in rules
    assert "Do not create new clusters." in rules
    assert "Do not modify production cluster assignments." in rules
    assert "Do not perform GeoIP lookup." in rules


def test_contract_independence():
    contract = load_contract()

    independence = contract["independence"]

    assert independence["depends_on_session_analytics"] is False
    assert independence["depends_on_attacker_ip_analytics"] is False
    assert independence["depends_on_geoip_analytics"] is False
    assert (
        independence["consumes_production_ml_output_directly"]
        is True
    )


def test_contract_empty_data_behavior():
    contract = load_contract()

    empty = contract["empty_data_behavior"]

    assert empty["allowed"] is True
    assert empty["analytics_layer"] == "CLUSTER_ANALYTICS"
    assert empty["cluster_count"] == 0
    assert empty["session_count"] == 0
    assert empty["noise_session_count"] == 0
    assert empty["clusters"] == []


def test_contract_validation_rules_are_present():
    contract = load_contract()

    validation_tests = set(contract["validation_tests"])

    expected = {
        "required fields are present",
        "required fields are non-empty",
        "production cluster assignment is preserved",
        "noise cluster is represented by -1",
        "noise assignment is valid",
        "nearest behavioral cluster may differ from production assignment",
        "nearest behavioral distance is optional enrichment",
        "reference artifacts are read-only",
        "GeoIP enrichment is not required",
        "missing optional enrichment does not fail validation",
        "empty input returns valid zero-state analytics",
        "cluster percentages use total input sessions as denominator",
        "input records are not mutated",
        "no DBSCAN fitting is performed",
        "no retraining is performed",
        "no new cluster is created",
        "no external enrichment is performed",
    }

    assert expected.issubset(validation_tests)
