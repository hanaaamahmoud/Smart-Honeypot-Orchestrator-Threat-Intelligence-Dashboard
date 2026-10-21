"""
Canonical Event field mapping.

L2.3-A
------
Maps the 24-field CanonicalEvent contract to the corresponding
Elasticsearch _source field names.

Important:
- No defaults are introduced here.
- No type conversion is performed here.
- No normalization is performed here.
- No ML processing is performed here.
- Missing/null handling belongs to the later L2.4 stage.
"""

from typing import Dict


CANONICAL_FIELD_MAPPING: Dict[str, str] = {
    "timestamp": "timestamp",
    "honeypot": "honeypot",
    "protocol": "protocol",
    "source_ip": "source_ip",
    "source_port": "source_port",
    "destination_ip": "destination_ip",
    "destination_port": "destination_port",
    "session_id": "session_id",
    "username": "username",
    "password": "password",
    "user_attempt": "user_attempt",
    "pass_attempt": "pass_attempt",
    "auth_attempt": "auth_attempt",
    "anonymous": "anonymous",
    "command_count": "command_count",
    "country": "country",
    "country_code": "country_code",
    "asn": "asn",
    "ip_reputation": "ip_reputation",
    "attack_type": "attack_type",
    "mitre_technique": "mitre_technique",
    "attack_stage": "attack_stage",
    "severity": "severity",
    "source_dataset": "source_dataset",
}


CANONICAL_FIELDS = tuple(CANONICAL_FIELD_MAPPING.keys())


def get_canonical_source_field(canonical_field: str) -> str:
    """
    Return the Elasticsearch _source field corresponding
    to a canonical field.
    """
    try:
        return CANONICAL_FIELD_MAPPING[canonical_field]
    except KeyError as exc:
        raise KeyError(
            f"Unknown canonical field: {canonical_field}"
        ) from exc
