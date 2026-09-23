"""
GeoIP Analytics
===============

Consumes validated GeoIP fields already present in pipeline outputs.

IMPORTANT:
- No GeoIP inference from source_ip.
- No external lookup.
- No mutation of the ML feature contract.
- Missing/unresolved GeoIP remains explicitly unresolved.
"""

from __future__ import annotations

from typing import Any, Iterable, Mapping


GEOIP_FIELDS = (
    "source_ip",
    "country",
    "country_code",
    "city",
    "latitude",
    "longitude",
    "asn",
    "asn_org",
    "resolution_status",
    "location_source",
)

REQUIRED_FIELDS = (
    "source_ip",
    "resolution_status",
    "location_source",
)


def _clean(value: Any) -> Any:
    if value is None:
        return None

    if isinstance(value, str):
        value = value.strip()
        return value if value else None

    return value


def _is_present(value: Any) -> bool:
    return _clean(value) is not None


def _safe_unique(values: Iterable[Any]) -> int:
    return len(
        {
            str(value)
            for value in values
            if _is_present(value)
        }
    )


def _rows(records: Iterable[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    return list(records)


def build_geoip_analytics(
    records: Iterable[Mapping[str, Any]],
) -> dict[str, Any]:
    """
    Build dashboard-ready GeoIP analytics from validated records.

    This function never resolves an IP address itself.
    """

    rows = _rows(records)

    if not rows:
        return {
            "analytics_layer": "GEOIP_ANALYTICS",
            "row_count": 0,
            "unique_source_ips": 0,
            "resolved_rows": 0,
            "unresolved_rows": 0,
            "country_diversity": 0,
            "country_code_diversity": 0,
            "city_diversity": 0,
            "asn_diversity": 0,
            "resolution_status_counts": {},
            "location_source_counts": {},
            "countries": [],
            "country_codes": [],
            "asns": [],
        }

    missing = []

    for index, row in enumerate(rows):
        for field in REQUIRED_FIELDS:
            if field not in row:
                missing.append(
                    f"row={index} missing={field}"
                )

    if missing:
        raise ValueError(
            "GeoIP input contract violation: "
            + "; ".join(missing[:10])
        )

    countries = [
        _clean(row.get("country"))
        for row in rows
    ]

    country_codes = [
        _clean(row.get("country_code"))
        for row in rows
    ]

    cities = [
        _clean(row.get("city"))
        for row in rows
    ]

    asns = [
        _clean(row.get("asn"))
        for row in rows
    ]

    resolution_statuses = [
        _clean(row.get("resolution_status"))
        for row in rows
    ]

    location_sources = [
        _clean(row.get("location_source"))
        for row in rows
    ]

    resolution_status_counts: dict[str, int] = {}

    for status in resolution_statuses:
        if status is not None:
            resolution_status_counts[str(status)] = (
                resolution_status_counts.get(str(status), 0) + 1
            )

    location_source_counts: dict[str, int] = {}

    for source in location_sources:
        if source is not None:
            location_source_counts[str(source)] = (
                location_source_counts.get(str(source), 0) + 1
            )

    resolved_rows = sum(
        1
        for status in resolution_statuses
        if status is not None
        and str(status).startswith("RESOLVED")
    )

    unresolved_rows = sum(
        1
        for status in resolution_statuses
        if status == "UNRESOLVED"
    )

    return {
        "analytics_layer": "GEOIP_ANALYTICS",

        "row_count": len(rows),

        "unique_source_ips": _safe_unique(
            row.get("source_ip")
            for row in rows
        ),

        "resolved_rows": resolved_rows,
        "unresolved_rows": unresolved_rows,

        "country_diversity": _safe_unique(countries),
        "country_code_diversity": _safe_unique(country_codes),
        "city_diversity": _safe_unique(cities),
        "asn_diversity": _safe_unique(asns),

        "resolution_status_counts": resolution_status_counts,
        "location_source_counts": location_source_counts,

        "countries": sorted(
            {str(v) for v in countries if v is not None}
        ),

        "country_codes": sorted(
            {str(v) for v in country_codes if v is not None}
        ),

        "asns": sorted(
            {str(v) for v in asns if v is not None}
        ),
    }


def validate_geoip_record(
    record: Mapping[str, Any],
) -> dict[str, Any]:
    """
    Validate one already-resolved GeoIP record.

    This does not perform a lookup.
    """

    missing = [
        field
        for field in REQUIRED_FIELDS
        if field not in record
    ]

    if missing:
        raise ValueError(
            f"Missing required GeoIP fields: {missing}"
        )

    status = _clean(record.get("resolution_status"))
    source = _clean(record.get("location_source"))

    if status == "UNRESOLVED":
        return {
            "valid": True,
            "resolved": False,
            "resolution_status": status,
            "location_source": source,
        }

    if status is None:
        raise ValueError(
            "resolution_status must be explicit"
        )

    return {
        "valid": True,
        "resolved": status.startswith("RESOLVED"),
        "resolution_status": status,
        "location_source": source,
    }


__all__ = [
    "GEOIP_FIELDS",
    "REQUIRED_FIELDS",
    "build_geoip_analytics",
    "validate_geoip_record",
]
