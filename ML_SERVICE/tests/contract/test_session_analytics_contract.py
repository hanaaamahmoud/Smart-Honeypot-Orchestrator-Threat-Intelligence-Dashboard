"""Contract tests for session_analytics."""

import json
from pathlib import Path

from app.analytics.session_analytics import (
    ALLOWED_ASSIGNMENT_STATUS,
    NOISE_CLUSTER_ID,
    OPTIONAL_FIELDS,
    OUTPUT_FIELDS,
    REQUIRED_FIELDS,
)


CONTRACT_PATH = (
    Path(__file__).parents[2]
    / "app"
    / "analytics"
    / "contracts"
    / "session_analytics_contract.json"
)


def load_contract():
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def test_contract_exists_and_is_valid_json():
    contract = load_contract()
    assert contract["name"] == "SESSION_ANALYTICS_CONTRACT"
    assert contract["status"] == "ACTIVE"
    assert contract["version"] == "2.0.0"


def test_required_fields_match():
    contract = load_contract()
    assert tuple(contract["required_input_fields"]) == REQUIRED_FIELDS


def test_optional_fields_match():
    contract = load_contract()
    assert tuple(contract["optional_input_fields"]) == OPTIONAL_FIELDS


def test_output_required_fields_match():
    contract = load_contract()
    assert tuple(contract["output"]["required_fields"]) == REQUIRED_FIELDS


def test_output_optional_fields_match():
    contract = load_contract()
    assert tuple(contract["output"]["optional_fields"]) == OPTIONAL_FIELDS


def test_allowed_assignment_status_match():
    contract = load_contract()
    assert set(contract["allowed_assignment_status_values"]) == ALLOWED_ASSIGNMENT_STATUS


def test_noise_cluster_id_match():
    contract = load_contract()
    assert contract["production_cluster_semantics"]["noise_cluster_id"] == NOISE_CLUSTER_ID


def test_cluster_is_integer():
    contract = load_contract()
    assert contract["production_cluster_semantics"]["cluster_id_type"] == "integer"


def test_one_output_row_per_input_session():
    contract = load_contract()
    assert contract["output"]["one_output_row_per_input_session"] is True


def test_null_rules():
    contract = load_contract()
    assert contract["null_rules"]["required_fields"] == "must_not_be_null_or_empty"
    assert contract["null_rules"]["optional_fields_are_not_fabricated"] is True
