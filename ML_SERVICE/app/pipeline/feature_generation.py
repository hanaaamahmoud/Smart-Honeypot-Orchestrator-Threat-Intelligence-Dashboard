"""
D4.3 — Exact 48-Feature Assembly + Validation

The production feature order must remain identical
to the frozen Step 7 contract.

The assembled feature vector is validated before
being returned to the ML pipeline.
"""

from typing import Any, Dict, List

from app.pipeline.feature_validation import validate_48_features


FROZEN_FEATURE_ORDER: List[str] = [
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
]


def assemble_48_features(
    feature_groups: Dict[str, Any],
) -> Dict[str, float]:
    """
    Assemble and validate the frozen 48-feature vector.

    This function:
    - requires exactly the frozen feature names
    - preserves the frozen order
    - rejects missing features
    - rejects unexpected features
    - converts values to float
    - validates numeric and finite values
    - validates the exact feature order
    - does not calculate feature values
    """

    if not isinstance(feature_groups, dict):
        raise TypeError("feature_groups must be a dictionary")

    expected = set(FROZEN_FEATURE_ORDER)
    actual = set(feature_groups.keys())

    missing = expected - actual
    unexpected = actual - expected

    if missing:
        raise ValueError(
            f"Missing features: {sorted(missing)}"
        )

    if unexpected:
        raise ValueError(
            f"Unexpected features: {sorted(unexpected)}"
        )

    feature_vector = {
        feature_name: float(feature_groups[feature_name])
        for feature_name in FROZEN_FEATURE_ORDER
    }

    validate_48_features(
        feature_vector,
        FROZEN_FEATURE_ORDER,
    )

    return feature_vector
