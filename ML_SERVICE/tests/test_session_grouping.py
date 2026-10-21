from app.pipeline.session_grouping import group_events_by_session


def test_events_are_grouped_by_session_id():
    events = [
        {"session_id": "A", "event": 1},
        {"session_id": "B", "event": 2},
        {"session_id": "A", "event": 3},
    ]

    grouped, unassigned = group_events_by_session(events)

    assert set(grouped.keys()) == {"A", "B"}

    assert [e["event"] for e in grouped["A"]] == [1, 3]
    assert [e["event"] for e in grouped["B"]] == [2]

    assert unassigned == []


def test_different_session_ids_are_not_mixed():
    events = [
        {"session_id": "A", "event": 1},
        {"session_id": "B", "event": 2},
    ]

    grouped, _ = group_events_by_session(events)

    assert len(grouped["A"]) == 1
    assert len(grouped["B"]) == 1


def test_missing_session_id_is_not_fabricated():
    events = [
        {"event": 1},
        {"session_id": "A", "event": 2},
    ]

    grouped, unassigned = group_events_by_session(events)

    assert list(grouped.keys()) == ["A"]
    assert len(unassigned) == 1
    assert unassigned[0]["event"] == 1


def test_empty_session_id_is_not_fabricated():
    events = [
        {"session_id": "", "event": 1},
        {"session_id": "   ", "event": 2},
    ]

    grouped, unassigned = group_events_by_session(events)

    assert grouped == {}
    assert [e["event"] for e in unassigned] == [1, 2]


def test_input_is_not_mutated():
    events = [
        {"session_id": "A", "event": 1},
        {"session_id": "A", "event": 2},
    ]

    original = [dict(event) for event in events]

    group_events_by_session(events)

    assert events == original


def test_event_conservation():
    events = [
        {"session_id": "A", "event": 1},
        {"session_id": "B", "event": 2},
        {"session_id": "A", "event": 3},
        {"event": 4},
    ]

    grouped, unassigned = group_events_by_session(events)

    grouped_count = sum(
        len(session_events)
        for session_events in grouped.values()
    )

    total_output = grouped_count + len(unassigned)

    assert total_output == len(events)


def test_non_string_session_id_is_rejected():
    events = [
        {"session_id": 123, "event": 1},
    ]

    try:
        group_events_by_session(events)
    except TypeError:
        return

    assert False, "Expected TypeError for non-string session_id"
