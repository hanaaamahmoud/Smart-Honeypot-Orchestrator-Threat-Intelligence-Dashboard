"""
D3.2 — Base / Count Feature Generation

Generates the first seven production behavioral features.

This module does NOT:
- scale features
- cluster
- modify input sessions
- generate the remaining 41 features
"""

from copy import deepcopy
from typing import Any, Dict


def _normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip().lower()


def _event_type(event: Dict[str, Any]) -> str:
    return _normalize_text(
        event.get("event_type")
        or event.get("type")
        or event.get("event")
    )


def _username(event: Dict[str, Any]) -> str:
    return _normalize_text(
        event.get("username")
        or event.get("user")
        or event.get("user_name")
    )


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


def generate_base_features(
    session: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Generate the seven base/count features for one stable session.
    """

    if not isinstance(session, dict):
        raise TypeError("session must be a dictionary")

    events = session.get("events")

    if not isinstance(events, list):
        raise TypeError("session['events'] must be a list")

    # Work on copies only.
    copied_events = [
        deepcopy(event)
        for event in events
    ]

    event_count = len(copied_events)

    auth_attempt_total = sum(
        1
        for event in copied_events
        if _is_auth_event(event)
    )

    user_attempt_total = sum(
        1
        for event in copied_events
        if (
            _is_auth_event(event)
            and _username(event) != ""
        )
    )

    pass_attempt_total = sum(
        1
        for event in copied_events
        if (
            _is_auth_event(event)
            and (
                "password" in event
                or "pass" in event
                or "credential" in event
            )
        )
    )

    command_count_total = sum(
        1
        for event in copied_events
        if _is_command_event(event)
    )

    anonymous_event_count = sum(
        1
        for event in copied_events
        if _username(event) in {
            "",
            "anonymous",
            "anon",
            "null",
            "none",
        }
    )

    duration = session.get("duration_seconds", 0.0)

    if duration is None:
        duration = 0.0

    duration = float(duration)

    if duration < 0:
        raise ValueError(
            "session duration cannot be negative"
        )

    return {
        "event_count": int(event_count),
        "session_duration_seconds": duration,
        "auth_attempt_total": int(auth_attempt_total),
        "user_attempt_total": int(user_attempt_total),
        "pass_attempt_total": int(pass_attempt_total),
        "command_count_total": int(command_count_total),
        "anonymous_event_count": int(
            anonymous_event_count
        ),
    }
