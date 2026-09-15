"""
L2.8 — 48 Feature Dependency Map

Documents the dependency of every production feature on the
canonical 24-field event contract.

This file is documentation/validation metadata only.
It does not calculate features and does not change the ML pipeline.
"""

FEATURE_DEPENDENCIES = {
    "event_count": {
        "canonical_fields": set(),
        "source": "session event collection",
    },
    "session_duration_seconds": {
        "canonical_fields": {"timestamp"},
        "source": "session event timestamps",
    },
    "auth_attempt_total": {
        "canonical_fields": {
            "auth_attempt",
            "user_attempt",
            "pass_attempt",
            "username",
            "password",
        },
        "source": "existing base feature logic",
    },
    "user_attempt_total": {
        "canonical_fields": {
            "user_attempt",
            "username",
        },
        "source": "existing base feature logic",
    },
    "pass_attempt_total": {
        "canonical_fields": {
            "pass_attempt",
            "password",
        },
        "source": "existing base feature logic",
    },
    "command_count_total": {
        "canonical_fields": {
            "command_count",
        },
        "source": "existing base feature logic",
    },
    "anonymous_event_count": {
        "canonical_fields": {
            "anonymous",
        },
        "source": "existing base feature logic",
    },
    "unique_destinations": {
        "canonical_fields": {"destination_ip"},
        "source": "existing diversity feature logic",
    },
    "unique_destination_ports": {
        "canonical_fields": {"destination_port"},
        "source": "existing diversity feature logic",
    },
    "unique_source_ips": {
        "canonical_fields": {"source_ip"},
        "source": "existing diversity feature logic",
    },
    "unique_protocols": {
        "canonical_fields": {"protocol"},
        "source": "existing diversity feature logic",
    },
    "unique_honeypots": {
        "canonical_fields": {"honeypot"},
        "source": "existing diversity feature logic",
    },
    "unique_usernames": {
        "canonical_fields": {"username"},
        "source": "existing diversity feature logic",
    },
    "unique_countries": {
        "canonical_fields": {"country"},
        "source": "existing diversity feature logic",
    },
    "unique_country_codes": {
        "canonical_fields": {"country_code"},
        "source": "existing diversity feature logic",
    },
    "unique_cities": {
        "canonical_fields": set(),
        "source": "legacy normalized field; city is not part of CanonicalEvent",
    },
    "latitude_mean": {
        "canonical_fields": set(),
        "source": "legacy normalized field; latitude is not part of CanonicalEvent",
    },
    "longitude_mean": {
        "canonical_fields": set(),
        "source": "legacy normalized field; longitude is not part of CanonicalEvent",
    },
    "inter_event_gap_mean": {
        "canonical_fields": {"timestamp"},
        "source": "session event timestamps",
    },
    "inter_event_gap_min": {
        "canonical_fields": {"timestamp"},
        "source": "session event timestamps",
    },
    "inter_event_gap_max": {
        "canonical_fields": {"timestamp"},
        "source": "session event timestamps",
    },
    "session_duration_recomputed_seconds": {
        "canonical_fields": {"timestamp"},
        "source": "session event timestamps",
    },
    "events_per_second": {
        "canonical_fields": {"timestamp"},
        "source": "event count + session timestamps",
    },
    "auth_attempt_rate": {
        "canonical_fields": {
            "auth_attempt",
            "user_attempt",
            "pass_attempt",
            "username",
            "password",
            "timestamp",
        },
        "source": "existing auth logic + temporal duration",
    },
    "command_rate": {
        "canonical_fields": {
            "command_count",
            "timestamp",
        },
        "source": "existing command logic + temporal duration",
    },
    "session_duration_log1p": {
        "canonical_fields": {"timestamp"},
        "source": "derived from session duration",
    },
    "event_count_log1p": {
        "canonical_fields": set(),
        "source": "derived from event count",
    },
    "inter_event_gap_mean_log1p": {
        "canonical_fields": {"timestamp"},
        "source": "derived from inter-event gaps",
    },
    "inter_event_gap_max_log1p": {
        "canonical_fields": {"timestamp"},
        "source": "derived from inter-event gaps",
    },
    "event_density": {
        "canonical_fields": {"timestamp"},
        "source": "event count + session duration",
    },
    "command_density": {
        "canonical_fields": {
            "command_count",
            "timestamp",
        },
        "source": "command count + session duration",
    },
    "auth_attempt_density": {
        "canonical_fields": {
            "auth_attempt",
            "user_attempt",
            "pass_attempt",
            "username",
            "password",
            "timestamp",
        },
        "source": "auth count + session duration",
    },
    "credential_attempt_density": {
        "canonical_fields": {
            "user_attempt",
            "pass_attempt",
            "username",
            "password",
        },
        "source": "existing credential logic",
    },
    "destination_diversity": {
        "canonical_fields": {"destination_ip"},
        "source": "existing diversity feature logic",
    },
    "destination_port_diversity": {
        "canonical_fields": {"destination_port"},
        "source": "existing diversity feature logic",
    },
    "protocol_diversity": {
        "canonical_fields": {"protocol"},
        "source": "existing diversity feature logic",
    },
    "honeypot_diversity": {
        "canonical_fields": {"honeypot"},
        "source": "existing diversity feature logic",
    },
    "username_diversity": {
        "canonical_fields": {"username"},
        "source": "existing diversity feature logic",
    },
    "geo_country_diversity": {
        "canonical_fields": {"country", "country_code"},
        "source": "existing diversity feature logic",
    },
    "geo_city_diversity": {
        "canonical_fields": set(),
        "source": "legacy normalized field; city is not part of CanonicalEvent",
    },
    "geo_latitude_abs": {
        "canonical_fields": set(),
        "source": "legacy normalized field; latitude is not part of CanonicalEvent",
    },
    "geo_longitude_abs": {
        "canonical_fields": set(),
        "source": "legacy normalized field; longitude is not part of CanonicalEvent",
    },
    "session_start_hour": {
        "canonical_fields": {"timestamp"},
        "source": "session start timestamp",
    },
    "session_start_dayofweek": {
        "canonical_fields": {"timestamp"},
        "source": "session start timestamp",
    },
    "session_start_dayofmonth": {
        "canonical_fields": {"timestamp"},
        "source": "session start timestamp",
    },
    "geo_location_available": {
        "canonical_fields": set(),
        "source": "legacy normalized latitude/longitude fields",
    },
    "ip_reputation_available": {
        "canonical_fields": {"ip_reputation"},
        "source": "existing geo availability logic",
    },
    "ip_reputation_missing_count": {
        "canonical_fields": {"ip_reputation"},
        "source": "existing geo availability logic",
    },
}


