"""
D2.4 — Stable Chronological Session Ordering

Orders events within each reconstructed session by timestamp.

This module does NOT:
- create session IDs
- remove events
- create events
- calculate duration
- generate behavioral features
- mutate input
"""

from copy import deepcopy
from datetime import datetime
from typing import Any, Dict, List


def _parse_timestamp(timestamp: Any) -> datetime:
    """
    Parse an ISO-8601 timestamp.

    Raises:
        ValueError: if timestamp is missing or invalid.
        TypeError: if timestamp is not a string.
    """

    if not isinstance(timestamp, str):
        raise TypeError("timestamp must be a string")

    value = timestamp.strip()

    if not value:
        raise ValueError("timestamp cannot be empty")

    # Support ISO timestamps ending in Z.
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"

    try:
        return datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(
            f"Invalid ISO-8601 timestamp: {timestamp}"
        ) from exc


def order_session_events(
    grouped_sessions: Dict[str, List[Dict[str, Any]]],
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Return a chronologically ordered copy of every session.

    Python's sorted() is stable, so events with identical timestamps
    retain their original relative ordering.
    """

    ordered: Dict[str, List[Dict[str, Any]]] = {}

    for session_id, events in grouped_sessions.items():

        copied_events = [
            deepcopy(event)
            for event in events
        ]

        ordered[session_id] = sorted(
            copied_events,
            key=lambda event: _parse_timestamp(event["timestamp"]),
        )

    return ordered
