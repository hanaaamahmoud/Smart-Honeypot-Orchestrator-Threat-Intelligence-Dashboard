"""Unit tests for mitre_statistics."""

import pytest

from app.analytics.mitre_statistics import (
    ANALYTICS_LAYER,
    STATISTIC_TYPES,
    build_mitre_statistics,
)


def make(**overrides):
    r = {
        "timestamp": "2025-06-10T10:00:00Z",
        "session_id": "s-001",
        "event_count": 5,
        "production_cluster_assignment": 28,
        "mitre_technique": "T1595",
        "attack_type": "SSH Connection Probe",
        "attack_stage": "Reconnaissance",
    }
    r.update(overrides)
    return r


# ---------------- Basic ----------------

def test_empty_input():
    result = build_mitre_statistics([])
    assert result["analytics_layer"] == ANALYTICS_LAYER
    assert result["statistics"] == []
    assert result["summary"]["total_rows"] == 0


def test_single_record_produces_5_rows():
    result = build_mitre_statistics([make()])
    types = [r["statistic_type"] for r in result["statistics"]]
    assert types.count("OVERALL") == 1
    assert types.count("CLUSTER") == 1
    assert types.count("MITRE_TECHNIQUE") == 1
    assert types.count("ATTACK_TYPE") == 1
    assert types.count("ATTACK_STAGE") == 1


def test_overall_row():
    result = build_mitre_statistics([make(), make(session_id="s-002")])
    overall = [r for r in result["statistics"] if r["statistic_type"] == "OVERALL"][0]
    assert overall["statistic_key"] == "ALL_SESSIONS"
    assert overall["session_count"] == 2
    assert overall["event_count"] == 10
    assert overall["session_share_pct"] == 100.0
    assert overall["mapped_mitre_sessions"] == 2
    assert overall["unmapped_mitre_sessions"] == 0


def test_cluster_rows():
    records = [
        make(session_id="s-1", production_cluster_assignment=5),
        make(session_id="s-2", production_cluster_assignment=5),
        make(session_id="s-3", production_cluster_assignment=10),
    ]
    result = build_mitre_statistics(records)
    clusters = {r["statistic_key"]: r for r in result["statistics"] if r["statistic_type"] == "CLUSTER"}
    assert clusters["5"]["session_count"] == 2
    assert clusters["10"]["session_count"] == 1


def test_mitre_technique_rows():
    records = [
        make(session_id="s-1", mitre_technique="T1595"),
        make(session_id="s-2", mitre_technique="T1595"),
        make(session_id="s-3", mitre_technique="T1110"),
    ]
    result = build_mitre_statistics(records)
    techs = {r["statistic_key"]: r for r in result["statistics"] if r["statistic_type"] == "MITRE_TECHNIQUE"}
    assert techs["T1595"]["session_count"] == 2
    assert techs["T1595"]["mitre_attack_name"] == "Active Scanning"
    assert techs["T1110"]["mitre_attack_name"] == "Brute Force"


def test_attack_type_rows():
    records = [
        make(session_id="s-1", attack_type="FTP Brute Force"),
        make(session_id="s-2", attack_type="FTP Brute Force"),
        make(session_id="s-3", attack_type="Network Scanning"),
    ]
    result = build_mitre_statistics(records)
    types = {r["statistic_key"]: r for r in result["statistics"] if r["statistic_type"] == "ATTACK_TYPE"}
    assert types["FTP Brute Force"]["session_count"] == 2
    assert types["Network Scanning"]["session_count"] == 1


def test_attack_stage_rows():
    records = [
        make(session_id="s-1", attack_stage="Reconnaissance"),
        make(session_id="s-2", attack_stage="Credential Access"),
    ]
    result = build_mitre_statistics(records)
    stages = {r["statistic_key"]: r for r in result["statistics"] if r["statistic_type"] == "ATTACK_STAGE"}
    assert "Reconnaissance" in stages
    assert "Credential Access" in stages


def test_empty_mitre_excluded_from_technique_rows():
    records = [
        make(session_id="s-1", mitre_technique=None),
        make(session_id="s-2", mitre_technique=""),
        make(session_id="s-3", mitre_technique="T1595"),
    ]
    result = build_mitre_statistics(records)
    techs = [r for r in result["statistics"] if r["statistic_type"] == "MITRE_TECHNIQUE"]
    assert len(techs) == 1
    # OVERALL must show unmapped count
    overall = [r for r in result["statistics"] if r["statistic_type"] == "OVERALL"][0]
    assert overall["mapped_mitre_sessions"] == 1
    assert overall["unmapped_mitre_sessions"] == 2


def test_session_share_pct():
    records = [
        make(session_id="s-1"),
        make(session_id="s-2"),
        make(session_id="s-3"),
        make(session_id="s-4"),
    ]
    result = build_mitre_statistics(records)
    tech = [r for r in result["statistics"] if r["statistic_type"] == "MITRE_TECHNIQUE"][0]
    assert tech["session_share_pct"] == 100.0


def test_event_count_summed():
    records = [
        make(session_id="s-1", event_count=10),
        make(session_id="s-2", event_count=20),
        make(session_id="s-3", event_count=30),
    ]
    result = build_mitre_statistics(records)
    overall = [r for r in result["statistics"] if r["statistic_type"] == "OVERALL"][0]
    assert overall["event_count"] == 60


def test_summary_by_type():
    result = build_mitre_statistics([make()])
    s = result["summary"]
    assert s["total_rows"] == 5
    assert s["by_statistic_type"]["OVERALL"] == 1
    assert s["by_statistic_type"]["CLUSTER"] == 1
    for t in STATISTIC_TYPES:
        assert t in s["by_statistic_type"]


def test_input_not_mutated():
    records = [make()]
    original = [dict(r) for r in records]
    build_mitre_statistics(records)
    assert records == original


def test_missing_timestamp_fails():
    with pytest.raises(ValueError, match="timestamp"):
        build_mitre_statistics([make(timestamp=None)])


def test_invalid_timestamp_fails():
    with pytest.raises(ValueError, match="timestamp"):
        build_mitre_statistics([make(timestamp="BAD")])


def test_unknown_technique_has_empty_attack_name():
    result = build_mitre_statistics([make(mitre_technique="T9999")])
    tech = [r for r in result["statistics"] if r["statistic_type"] == "MITRE_TECHNIQUE"][0]
    assert tech["mitre_technique"] == "T9999"
    assert tech["mitre_attack_name"] == ""


def test_non_applicable_fields_are_empty_string():
    result = build_mitre_statistics([make()])
    overall = [r for r in result["statistics"] if r["statistic_type"] == "OVERALL"][0]
    assert overall["mitre_technique"] == ""
    assert overall["attack_type"] == ""
    assert overall["attack_stage"] == ""
