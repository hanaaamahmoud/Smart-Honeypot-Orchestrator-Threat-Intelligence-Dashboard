"""Contract tests for session_replay."""

import json
from pathlib import Path

from app.analytics.session_replay import ANALYTICS_LAYER


CONTRACT_PATH = (
    Path(__file__).parents[2]
    / "app"
    / "analytics"
    / "contracts"
    / "session_replay_contract.json"
)


def load_contract():
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def test_contract_exists_and_active():
    c = load_contract()
    assert c["contract_name"] == "SESSION_REPLAY"
    assert c["status"] == "ACTIVE"
    assert c["version"] == "2.0.0"


def test_grain():
    c = load_contract()
    assert c["grain"] == "SESSION"


def test_required_input_fields():
    c = load_contract()
    assert c["input"]["required_fields"] == [
        "timestamp",
        "honeypot",
        "protocol",
        "source_dataset",
        "source_ip",
    ]


def test_session_grouping_field():
    c = load_contract()
    assert c["input"]["session_grouping_field"] == "session_id"


def test_required_output_fields():
    c = load_contract()
    assert c["output"]["required_fields"] == [
        "reconstructed_session_id",
        "event_count",
        "first_event_utc",
        "last_event_utc",
        "session_duration_seconds",
        "events",
    ]


def test_no_fabrication():
    c = load_contract()
    assert c["replay_rules"]["fabricated_data"] is False
    assert "fabricated" in c["null_rules"]["session_id"]["behavior"].lower()


def test_analytics_layer_value():
    assert ANALYTICS_LAYER == "SESSION_REPLAY"
