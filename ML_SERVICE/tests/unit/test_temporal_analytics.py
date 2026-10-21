from datetime import date

import pytest

from app.analytics.temporal_analytics import (
    OUTPUT_FIELDS,
    build_temporal_analytics,
)


def make_record(**overrides):
    record = {
        "reconstructed_session_id": "session-001",
        "event_count": 10,
        "session_start": "2025-06-11T10:00:00Z",
        "session_end": "2025-06-11T10:00:25Z",
    }

    record.update(overrides)
    return record


def test_build_temporal_analytics_returns_expected_fields():
    result = build_temporal_analytics(
        [make_record()]
    )

    assert len(result) == 1
    assert tuple(result[0].keys()) == OUTPUT_FIELDS


def test_build_temporal_analytics_calculates_values():
    records = [
        make_record(
            reconstructed_session_id="session-001",
            event_count=10,
            session_start="2025-06-11T10:00:00Z",
            session_end="2025-06-11T10:00:25Z",
        ),
        make_record(
            reconstructed_session_id="session-002",
            event_count=20,
            session_start="2025-06-11T11:00:00Z",
            session_end="2025-06-11T11:01:05Z",
        ),
    ]

    result = build_temporal_analytics(records)

    assert len(result) == 1

    row = result[0]

    assert row["trend_date"] == date(2025, 6, 11)
    assert row["session_count"] == 2
    assert row["total_events"] == 30
    assert row["event_count"] == 30
    assert row["unique_sessions"] == 2

    # (25 + 65) / 2
    assert row["avg_session_duration_seconds"] == 45.0

    assert row["trend_type"] == "DAILY"


def test_multiple_daily_rows_are_preserved():
    records = [
        make_record(
            reconstructed_session_id="session-001",
            event_count=5,
            session_start="2025-06-09T10:00:00Z",
            session_end="2025-06-09T10:00:10Z",
        ),
        make_record(
            reconstructed_session_id="session-002",
            event_count=8,
            session_start="2025-06-10T10:00:00Z",
            session_end="2025-06-10T10:00:20Z",
        ),
        make_record(
            reconstructed_session_id="session-003",
            event_count=10,
            session_start="2025-06-11T10:00:00Z",
            session_end="2025-06-11T10:00:30Z",
        ),
    ]

    result = build_temporal_analytics(records)

    assert len(result) == 3

    assert [
        row["trend_date"]
        for row in result
    ] == [
        date(2025, 6, 9),
        date(2025, 6, 10),
        date(2025, 6, 11),
    ]


def test_multiple_sessions_same_day_are_aggregated():
    records = [
        make_record(
            reconstructed_session_id="session-a",
            event_count=10,
            session_start="2025-06-11T10:00:00Z",
            session_end="2025-06-11T10:00:20Z",
        ),
        make_record(
            reconstructed_session_id="session-b",
            event_count=15,
            session_start="2025-06-11T12:00:00Z",
            session_end="2025-06-11T12:00:40Z",
        ),
    ]

    result = build_temporal_analytics(records)

    assert len(result) == 1

    row = result[0]

    assert row["session_count"] == 2
    assert row["total_events"] == 25
    assert row["event_count"] == 25
    assert row["unique_sessions"] == 2
    assert row["avg_session_duration_seconds"] == 30.0


def test_missing_required_field_is_rejected():
    record = make_record()
    del record["reconstructed_session_id"]

    with pytest.raises(ValueError):
        build_temporal_analytics([record])


def test_missing_session_boundaries_are_rejected():
    record = make_record()
    del record["session_start"]

    with pytest.raises(ValueError):
        build_temporal_analytics([record])


def test_invalid_event_count_type_is_rejected():
    record = make_record(
        event_count="10"
    )

    with pytest.raises(TypeError):
        build_temporal_analytics([record])


def test_negative_event_count_is_rejected():
    record = make_record(
        event_count=-1
    )

    with pytest.raises(ValueError):
        build_temporal_analytics([record])


def test_invalid_timestamp_is_rejected():
    record = make_record(
        session_start="NOT-A-DATE"
    )

    with pytest.raises(ValueError):
        build_temporal_analytics([record])


def test_end_before_start_is_rejected():
    record = make_record(
        session_start="2025-06-11T11:00:00Z",
        session_end="2025-06-11T10:00:00Z",
    )

    with pytest.raises(ValueError):
        build_temporal_analytics([record])


def test_empty_input_returns_empty_list():
    result = build_temporal_analytics([])

    assert result == []


def test_output_contract_fields_are_exact():
    result = build_temporal_analytics(
        [make_record()]
    )

    assert set(result[0].keys()) == set(
        OUTPUT_FIELDS
    )


def test_daily_trend_type_is_constant():
    result = build_temporal_analytics(
        [make_record()]
    )

    assert result[0]["trend_type"] == "DAILY"
