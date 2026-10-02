"""
D3.2 — Base / Count Feature Generation

Generates the first seven production behavioral features.

COLAB PARITY NOTE
-----------------
This module now mirrors the original Colab Step 5B-1 aggregation:

    auth_attempt_total    = sum(auth_attempt)
    user_attempt_total    = sum(user_attempt)
    pass_attempt_total    = sum(pass_attempt)
    command_count_total   = sum(command_count)
    anonymous_event_count = sum(anonymous)

Each of these fields exists in the canonical 24-field schema and
is aggregated as a plain integer sum. Missing / None values are
treated as 0, matching pandas ``sum`` semantics on NaN columns.

This module does NOT:
- scale features
- cluster
- modify input sessions
- generate the remaining 41 features
"""

from copy import deepcopy
from typing import Any, Dict, List


def _safe_int(value: Any) -> int:
    if value is None:
        return 0
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _sum_field(
    events: List[Dict[str, Any]],
    field_name: str,
) -> int:
    """
    Sum a direct integer counter across all events in a session.

    Matches pandas ``df.groupby(...)[field_name].sum()`` where
    NaN / missing values contribute 0.
    """
    return sum(
        _safe_int(event.get(field_name))
        for event in events
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

    copied_events = [
        deepcopy(event)
        for event in events
    ]

    event_count = len(copied_events)

    auth_attempt_total = _sum_field(
        copied_events,
        "auth_attempt",
    )

    user_attempt_total = _sum_field(
        copied_events,
        "user_attempt",
    )

    pass_attempt_total = _sum_field(
        copied_events,
        "pass_attempt",
    )

    command_count_total = _sum_field(
        copied_events,
        "command_count",
    )

    anonymous_event_count = _sum_field(
        copied_events,
        "anonymous",
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
