"""Session analytics adapter for validated production ML output.

Two layers:
1. build_session_records   → one row per session (table data)
2. build_session_summary   → KPI cards + distributions (dashboard)
"""

from __future__ import annotations

from collections import Counter
from copy import deepcopy
from datetime import datetime
from typing import Any, Iterable


# ---------------------------------------------------------------
# Contract constants
# ---------------------------------------------------------------

REQUIRED_FIELDS = (
    "reconstructed_session_id",
    "production_cluster_assignment",
    "assignment_status",
    "feature_validation_status",
)

OPTIONAL_FIELDS = (
    "distance",
    "event_count",
    "session_start",
    "session_end",
    "session_duration_seconds",
    "honeypot",
    "protocol",
    "source_ip",
    "country",
    "country_code",
    "attack_type",
    "mitre_technique",
    "attack_stage",
    "severity",
    "source",
)

OUTPUT_FIELDS = REQUIRED_FIELDS + OPTIONAL_FIELDS

ALLOWED_ASSIGNMENT_STATUS = {
    "EXISTING_PRODUCTION_CLUSTER",
    "NOISE",
}

NOISE_CLUSTER_ID = -1


# ---------------------------------------------------------------
# Validation
# ---------------------------------------------------------------

def _validate_record(record: dict[str, Any]) -> None:
    if not isinstance(record, dict):
        raise TypeError(
            "Each session analytics input must be a dictionary"
        )

    missing = [f for f in REQUIRED_FIELDS if f not in record]
    if missing:
        raise ValueError(
            f"Missing required session analytics fields: {missing}"
        )

    null_required = [f for f in REQUIRED_FIELDS if record[f] is None]
    if null_required:
        raise ValueError(
            "Required session analytics fields cannot be null: "
            f"{null_required}"
        )

    sid = record["reconstructed_session_id"]
    if not isinstance(sid, str) or not sid.strip():
        raise ValueError(
            "reconstructed_session_id must be a non-empty string"
        )

    cid = record["production_cluster_assignment"]
    if isinstance(cid, bool) or not isinstance(cid, int):
        raise ValueError(
            "production_cluster_assignment must be an integer"
        )

    status = record["assignment_status"]
    if status not in ALLOWED_ASSIGNMENT_STATUS:
        raise ValueError(
            "assignment_status must be one of "
            f"{sorted(ALLOWED_ASSIGNMENT_STATUS)}, got {status!r}"
        )

    fvs = record["feature_validation_status"]
    if not isinstance(fvs, str) or not fvs.strip():
        raise ValueError(
            "feature_validation_status must be a non-empty string"
        )


# ---------------------------------------------------------------
# Layer 1: Records (table data)
# ---------------------------------------------------------------

