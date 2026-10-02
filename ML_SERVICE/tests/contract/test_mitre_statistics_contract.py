"""Contract tests for mitre_statistics."""

import json
from pathlib import Path

from app.analytics.mitre_statistics import (
    ANALYTICS_LAYER,
    STATISTIC_TYPES,
)


CONTRACT_PATH = (
    Path(__file__).parents[2]
    / "app"
    / "analytics"
    / "contracts"
    / "mitre_statistics_contract.json"
)


def load_contract():
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def test_contract_active():
    c = load_contract()
    assert c["contract_name"] == "MITRE_STATISTICS"
    assert c["status"] == "ACTIVE"
    assert c["version"] == "2.0.0"


def test_grain():
    c = load_contract()
    assert c["grain"] == "STATISTIC_RECORD"


def test_statistic_types_match():
    c = load_contract()
    assert tuple(c["statistic_types"]) == STATISTIC_TYPES


def test_required_output_fields():
    c = load_contract()
    required = c["output"]["required_fields"]
    for f in [
        "statistic_type",
        "statistic_key",
        "session_count",
        "event_count",
        "session_share_pct",
    ]:
        assert f in required


def test_percentage_rule():
    c = load_contract()
    rule = c["session_share_pct_rule"]
    assert rule["denominator"] == "total_sessions"
    assert rule["rounded_to"] == 2


def test_no_fabrication_rule_present():
    c = load_contract()
    rules = " ".join(c["transformation_rules"]).lower()
    assert "no fabrication" in rules or "must not be invented" in rules


def test_independence():
    c = load_contract()
    indep = c["independence"]
    assert indep["depends_on_mitre_analytics"] is False
    assert indep["depends_on_cluster_analytics"] is False
    assert indep["consumes_ml_output_directly"] is True


def test_analytics_layer_value():
    assert ANALYTICS_LAYER == "MITRE_STATISTICS"
