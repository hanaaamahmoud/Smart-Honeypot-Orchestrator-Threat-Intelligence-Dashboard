import os

from app.pipeline.input_adapter import adapt_input
from app.pipeline.canonical_adapter import canonicalize_events
from app.pipeline.session_reconstruction import reconstruct_sessions

from app.pipeline.feature_generation_base import generate_base_features
from app.pipeline.feature_generation_diversity import generate_diversity_features
from app.pipeline.feature_generation_temporal import generate_temporal_features
from app.pipeline.feature_generation_density import generate_density_features
from app.pipeline.feature_generation_geo import generate_geo_availability_features
from app.pipeline.feature_generation import assemble_48_features

from app.model_loader import load_frozen_model


def _fetch_real_elk_events(limit=100):
    from elasticsearch import Elasticsearch

    url = os.getenv(
        "ELASTICSEARCH_URL",
        "http://elasticsearch:9200",
    )
    index = os.getenv(
        "ELASTICSEARCH_INDEX",
        "honeypot-events",
    )

    client = Elasticsearch(url)

    response = client.search(
        index=index,
        size=limit,
        query={
            "match_all": {}
        },
        sort=[
            {
                "timestamp": {
                    "order": "asc"
                }
            }
        ],
    )

    return [
        hit["_source"]
        for hit in response["hits"]["hits"]
    ]


def test_l210_real_elk_canonical_to_frozen_pipeline():
    raw_events = _fetch_real_elk_events(limit=100)

    assert raw_events, "Real ELK returned no events."

    # L2.1-L2.3 existing normalization path
    normalized_events = adapt_input(
        {
            "events": raw_events
        }
    )

    assert normalized_events
    assert all(
        isinstance(event, dict)
        for event in normalized_events
    )

    # L2.4 canonical contract
    canonical_events = canonicalize_events(
        normalized_events
    )

    assert canonical_events
    assert len(canonical_events) == len(normalized_events)

    # Canonical contract must remain stable.
    for event in canonical_events:
        assert len(event.model_dump()) == 24

    # Session reconstruction must still work.
    #
    # IMPORTANT:
    # canonicalization does not fabricate session IDs.
    # We therefore reconstruct from the normalized events,
    # preserving the existing session semantics.
    sessions = reconstruct_sessions(
        normalized_events
    )

    assert sessions

    frozen_model = load_frozen_model()

    processed_sessions = 0

    for session in sessions:
        feature_groups = {}

        feature_groups.update(
            generate_base_features(session)
        )
        feature_groups.update(
            generate_diversity_features(session)
        )
        feature_groups.update(
            generate_temporal_features(session)
        )
        feature_groups.update(
            generate_density_features(session)
        )
        feature_groups.update(
            generate_geo_availability_features(session)
        )

        feature_vector = assemble_48_features(
            feature_groups
        )

        # Exact frozen feature contract.
        assert len(feature_vector) == 48
        assert list(feature_vector.keys()) == list(
            frozen_model.feature_names
        )

        # Frozen scaler must accept the vector.
        scaled_features = frozen_model.scale_features(
            feature_vector
        )

        assert len(scaled_features) == 48

        # Production assignment must use an existing
        # frozen centroid only.
        cluster_id, distance = (
            frozen_model.nearest_centroid(
                scaled_features
            )
        )

        assert isinstance(cluster_id, int)
        assert cluster_id in {
            int(centroid["dbscan_cluster"])
            for centroid in frozen_model.centroids
        }

        assert distance >= 0.0

        processed_sessions += 1

    assert processed_sessions == len(sessions)