FEATURE_ORDER = (
    "event_count",
    "session_duration_seconds",
    "auth_attempt_total",
    "user_attempt_total",
    "pass_attempt_total",
    "command_count_total",
    "anonymous_event_count",
    "unique_destinations",
    "unique_destination_ports",
    "unique_source_ips",
    "unique_protocols",
    "unique_honeypots",
    "unique_usernames",
    "unique_countries",
    "unique_country_codes",
    "unique_cities",
    "latitude_mean",
    "longitude_mean",
    "inter_event_gap_mean",
    "inter_event_gap_min",
    "inter_event_gap_max",
    "session_duration_recomputed_seconds",
    "events_per_second",
    "auth_attempt_rate",
    "command_rate",
    "session_duration_log1p",
    "event_count_log1p",
    "inter_event_gap_mean_log1p",
    "inter_event_gap_max_log1p",
    "event_density",
    "command_density",
    "auth_attempt_density",
    "credential_attempt_density",
    "destination_diversity",
    "destination_port_diversity",
    "protocol_diversity",
    "honeypot_diversity",
    "username_diversity",
    "geo_country_diversity",
    "geo_city_diversity",
    "geo_latitude_abs",
    "geo_longitude_abs",
    "session_start_hour",
    "session_start_dayofweek",
    "session_start_dayofmonth",
    "geo_location_available",
    "ip_reputation_available",
    "ip_reputation_missing_count",
)


def validate_feature_dependency_map():
    if len(FEATURE_ORDER) != 48:
        raise AssertionError(
            f"Expected 48 features, got {len(FEATURE_ORDER)}"
        )

    if set(FEATURE_ORDER) != set(FEATURE_DEPENDENCIES):
        missing = set(FEATURE_ORDER) - set(FEATURE_DEPENDENCIES)
        extra = set(FEATURE_DEPENDENCIES) - set(FEATURE_ORDER)
        raise AssertionError(
            f"Dependency map mismatch: missing={missing}, extra={extra}"
        )

    return True


__all__ = [
    "FEATURE_DEPENDENCIES",
    "FEATURE_ORDER",
    "validate_feature_dependency_map",
]
