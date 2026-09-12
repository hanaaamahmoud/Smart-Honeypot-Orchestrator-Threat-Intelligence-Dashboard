"""
D3.6 — Geo / Availability Feature Generation

Generates:
- latitude_mean
- longitude_mean
- geo_latitude_abs
- geo_longitude_abs
- geo_location_available
- ip_reputation_available
- ip_reputation_missing_count

This module does NOT:
- scale features
- mutate input sessions
- generate session IDs
- generate other behavioral features
"""

from copy import deepcopy
from math import isfinite
from typing import Any, Dict, List, Optional


def _numeric_value(value: Any) -> Optional[float]:
    if value is None:
        return None

    if isinstance(value, bool):
        return None

    try:
        number = float(value)
    except (TypeError, ValueError):
        return None

    if not isfinite(number):
        return None

    return number


def _first_present(
    event: Dict[str, Any],
    aliases: List[str],
) -> Any:
    for key in aliases:
        if key in event:
            return event.get(key)

    return None


def _ip_reputation_present(event: Dict[str, Any]) -> bool:
    """
    Determine whether an IP reputation value is available.

    Presence means the field exists and contains a usable value.
    """

    aliases = [
        "ip_reputation",
        "ip_reputation_score",
        "reputation_score",
        "ip_reputation_available",
    ]

    value = _first_present(event, aliases)

    if value is None:
        return False

    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        return bool(value.strip())

    return True


def generate_geo_availability_features(
    session: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Generate geo-location and IP-reputation availability features.
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

    latitudes: List[float] = []
    longitudes: List[float] = []

    ip_reputation_missing_count = 0

    for event in copied_events:
        latitude = _numeric_value(
            _first_present(
                event,
                [
                    "latitude",
                    "lat",
                    "geo_latitude",
                ],
            )
        )

        longitude = _numeric_value(
            _first_present(
                event,
                [
                    "longitude",
                    "lon",
                    "lng",
                    "geo_longitude",
                ],
            )
        )

        if latitude is not None:
            latitudes.append(latitude)

        if longitude is not None:
            longitudes.append(longitude)

        if not _ip_reputation_present(event):
            ip_reputation_missing_count += 1

    latitude_mean = (
        sum(latitudes) / len(latitudes)
        if latitudes
        else 0.0
    )

    longitude_mean = (
        sum(longitudes) / len(longitudes)
        if longitudes
        else 0.0
    )

    geo_latitude_abs = abs(latitude_mean)
    geo_longitude_abs = abs(longitude_mean)

    geo_location_available = (
        len(latitudes) > 0
        and len(longitudes) > 0
    )

    ip_reputation_available = (
        ip_reputation_missing_count < len(copied_events)
        if copied_events
        else False
    )

    return {
        "latitude_mean": float(latitude_mean),
        "longitude_mean": float(longitude_mean),
        "geo_latitude_abs": float(
            geo_latitude_abs
        ),
        "geo_longitude_abs": float(
            geo_longitude_abs
        ),
        "geo_location_available": bool(
            geo_location_available
        ),
        "ip_reputation_available": bool(
            ip_reputation_available
        ),
        "ip_reputation_missing_count": int(
            ip_reputation_missing_count
        ),
    }
