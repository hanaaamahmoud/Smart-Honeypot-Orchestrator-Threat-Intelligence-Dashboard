"""Unit tests for session_replay."""

import pytest

from app.analytics.session_replay import (
    ANALYTICS_LAYER,
    build_session_replay,
)


def make(**o):
    r = {
        "timestamp": "2025-06-10T10:00:00Z",
        "session_id": "s-001",
        "honeypot": "cowrie",
        "protocol": "SSH",
        "source_ip": "1.2.3.4",
        "source_dataset": "cowrie_ssh",
        "country": "Egypt",
        "country_code": "EG",
        "username": "root",
        "attack_type": "SSH Probe",
        "mitre_technique": "T1595",
        "attack_stage": "Reconnaissance",
        "severity": "Low",
        "auth_attempt": 1,
    }
    r.update(o)
    return r


def test_empty_input():
    result = build_session_replay([])
    assert result["analytics_layer"] == ANALYTICS_LAYER
    assert result["sessions"] == []


def test_single_event_session():
    result = build_session_replay([make()])
    assert len(result["sessions"]) == 1
    s = result["sessions"][0]
    assert s["reconstructed_session_id"] == "s-001"
    assert s["summary"]["event_count"] == 1
    assert s["summary"]["context"]["honeypot"] == "cowrie"
    assert s["summary"]["classification"]["mitre_technique"] == "T1595"


def test_session_summary_structure():
    result = build_session_replay([make()])
    s = result["sessions"][0]["summary"]
    assert "context" in s
    assert "classification" in s
    assert "credentials" in s
    assert "commands" in s
    assert "flags" in s
    assert "source_ips" in s


def test_events_have_offsets():
    events = [
        make(timestamp="2025-06-10T10:00:00Z"),
        make(timestamp="2025-06-10T10:00:05Z"),
        make(timestamp="2025-06-10T10:00:10Z"),
    ]
    result = build_session_replay(events)
    session = result["sessions"][0]
    offs = [e["_offset_seconds"] for e in session["events"]]
    assert offs == [0.0, 5.0, 10.0]


def test_events_have_index():
    events = [make(), make(), make()]
    result = build_session_replay(events)
    session = result["sessions"][0]
    idx = [e["_event_index"] for e in session["events"]]
    assert idx == [1, 2, 3]


def test_events_sorted_by_timestamp():
    events = [
        make(timestamp="2025-06-10T10:00:10Z", username="c"),
        make(timestamp="2025-06-10T10:00:00Z", username="a"),
        make(timestamp="2025-06-10T10:00:05Z", username="b"),
    ]
    result = build_session_replay(events)
    e = result["sessions"][0]["events"]
    assert [x["username"] for x in e] == ["a", "b", "c"]


def test_credentials_summary():
    events = [
        make(username="root", auth_attempt=1),
        make(username="admin", auth_attempt=1),
        make(username="root", auth_attempt=1),
    ]
    result = build_session_replay(events)
    creds = result["sessions"][0]["summary"]["credentials"]
    assert set(creds["unique_usernames"]) == {"root", "admin"}
    assert creds["auth_attempt_total"] == 3


def test_commands_summary():
    events = [
        make(command_count=1, command="ls"),
        make(command_count=1, command="whoami"),
    ]
    result = build_session_replay(events)
    cmds = result["sessions"][0]["summary"]["commands"]
    assert cmds["command_count_total"] == 2
    assert set(cmds["sample_commands"]) == {"ls", "whoami"}


def test_brute_force_flag():
    events = [make(username=f"u{i}", auth_attempt=1) for i in range(10)]
    result = build_session_replay(events)
    flags = result["sessions"][0]["summary"]["flags"]
    assert flags["is_brute_force_candidate"] is True


def test_orphan_events():
    events = [
        make(),
        make(session_id=None),
        make(session_id=""),
    ]
    result = build_session_replay(events)
    assert result["summary"]["orphan_events"] == 2
    assert result["summary"]["total_sessions"] == 1


def test_multiple_sessions():
    events = [
        make(session_id="s-1"),
        make(session_id="s-2"),
    ]
    result = build_session_replay(events)
    assert len(result["sessions"]) == 2


def test_input_not_mutated():
    events = [make()]
    original = [dict(e) for e in events]
    build_session_replay(events)
    assert events == original
