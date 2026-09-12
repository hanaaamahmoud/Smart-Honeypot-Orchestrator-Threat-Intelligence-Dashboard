"""
D2.3 — Group Events by Session

Groups normalized events using their existing session_id.

This module does NOT:
- create session IDs
- sort events
- calculate duration
- calculate behavioral features
- mutate input events
"""

from copy import deepcopy
from typing import Any, Dict, List, Mapping, Tuple


def group_events_by_session(
    events: List[Mapping[str, Any]],
) -> Tuple[Dict[str, List[Dict[str, Any]]], List[Dict[str, Any]]]:
    """
    Group events by their existing session_id.

    Returns:
        (
            grouped_sessions,
            events_without_session_id,
        )

    grouped_sessions:
        {
            "session_id": [event, event, ...]
        }

    Events without a valid session_id are returned separately.
    No session ID is fabricated.
    """

    grouped: Dict[str, List[Dict[str, Any]]] = {}
    unassigned: List[Dict[str, Any]] = []

    for event in events:
        session_id = event.get("session_id")

        if session_id is None:
            unassigned.append(deepcopy(dict(event)))
            continue

        if not isinstance(session_id, str):
            raise TypeError(
                "session_id must be a string when provided"
            )

        session_id = session_id.strip()

        if not session_id:
            unassigned.append(deepcopy(dict(event)))
            continue

        if session_id not in grouped:
            grouped[session_id] = []

        grouped[session_id].append(deepcopy(dict(event)))

    return grouped, unassigned
