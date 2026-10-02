"""Unit tests for mitre_analytics."""

import pytest

from app.analytics.mitre_analytics import (
    ANALYTICS_LAYER,
    OUTPUT_REQUIRED_FIELDS,
    build_mitre_analytics,
)


def make_record(**overrides):
    r = {
        "timestamp": "2025-06-10T10:00:00Z",
        "session_id": "s-001",
        "mitre_technique": "T1595",
        "attack_type": "SSH Connection Probe",
        "attack_stage": "Reconnaissance",
        "severity": "Low",
    }
    r.update(overrides)
    return r


def test_empty_input_returns_zero_state():
    result = build_mitre_analytics([])
    assert result["analytics_layer"] == ANALYTICS_LAYER
    assert result["mitre_technique_distribution"] == []
    assert result["summary"]["total_records"] == 0


def test_output_has_required_fields():
    result = build_mitre_analytics([make_record()])
    for f in OUTPUT_REQUIRED_FIELDS:
        assert f in result


def test_single_record_distribution():
    result = build_mitre_analytics([make_record()])
    assert len(result["mitre_technique_distribution"]) == 1
    assert result["mitre_technique_distribution"][0]["value"] == "T1595"
    assert result["mitre_technique_distribution"][0]["count"] == 1
    assert result["mitre_technique_distribution"][0]["percentage"] == 100.0


def test_multiple_records_distribution():
    records = [
        make_record(session_id="s-1", mitre_technique="T1595"),
        make_record(session_id="s-2", mitre_technique="T1595"),
        make_record(session_id="s-3", mitre_technique="T1110"),
    ]
    result = build_mitre_analytics(records)
    dist = {d["value"]: d for d in result["mitre_technique_distribution"]}
    assert dist["T1595"]["count"] == 2
    assert dist["T1110"]["count"] == 1
    assert dist["T1595"]["percentage"] == pytest.approx(66.67, abs=0.01)
    assert dist["T1110"]["percentage"] == pytest.approx(33.33, abs=0.01)


def test_empty_mitre_values_are_not_fabricated():
    records = [
        make_record(mitre_technique=None),
        make_record(mitre_technique=""),
        make_record(mitre_technique="  "),
        make_record(mitre_technique="T1595"),
    ]
    result = build_mitre_analytics(records)
    # Only 1 record has valid MITRE
    assert len(result["mitre_technique_distribution"]) == 1
    assert result["mitre_technique_distribution"][0]["value"] == "T1595"
    assert result["summary"]["records_with_mitre"] == 1
    assert result["summary"]["total_records"] == 4


def test_empty_attack_type_and_stage_ok():
    records = [make_record(attack_type=None, attack_stage=None)]
    result = build_mitre_analytics(records)
    assert result["attack_type_distribution"] == []
    assert result["attack_stage_distribution"] == []


def test_session_relationships():
    records = [
        make_record(session_id="s-1", mitre_technique="T1595"),
        make_record(session_id="s-1", mitre_technique="T1110"),
        make_record(session_id="s-2", mitre_technique="T1190"),
    ]
    result = build_mitre_analytics(records)
    rels = {r["session_id"]: r for r in result["session_mitre_relationships"]}
    assert set(rels["s-1"]["mitre_techniques"]) == {"T1595", "T1110"}
    assert rels["s-2"]["mitre_techniques"] == ["T1190"]


def test_activity_over_time():
    records = [
        make_record(timestamp="2025-06-10T10:00:00Z", session_id="s-1"),
        make_record(timestamp="2025-06-10T11:00:00Z", session_id="s-2"),
        make_record(timestamp="2025-06-11T10:00:00Z", session_id="s-3"),
    ]
    result = build_mitre_analytics(records)
    activity = {a["date"]: a["count"] for a in result["mitre_activity_over_time"]}
    assert activity["2025-06-10"] == 2
    assert activity["2025-06-11"] == 1


def test_missing_timestamp_fails():
    with pytest.raises(ValueError, match="timestamp"):
        build_mitre_analytics([make_record(timestamp=None)])


def test_invalid_timestamp_fails():
    with pytest.raises(ValueError, match="timestamp"):
        build_mitre_analytics([make_record(timestamp="NOT-A-DATE")])


