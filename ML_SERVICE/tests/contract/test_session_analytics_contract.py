import json
from pathlib import Path

from app.analytics.session_analytics import (
    ALLOWED_CLUSTER_VALUES,
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
    return json.loads(
        CONTRACT_PATH.read_text(encoding="utf-8")
    )


def test_contract_exists_and_is_valid_json():
    contract = load_contract()

    assert contract["name"] == "SESSION_ANALYTICS_CONTRACT"
    assert contract["status"] == "ACTIVE"


def test_contract_fields_match_implementation():
    contract = load_contract()

    assert tuple(
        contract["required_input_fields"]
    ) == REQUIRED_FIELDS

    assert tuple(
        contract["optional_input_fields"]
    ) == OPTIONAL_FIELDS

    assert tuple(
        contract["output"]["fields"]
    ) == OUTPUT_FIELDS


def test_contract_assignment_boundary_is_immutable():
    boundary = load_contract()["assignment_boundary"]

    assert boundary["adapter_may_assign_clusters"] is False
    assert boundary["adapter_may_modify_assignments"] is False
    assert boundary["adapter_may_create_clusters"] is False
    assert boundary["adapter_may_retrain_model"] is False
    assert boundary["adapter_may_infer_from_ip_only"] is False


def test_contract_matches_9f_cluster_boundary():
    contract = load_contract()

    assert (
        set(contract["allowed_cluster_values"])
        == ALLOWED_CLUSTER_VALUES
    )

    assert (
        contract["output"]["one_output_row_per_input_session"]
        is True
    )

    assert (
        contract["null_rules"]["required_fields"]
        == "must_not_be_null"
    )
