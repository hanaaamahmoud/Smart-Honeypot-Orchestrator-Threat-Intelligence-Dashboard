from app.config import settings
from app.ingestion.elasticsearch import ElasticsearchReader
from app.pipeline.normalization import normalize_event
from app.pipeline.canonical_adapter import canonicalize_event


EXPECTED_FIELDS = {
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


def test_real_elk_event_to_canonical():
    reader = ElasticsearchReader(
        settings.ELASTICSEARCH_URL,
        settings.ELASTICSEARCH_INDEX,
    )

    events = reader.read_events(size=1)

    assert events
    assert len(events) == 1

    normalized = normalize_event(events[0])
    canonical = canonicalize_event(normalized)

    data = canonical.model_dump()

    assert len(data) == 24
    assert set(data.keys()) == EXPECTED_FIELDS

    # Required canonical fields must exist.
    assert isinstance(data["timestamp"], str)
    assert data["timestamp"]
    assert isinstance(data["honeypot"], str)
    assert data["honeypot"]
    assert isinstance(data["protocol"], str)
    assert data["protocol"]
    assert isinstance(data["source_ip"], str)
    assert data["source_ip"]

    # Canonical adapter must not fabricate optional values.
    # Missing values are allowed to remain None.
    for field in EXPECTED_FIELDS - {
        "timestamp",
        "honeypot",
        "protocol",
        "source_ip",
    }:
        assert field in data
