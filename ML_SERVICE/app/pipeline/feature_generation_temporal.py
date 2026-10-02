"""
D3.4 — Temporal / Rate Feature Generation

COLAB PARITY NOTE
-----------------
``auth_attempt_rate`` and ``command_rate`` are now computed as:

    auth_attempt_rate = auth_attempt_total / duration
    command_rate      = command_count_total / duration

using the per-event ``auth_attempt`` and ``command_count`` counters
directly (matching pandas aggregation in the original notebook),
rather than counting events that match a heuristic predicate.

This module does NOT:
- scale features
- cluster
- modify input sessions
- mutate input
"""

from copy import deepcopy
from datetime import datetime
from typing import Any, Dict, List


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


def _safe_rate(
    numerator: float,
    duration_seconds: float,
) -> float:
    if duration_seconds <= 0:
        return 0.0

    return float(numerator / duration_seconds)


def _sum_int_field(
    events: List[Dict[str, Any]],
    field_name: str,
) -> int:
    """
    Sum an integer counter across all events.

    Matches pandas ``groupby(...)[field].sum()`` semantics:
    missing / None values contribute 0.
    """
    total = 0
    for event in events:
        value = event.get(field_name)
        if value is None:
            continue
        try:
            total += int(value)
        except (TypeError, ValueError):
            continue
    return total


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

    session_start_hour = float(session_start.hour)
    session_start_dayofweek = float(session_start.weekday())
    session_start_dayofmonth = float(session_start.day)

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
        # Frozen training compatibility:
        # inter_event_gap_min was constant 0.0 in training.
        inter_event_gap_min = 0.0
        inter_event_gap_max = float(max(gaps))
    else:
        inter_event_gap_mean = 0.0
        inter_event_gap_min = 0.0
        inter_event_gap_max = 0.0

    # Recomputed duration from event timestamps.
    session_duration_recomputed_seconds = float(
        (timestamps[-1] - timestamps[0]).total_seconds()
    )

    if session_duration_recomputed_seconds < 0:
        raise ValueError(
            "Recomputed session duration cannot be negative"
        )

    # ----------------------------------------------------------
    # Colab parity:
    # auth_attempt_rate uses auth_attempt_total (per-event counter)
    # command_rate uses command_count_total (per-event counter)
    # rather than counting predicate-matching events.
    # ----------------------------------------------------------
    auth_attempt_total = _sum_int_field(
        copied_events,
        "auth_attempt",
    )

    command_count_total = _sum_int_field(
        copied_events,
        "command_count",
    )

    events_per_second = _safe_rate(
        len(copied_events),
        session_duration_recomputed_seconds,
    )

    auth_attempt_rate = _safe_rate(
        auth_attempt_total,
        session_duration_recomputed_seconds,
    )

    command_rate = _safe_rate(
        command_count_total,
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
