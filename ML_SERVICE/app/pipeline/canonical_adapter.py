"""
L2.4 — Canonical Event Adapter

Converts an already-normalized event into the stable
24-field CanonicalEvent contract.

This layer:
- preserves existing normalization
- does not calculate features
- does not fabricate values
- preserves None for missing optional fields
- does not create session IDs
- validates the final object through CanonicalEvent
"""

from typing import Any, Dict, Iterable, List

from app.schemas import CanonicalEvent


CANONICAL_FIELDS = (
    "timestamp",
    "honeypot",
    "protocol",
    "source_ip",
    "source_port",
    "destination_ip",
    "destination_port",
    "session_id",
    "username",
    "password",
    "user_attempt",
    "pass_attempt",
    "auth_attempt",
    "anonymous",
    "command_count",
    "country",
    "country_code",
    "asn",
    "ip_reputation",
    "attack_type",
    "mitre_technique",
    "attack_stage",
    "severity",
    "source_dataset",
)


def _source(event: Dict[str, Any]) -> Dict[str, Any]:
    raw = event.get("raw")

    if isinstance(raw, dict):
        return raw

    return {}


def _value(
    event: Dict[str, Any],
    field: str,
) -> Any:
    """
    Prefer the normalized value when it exists.
    Otherwise read the original raw ELK event.
    """

    if field in event and event[field] is not None:
        return event[field]

    raw = _source(event)

    return raw.get(field)


def _optional_int(
    value: Any,
    field: str,
) -> int | None:
    if value is None:
        return None

    if isinstance(value, bool):
        raise TypeError(
            f"{field} must be an integer or None"
        )

    if isinstance(value, int):
        return value

    if isinstance(value, float):
        if not value.is_integer():
            raise TypeError(
                f"{field} must be an integer or None"
            )
        return int(value)

    if isinstance(value, str):
        text = value.strip()

        if not text:
            return None

        try:
            return int(text)
        except ValueError as exc:
            raise TypeError(
                f"{field} must be an integer or None"
            ) from exc

    raise TypeError(
        f"{field} must be an integer or None"
    )


def _optional_str(
    value: Any,
    field: str,
) -> str | None:
    if value is None:
        return None

    if isinstance(value, str):
        value = value.strip()

        return value if value else None

    raise TypeError(
        f"{field} must be a string or None"
    )


def canonicalize_event(
    event: Dict[str, Any],
) -> CanonicalEvent:
    """
    Convert one normalized event into CanonicalEvent.
    """

    if not isinstance(event, dict):
        raise TypeError(
            "Event must be a dictionary"
        )

    return CanonicalEvent(
        timestamp=_value(event, "timestamp"),
        honeypot=_value(event, "honeypot"),
        protocol=_value(event, "protocol"),
        source_ip=_value(event, "source_ip"),

        source_port=_optional_int(
            _value(event, "source_port"),
            "source_port",
        ),

        destination_ip=_optional_str(
            _value(event, "destination_ip"),
            "destination_ip",
        ),

        destination_port=_optional_int(
            _value(event, "destination_port"),
            "destination_port",
        ),

        session_id=_optional_str(
            _value(event, "session_id"),
            "session_id",
        ),

        username=_optional_str(
            _value(event, "username"),
            "username",
        ),

        password=_optional_str(
            _value(event, "password"),
            "password",
        ),

        user_attempt=_optional_int(
            _value(event, "user_attempt"),
            "user_attempt",
        ),

        pass_attempt=_optional_int(
            _value(event, "pass_attempt"),
            "pass_attempt",
        ),

        auth_attempt=_optional_int(
            _value(event, "auth_attempt"),
            "auth_attempt",
        ),

        anonymous=_optional_int(
            _value(event, "anonymous"),
            "anonymous",
        ),

        command_count=_optional_int(
            _value(event, "command_count"),
            "command_count",
        ),

        country=_optional_str(
            _value(event, "country"),
            "country",
        ),

        country_code=_optional_str(
            _value(event, "country_code"),
            "country_code",
        ),

        asn=_optional_int(
            _value(event, "asn"),
            "asn",
        ),

        ip_reputation=_optional_str(
            _value(event, "ip_reputation"),
            "ip_reputation",
        ),

        attack_type=_optional_str(
            _value(event, "attack_type"),
            "attack_type",
        ),

        mitre_technique=_optional_str(
            _value(event, "mitre_technique"),
            "mitre_technique",
        ),

        attack_stage=_optional_str(
            _value(event, "attack_stage"),
            "attack_stage",
        ),

        severity=_optional_str(
            _value(event, "severity"),
            "severity",
        ),

        source_dataset=_optional_str(
            _value(event, "source_dataset"),
            "source_dataset",
        ),
    )


def canonicalize_events(
    events: Iterable[Dict[str, Any]],
) -> List[CanonicalEvent]:
    """
    Convert multiple normalized events into CanonicalEvent objects.
    """

    if events is None:
        raise TypeError(
            "Events cannot be None"
        )

    return [
        canonicalize_event(event)
        for event in events
    ]


__all__ = [
    "CANONICAL_FIELDS",
    "canonicalize_event",
    "canonicalize_events",
]
