import json
from pathlib import Path


CONTRACT_PATH = (
    Path(__file__).resolve().parents[2]
    / "analytics"
    / "contracts"
    / "session_replay_contract.json"
)


def load_contract():
    with CONTRACT_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def test_session_replay_contract_exists():
    assert CONTRACT_PATH.exists()


def test_session_replay_contract_is_deferred():
    contract = load_contract()

    assert contract["contract_name"] == "SESSION_REPLAY"
    assert contract["status"] == "DEFERRED"
    assert contract["availability"]["status"] == "DEFERRED"


def test_required_input_fields():
    contract = load_contract()

    assert contract["input"]["required_fields"] == [
        "timestamp",
        "honeypot",
        "protocol",
        "source_dataset",
        "source_ip",
    ]


def test_session_grouping_field():
    contract = load_contract()

    assert contract["input"]["session_grouping_field"] == "session_id"


def test_required_output_fields():
    contract = load_contract()

    assert contract["output"]["required_fields"] == [
        "reconstructed_session_id",
        "event_count",
        "first_event_utc",
        "last_event_utc",
        "session_duration_seconds",
        "events",
    ]


def test_no_fabricated_session_ids():
    contract = load_contract()

    assert (
        "fabricated session identifier"
        in contract["null_rules"]["session_id"]["behavior"]
    )


def test_replay_is_independent_of_ml_processing():
    contract = load_contract()

    rules = contract["independence_rules"]

    assert "SESSION_REPLAY must not generate ML features." in rules
    assert "SESSION_REPLAY must not perform feature scaling." in rules
    assert "SESSION_REPLAY must not perform clustering." in rules
