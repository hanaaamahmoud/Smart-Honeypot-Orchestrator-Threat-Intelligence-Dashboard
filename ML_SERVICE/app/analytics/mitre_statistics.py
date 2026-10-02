"""MITRE statistics for ML session output.

Produces a flat list of statistic records across five dimensions:
OVERALL, CLUSTER, MITRE_TECHNIQUE, ATTACK_TYPE, ATTACK_STAGE.

Does NOT fabricate MITRE/attack values.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime
from typing import Any, Iterable


# ---------------------------------------------------------------
# Constants
# ---------------------------------------------------------------

ANALYTICS_LAYER = "MITRE_STATISTICS"

STATISTIC_TYPES = (
    "OVERALL",
    "CLUSTER",
    "MITRE_TECHNIQUE",
    "ATTACK_TYPE",
    "ATTACK_STAGE",
)

REQUIRED_INPUT_FIELDS = ("timestamp",)

# Small official human-readable map for known techniques.
MITRE_ATTACK_NAME = {
    "T1595": "Active Scanning",
    "T1592": "Gather Victim Host Information",
    "T1589": "Gather Victim Identity Information",
    "T1590": "Gather Victim Network Information",
    "T1598": "Phishing for Information",
    "T1597": "Search Closed Sources",
    "T1596": "Search Open Technical Databases",
    "T1110": "Brute Force",
    "T1190": "Exploit Public-Facing Application",
    "T1133": "External Remote Services",
    "T1566": "Phishing",
    "T1078": "Valid Accounts",
    "T1046": "Network Service Scanning",
    "T1040": "Network Sniffing",
    "T1087": "Account Discovery",
    "T1090": "Proxy",
    "T1071": "Application Layer Protocol",
    "T1105": "Ingress Tool Transfer",
    "T1059": "Command and Scripting Interpreter",
    "T1055": "Process Injection",
    "T1112": "Modify Registry",
    "T1003": "OS Credential Dumping",
    "T1021": "Remote Services",
    "T1041": "Exfiltration Over C2 Channel",
    "T1486": "Data Encrypted for Impact",
}


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
        raise TypeError("Each MITRE statistic input must be a dictionary")
    for f in REQUIRED_INPUT_FIELDS:
        if f not in record:
            raise ValueError(f"Missing required field: {f}")
    if _parse_ts(record.get("timestamp")) is None:
        raise ValueError("MITRE statistics requires a valid timestamp")


def _make_row(
    statistic_type: str,
    statistic_key: str,
    session_count: int,
    event_count: int,
    session_share_pct: float,
    mapped: int | None = None,
    unmapped: int | None = None,
    mitre_technique: str = "",
    mitre_attack_name: str = "",
    attack_type: str = "",
    attack_stage: str = "",
) -> dict[str, Any]:
    return {
        "statistic_type": statistic_type,
        "statistic_key": statistic_key,
        "session_count": session_count,
        "event_count": event_count,
        "session_share_pct": round(session_share_pct, 2),
        "mapped_mitre_sessions": mapped if mapped is not None else "",
        "unmapped_mitre_sessions": unmapped if unmapped is not None else "",
        "mitre_technique": mitre_technique,
        "mitre_attack_name": mitre_attack_name,
        "attack_type": attack_type,
        "attack_stage": attack_stage,
    }


# ---------------------------------------------------------------
# Public API
# ---------------------------------------------------------------

def build_mitre_statistics(
    records: Iterable[dict[str, Any]],
) -> dict[str, Any]:
    """Build flat MITRE statistics from ML session records."""
    if records is None:
        raise TypeError("records cannot be None")

    records = list(records)

    empty = {
        "analytics_layer": ANALYTICS_LAYER,
        "statistics": [],
        "summary": {
            "total_records": 0,
            "total_sessions": 0,
            "total_events": 0,
            "total_rows": 0,
            "by_statistic_type": {t: 0 for t in STATISTIC_TYPES},
        },
    }

    if not records:
        return empty

    for r in records:
        _validate(r)

    # ---------- Clean per-record fields ----------
    cleaned = []
    for r in records:
        cleaned.append({
            "session_id": _clean(r.get("session_id")),
            "event_count": int(r.get("event_count") or 0),
            "cluster_id": r.get("production_cluster_assignment"),
            "technique": _clean(r.get("mitre_technique")),
            "attack_type": _clean(r.get("attack_type")),
            "attack_stage": _clean(r.get("attack_stage")),
            "mapped": _clean(r.get("mitre_technique")) is not None,
        })

    total_sessions = len(cleaned)
    total_events = sum(c["event_count"] for c in cleaned)

    rows: list[dict[str, Any]] = []

    # ==========================================================
    # OVERALL
    # ==========================================================
    mapped_total = sum(1 for c in cleaned if c["mapped"])
    unmapped_total = total_sessions - mapped_total

    rows.append(_make_row(
        statistic_type="OVERALL",
        statistic_key="ALL_SESSIONS",
        session_count=total_sessions,
        event_count=total_events,
        session_share_pct=100.0,
        mapped=mapped_total,
        unmapped=unmapped_total,
    ))

    # ==========================================================
    # CLUSTER
    # ==========================================================
    cluster_sessions: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"count": 0, "events": 0, "mapped": 0}
    )
    for c in cleaned:
        cid = c["cluster_id"]
        if cid is None:
            continue
        key = str(cid)
        cluster_sessions[key]["count"] += 1
        cluster_sessions[key]["events"] += c["event_count"]
        if c["mapped"]:
            cluster_sessions[key]["mapped"] += 1

    for cid in sorted(cluster_sessions.keys(), key=lambda x: int(x)):
        bucket = cluster_sessions[cid]
        rows.append(_make_row(
            statistic_type="CLUSTER",
            statistic_key=cid,
            session_count=bucket["count"],
            event_count=bucket["events"],
            session_share_pct=bucket["count"] / total_sessions * 100,
            mapped=bucket["mapped"],
            unmapped=bucket["count"] - bucket["mapped"],
        ))

    # ==========================================================
    # MITRE_TECHNIQUE
    # ==========================================================
    tech_counter: Counter = Counter()
    tech_events: Counter = Counter()
    for c in cleaned:
        if c["technique"]:
            tech_counter[c["technique"]] += 1
            tech_events[c["technique"]] += c["event_count"]

    for tech, cnt in tech_counter.most_common():
        rows.append(_make_row(
            statistic_type="MITRE_TECHNIQUE",
            statistic_key=tech,
            session_count=cnt,
            event_count=tech_events[tech],
            session_share_pct=cnt / total_sessions * 100,
            mapped=cnt,
            unmapped=0,
            mitre_technique=tech,
            mitre_attack_name=MITRE_ATTACK_NAME.get(tech, ""),
        ))

    # ==========================================================
    # ATTACK_TYPE
    # ==========================================================
    type_counter: Counter = Counter()
    type_events: Counter = Counter()
    for c in cleaned:
        if c["attack_type"]:
            type_counter[c["attack_type"]] += 1
            type_events[c["attack_type"]] += c["event_count"]

    for at, cnt in type_counter.most_common():
        rows.append(_make_row(
            statistic_type="ATTACK_TYPE",
            statistic_key=at,
            session_count=cnt,
            event_count=type_events[at],
            session_share_pct=cnt / total_sessions * 100,
            attack_type=at,
        ))

    # ==========================================================
    # ATTACK_STAGE
    # ==========================================================
    stage_counter: Counter = Counter()
    stage_events: Counter = Counter()
    for c in cleaned:
        if c["attack_stage"]:
            stage_counter[c["attack_stage"]] += 1
            stage_events[c["attack_stage"]] += c["event_count"]

    for st, cnt in stage_counter.most_common():
        rows.append(_make_row(
            statistic_type="ATTACK_STAGE",
            statistic_key=st,
            session_count=cnt,
            event_count=stage_events[st],
            session_share_pct=cnt / total_sessions * 100,
            attack_stage=st,
        ))

    # ==========================================================
    # Summary
    # ==========================================================
    by_type: dict[str, int] = {t: 0 for t in STATISTIC_TYPES}
    for r in rows:
        by_type[r["statistic_type"]] += 1

    return {
        "analytics_layer": ANALYTICS_LAYER,
        "statistics": rows,
        "summary": {
            "total_records": total_sessions,
            "total_sessions": total_sessions,
            "total_events": total_events,
            "total_rows": len(rows),
            "by_statistic_type": by_type,
        },
    }


__all__ = [
    "ANALYTICS_LAYER",
    "STATISTIC_TYPES",
    "MITRE_ATTACK_NAME",
    "build_mitre_statistics",
]
