import pytest

from app.pipeline.canonical_adapter import canonicalize_event


REQUIRED_FIELDS = {
    "timestamp": "2026-08-05T05:58:01.983Z",
    "honeypot": "dionaea",
    "protocol": "ftpd",
    "source_ip": "172.22.0.1",
}


def test_required_fields_are_preserved():
    event = {
        **REQUIRED_FIELDS,
        "source_port": 39856,
        "destination_ip": "172.22.0.2",
        "destination_port": 21,
    }

    result = canonicalize_event(event)
    data = result.model_dump()

    assert data["timestamp"] == REQUIRED_FIELDS["timestamp"]
    assert data["honeypot"] == "dionaea"
    assert data["protocol"] == "ftpd"
    assert data["source_ip"] == "172.22.0.1"


def test_missing_optional_fields_become_none():
    result = canonicalize_event(REQUIRED_FIELDS)
    data = result.model_dump()

    optional_fields = [
        "source_port",
        "destination_ip",
        "destination_port",
        "session_id",
        "username",
        "password",
        "user_attempt",
        "pass_attempt",
        "auth_attempt",
        "anonymous",
        "command_count",
        "country",
        "country_code",
        "asn",
        "ip_reputation",
        "attack_type",
        "mitre_technique",
        "attack_stage",
        "severity",
        "source_dataset",
    ]

    for field in optional_fields:
        assert data[field] is None, field


@pytest.mark.parametrize(
    "field,value,expected",
    [
        ("source_port", "39856", 39856),
        ("source_port", 39856.0, 39856),
        ("destination_port", "21", 21),
        ("destination_port", 21.0, 21),
        ("asn", "64500", 64500),
        ("user_attempt", "3", 3),
        ("pass_attempt", 2.0, 2),
        ("auth_attempt", "4", 4),
        ("anonymous", "1", 1),
        ("command_count", 7.0, 7),
    ],
)
def test_integer_normalization(field, value, expected):
    event = {
        **REQUIRED_FIELDS,
        field: value,
    }

    result = canonicalize_event(event)

    assert result.model_dump()[field] == expected
    assert isinstance(result.model_dump()[field], int)


@pytest.mark.parametrize(
    "field,value",
    [
        ("source_port", "not-an-int"),
        ("destination_port", "21.5"),
        ("asn", "abc"),
        ("user_attempt", "1.5"),
        ("command_count", object()),
    ],
)
def test_invalid_integer_raises_error(field, value):
    event = {
        **REQUIRED_FIELDS,
        field: value,
    }

    with pytest.raises((TypeError, ValueError)):
        canonicalize_event(event)


def test_no_fabricated_values():
    result = canonicalize_event(REQUIRED_FIELDS)
    data = result.model_dump()

    # No defaults such as 0, "", "unknown", etc.
    assert data["source_port"] is None
    assert data["destination_ip"] is None
    assert data["destination_port"] is None
    assert data["session_id"] is None
    assert data["username"] is None
    assert data["password"] is None
    assert data["user_attempt"] is None
    assert data["pass_attempt"] is None
    assert data["auth_attempt"] is None
    assert data["anonymous"] is None
    assert data["command_count"] is None
    assert data["country"] is None
    assert data["country_code"] is None
    assert data["asn"] is None
    assert data["ip_reputation"] is None
    assert data["attack_type"] is None
    assert data["mitre_technique"] is None
    assert data["attack_stage"] is None
    assert data["severity"] is None
    assert data["source_dataset"] is None


def test_exactly_24_fields():
    result = canonicalize_event(REQUIRED_FIELDS)
    data = result.model_dump()

    assert len(data) == 24

    expected_fields = {
        "timestamp",
        "honeypot",
        "protocol",
        "source_ip",
        "source_port",
        "destination_ip",
        "destination_port",
        "session_id",
        "username",
        "password",
        "user_attempt",
        "pass_attempt",
        "auth_attempt",
        "anonymous",
        "command_count",
        "country",
        "country_code",
        "asn",
        "ip_reputation",
        "attack_type",
        "mitre_technique",
        "attack_stage",
        "severity",
        "source_dataset",
    }

    assert set(data.keys()) == expected_fields
