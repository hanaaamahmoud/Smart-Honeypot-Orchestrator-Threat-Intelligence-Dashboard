"""Diagnostic script - shows current pipeline behavior on real ES sessions."""
import json
import urllib.request

from app.pipeline.input_adapter import adapt_input
from app.pipeline.session_reconstruction import reconstruct_sessions
from app.pipeline.feature_generation_base import generate_base_features
from app.pipeline.feature_generation_diversity import generate_diversity_features
from app.pipeline.feature_generation_temporal import generate_temporal_features
from app.pipeline.feature_generation_density import generate_density_features
from app.pipeline.feature_generation_geo import generate_geo_availability_features
from app.pipeline.feature_generation import assemble_48_features
from app.model_loader import load_frozen_model


def fetch_events(size=1000):
    url = f"http://elasticsearch:9200/honeypot-events/_search?size={size}"
    req = urllib.request.Request(url)
    data = json.loads(urllib.request.urlopen(req).read().decode())
    return [hit["_source"] for hit in data["hits"]["hits"]]


def main():
    print("=" * 70)
    print("LOADING FROZEN MODEL")
    print("=" * 70)
    model = load_frozen_model()
    print(f"Model loaded: {len(model.feature_names)} features, {len(model.centroids)} centroids\n")

    print("=" * 70)
    print("FETCHING EVENTS FROM ELASTICSEARCH")
    print("=" * 70)
    events = fetch_events(1000)
    print(f"Fetched {len(events)} raw events\n")

    print("=" * 70)
    print("RUNNING PIPELINE: normalize → reconstruct_sessions")
    print("=" * 70)
    normalized = adapt_input({"events": events})
    sessions = reconstruct_sessions(normalized)
    print(f"Built {len(sessions)} sessions\n")

    # Load scaler for comparison
    with open("/app/models/frozen_production_reference/standard_scaler_params.json") as f:
        scaler = json.load(f)

    print("=" * 70)
    print("PROCESSING FIRST 10 SESSIONS")
    print("=" * 70)

    cluster_counts = {}
    distances = []

    # Process all sessions (for stats) but print first 10
    for i, session in enumerate(sessions):
        feature_groups = {}
        feature_groups.update(generate_base_features(session))
        feature_groups.update(generate_diversity_features(session))
        feature_groups.update(generate_temporal_features(session))
        feature_groups.update(generate_density_features(session))
        feature_groups.update(generate_geo_availability_features(session))

        features = assemble_48_features(feature_groups)
        scaled = model.scale_features(features)
        cluster, distance = model.nearest_centroid(scaled)

        cluster_counts[cluster] = cluster_counts.get(cluster, 0) + 1
        distances.append(distance)

        if i < 10:
            print(f"\n--- Session {i+1}: {session['session_id']} ---")
            print(f"  event_count: {session['event_count']}")
            print(f"  protocol: {session['events'][0].get('protocol')}")
            print(f"  honeypot: {session['events'][0].get('honeypot')}")
            print(f"  → CLUSTER: {cluster}, DISTANCE: {distance:.4f}")
            print(f"\n  KEY FEATURES (actual vs training_mean):")
            key_features = [
                "event_count",
                "session_duration_seconds",
                "unique_destinations",
                "unique_countries",
                "unique_cities",
                "inter_event_gap_min",
                "geo_location_available",
                "ip_reputation_available",
                "ip_reputation_missing_count",
                "session_duration_log1p",
                "events_per_second",
                "event_density",
                "auth_attempt_total",
                "command_count_total",
            ]
            for name in key_features:
                actual = features[name]
                train_mean = scaler["mean"][name]
                train_scale = scaler["scale"][name]
                if train_scale != 0:
                    scaled_val = (actual - train_mean) / train_scale
                else:
                    scaled_val = 0.0
                print(f"    {name:35s}: {actual:12.4f}  (train_mean={train_mean:.4f}, scaled={scaled_val:+.3f})")

    print("\n" + "=" * 70)
    print("SUMMARY STATISTICS")
    print("=" * 70)
    print(f"Total sessions: {len(sessions)}")
    print(f"\nCluster distribution:")
    for cid in sorted(cluster_counts.keys()):
        print(f"  Cluster {cid:2d}: {cluster_counts[cid]:5d} sessions")

    print(f"\nDistance statistics:")
    distances.sort()
    print(f"  min:    {distances[0]:.4f}")
    print(f"  median: {distances[len(distances)//2]:.4f}")
    print(f"  p95:    {distances[int(len(distances)*0.95)]:.4f}")
    print(f"  max:    {distances[-1]:.4f}")
    print(f"  mean:   {sum(distances)/len(distances):.4f}")

    print(f"\nTraining reference (for comparison):")
    print(f"  min:    0.0002")
    print(f"  median: 0.2432")
    print(f"  p95:    7.154")
    print(f"  max:    200.07")
    print(f"  mean:   1.457")


if __name__ == "__main__":
    main()
