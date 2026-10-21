import json
from pathlib import Path


CONTRACT_PATH = (
    Path(__file__).resolve().parents[2]
    / "app"
    / "analytics"
    / "contracts"
    / "temporal_analytics_contract.json"
)


EXPECTED_FIELDS = {
    "trend_date",
    "session_count",
    "total_events",
    "avg_session_duration_seconds",
    "event_count",
    "unique_sessions",
    "trend_type",
}


def load_contract():
    with CONTRACT_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def test_contract_file_exists():
    assert CONTRACT_PATH.exists()


def test_contract_name():
    contract = load_contract()

    assert contract["contract_name"] == "TEMPORAL_ANALYTICS"


def test_contract_grain():
    contract = load_contract()

    assert (
        contract["grain"]
        == "One row per daily temporal trend date."
    )


def test_contract_is_daily():
    contract = load_contract()

    assert contract["trend_type"] == "DAILY"


def test_contract_contains_all_required_fields():
    contract = load_contract()

    fields = set(contract["required_fields"].keys())

    assert fields == EXPECTED_FIELDS


def test_all_fields_are_required():
    contract = load_contract()

    for field in EXPECTED_FIELDS:
        assert contract["required_fields"][field]["required"] is True


def test_nulls_are_not_allowed():
    contract = load_contract()

    assert contract["null_policy"]["allowed"] is False


def test_daily_is_only_allowed_trend_type():
    contract = load_contract()

    assert contract["required_fields"]["trend_type"][
        "allowed_values"
    ] == ["DAILY"]


def test_formula_policy_does_not_invent_formulas():
    contract = load_contract()

    assert contract["formula_policy"]["documented"] is False


def test_mitre_is_not_a_temporal_dimension():
    contract = load_contract()

    assert contract["mitre_dimension"]["present"] is False
