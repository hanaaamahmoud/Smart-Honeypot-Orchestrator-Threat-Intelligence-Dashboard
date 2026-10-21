"""
Unified Event Schema normalization.

STEP D-2

This module converts raw dictionary events into a stable internal
event representation.

Important production rules:
- Input normalization is deterministic.
- Unknown input fields are preserved under ``raw``.
- Missing optional fields remain None.
- No ML model is loaded here.
- No fitting/retraining is performed here.
- No cluster assignment is performed here.
- No behavioral feature values are invented here.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional


class EventNormalizationError(ValueError):
    """Raised when an input event cannot be normalized."""


# ------------------------------------------------------------
# Canonical field aliases
# ------------------------------------------------------------

_FIELD_ALIASES = {
    "event_id": (
        "event_id",
        "id",
        "_id",
    ),

    "timestamp": (
        "timestamp",
        "@timestamp",
        "time",
        "event_time",
        "datetime",
    ),

    "session_id": (
        "session_id",
        "session.id",
        "sessionId",
        "session",
    ),

    "source_ip": (
        "source_ip",
        "src_ip",
        "source.ip",
        "source_address",
        "client_ip",
        "client.ip",
        "src",
        "ip",
    ),

    "destination": (
        "destination",
        "destination_ip",
        "dest_ip",
        "destination.ip",
        "dst_ip",
        "dst",
        "host",
        "hostname",
    ),

    "destination_port": (
        "destination_port",
        "dest_port",
        "destination.port",
        "dst_port",
        "port",
    ),

    "protocol": (
        "protocol",
        "network.protocol",
        "transport",
    ),

    "username": (
        "username",
        "user.name",
        "user_name",
        "account",
        "user",
    ),

    "country": (
        "country",
        "geo.country",
        "geo_country",
    ),

    "country_code": (
        "country_code",
        "geo.country_code",
        "geo_country_code",
    ),

    "city": (
        "city",
        "geo.city",
        "geo_city",
    ),

    "latitude": (
        "latitude",
        "geo.latitude",
        "geo_latitude",
    ),

    "longitude": (
        "longitude",
        "geo.longitude",
        "geo_longitude",
    ),

    "honeypot": (
        "honeypot",
        "honeypot_name",
        "sensor.name",
        "sensor",
    ),

    "event_type": (
        "event_type",
        "event.type",
        "type",
        "action",
    ),

    "command": (
        "command",
        "cmd",
        "process.command_line",
        "process.command",
    ),

    "auth_attempt": (
        "auth_attempt",
    ),

    "user_attempt": (
        "user_attempt",
    ),

    "pass_attempt": (
        "pass_attempt",
    ),

    "anonymous": (
        "anonymous",
    ),

    "command_count": (
        "command_count",
    ),

    "source_port": (
        "source_port",
    ),

    "password": (
        "password",
    ),

}


def _get_nested_value(
    event: Dict[str, Any],
    path: str,
) -> Any:
    """
    Resolve a canonical field path.

    Resolution rules:

    1. Exact/direct scalar value wins.
    2. If an exact/direct value is a dict, do not return the
       dict as the canonical scalar value.
    3. Continue through the dotted ECS path.
    4. Return None when the path cannot be resolved.

    Examples:

        {
            "destination": "10.0.0.5",
            "destination": {"ip": "10.0.0.5"},
        }

    For nested ECS:

        destination.ip
        user.name
        sensor.name

    Important:
        A container dictionary is not considered the final
        canonical scalar value.
    """

    if not isinstance(event, dict):
        return None

    # --------------------------------------------------------
    # 1. Exact/direct key has priority ONLY when it is a
    #    scalar/non-container value.
    #
    #    Example:
    #
    #        {"username": "alice"}
    #
    #    wins over:
    #
    #        {"user": {"name": "bob"}}
    #
    #    But:
    #
    #        {"user": {"name": "bob"}}
    #
    #    must not become:
    #
    #        "{'name': 'bob'}"
    # --------------------------------------------------------

    if path in event:

        direct_value = event[path]

        if not isinstance(
            direct_value,
            dict
        ):

            return direct_value

    # --------------------------------------------------------
    # 2. Traverse dotted ECS path.
    # --------------------------------------------------------

    current: Any = event

    for part in path.split("."):

        if not isinstance(
            current,
            dict
        ):

            return None

        if part not in current:

            return None

        current = current[part]

    # --------------------------------------------------------
    # 3. Do not return container dictionaries as scalar
    #    canonical values.
    # --------------------------------------------------------

    if isinstance(
        current,
        dict
    ):

        return None

    return current
def _first_present(
    event: Dict[str, Any],
    aliases: Iterable[str],
) -> Any:
    for alias in aliases:
        value = _get_nested_value(event, alias)

        if value is not None:
            return value

    return None


def _clean_string(value: Any) -> Optional[str]:
    if value is None:
        return None

    if isinstance(value, str):
        value = value.strip()

        if not value:
            return None

        return value

    return str(value)


def _clean_number(value: Any) -> Optional[float]:
    if value is None:
        return None

    if isinstance(value, bool):
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _normalize_timestamp(value: Any) -> Optional[str]:
    """
    Return an ISO-8601 UTC timestamp when possible.

    The original raw value is still preserved in ``raw``.
    """
    if value is None:
        return None

    if isinstance(value, datetime):
        dt = value

        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)

        return dt.astimezone(timezone.utc).isoformat()

    if isinstance(value, (int, float)):
        try:
            dt = datetime.fromtimestamp(
                float(value),
                tz=timezone.utc,
            )

            return dt.isoformat()
        except (OverflowError, OSError, ValueError):
            return None

    if isinstance(value, str):
        text = value.strip()

        if not text:
            return None

        # Common UTC suffix normalization.
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"

        try:
            dt = datetime.fromisoformat(text)

            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)

            return dt.astimezone(timezone.utc).isoformat()

        except ValueError:
            # Keep the original textual timestamp if parsing fails.
            return value.strip()

    return None


def normalize_event(
    event: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Normalize one raw event.

    Required:
        event must be a dictionary.

    Returns:
        Stable dictionary containing canonical fields plus ``raw``.
    """
    if not isinstance(event, dict):
        raise EventNormalizationError(
            "Event must be a dictionary."
        )

    raw = deepcopy(event)

    normalized = {
        "event_id": _clean_string(
            _first_present(event, _FIELD_ALIASES["event_id"])
        ),
        "timestamp": _normalize_timestamp(
            _first_present(event, _FIELD_ALIASES["timestamp"])
        ),
        "session_id": _clean_string(
            _first_present(event, _FIELD_ALIASES["session_id"])
        ),
        "source_ip": _clean_string(
            _first_present(event, _FIELD_ALIASES["source_ip"])
        ),
        "destination": _clean_string(
            _first_present(event, _FIELD_ALIASES["destination"])
        ),
        "destination_port": _clean_number(
            _first_present(event, _FIELD_ALIASES["destination_port"])
        ),
        "protocol": _clean_string(
            _first_present(event, _FIELD_ALIASES["protocol"])
        ),
        "username": _clean_string(
            _first_present(event, _FIELD_ALIASES["username"])
        ),
        "country": _clean_string(
            _first_present(event, _FIELD_ALIASES["country"])
        ),
        "country_code": _clean_string(
            _first_present(event, _FIELD_ALIASES["country_code"])
        ),
        "city": _clean_string(
            _first_present(event, _FIELD_ALIASES["city"])
        ),
        "latitude": _clean_number(
            _first_present(event, _FIELD_ALIASES["latitude"])
        ),
        "longitude": _clean_number(
            _first_present(event, _FIELD_ALIASES["longitude"])
        ),
        "honeypot": _clean_string(
            _first_present(event, _FIELD_ALIASES["honeypot"])
        ),
        "event_type": _clean_string(
            _first_present(event, _FIELD_ALIASES["event_type"])
        ),
        "command": _clean_string(
            _first_present(event, _FIELD_ALIASES["command"])
        ),
        "auth_attempt": _clean_number(
            _first_present(event, _FIELD_ALIASES["auth_attempt"])
        ),
        "user_attempt": _clean_number(
            _first_present(event, _FIELD_ALIASES["user_attempt"])
        ),
        "pass_attempt": _clean_number(
            _first_present(event, _FIELD_ALIASES["pass_attempt"])
        ),
        "anonymous": _clean_number(
            _first_present(event, _FIELD_ALIASES["anonymous"])
        ),
        "command_count": _clean_number(
            _first_present(event, _FIELD_ALIASES["command_count"])
        ),
        "source_port": _clean_number(
            _first_present(event, _FIELD_ALIASES["source_port"])
        ),
        "password": _clean_string(
            _first_present(event, _FIELD_ALIASES["password"])
        ),
        "raw": raw,
    }

    return normalized


def normalize_events(
    events: Iterable[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Normalize a collection of raw events.
    """
    if events is None:
        raise EventNormalizationError(
            "Events cannot be None."
        )

    return [
        normalize_event(event)
        for event in events
    ]


__all__ = [
    "EventNormalizationError",
    "normalize_event",
    "normalize_events",
]
