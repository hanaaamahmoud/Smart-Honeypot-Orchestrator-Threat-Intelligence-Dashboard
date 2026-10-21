"""MITRE ATT&CK analytics for ML session/event output.

Consumes ML output records and produces MITRE-oriented distributions,
tactics mapping, and per-technique attacker IPs.
Does NOT fabricate MITRE values.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime
from typing import Any, Iterable


# ---------------------------------------------------------------
# Constants
# ---------------------------------------------------------------

ANALYTICS_LAYER = "MITRE_ANALYTICS"

REQUIRED_INPUT_FIELDS = ("timestamp",)

OPTIONAL_INPUT_FIELDS = (
    "session_id",
    "mitre_technique",
    "attack_type",
    "attack_stage",
    "severity",
    "source_ip",
)

OUTPUT_REQUIRED_FIELDS = (
    "analytics_layer",
    "mitre_technique_distribution",
    "mitre_tactics_distribution",
    "attack_type_distribution",
    "attack_stage_distribution",
    "session_mitre_relationships",
    "mitre_activity_over_time",
    "summary",
)


# MITRE ATT&CK official technique -> tactic mapping.
# Source: MITRE ATT&CK Enterprise framework (public standard).
TECHNIQUE_TO_TACTIC: dict[str, str] = {
    "T1595": "Reconnaissance",
    "T1592": "Reconnaissance",
    "T1589": "Reconnaissance",
    "T1590": "Reconnaissance",
    "T1598": "Reconnaissance",
    "T1597": "Reconnaissance",
    "T1596": "Reconnaissance",
    "T1110": "Credential Access",
    "T1190": "Initial Access",
    "T1133": "Initial Access",
    "T1566": "Initial Access",
    "T1078": "Defense Evasion",
    "T1046": "Discovery",
    "T1040": "Discovery",
    "T1087": "Discovery",
    "T1090": "Command and Control",
    "T1071": "Command and Control",
    "T1105": "Command and Control",
    "T1059": "Execution",
    "T1055": "Defense Evasion",
    "T1112": "Defense Evasion",
    "T1003": "Credential Access",
    "T1021": "Lateral Movement",
    "T1041": "Exfiltration",
    "T1486": "Impact",
}


# ---------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------

def _clean(value: Any) -> str | None:
    """Return stripped string or None. Never fabricate."""
    if value is None:
        return None
    s = str(value).strip()
    return s if s else None


def _parse_timestamp(value: Any) -> datetime | None:
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        v = value.replace("Z", "+00:00")
        try:
            return datetime.fromisoformat(v)
        except ValueError:
            return None
    return None


def _validate_record(record: dict[str, Any]) -> None:
    if not isinstance(record, dict):
        raise TypeError(
            "Each MITRE analytics input must be a dictionary"
        )
    for field in REQUIRED_INPUT_FIELDS:
        if field not in record:
            raise ValueError(
                f"Missing required MITRE field: {field}"
            )
    if _parse_timestamp(record.get("timestamp")) is None:
        raise ValueError(
            "MITRE analytics requires a valid timestamp"
        )


def _tactic_for(technique: str) -> str | None:
    """Return MITRE tactic for a technique, or None if unknown."""
    return TECHNIQUE_TO_TACTIC.get(technique)


# ---------------------------------------------------------------
# Public API
# ---------------------------------------------------------------

def build_mitre_analytics(
    records: Iterable[dict[str, Any]],
) -> dict[str, Any]:
    """Build MITRE analytics from ML session/event records.

    Empty input returns a valid zero-state payload.
    Does not mutate input. Does not fabricate MITRE values.
    """
    if records is None:
        raise TypeError("records cannot be None")

    records = list(records)

    empty_payload = {
        "analytics_layer": ANALYTICS_LAYER,
        "mitre_technique_distribution": [],
        "mitre_tactics_distribution": [],
        "attack_type_distribution": [],
        "attack_stage_distribution": [],
        "session_mitre_relationships": [],
        "mitre_activity_over_time": [],
        "summary": {
            "total_records": 0,
            "records_with_mitre": 0,
            "records_with_attack_type": 0,
            "records_with_attack_stage": 0,
            "unique_techniques": 0,
            "unique_tactics": 0,
            "unique_attack_types": 0,
            "unique_attack_stages": 0,
        },
    }

    if not records:
        return empty_payload

    for r in records:
        _validate_record(r)

    # ---------- Pre-compute per-record cleaned values ----------
    cleaned: list[dict[str, Any]] = []
    for r in records:
        cleaned.append({
            "ts": _parse_timestamp(r.get("timestamp")),
            "session_id": _clean(r.get("session_id")),
            "technique": _clean(r.get("mitre_technique")),
            "attack_type": _clean(r.get("attack_type")),
            "attack_stage": _clean(r.get("attack_stage")),
            "severity": _clean(r.get("severity")),
            "source_ip": _clean(r.get("source_ip")),
        })

    # ==========================================================
    # 1. MITRE Technique distribution + per-technique top IPs
    # ==========================================================
    technique_counter: Counter = Counter()
    technique_ips: dict[str, Counter] = defaultdict(Counter)

    for c in cleaned:
        if c["technique"]:
            technique_counter[c["technique"]] += 1
            if c["source_ip"]:
                technique_ips[c["technique"]][c["source_ip"]] += 1

    total_with_mitre = sum(technique_counter.values())

    mitre_technique_distribution = []
    for tech, count in technique_counter.most_common():
        entry = {
            "value": tech,
            "count": count,
            "percentage": (
                round(count / total_with_mitre * 100, 2)
                if total_with_mitre else 0.0
            ),
            "tactic": _tactic_for(tech),
            "top_source_ips": [
                {"ip": ip, "session_count": n}
                for ip, n in technique_ips[tech].most_common(5)
            ],
        }
        mitre_technique_distribution.append(entry)

    # ==========================================================
    # 2. MITRE Tactics distribution (aggregated by tactic)
    # ==========================================================
    tactic_counter: Counter = Counter()
    for tech, count in technique_counter.items():
        tactic = _tactic_for(tech)
        if tactic:
            tactic_counter[tactic] += count

    total_with_tactic = sum(tactic_counter.values())
    mitre_tactics_distribution = [
        {
            "value": tactic,
            "count": count,
            "percentage": (
                round(count / total_with_tactic * 100, 2)
                if total_with_tactic else 0.0
            ),
        }
        for tactic, count in tactic_counter.most_common()
    ]

    # ==========================================================
    # 3. Attack Type distribution
    # ==========================================================
    attack_type_counter: Counter = Counter()
    for c in cleaned:
        if c["attack_type"]:
            attack_type_counter[c["attack_type"]] += 1

    total_attack_type = sum(attack_type_counter.values())
    attack_type_distribution = [
        {
            "value": v,
            "count": n,
            "percentage": (
                round(n / total_attack_type * 100, 2)
                if total_attack_type else 0.0
            ),
        }
        for v, n in attack_type_counter.most_common()
    ]

    # ==========================================================
    # 4. Attack Stage distribution
    # ==========================================================
    attack_stage_counter: Counter = Counter()
    for c in cleaned:
        if c["attack_stage"]:
            attack_stage_counter[c["attack_stage"]] += 1

    total_attack_stage = sum(attack_stage_counter.values())
    attack_stage_distribution = [
        {
            "value": v,
            "count": n,
            "percentage": (
                round(n / total_attack_stage * 100, 2)
                if total_attack_stage else 0.0
            ),
        }
        for v, n in attack_stage_counter.most_common()
    ]

    # ==========================================================
    # 5. Session -> MITRE relationships
    # ==========================================================
    session_map: dict[str, set[str]] = defaultdict(set)
    session_attack: dict[str, set[str]] = defaultdict(set)
    session_stage: dict[str, set[str]] = defaultdict(set)

    for c in cleaned:
        sid = c["session_id"]
        if not sid:
            continue
        if c["technique"]:
            session_map[sid].add(c["technique"])
        if c["attack_type"]:
            session_attack[sid].add(c["attack_type"])
        if c["attack_stage"]:
            session_stage[sid].add(c["attack_stage"])

    session_mitre_relationships = [
        {
            "session_id": sid,
            "mitre_techniques": sorted(session_map[sid]),
            "attack_types": sorted(session_attack.get(sid, set())),
            "attack_stages": sorted(session_stage.get(sid, set())),
        }
        for sid in sorted(session_map.keys())
    ]

    # ==========================================================
    # 6. Activity over time (daily)
    # ==========================================================
    daily_mitre: Counter = Counter()
    for c in cleaned:
        if c["technique"] and c["ts"]:
            daily_mitre[c["ts"].date().isoformat()] += 1

    mitre_activity_over_time = [
        {"date": d, "count": n}
        for d, n in sorted(daily_mitre.items())
    ]

    # ==========================================================
    # 7. Summary
    # ==========================================================
    records_with_mitre = sum(
        1 for c in cleaned if c["technique"]
    )
    records_with_attack = sum(
        1 for c in cleaned if c["attack_type"]
    )
    records_with_stage = sum(
        1 for c in cleaned if c["attack_stage"]
    )

    summary = {
        "total_records": len(cleaned),
        "records_with_mitre": records_with_mitre,
        "records_with_attack_type": records_with_attack,
        "records_with_attack_stage": records_with_stage,
        "unique_techniques": len(technique_counter),
        "unique_tactics": len(tactic_counter),
        "unique_attack_types": len(attack_type_counter),
        "unique_attack_stages": len(attack_stage_counter),
    }

    return {
        "analytics_layer": ANALYTICS_LAYER,
        "mitre_technique_distribution": mitre_technique_distribution,
        "mitre_tactics_distribution": mitre_tactics_distribution,
        "attack_type_distribution": attack_type_distribution,
        "attack_stage_distribution": attack_stage_distribution,
        "session_mitre_relationships": session_mitre_relationships,
        "mitre_activity_over_time": mitre_activity_over_time,
        "summary": summary,
    }


__all__ = [
    "ANALYTICS_LAYER",
    "REQUIRED_INPUT_FIELDS",
    "OPTIONAL_INPUT_FIELDS",
    "OUTPUT_REQUIRED_FIELDS",
    "TECHNIQUE_TO_TACTIC",
    "build_mitre_analytics",
]
