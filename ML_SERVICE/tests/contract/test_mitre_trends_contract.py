"""Contract tests for mitre_trends."""

import json
from pathlib import Path

from app.analytics.mitre_trends import (
    ANALYTICS_LAYER,
    TREND_DIMENSIONS,
)


CONTRACT_PATH = (
    Path(__file__).parents[2]
    / "app"
    / "analytics"
    / "contracts"
    / "mitre_trends_contract.json"
)


def load_contract():
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def test_contract_active():
    c = load_contract()
    assert c["contract_name"] == "MITRE_TRENDS"
    assert c["status"] == "ACTIVE"
    assert c["version"] == "2.0.0"


def test_grain():
    c = load_contract()
    assert c["grain"] == "TREND_RECORD"


def test_dimensions_match():
    c = load_contract()
    assert tuple(c["trend_dimensions"]) == TREND_DIMENSIONS


def test_required_output_fields():
    c = load_contract()
    for f in ["trend_date", "trend_dimension", "trend_value", "session_count", "event_count"]:
        assert f in c["output"]["required_fields"]


def test_no_fabrication_rule_present():
    c = load_contract()
    rules = " ".join(c["transformation_rules"]).lower()
    assert "no fabrication" in rules


def test_independence():
    c = load_contract()
    indep = c["independence"]
    assert indep["depends_on_mitre_analytics"] is False
    assert indep["depends_on_mitre_statistics"] is False
    assert indep["consumes_ml_output_directly"] is True


def test_analytics_layer_value():
    assert ANALYTICS_LAYER == "MITRE_TRENDS"
