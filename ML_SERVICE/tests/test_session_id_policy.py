import pytest

from app.pipeline.session_id_policy import get_session_id


def test_existing_session_id_is_preserved():
    event = {
        "session_id": "session-001",
        "timestamp": "2026-01-01T10:00:00Z",
    }

    assert get_session_id(event) == "session-001"


def test_missing_session_id_returns_none():
    event = {
        "timestamp": "2026-01-01T10:00:00Z",
    }

    assert get_session_id(event) is None


def test_none_session_id_returns_none():
    event = {
        "session_id": None,
    }

    assert get_session_id(event) is None


def test_empty_session_id_returns_none():
    event = {
        "session_id": "",
    }

    assert get_session_id(event) is None


def test_whitespace_session_id_returns_none():
    event = {
        "session_id": "   ",
    }

    assert get_session_id(event) is None


def test_session_id_is_not_modified():
    event = {
        "session_id": "  session-001  ",
    }

    result = get_session_id(event)

    assert result == "session-001"
    assert event["session_id"] == "  session-001  "


def test_non_string_session_id_is_rejected():
    event = {
        "session_id": 12345,
    }

    with pytest.raises(TypeError):
        get_session_id(event)
