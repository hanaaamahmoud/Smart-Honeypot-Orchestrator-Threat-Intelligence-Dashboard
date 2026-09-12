"""
D2.5 — Session Boundary Calculation

Calculates start time, end time, duration, and event count
for already ordered session events.

This module does NOT:
- create session IDs
- reorder events
- generate behavioral features
- mutate input events
"""

from copy import deepcopy
from datetime import datetime
from typing import Any, Dict, List


def _parse_timestamp(timestamp: Any) -> datetime:
    if not isinstance(timestamp, str):
        raise TypeError("timestamp must be a string")

    value = timestamp.strip()

    if not value:
        raise ValueError("timestamp cannot be empty")

    if value.endswith("Z"):
        value = value[:-1] + "+00:00"

    try:
        return datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(
            f"Invalid ISO-8601 timestamp: {timestamp}"
        ) from exc


def calculate_session_boundaries(
    session_id: str,
    events: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Calculate stable session boundaries from ordered events.

    Assumption:
        events are already chronologically ordered by D2.4.
    """

    if not isinstance(session_id, str):
        raise TypeError("session_id must be a string")

    if not session_id.strip():
        raise ValueError("session_id cannot be empty")

    if not events:
        raise ValueError(
            "Cannot calculate boundaries for an empty session"
        )

    copied_events = [
        deepcopy(event)
        for event in events
    ]

    # Validate timestamps and use them directly from the
    # already ordered event sequence.
    parsed_timestamps = [
        _parse_timestamp(event["timestamp"])
        for event in copied_events
    ]

    start_dt = parsed_timestamps[0]
    end_dt = parsed_timestamps[-1]

    duration_seconds = (
        end_dt - start_dt
    ).total_seconds()

    if duration_seconds < 0:
        raise ValueError(
            "Session events are not chronologically ordered"
        )

    return {
        "session_id": session_id,
        "events": copied_events,
        "event_count": len(copied_events),
        "start_time": copied_events[0]["timestamp"],
        "end_time": copied_events[-1]["timestamp"],
        "duration_seconds": float(duration_seconds),
    }
