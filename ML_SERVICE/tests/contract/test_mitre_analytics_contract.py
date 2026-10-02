"""Contract tests for mitre_analytics."""

import json
from pathlib import Path

from app.analytics.mitre_analytics import (
    ANALYTICS_LAYER,
    OUTPUT_REQUIRED_FIELDS,
)


CONTRACT_PATH = (
    Path(__file__).parents[2]
    / "app"
    / "analytics"
    / "contracts"
    / "mitre_analytics_contract.json"
)


def load_contract():
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def test_contract_exists_and_active():
    c = load_contract()
    assert c["contract_name"] == "MITRE_ANALYTICS"
    assert c["status"] == "ACTIVE"
    assert c["version"] == "2.0.0"


def test_analytics_layer_matches():
    c = load_contract()
    assert c["output"]["required_fields"][0] == "analytics_layer"


def test_output_required_fields_match():
    c = load_contract()
    contract_fields = tuple(c["output"]["required_fields"])
    # Every contract field must be present in our constant
    for f in contract_fields:
        assert f in OUTPUT_REQUIRED_FIELDS


def test_primary_dimension_is_mitre_technique():
    c = load_contract()
    assert c["primary_analytics_dimension"] == "mitre_technique"


def test_no_fabrication_rule_present():
    c = load_contract()
    rules = c["transformation_rules"]
    assert any("must not fabricate" in r.lower() for r in rules)
    assert any("must not generate" in r.lower() for r in rules)


def test_mitre_empty_values_not_fabricated():
    c = load_contract()
    behavior = c["null_empty_rules"]["mitre_technique"]["behavior"]
    assert "not be fabricated" in behavior.lower()


def test_independence_declarations():
    c = load_contract()
    indep = c["independence"]
    assert indep["depends_on_session_analytics"] is False
    assert indep["depends_on_cluster_analytics"] is False
    assert indep["depends_on_temporal_analytics"] is False
    assert indep["consumes_ml_output_directly"] is True


def test_analytics_layer_value():
    assert ANALYTICS_LAYER == "MITRE_ANALYTICS"
