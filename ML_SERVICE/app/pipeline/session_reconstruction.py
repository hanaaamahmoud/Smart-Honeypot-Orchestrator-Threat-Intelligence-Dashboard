"""
D2.6 — Session Reconstruction Integration

Combines the D2 session reconstruction stages:

1. Validate existing session_id
2. Group events by session_id
3. Sort events chronologically
4. Calculate session boundaries
5. Return complete stable sessions

This module does NOT:
- fabricate session IDs
- generate behavioral features
- scale data
- cluster sessions
- mutate input events
"""

from copy import deepcopy
from datetime import datetime
from typing import Any, Dict, List

from app.pipeline.session_grouping import group_events_by_session
from app.pipeline.session_boundaries import calculate_session_boundaries


def _timestamp_key(event: Dict[str, Any]) -> datetime:
    """
    Parse an event timestamp for chronological ordering.
    """

    timestamp = event.get("timestamp")

    if not isinstance(timestamp, str):
        raise TypeError(
            "Each event must contain a string timestamp"
        )

    value = timestamp.strip()

    if not value:
        raise ValueError(
            "timestamp cannot be empty"
        )

    if value.endswith("Z"):
        value = value[:-1] + "+00:00"

    try:
        return datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(
            f"Invalid ISO-8601 timestamp: {timestamp}"
        ) from exc


def reconstruct_sessions(
    events: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Reconstruct stable sessions from normalized events.

    Events without a valid session_id are NOT assigned
    a fabricated session ID.

    Returns:
        List of complete session dictionaries.
    """

    # Protect caller input.
    working_events = deepcopy(events)

    # D2.3 — Group events by existing session_id.
    grouped, unassigned = group_events_by_session(
        working_events
    )

    # Events without a session_id are intentionally
    # excluded from reconstructed sessions.
    #
    # No session ID is fabricated.
    _ = unassigned

    sessions: List[Dict[str, Any]] = []

    for session_id, session_events in grouped.items():

        # D2.4 — Stable chronological ordering.
        ordered_events = sorted(
            session_events,
            key=_timestamp_key,
        )

        # D2.5 — Calculate session boundaries.
        session = calculate_session_boundaries(
            session_id=session_id,
            events=ordered_events,
        )

        sessions.append(session)

    # Ensure deterministic session ordering.
    sessions.sort(
        key=lambda session: session["session_id"]
    )

    return sessions
