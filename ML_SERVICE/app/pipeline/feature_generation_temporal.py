"""
D3.4 — Temporal / Rate Feature Generation

Generates temporal and rate-based behavioral features.

Features:
- inter_event_gap_mean
- inter_event_gap_min
- inter_event_gap_max
- session_duration_recomputed_seconds
- events_per_second
- auth_attempt_rate
- command_rate
- session_start_hour
- session_start_dayofweek
- session_start_dayofmonth

Assumptions:
- D2 already reconstructed the session.
- session["events"] are chronologically ordered.
- D2 already provides session duration.
- This module does not scale features.
- This module does not mutate input.
"""

from copy import deepcopy
from datetime import datetime
from typing import Any, Dict


def _parse_timestamp(value: Any) -> datetime:
    if not isinstance(value, str):
        raise TypeError("timestamp must be a string")

    value = value.strip()

    if not value:
        raise ValueError("timestamp cannot be empty")

    if value.endswith("Z"):
        value = value[:-1] + "+00:00"

    try:
        return datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(
            f"Invalid ISO-8601 timestamp: {value}"
        ) from exc


def _event_type(event: Dict[str, Any]) -> str:
    value = (
        event.get("event_type")
        or event.get("type")
        or event.get("event")
        or ""
    )

    return str(value).strip().lower()


def _is_auth_event(event: Dict[str, Any]) -> bool:
    event_type = _event_type(event)

    return (
        event_type == "auth"
        or event_type == "authentication"
        or "auth" in event_type
        or "login" in event_type
    )


def _is_command_event(event: Dict[str, Any]) -> bool:
    event_type = _event_type(event)

    return (
        event_type == "command"
        or event_type == "cmd"
        or "command" in event_type
    )


def _safe_rate(
    numerator: float,
    duration_seconds: float,
) -> float:
    if duration_seconds <= 0:
        return 0.0

    return float(numerator / duration_seconds)


def generate_temporal_features(
    session: Dict[str, Any],
) -> Dict[str, float]:
    """
    Generate temporal/rate features for one reconstructed session.
    """

    if not isinstance(session, dict):
        raise TypeError("session must be a dictionary")

    events = session.get("events")

    if not isinstance(events, list):
        raise TypeError("session['events'] must be a list")

    copied_events = [
        deepcopy(event)
        for event in events
    ]

    # Empty session
    if not copied_events:
        return {
            "inter_event_gap_mean": 0.0,
            "inter_event_gap_min": 0.0,
            "inter_event_gap_max": 0.0,
            "session_duration_recomputed_seconds": 0.0,
            "events_per_second": 0.0,
            "auth_attempt_rate": 0.0,
            "command_rate": 0.0,
            "session_start_hour": 0.0,
            "session_start_dayofweek": 0.0,
            "session_start_dayofmonth": 0.0,
        }

    timestamps = [
        _parse_timestamp(event["timestamp"])
        for event in copied_events
    ]

    # D2 guarantees chronological ordering.
    for previous, current in zip(
        timestamps,
        timestamps[1:],
    ):
        if current < previous:
            raise ValueError(
                "Session events are not chronologically ordered"
            )

    # Session start time features.
    session_start = timestamps[0]

    session_start_hour = float(
        session_start.hour
    )

    session_start_dayofweek = float(
        session_start.weekday()
    )

    session_start_dayofmonth = float(
        session_start.day
    )

    # Inter-event gaps.
    gaps = [
        (current - previous).total_seconds()
        for previous, current in zip(
            timestamps,
            timestamps[1:],
        )
    ]

    if gaps:
        inter_event_gap_mean = float(
            sum(gaps) / len(gaps)
        )
        inter_event_gap_min = float(min(gaps))
        inter_event_gap_max = float(max(gaps))
    else:
        # A single-event session has no inter-event gap.
        inter_event_gap_mean = 0.0
        inter_event_gap_min = 0.0
        inter_event_gap_max = 0.0

    # Recomputed duration from event timestamps.
    session_duration_recomputed_seconds = float(
        (
            timestamps[-1] - timestamps[0]
        ).total_seconds()
    )

    if session_duration_recomputed_seconds < 0:
        raise ValueError(
            "Recomputed session duration cannot be negative"
        )

    auth_count = sum(
        1
        for event in copied_events
        if _is_auth_event(event)
    )

    command_count = sum(
        1
        for event in copied_events
        if _is_command_event(event)
    )

    events_per_second = _safe_rate(
        len(copied_events),
        session_duration_recomputed_seconds,
    )

    auth_attempt_rate = _safe_rate(
        auth_count,
        session_duration_recomputed_seconds,
    )

    command_rate = _safe_rate(
        command_count,
        session_duration_recomputed_seconds,
    )

    return {
        "inter_event_gap_mean": inter_event_gap_mean,
        "inter_event_gap_min": inter_event_gap_min,
        "inter_event_gap_max": inter_event_gap_max,
        "session_duration_recomputed_seconds":
            session_duration_recomputed_seconds,
        "events_per_second": events_per_second,
        "auth_attempt_rate": auth_attempt_rate,
        "command_rate": command_rate,
        "session_start_hour": session_start_hour,
        "session_start_dayofweek": session_start_dayofweek,
        "session_start_dayofmonth": session_start_dayofmonth,
    }
