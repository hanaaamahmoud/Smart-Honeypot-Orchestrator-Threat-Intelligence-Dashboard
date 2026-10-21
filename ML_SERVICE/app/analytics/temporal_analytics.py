"""
Temporal analytics.

Build daily temporal trends from validated ML session results.

The temporal analytics layer consumes the existing ML Result Contract.
It does not rerun normalization, session reconstruction, feature
generation, clustering, or model inference.
"""

from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime
from typing import Any, Iterable


OUTPUT_FIELDS = (
    "trend_date",
    "session_count",
    "total_events",
    "avg_session_duration_seconds",
    "event_count",
    "unique_sessions",
    "trend_type",
)

TREND_TYPE = "DAILY"


def _parse_datetime(value: Any) -> datetime:
    """Convert a supported session timestamp into datetime."""

    if isinstance(value, datetime):
        return value

    if isinstance(value, str):
        normalized = value.replace("Z", "+00:00")

        try:
            return datetime.fromisoformat(normalized)
        except ValueError as exc:
            raise ValueError(
                f"Invalid session timestamp: {value}"
            ) from exc

    raise TypeError(
        "Session timestamp must be datetime or ISO datetime string"
    )


def _trend_date(record: dict[str, Any]) -> date:
    """Extract the daily trend date from session_start."""

    value = record.get("session_start")

    if value is None:
        raise ValueError(
            "session_start is required for temporal analytics"
        )

    return _parse_datetime(value).date()


def _session_duration_seconds(
    record: dict[str, Any],
) -> float:
    """Calculate duration from the ML session boundaries."""

    start = record.get("session_start")
    end = record.get("session_end")

    if start is None or end is None:
        raise ValueError(
            "session_start and session_end are required "
            "for temporal analytics"
        )

    start_dt = _parse_datetime(start)
    end_dt = _parse_datetime(end)

    duration = (end_dt - start_dt).total_seconds()

    if duration < 0:
        raise ValueError(
            "session_end cannot be earlier than session_start"
        )

    return float(duration)


def _validate_record(record: dict[str, Any]) -> None:
    """Validate the required ML Result Contract fields."""

    if not isinstance(record, dict):
        raise TypeError(
            "Temporal analytics input must be a dictionary"
        )

    required_fields = (
        "reconstructed_session_id",
        "event_count",
        "session_start",
        "session_end",
    )

    missing = [
        field
        for field in required_fields
        if field not in record
    ]

    if missing:
        raise ValueError(
            f"Missing temporal analytics input fields: {missing}"
        )

    if not record["reconstructed_session_id"]:
        raise ValueError(
            "reconstructed_session_id cannot be empty"
        )

    if not isinstance(record["event_count"], int):
        raise TypeError(
            "event_count must be an integer"
        )

    if record["event_count"] < 0:
        raise ValueError(
            "event_count cannot be negative"
        )

    _trend_date(record)
    _session_duration_seconds(record)


def build_temporal_analytics(
    records: Iterable[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Build one DAILY temporal trend row per calendar date.

    Input:
        Validated ML session-result records.

    Output:
        Daily temporal trend records.

    Important:
        total_events is represented using the aggregate event count
        supplied by the ML Result Contract. No independent raw-event
        formula is inferred here.
    """

    daily: dict[date, dict[str, Any]] = defaultdict(
        lambda: {
            "session_count": 0,
            "event_count": 0,
            "unique_session_ids": set(),
            "durations": [],
        }
    )

    for record in records:
        _validate_record(record)

        trend_date = _trend_date(record)

        bucket = daily[trend_date]

        bucket["session_count"] += 1
        bucket["event_count"] += record["event_count"]
        bucket["unique_session_ids"].add(
            record["reconstructed_session_id"]
        )
        bucket["durations"].append(
            _session_duration_seconds(record)
        )

    output: list[dict[str, Any]] = []

    for trend_date in sorted(daily):
        bucket = daily[trend_date]

        durations = bucket["durations"]

        avg_duration = (
            sum(durations) / len(durations)
            if durations
            else 0.0
        )

        event_count = bucket["event_count"]

        output.append(
            {
                "trend_date": trend_date,
                "session_count": bucket["session_count"],
                "total_events": event_count,
                "avg_session_duration_seconds": float(
                    avg_duration
                ),
                "event_count": event_count,
                "unique_sessions": len(
                    bucket["unique_session_ids"]
                ),
                "trend_type": TREND_TYPE,
            }
        )

    return output


__all__ = [
    "OUTPUT_FIELDS",
    "TREND_TYPE",
    "build_temporal_analytics",
]