def test_missing_required_field_fails():
    record = make_record()
    del record["timestamp"]
    with pytest.raises(ValueError, match="Missing required"):
        build_mitre_analytics([record])


def test_input_not_mutated():
    records = [make_record()]
    original = [dict(r) for r in records]
    build_mitre_analytics(records)
    assert records == original


def test_summary_counts():
    records = [
        make_record(session_id="s-1", mitre_technique="T1595", attack_type="SSH Probe", attack_stage="Recon"),
        make_record(session_id="s-2", mitre_technique="T1110", attack_type="Brute Force", attack_stage="Cred Access"),
        make_record(session_id="s-3", mitre_technique=None, attack_type=None, attack_stage=None),
    ]
    result = build_mitre_analytics(records)
    s = result["summary"]
    assert s["total_records"] == 3
    assert s["records_with_mitre"] == 2
    assert s["records_with_attack_type"] == 2
    assert s["records_with_attack_stage"] == 2
    assert s["unique_techniques"] == 2
    assert s["unique_attack_types"] == 2
    assert s["unique_attack_stages"] == 2


# ===============================================================
# NEW: Tactics mapping + top source IPs
# ===============================================================

def test_tactic_mapping_in_technique_distribution():
    records = [
        make_record(session_id="s-1", mitre_technique="T1595"),
        make_record(session_id="s-2", mitre_technique="T1110"),
        make_record(session_id="s-3", mitre_technique="T1190"),
    ]
    result = build_mitre_analytics(records)
    dist = {d["value"]: d for d in result["mitre_technique_distribution"]}
    assert dist["T1595"]["tactic"] == "Reconnaissance"
    assert dist["T1110"]["tactic"] == "Credential Access"
    assert dist["T1190"]["tactic"] == "Initial Access"


def test_unknown_technique_has_no_tactic():
    records = [make_record(mitre_technique="T9999")]
    result = build_mitre_analytics(records)
    assert result["mitre_technique_distribution"][0]["tactic"] is None


def test_tactics_distribution_aggregation():
    records = [
        make_record(session_id="s-1", mitre_technique="T1595"),
        make_record(session_id="s-2", mitre_technique="T1592"),  # also Recon
        make_record(session_id="s-3", mitre_technique="T1110"),  # Cred Access
    ]
    result = build_mitre_analytics(records)
    tactics = {t["value"]: t for t in result["mitre_tactics_distribution"]}
    assert tactics["Reconnaissance"]["count"] == 2
    assert tactics["Credential Access"]["count"] == 1


def test_top_source_ips_per_technique():
    records = [
        make_record(session_id="s-1", mitre_technique="T1595", source_ip="1.1.1.1"),
        make_record(session_id="s-2", mitre_technique="T1595", source_ip="1.1.1.1"),
        make_record(session_id="s-3", mitre_technique="T1595", source_ip="2.2.2.2"),
        make_record(session_id="s-4", mitre_technique="T1110", source_ip="3.3.3.3"),
    ]
    result = build_mitre_analytics(records)
    dist = {d["value"]: d for d in result["mitre_technique_distribution"]}
    t1595_ips = {x["ip"]: x["session_count"] for x in dist["T1595"]["top_source_ips"]}
    assert t1595_ips == {"1.1.1.1": 2, "2.2.2.2": 1}
    t1110_ips = {x["ip"]: x["session_count"] for x in dist["T1110"]["top_source_ips"]}
    assert t1110_ips == {"3.3.3.3": 1}


def test_top_source_ips_capped_at_5():
    records = [
        make_record(session_id=f"s-{i}", mitre_technique="T1595", source_ip=f"{i}.{i}.{i}.{i}")
        for i in range(1, 11)
    ]
    result = build_mitre_analytics(records)
    entry = result["mitre_technique_distribution"][0]
    assert len(entry["top_source_ips"]) == 5


def test_summary_includes_unique_tactics():
    records = [
        make_record(session_id="s-1", mitre_technique="T1595"),
        make_record(session_id="s-2", mitre_technique="T1110"),
    ]
    result = build_mitre_analytics(records)
    assert result["summary"]["unique_tactics"] == 2
