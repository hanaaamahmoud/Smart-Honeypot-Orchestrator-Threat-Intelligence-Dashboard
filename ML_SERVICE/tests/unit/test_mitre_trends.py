"""Unit tests for mitre_trends."""

import pytest

from app.analytics.mitre_trends import (
    ANALYTICS_LAYER,
    TREND_DIMENSIONS,
    build_mitre_trends,
)


def make(**o):
    r = {
        "timestamp": "2025-06-10T10:00:00Z",
        "session_id": "s-001",
        "event_count": 5,
        "mitre_technique": "T1595",
        "attack_type": "SSH Probe",
        "attack_stage": "Reconnaissance",
    }
    r.update(o)
    return r


def test_empty_input():
    result = build_mitre_trends([])
    assert result["analytics_layer"] == ANALYTICS_LAYER
    assert result["trends"] == []
    assert result["summary"]["total_trend_rows"] == 0


def test_single_record_creates_3_dim_rows():
    result = build_mitre_trends([make()])
    # Each record contributes to 3 dimensions
    assert len(result["trends"]) == 3
    dims = {r["trend_dimension"] for r in result["trends"]}
    assert dims == set(TREND_DIMENSIONS)


def test_same_day_aggregation():
    records = [
        make(session_id="s-1"),
        make(session_id="s-2"),
    ]
    result = build_mitre_trends(records)
    # One (day, dim, value) row per dimension
    assert len(result["trends"]) == 3
    for r in result["trends"]:
        assert r["session_count"] == 2


def test_different_days():
    records = [
        make(session_id="s-1", timestamp="2025-06-10T10:00:00Z"),
        make(session_id="s-2", timestamp="2025-06-11T10:00:00Z"),
    ]
    result = build_mitre_trends(records)
    dates = {r["trend_date"] for r in result["trends"]}
    assert dates == {"2025-06-10", "2025-06-11"}


def test_empty_mitre_skipped():
    records = [
        make(session_id="s-1", mitre_technique=None),
        make(session_id="s-2", mitre_technique="T1595"),
    ]
    result = build_mitre_trends(records)
    tech_rows = [r for r in result["trends"] if r["trend_dimension"] == "MITRE_TECHNIQUE"]
    # Only one technique value (T1595) across the day
    assert len(tech_rows) == 1
    assert tech_rows[0]["trend_value"] == "T1595"
    assert tech_rows[0]["session_count"] == 1


def test_event_count_summed():
    records = [
        make(session_id="s-1", event_count=10),
        make(session_id="s-2", event_count=20),
    ]
    result = build_mitre_trends(records)
    tech_row = [r for r in result["trends"] if r["trend_dimension"] == "MITRE_TECHNIQUE"][0]
    assert tech_row["event_count"] == 30


def test_summary_by_dimension():
    result = build_mitre_trends([make()])
    s = result["summary"]
    assert s["total_records"] == 1
    assert s["total_trend_rows"] == 3
    for d in TREND_DIMENSIONS:
        assert s["by_dimension"][d] == 1


def test_missing_timestamp_fails():
    with pytest.raises(ValueError, match="timestamp"):
        build_mitre_trends([make(timestamp=None)])


def test_input_not_mutated():
    records = [make()]
    original = [dict(r) for r in records]
    build_mitre_trends(records)
    assert records == original


def test_unique_dates():
    records = [
        make(session_id="s-1", timestamp="2025-06-10T10:00:00Z"),
        make(session_id="s-2", timestamp="2025-06-10T11:00:00Z"),
        make(session_id="s-3", timestamp="2025-06-11T10:00:00Z"),
    ]
    result = build_mitre_trends(records)
    assert result["summary"]["unique_dates"] == 2


# ===============================================================
# NEW: series + top_values
# ===============================================================

def test_series_exists_and_grouped():
    records = [
        make(session_id="s-1", timestamp="2025-06-10T10:00:00Z"),
        make(session_id="s-2", timestamp="2025-06-11T10:00:00Z"),
    ]
    result = build_mitre_trends(records)
    assert "series" in result
    tech_series = result["series"]["MITRE_TECHNIQUE"]
    assert "T1595" in tech_series
    points = tech_series["T1595"]
    assert len(points) == 2
    assert points[0]["date"] == "2025-06-10"
    assert points[1]["date"] == "2025-06-11"
    assert points[0]["session_count"] == 1


def test_series_sorted_by_date():
    records = [
        make(session_id="s-3", timestamp="2025-06-11T10:00:00Z"),
        make(session_id="s-1", timestamp="2025-06-09T10:00:00Z"),
        make(session_id="s-2", timestamp="2025-06-10T10:00:00Z"),
    ]
    result = build_mitre_trends(records)
    points = result["series"]["MITRE_TECHNIQUE"]["T1595"]
    dates = [p["date"] for p in points]
    assert dates == ["2025-06-09", "2025-06-10", "2025-06-11"]


def test_top_values_per_dimension():
    records = [
        make(session_id="s-1", mitre_technique="T1595"),
        make(session_id="s-2", mitre_technique="T1595"),
        make(session_id="s-3", mitre_technique="T1595"),
        make(session_id="s-4", mitre_technique="T1110"),
    ]
    result = build_mitre_trends(records)
    top = result["top_values"]["MITRE_TECHNIQUE"]
    assert top[0]["value"] == "T1595"
    assert top[0]["total_sessions"] == 3
    assert top[1]["value"] == "T1110"
    assert top[1]["total_sessions"] == 1


def test_top_values_capped_at_10():
    records = [
        make(session_id=f"s-{i}", mitre_technique=f"T{i:04d}")
        for i in range(20)
    ]
    result = build_mitre_trends(records)
    top = result["top_values"]["MITRE_TECHNIQUE"]
    assert len(top) == 10


def test_empty_input_has_empty_series():
    result = build_mitre_trends([])
    assert result["series"] == {d: {} for d in TREND_DIMENSIONS}
    assert result["top_values"] == {d: [] for d in TREND_DIMENSIONS}
