"""
Attacker IP Analytics

Contract derived from the existing Step 8 attacker IP analytics artifact.

Important:
- This module consumes already-enriched values.
- It does NOT perform GeoIP lookups.
- It does NOT call external providers.
- It does NOT infer country, ASN, city, or reputation.
- Missing optional enrichment is preserved.
"""

from __future__ import annotations

from collections import Counter
from typing import Any, Dict, Iterable, List


ATTACKER_IP_FIELDS = (
    "source_ip",
    "event_count",
    "unique_sessions",
    "unique_destinations",
    "unique_destination_ports",
    "unique_protocols",
    "unique_honeypots",
    "unique_usernames",
    "unique_countries",
    "unique_country_codes",
    "unique_geoip_countries",
    "unique_geoip_cities",
    "auth_attempt_total",
    "user_attempt_total",
    "pass_attempt_total",
    "command_count_total",
    "anonymous_total",
    "first_seen",
    "last_seen",
    "dominant_attack_type",
    "dominant_protocol",
    "dominant_honeypot",
    "ip_scope",
    "resolution_status",
    "location_source",
    "country",
    "country_code",
    "city",
    "latitude",
    "longitude",
    "asn",
    "asn_org",
    "dashboard_source",
)


REQUIRED_FIELDS = (
    "source_ip",
    "ip_scope",
    "resolution_status",
    "location_source",
    "dashboard_source",
)


OPTIONAL_GEOIP_FIELDS = (
    "country",
    "country_code",
    "city",
    "latitude",
    "longitude",
    "asn",
    "asn_org",
)


def _value(record: Dict[str, Any], field: str) -> Any:
    """Return a field without inventing a replacement value."""
    return record.get(field)


def _non_empty(value: Any) -> bool:
    return value is not None and str(value).strip() != ""


def _unique_non_empty(records: Iterable[Dict[str, Any]], field: str) -> int:
    values = {
        str(record[field]).strip()
        for record in records
        if _non_empty(record.get(field))
    }
    return len(values)


def validate_attacker_ip_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate one attacker-IP analytics record.

    Required fields must exist and be non-empty.
    GeoIP enrichment remains optional.
    """

    if not isinstance(record, dict):
        raise TypeError("attacker IP record must be a dictionary")

    missing = [
        field
        for field in REQUIRED_FIELDS
        if not _non_empty(record.get(field))
    ]

    if missing:
        raise ValueError(
            "Missing required attacker IP fields: "
            + ", ".join(missing)
        )

    source_ip = str(record["source_ip"]).strip()

    if not source_ip:
        raise ValueError("source_ip must not be empty")

    return {
        "valid": True,
        "source_ip": source_ip,
        "ip_scope": str(record["ip_scope"]).strip(),
        "resolution_status": str(
            record["resolution_status"]
        ).strip(),
        "location_source": str(
            record["location_source"]
        ).strip(),
    }


def build_attacker_ip_analytics(
    records: Iterable[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Build aggregate attacker-IP analytics from existing records.

    No external lookup or enrichment is performed.
    """

    records = list(records)

    if not records:
        return {
            "analytics_layer": "ATTACKER_IP_ANALYTICS",
            "row_count": 0,
            "unique_source_ips": 0,
            "public_source_ips": 0,
            "resolved_source_ips": 0,
            "unresolved_source_ips": 0,
            "country_diversity": 0,
            "country_code_diversity": 0,
            "city_diversity": 0,
            "asn_diversity": 0,
            "geoip_resolved_ratio": 0.0,
        }

    for record in records:
        validate_attacker_ip_record(record)

    source_ips = {
        str(record["source_ip"]).strip()
        for record in records
    }

    public_count = sum(
        str(record["ip_scope"]).strip().upper() == "PUBLIC"
        for record in records
    )

    resolved_count = sum(
        str(record["resolution_status"]).strip().upper()
        != "UNRESOLVED"
        for record in records
    )

    unresolved_count = len(records) - resolved_count

    result = {
        "analytics_layer": "ATTACKER_IP_ANALYTICS",
        "row_count": len(records),
        "unique_source_ips": len(source_ips),
        "public_source_ips": public_count,
        "resolved_source_ips": resolved_count,
        "unresolved_source_ips": unresolved_count,
        "country_diversity": _unique_non_empty(
            records,
            "country",
        ),
        "country_code_diversity": _unique_non_empty(
            records,
            "country_code",
        ),
        "city_diversity": _unique_non_empty(
            records,
            "city",
        ),
        "asn_diversity": _unique_non_empty(
            records,
            "asn",
        ),
        "geoip_resolved_ratio": (
            resolved_count / len(records)
        ),
    }

    return result


def summarize_resolution_status(
    records: Iterable[Dict[str, Any]],
) -> Dict[str, int]:
    """Return resolution-status counts without modifying records."""

    counter: Counter[str] = Counter()

    for record in records:
        status = record.get("resolution_status")

        if _non_empty(status):
            counter[str(status).strip()] += 1

    return dict(counter)


def summarize_location_source(
    records: Iterable[Dict[str, Any]],
) -> Dict[str, int]:
    """Return location-source counts without performing lookups."""

    counter: Counter[str] = Counter()

    for record in records:
        source = record.get("location_source")

        if _non_empty(source):
            counter[str(source).strip()] += 1

    return dict(counter)
