from app.config import settings
from app.ingestion.elasticsearch import ElasticsearchReader
from app.pipeline.normalization import normalize_event
from app.pipeline.session_reconstruction import reconstruct_sessions
from app.pipeline.feature_generation import assemble_48_features

from app.pipeline.feature_generation_base import generate_base_features
from app.pipeline.feature_generation_diversity import generate_diversity_features
from app.pipeline.feature_generation_temporal import generate_temporal_features
from app.pipeline.feature_generation_density import generate_density_features
from app.pipeline.feature_generation_geo import generate_geo_availability_features


EXPECTED_FEATURES = (
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


def test_real_elk_existing_48_feature_pipeline_compatibility():
    reader = ElasticsearchReader(
        settings.ELASTICSEARCH_URL,
        settings.ELASTICSEARCH_INDEX,
    )

    raw_events = reader.read_events(size=100)
    assert raw_events

    normalized_events = [
        normalize_event(event)
        for event in raw_events
    ]

    sessions = reconstruct_sessions(normalized_events)

    assert sessions

    all_features = []

    for session in sessions:
        base = generate_base_features(session)
        diversity = generate_diversity_features(session)
        temporal = generate_temporal_features(session)
        density = generate_density_features(
            base,
            temporal,
        )
        geo = generate_geo_availability_features(session)

        features = {
            **base,
            **diversity,
            **temporal,
            **density,
            **geo,
        }

        assembled = assemble_48_features(features)
        all_features.append(assembled)

    assert all_features

    for feature_vector in all_features:
        assert len(feature_vector) == 48
        assert list(feature_vector.keys()) == list(EXPECTED_FEATURES)

        for name, value in feature_vector.items():
            assert name in EXPECTED_FEATURES
            assert isinstance(value, (int, float))
            assert value == value  # NaN check
