"""Session Replay — dashboard-ready per-session event timelines.

Produces:
- summary: compact per-session context (attack, MITRE, severity, stats)
- events: full ordered event timeline with per-event counters

Reads enrichment fields both from top level AND from `raw` fallback.
Does NOT fabricate fields. Does NOT mutate source events.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime
from typing import Any, Iterable


ANALYTICS_LAYER = "SESSION_REPLAY"

EVENT_KEEP_FIELDS = (
    "timestamp",
    "event_type",
    "command",
    "username",
    "password",
    "source_ip",
    "source_port",
    "destination_ip",
    "destination_port",
    "protocol",
    "honeypot",
    "country",
    "country_code",
    "asn",
    "attack_type",
    "mitre_technique",
    "attack_stage",
    "severity",
    "auth_attempt",
    "user_attempt",
    "pass_attempt",
    "anonymous",
    "command_count",
)


def _clean(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, str):
        s = value.strip()
        return s if s else None
    return value


def _get(event: dict, field: str) -> Any:
    """Read from top level, fallback to `raw`, then to None."""
    v = _clean(event.get(field))
    if v is not None:
        return v
    raw = event.get("raw")
    if isinstance(raw, dict):
        return _clean(raw.get(field))
    return None


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


def _safe_int(v: Any) -> int:
    try:
        if v is None:
            return 0
        return int(v)
    except (TypeError, ValueError):
        return 0


def _compact_event(event: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for f in EVENT_KEEP_FIELDS:
        v = _get(event, f)
        if v is not None:
            out[f] = v
    return out



def _phase_of(event: dict, index: int, total: int) -> str:
    """Determine which phase of the session this event belongs to."""
    if index == 1:
        return "connection"
    if index == total:
        return "disconnect"
    if _get(event, "command") or _safe_int(_get(event, "command_count")) > 0:
        return "command"
    if _get(event, "username") or _get(event, "password"):
        return "auth"
    if _safe_int(_get(event, "auth_attempt")) > 0 or \
       _safe_int(_get(event, "user_attempt")) > 0 or \
       _safe_int(_get(event, "pass_attempt")) > 0:
        return "auth"
    return "activity"


def _describe_event(
    event: dict,
    index: int,
    total_events: int,
    offset: float,
    session_start_ctx: dict,
) -> dict:
    """
    Build a rich, cinematic step description.

    Uses EVERY available field. Never fabricates.
    """
    ts = event.get("timestamp")
    src_ip = _get(event, "source_ip")
    src_port = _get(event, "source_port")
    dst_ip = _get(event, "destination_ip")
    dst_port = _get(event, "destination_port")
    protocol = _get(event, "protocol")
    honeypot = _get(event, "honeypot")
    username = _get(event, "username")
    password = _get(event, "password")
    command = _get(event, "command")
    event_type = _get(event, "event_type")

    auth_attempt = _safe_int(_get(event, "auth_attempt"))
    user_attempt = _safe_int(_get(event, "user_attempt"))
    pass_attempt = _safe_int(_get(event, "pass_attempt"))
    command_count = _safe_int(_get(event, "command_count"))
    anonymous = _safe_int(_get(event, "anonymous"))

    phase = _phase_of(event, index, total_events)

    # ────────────────────────────────────────────────
    # Step type + icon + title
    # ────────────────────────────────────────────────
    if phase == "connection":
        step_type = "connection"
        icon = "🚪"
        title = "CONNECTION ESTABLISHED"
    elif phase == "disconnect":
        step_type = "disconnect"
        icon = "🔚"
        title = "SESSION ENDED"
    elif phase == "command" and command:
        step_type = "command"
        icon = "💻"
        title = "COMMAND EXECUTED"
    elif phase == "command":
        step_type = "command"
        icon = "💻"
        title = "COMMAND ACTIVITY"
    elif phase == "auth" and (username or password):
        step_type = "auth_attempt"
        icon = "🔑"
        title = "AUTH ATTEMPT"
    elif phase == "auth":
        step_type = "auth_counter"
        icon = "🔑"
        title = "AUTH ACTIVITY"
    else:
        step_type = "activity"
        icon = "📌"
        title = "ACTIVITY"

    # ────────────────────────────────────────────────
    # Details (rich, ordered)
    # ────────────────────────────────────────────────
    details = []

    # 1. From / To
    if src_ip:
        from_str = src_ip
        if src_port:
            from_str += ":{}".format(src_port)
        details.append(("From", from_str))
    if dst_ip:
        to_str = dst_ip
        if dst_port:
            to_str += ":{}".format(dst_port)
        details.append(("To", to_str))
    elif dst_port:
        details.append(("Port", dst_port))

    # 2. Protocol / Honeypot
    if protocol:
        details.append(("Protocol", protocol))
    if honeypot:
        details.append(("Honeypot", honeypot))

    # 3. Credentials
    if username:
        details.append(("Username", username))
    if password:
        details.append(("Password", password))

    # 4. Command
    if command:
        details.append(("Command", command))

    # 5. Event type
    if event_type:
        details.append(("Event type", event_type))

    # 6. Counters
    if auth_attempt > 0:
        details.append(("Auth attempts", auth_attempt))
    if user_attempt > 0:
        details.append(("User attempts", user_attempt))
    if pass_attempt > 0:
        details.append(("Pass attempts", pass_attempt))
    if command_count > 0:
        details.append(("Command count", command_count))
    if anonymous > 0:
        details.append(("Anonymous", anonymous))

    # 7. Classification (if present per-event)
    at = _get(event, "attack_type")
    mt = _get(event, "mitre_technique")
    ast = _get(event, "attack_stage")
    sev = _get(event, "severity")
    if at:
        details.append(("Attack type", at))
    if mt:
        details.append(("MITRE", mt))
    if ast:
        details.append(("Stage", ast))
    if sev:
        details.append(("Severity", sev))

    # 8. Position in session
    details.append(("Event", "{}/{}".format(index, total_events)))

    return {
        "index": index,
        "offset_seconds": round(offset, 3),
        "phase": phase,
        "step_type": step_type,
        "icon": icon,
        "title": title,
        "details": [
            {"label": label, "value": value}
            for label, value in details
        ],
        "timestamp": ts,
    }


def _group_into_phases(steps: list) -> list:
    """Group consecutive steps into phases for nicer display."""
    if not steps:
        return []

    phases = []
    current = {
        "phase": steps[0]["phase"],
        "started_at_seconds": steps[0]["offset_seconds"],
        "step_count": 0,
        "steps": [],
    }

    for step in steps:
        if step["phase"] != current["phase"]:
            current["ended_at_seconds"] = current["steps"][-1]["offset_seconds"] if current["steps"] else 0
            phases.append(current)
            current = {
                "phase": step["phase"],
                "started_at_seconds": step["offset_seconds"],
                "step_count": 0,
                "steps": [],
            }
        current["steps"].append(step)
        current["step_count"] += 1

    if current["steps"]:
        current["ended_at_seconds"] = current["steps"][-1]["offset_seconds"]
        phases.append(current)

    return phases


def _build_narrative(events: list, first_ts, last_ts) -> dict:
    """Build rich cinematic narrative."""
    if not events:
        return {"steps": [], "phases": [], "total_steps": 0}

    steps = []
    for i, e in enumerate(events, 1):
        ts = _parse_ts(e.get("timestamp"))
        if ts is None:
            continue
        offset = (ts - first_ts).total_seconds()
        step = _describe_event(
            e,
            index=i,
            total_events=len(events),
            offset=offset,
            session_start_ctx={},
        )
        steps.append(step)

    phases = _group_into_phases(steps)

    return {
        "steps": steps,
        "phases": phases,
        "total_steps": len(steps),
    }


def _build_summary(session_id: str, events: list[dict], first_ts, last_ts) -> dict:
    usernames = []
    commands = []
    attack_types = []
    mitre_techniques = []
    attack_stages = []
    severities = []
    source_ips = set()
    honeypots = []
    protocols = []
    countries = []
    country_codes = []

    for e in events:
        u = _get(e, "username")
        if u: usernames.append(u)
        c = _get(e, "command")
        if c: commands.append(c)
        at = _get(e, "attack_type")
        if at: attack_types.append(at)
        mt = _get(e, "mitre_technique")
        if mt: mitre_techniques.append(mt)
        ast = _get(e, "attack_stage")
        if ast: attack_stages.append(ast)
        sev = _get(e, "severity")
        if sev: severities.append(sev)
        sip = _get(e, "source_ip")
        if sip: source_ips.add(sip)
        hp = _get(e, "honeypot")
        if hp: honeypots.append(hp)
        pr = _get(e, "protocol")
        if pr: protocols.append(pr)
        co = _get(e, "country")
        if co: countries.append(co)
        cc = _get(e, "country_code")
        if cc: country_codes.append(cc)

    auth_total = sum(_safe_int(_get(e, "auth_attempt")) for e in events)
    user_total = sum(_safe_int(_get(e, "user_attempt")) for e in events)
    pass_total = sum(_safe_int(_get(e, "pass_attempt")) for e in events)
    cmd_total = sum(_safe_int(_get(e, "command_count")) for e in events)
    anon_total = sum(_safe_int(_get(e, "anonymous")) for e in events)

    def top1(lst):
        if not lst:
            return None
        return Counter(lst).most_common(1)[0][0]

    context = {
        "honeypot": top1(honeypots),
        "protocol": top1(protocols),
        "country": top1(countries),
        "country_code": top1(country_codes),
    }

    classification = {
        "attack_type": top1(attack_types),
        "mitre_technique": top1(mitre_techniques),
        "attack_stage": top1(attack_stages),
        "severity": top1(severities),
    }

    duration = 0.0
    if first_ts and last_ts:
        duration = (last_ts - first_ts).total_seconds()

    # ---------- Flag computation ----------
    unique_usernames_count = len(set(usernames))
    unique_commands_count = len(set(commands))
    unique_ips_count = len(source_ips)

    has_attack_class = bool(attack_types)
    has_mitre = bool(mitre_techniques)

    # Severity normalized
    sev_set = {s.lower() for s in severities if s}
    is_high_severity = bool(sev_set & {"high", "critical"})
    is_medium_or_higher = bool(sev_set & {"medium", "high", "critical"})

    # Flags
    is_brute_force = auth_total > 3 or unique_usernames_count > 3
    has_commands = cmd_total > 0

    is_large_session = len(events) > 50
    is_long_running = duration > 3600
    is_multi_ip = unique_ips_count > 5

    has_attack_classification = has_attack_class or has_mitre

    is_suspicious = (
        is_brute_force
        or has_commands
        or is_large_session
        or is_long_running
        or is_multi_ip
        or is_high_severity
        or is_medium_or_higher
    )

    return {
        "reconstructed_session_id": session_id,
        "event_count": len(events),
        "duration_seconds": round(duration, 3),
        "first_event_utc": first_ts.isoformat() if first_ts else None,
        "last_event_utc": last_ts.isoformat() if last_ts else None,

        "context": context,
        "classification": classification,

        "source_ips": sorted(source_ips),

        "credentials": {
            "unique_usernames": sorted(set(usernames)),
            "unique_passwords_count": len({
                _get(e, "password") for e in events if _get(e, "password")
            }),
            "auth_attempt_total": auth_total,
            "user_attempt_total": user_total,
            "pass_attempt_total": pass_total,
            "anonymous_total": anon_total,
        },

        "commands": {
            "command_count_total": cmd_total,
            "unique_commands_count": len(set(commands)),
            "sample_commands": list(dict.fromkeys(commands))[:10],
        },

        "flags": {
            "is_suspicious": is_suspicious,
            "is_brute_force_candidate": is_brute_force,
            "has_commands_executed": has_commands,
            "has_attack_classification": has_attack_classification,
            "is_large_session": is_large_session,
            "is_long_running": is_long_running,
            "is_multi_ip": is_multi_ip,
            "is_high_severity": is_high_severity,
            "is_medium_or_higher_severity": is_medium_or_higher,
        },
    }


def build_session_replay(
    events: Iterable[dict[str, Any]],
) -> dict[str, Any]:
    if events is None:
        raise TypeError("events cannot be None")

    events = list(events)

    empty = {
        "analytics_layer": ANALYTICS_LAYER,
        "sessions": [],
        "summary": {
            "total_events": 0,
            "total_sessions": 0,
            "orphan_events": 0,
        },
    }

    if not events:
        return empty

    groups: dict[str, list[tuple[datetime, dict[str, Any]]]] = defaultdict(list)
    orphan_events = 0

    for e in events:
        if not isinstance(e, dict):
            raise TypeError("Each session replay input must be a dictionary")

        sid = _get(e, "session_id")
        ts = _parse_ts(e.get("timestamp"))

        if sid is None or ts is None:
            orphan_events += 1
            continue

        groups[sid].append((ts, e))

    sessions = []
    for sid in sorted(groups.keys()):
        entries = groups[sid]
        entries.sort(key=lambda x: x[0])

        ts_list = [t for t, _ in entries]
        first_ts = ts_list[0]
        last_ts = ts_list[-1]

        raw_events = [e for _, e in entries]

        event_timeline = []
        for i, (ts, e) in enumerate(entries, 1):
            ev = _compact_event(e)
            ev["_event_index"] = i
            ev["_offset_seconds"] = round((ts - first_ts).total_seconds(), 3)
            event_timeline.append(ev)

        summary = _build_summary(sid, raw_events, first_ts, last_ts)
        narrative = _build_narrative(raw_events, first_ts, last_ts)

        sessions.append({
            "reconstructed_session_id": sid,
            "summary": summary,
            "narrative": narrative,
            "events": event_timeline,
        })

    return {
        "analytics_layer": ANALYTICS_LAYER,
        "sessions": sessions,
        "summary": {
            "total_events": len(events),
            "total_sessions": len(sessions),
            "orphan_events": orphan_events,
        },
    }


__all__ = [
    "ANALYTICS_LAYER",
    "EVENT_KEEP_FIELDS",
    "build_session_replay",
]
