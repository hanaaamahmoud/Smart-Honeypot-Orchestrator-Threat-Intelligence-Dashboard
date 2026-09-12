from app.pipeline.feature_contract import (
    FROZEN_FEATURE_NAMES,
)


def test_exactly_48_features():
    assert len(FROZEN_FEATURE_NAMES) == 48


def test_feature_names_are_unique():
    assert len(FROZEN_FEATURE_NAMES) == len(
        set(FROZEN_FEATURE_NAMES)
    )


def test_frozen_feature_order():
    expected = [
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

    assert FROZEN_FEATURE_NAMES == expected
