"""MITRE trends for ML session output.

Produces:
- `trends`: flat list of (day, dimension, value) records
- `series`: chart-ready nested dict (dimension -> value -> [points])
- `top_values`: top values per dimension (for chart legends)

Does NOT fabricate values.
"""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from typing import Any, Iterable


ANALYTICS_LAYER = "MITRE_TRENDS"

TREND_DIMENSIONS = (
    "MITRE_TECHNIQUE",
    "ATTACK_TYPE",
    "ATTACK_STAGE",
)

DIMENSION_FIELD_MAP = {
    "MITRE_TECHNIQUE": "mitre_technique",
    "ATTACK_TYPE": "attack_type",
    "ATTACK_STAGE": "attack_stage",
}

REQUIRED_INPUT_FIELDS = ("timestamp",)

# How many top values to expose per dimension (for chart legends).
TOP_N = 10


# ---------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------

def _clean(value: Any) -> str | None:
    if value is None:
        return None
    s = str(value).strip()
    return s if s else None


def _parse_ts(value: Any) -> datetime | None:
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        v = value.replace("Z", "+00:00")
        try:
            return datetime.fromisoformat(v)
        except ValueError:
            return None
    return None


def _validate(record: dict[str, Any]) -> None:
    if not isinstance(record, dict):
        raise TypeError("Each MITRE trend input must be a dictionary")
    for f in REQUIRED_INPUT_FIELDS:
        if f not in record:
            raise ValueError(f"Missing required field: {f}")
    if _parse_ts(record.get("timestamp")) is None:
        raise ValueError("MITRE trends requires a valid timestamp")


# ---------------------------------------------------------------
# Public API
# ---------------------------------------------------------------

def build_mitre_trends(
    records: Iterable[dict[str, Any]],
) -> dict[str, Any]:
    """Build MITRE time-series trends.

    Returns flat trends, chart-ready series, and top values per dimension.
    """
    if records is None:
        raise TypeError("records cannot be None")

    records = list(records)

    empty = {
        "analytics_layer": ANALYTICS_LAYER,
        "trends": [],
        "series": {d: {} for d in TREND_DIMENSIONS},
        "top_values": {d: [] for d in TREND_DIMENSIONS},
        "summary": {
            "total_records": 0,
            "total_trend_rows": 0,
            "unique_dates": 0,
            "by_dimension": {d: 0 for d in TREND_DIMENSIONS},
        },
    }

    if not records:
        return empty

    for r in records:
        _validate(r)

    # ----------------------------------------------------------
    # Bucket: (day, dimension, value) -> {sessions:set, events:int}
    # ----------------------------------------------------------
    buckets: dict[tuple[str, str, str], dict[str, Any]] = defaultdict(
        lambda: {"session_ids": set(), "events": 0}
    )

    for r in records:
        ts = _parse_ts(r.get("timestamp"))
        if ts is None:
            continue
        day = ts.date().isoformat()
        sid = _clean(r.get("session_id")) or f"__anon_{id(r)}"
        events = int(r.get("event_count") or 0)

        for dim in TREND_DIMENSIONS:
            field_name = DIMENSION_FIELD_MAP[dim]
            value = _clean(r.get(field_name))
            if not value:
                continue
            key = (day, dim, value)
            buckets[key]["session_ids"].add(sid)
            buckets[key]["events"] += events

    # ----------------------------------------------------------
    # Flat rows
    # ----------------------------------------------------------
    rows = []
    for (day, dim, value) in sorted(buckets.keys()):
        bucket = buckets[(day, dim, value)]
        rows.append({
            "trend_date": day,
            "trend_dimension": dim,
            "trend_value": value,
            "session_count": len(bucket["session_ids"]),
            "event_count": bucket["events"],
        })

    # ----------------------------------------------------------
    # Series: dimension -> value -> sorted points
    # ----------------------------------------------------------
    series: dict[str, dict[str, list[dict[str, Any]]]] = {
        d: defaultdict(list) for d in TREND_DIMENSIONS
    }
    totals: dict[str, dict[str, int]] = {
        d: defaultdict(int) for d in TREND_DIMENSIONS
    }

    for row in rows:
        dim = row["trend_dimension"]
        val = row["trend_value"]
        series[dim][val].append({
            "date": row["trend_date"],
            "session_count": row["session_count"],
            "event_count": row["event_count"],
        })
        totals[dim][val] += row["session_count"]

    # ensure each series list is sorted by date
    for dim in TREND_DIMENSIONS:
        for val in series[dim]:
            series[dim][val].sort(key=lambda p: p["date"])

    # ----------------------------------------------------------
    # Top values per dimension
    # ----------------------------------------------------------
    top_values: dict[str, list[dict[str, Any]]] = {}
    for dim in TREND_DIMENSIONS:
        ranked = sorted(
            totals[dim].items(),
            key=lambda kv: -kv[1],
        )[:TOP_N]
        top_values[dim] = [
            {"value": v, "total_sessions": n}
            for v, n in ranked
        ]

    # ----------------------------------------------------------
    # Summary
    # ----------------------------------------------------------
    by_dim: dict[str, int] = {d: 0 for d in TREND_DIMENSIONS}
    for row in rows:
        by_dim[row["trend_dimension"]] += 1

    unique_dates = sorted({row["trend_date"] for row in rows})

    return {
        "analytics_layer": ANALYTICS_LAYER,
        "trends": rows,
        "series": {d: dict(series[d]) for d in TREND_DIMENSIONS},
        "top_values": top_values,
        "summary": {
            "total_records": len(records),
            "total_trend_rows": len(rows),
            "unique_dates": len(unique_dates),
            "by_dimension": by_dim,
        },
    }


__all__ = [
    "ANALYTICS_LAYER",
    "TREND_DIMENSIONS",
    "TOP_N",
    "build_mitre_trends",
]