def build_session_records(
    results: Iterable[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Return one validated row per session. Non-mutating."""
    if results is None:
        raise TypeError("results cannot be None")

    output: list[dict[str, Any]] = []
    for record in results:
        _validate_record(record)
        row = {f: deepcopy(record[f]) for f in OUTPUT_FIELDS if f in record}
        output.append(row)
    return output


# ---------------------------------------------------------------
# Helpers for summary
# ---------------------------------------------------------------

def _top_n(records, field, n=10):
    values = [r.get(field) for r in records if r.get(field)]
    if not values:
        return []
    total = len(values)
    counter = Counter(values)
    return [
        {
            "value": v,
            "count": c,
            "percentage": round(c / total * 100, 2),
        }
        for v, c in counter.most_common(n)
    ]


def _event_count_bucket(count: int) -> str:
    if count <= 1:
        return "1"
    if count <= 3:
        return "2-3"
    if count <= 5:
        return "4-5"
    if count <= 10:
        return "6-10"
    if count <= 50:
        return "11-50"
    if count <= 100:
        return "51-100"
    return "100+"


def _duration_bucket(seconds: float) -> str:
    if seconds < 1:
        return "< 1s"
    if seconds < 10:
        return "1-10s"
    if seconds < 60:
        return "10s-1m"
    if seconds < 3600:
        return "1m-1h"
    if seconds < 86400:
        return "1h-1d"
    return "> 1d"


def _parse_dt(value):
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        v = value.replace("Z", "+00:00")
        try:
            return datetime.fromisoformat(v)
        except ValueError:
            return None
    return None


def _session_duration(record: dict[str, Any]) -> float | None:
    # Prefer explicit duration field
    d = record.get("session_duration_seconds")
    if d is not None:
        try:
            return float(d)
        except (TypeError, ValueError):
            pass
    # Fallback: compute from start/end
    s = _parse_dt(record.get("session_start"))
    e = _parse_dt(record.get("session_end"))
    if s and e:
        return (e - s).total_seconds()
    return None


# ---------------------------------------------------------------
# Layer 2: Summary (dashboard)
# ---------------------------------------------------------------

def build_session_summary(
    results: Iterable[dict[str, Any]],
) -> dict[str, Any]:
    """Aggregate KPI + distributions for dashboard.

    Returns dict with:
      - summary        : top-level KPIs
      - distributions  : by honeypot, protocol, country, cluster, ...
      - top_source_ips : top 10 attackers
    """
    if results is None:
        raise TypeError("results cannot be None")

    records = list(results)
    for r in records:
        _validate_record(r)

    if not records:
        return {
            "summary": {
                "total_sessions": 0,
                "total_events": 0,
                "total_clusters_used": 0,
                "assigned_sessions": 0,
                "noise_sessions": 0,
                "avg_events_per_session": 0.0,
                "avg_session_duration_seconds": 0.0,
                "unique_source_ips": 0,
                "unique_countries": 0,
            },
            "distributions": {},
            "top_source_ips": [],
        }

    total = len(records)
    total_events = sum(r.get("event_count") or 0 for r in records)

    assigned = sum(
        1 for r in records
        if r["assignment_status"] == "EXISTING_PRODUCTION_CLUSTER"
    )
    noise = sum(
        1 for r in records
        if r["assignment_status"] == "NOISE"
    )

    clusters_used = set(
        r["production_cluster_assignment"] for r in records
    )

    durations = []
    for r in records:
        d = _session_duration(r)
        if d is not None:
            durations.append(d)

    avg_dur = sum(durations) / len(durations) if durations else 0.0
    durations_sorted = sorted(durations)
    median_dur = (
        durations_sorted[len(durations_sorted) // 2]
        if durations_sorted else 0.0
    )

    source_ips = {r.get("source_ip") for r in records if r.get("source_ip")}
    countries = {r.get("country") for r in records if r.get("country")}

    # Event count buckets
    ev_buckets: Counter = Counter()
    for r in records:
        ev_buckets[_event_count_bucket(r.get("event_count") or 0)] += 1

    # Duration buckets
    dur_buckets: Counter = Counter()
    for d in durations:
        dur_buckets[_duration_bucket(d)] += 1

    # Top source IPs with event counts
    ip_sessions: Counter = Counter()
    ip_events: Counter = Counter()
    for r in records:
        ip = r.get("source_ip")
        if ip:
            ip_sessions[ip] += 1
            ip_events[ip] += r.get("event_count") or 0

    top_ips = [
        {
            "ip": ip,
            "session_count": c,
            "event_count": ip_events[ip],
        }
        for ip, c in ip_sessions.most_common(10)
    ]

    return {
        "summary": {
            "total_sessions": total,
            "total_events": total_events,
            "total_clusters_used": len(clusters_used),
            "assigned_sessions": assigned,
            "noise_sessions": noise,
            "avg_events_per_session": round(total_events / total, 2),
            "avg_session_duration_seconds": round(avg_dur, 2),
            "median_session_duration_seconds": round(median_dur, 2),
            "min_session_duration_seconds": round(min(durations), 2) if durations else 0,
            "max_session_duration_seconds": round(max(durations), 2) if durations else 0,
            "unique_source_ips": len(source_ips),
            "unique_countries": len(countries),
        },
        "distributions": {
            "by_honeypot": _top_n(records, "honeypot", n=10),
            "by_protocol": _top_n(records, "protocol", n=10),
            "by_country": _top_n(records, "country", n=10),
            "by_attack_type": _top_n(records, "attack_type", n=10),
            "by_mitre_technique": _top_n(records, "mitre_technique", n=10),
            "by_attack_stage": _top_n(records, "attack_stage", n=10),
            "by_severity": _top_n(records, "severity", n=10),
            "by_cluster": _top_n(records, "production_cluster_assignment", n=40),
            "by_event_count_bucket": [
                {"bucket": b, "count": c}
                for b, c in sorted(ev_buckets.items(), key=lambda x: x[0])
            ],
            "by_duration_bucket": [
                {"bucket": b, "count": c}
                for b, c in [
                    ("< 1s", dur_buckets.get("< 1s", 0)),
                    ("1-10s", dur_buckets.get("1-10s", 0)),
                    ("10s-1m", dur_buckets.get("10s-1m", 0)),
                    ("1m-1h", dur_buckets.get("1m-1h", 0)),
                    ("1h-1d", dur_buckets.get("1h-1d", 0)),
                    ("> 1d", dur_buckets.get("> 1d", 0)),
                ]
            ],
        },
        "top_source_ips": top_ips,
    }


# Keep old name as alias for backward compat with existing tests
build_session_analytics = build_session_records


__all__ = [
    "REQUIRED_FIELDS",
    "OPTIONAL_FIELDS",
    "OUTPUT_FIELDS",
    "ALLOWED_ASSIGNMENT_STATUS",
    "NOISE_CLUSTER_ID",
    "build_session_records",
    "build_session_summary",
    "build_session_analytics",
]
