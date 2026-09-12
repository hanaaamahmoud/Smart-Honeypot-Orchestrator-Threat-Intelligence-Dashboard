import json

from app.schemas import AnalyticsResult


def test_analytics_result_contract_preserves_values():
    result = AnalyticsResult(
        cluster_id=12,
        session_count=20,
        event_count=340,
        top_commands=["whoami", "ls"],
        attack_types=["brute_force"],
        mitre_techniques=["T1110"],
    )

    assert result.cluster_id == 12
    assert result.session_count == 20
    assert result.event_count == 340
    assert result.top_commands == ["whoami", "ls"]
    assert result.attack_types == ["brute_force"]
    assert result.mitre_techniques == ["T1110"]


def test_analytics_result_field_types():
    result = AnalyticsResult(
        cluster_id=12,
        session_count=20,
        event_count=340,
        top_commands=[],
        attack_types=[],
        mitre_techniques=[],
    )

    assert isinstance(result.cluster_id, int)
    assert isinstance(result.session_count, int)
    assert isinstance(result.event_count, int)
    assert isinstance(result.top_commands, list)
    assert isinstance(result.attack_types, list)
    assert isinstance(result.mitre_techniques, list)


def test_analytics_result_defaults_to_empty_lists():
    result = AnalyticsResult(
        cluster_id=12,
    )

    assert result.top_commands == []
    assert result.attack_types == []
    assert result.mitre_techniques == []


def test_analytics_result_preserves_cluster_id():
    result = AnalyticsResult(
        cluster_id=12,
        session_count=20,
        event_count=340,
    )

    assert result.cluster_id == 12


def test_analytics_result_requires_cluster_id():
    try:
        AnalyticsResult()
        assert False, "cluster_id should be required"
    except Exception:
        pass


def test_analytics_result_defaults_counts_to_zero():
    result = AnalyticsResult(
        cluster_id=12,
    )

    assert result.session_count == 0
    assert result.event_count == 0


def test_analytics_result_serializes_to_json():
    result = AnalyticsResult(
        cluster_id=12,
        session_count=20,
        event_count=340,
        top_commands=[],
        attack_types=[],
        mitre_techniques=[],
    )

    payload = json.loads(result.model_dump_json())

    assert payload["cluster_id"] == 12
    assert payload["session_count"] == 20
    assert payload["event_count"] == 340
    assert payload["top_commands"] == []
    assert payload["attack_types"] == []
    assert payload["mitre_techniques"] == []
