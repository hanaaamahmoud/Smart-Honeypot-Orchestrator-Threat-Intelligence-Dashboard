from app.pipeline.session_grouping import group_events_by_session
from app.pipeline.session_reconstruction import reconstruct_sessions


def test_event_count_check_excludes_unassigned_from_loss():
    events = [
        {
            "session_id": "A",
            "timestamp": "2026-01-01T10:00:00Z",
        },
        {
            "session_id": "A",
            "timestamp": "2026-01-01T10:01:00Z",
        },
        {
            # No session_id — intentionally unassigned
            "timestamp": "2026-01-01T10:02:00Z",
        },
        {
            "session_id": "B",
            "timestamp": "2026-01-01T11:00:00Z",
        },
    ]

    grouped, unassigned = group_events_by_session(events)

    grouped_count = sum(
        len(session_events)
        for session_events in grouped.values()
    )

    unassigned_count = len(unassigned)

    total_input = len(events)

    # The conservation check must account for both
    # reconstructed events and intentionally unassigned events.
    assert grouped_count + unassigned_count == total_input

    # Unassigned events are not considered lost.
    assert unassigned_count == 1
    assert grouped_count == 3


def test_reconstruction_does_not_report_unassigned_as_lost():
    events = [
        {
            "session_id": "A",
            "timestamp": "2026-01-01T10:00:00Z",
        },
        {
            "session_id": "A",
            "timestamp": "2026-01-01T10:01:00Z",
        },
        {
            "timestamp": "2026-01-01T10:02:00Z",
        },
    ]

    sessions = reconstruct_sessions(events)

    reconstructed_count = sum(
        session["event_count"]
        for session in sessions
    )

    # Only events with valid session IDs become sessions.
    assert reconstructed_count == 2

    # The third event is intentionally unassigned,
    # not lost due to reconstruction failure.
    assert reconstructed_count < len(events)
