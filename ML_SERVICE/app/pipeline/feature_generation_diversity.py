"""
D3.3 — Diversity / Cardinality Feature Generation

Generates:
- unique cardinality features
- diversity ratio features

This module does NOT:
- scale features
- cluster
- modify input sessions
- calculate temporal features
"""

from copy import deepcopy
from typing import Any, Dict, List


def _clean(value: Any) -> str:
    if value is None:
        return ""

    return str(value).strip()


def _unique_count(
    events: List[Dict[str, Any]],
    aliases: List[str],
) -> int:
    values = set()

    for event in events:
        value = None

        for key in aliases:
            if key in event:
                value = event.get(key)

                if value is not None:
                    break

        value = _clean(value)

        if value:
            values.add(value)

    return len(values)


def _diversity(
    unique_count: int,
    event_count: int,
) -> float:
    if event_count <= 0:
        return 0.0

    return float(unique_count / event_count)


def generate_diversity_features(
    session: Dict[str, Any],
) -> Dict[str, float]:
    """
    Generate unique-value/cardinality and diversity
    features for one session.
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

    unique_destinations = _unique_count(
        copied_events,
        [
            "destination",
            "destination_ip",
            "dst_ip",
            "dest_ip",
            "destination_host",
        ],
    )

    unique_destination_ports = _unique_count(
        copied_events,
        [
            "destination_port",
            "dst_port",
            "dest_port",
        ],
    )

    unique_source_ips = _unique_count(
        copied_events,
        [
            "source_ip",
            "src_ip",
            "source",
        ],
    )

    unique_protocols = _unique_count(
        copied_events,
        [
            "protocol",
            "network_protocol",
        ],
    )

    unique_honeypots = _unique_count(
        copied_events,
        [
            "honeypot",
            "honeypot_id",
            "sensor",
            "sensor_id",
        ],
    )

    unique_usernames = _unique_count(
        copied_events,
        [
            "username",
            "user",
            "user_name",
        ],
    )

    unique_countries = _unique_count(
        copied_events,
        [
            "country",
            "geo_country",
        ],
    )

    unique_country_codes = _unique_count(
        copied_events,
        [
            "country_code",
            "countryCode",
            "geo_country_code",
        ],
    )

    unique_cities = _unique_count(
        copied_events,
        [
            "city",
            "geo_city",
        ],
    )

    return {
        # Cardinality features
        "unique_destinations": float(
            unique_destinations
        ),

        "unique_destination_ports": float(
            unique_destination_ports
        ),

        "unique_source_ips": float(
            unique_source_ips
        ),

        "unique_protocols": float(
            unique_protocols
        ),

        "unique_honeypots": float(
            unique_honeypots
        ),

        "unique_usernames": float(
            unique_usernames
        ),

        "unique_countries": float(
            unique_countries
        ),

        "unique_country_codes": float(
            unique_country_codes
        ),

        "unique_cities": float(
            unique_cities
        ),

        # Diversity features
        "destination_diversity": _diversity(
            unique_destinations,
            event_count,
        ),

        "destination_port_diversity": _diversity(
            unique_destination_ports,
            event_count,
        ),

        "protocol_diversity": _diversity(
            unique_protocols,
            event_count,
        ),

        "honeypot_diversity": _diversity(
            unique_honeypots,
            event_count,
        ),

        "username_diversity": _diversity(
            unique_usernames,
            event_count,
        ),

        "geo_country_diversity": _diversity(
            unique_countries,
            event_count,
        ),

        "geo_city_diversity": _diversity(
            unique_cities,
            event_count,
        ),
    }
