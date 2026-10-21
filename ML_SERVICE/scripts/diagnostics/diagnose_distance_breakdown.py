"""Forensic: what features cause the ~33 distance?"""
import json
import random
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


def fetch_all():
    url = "http://elasticsearch:9200/honeypot-events/_search?scroll=2m"
    body = {"size": 5000, "query": {"match_all": {}}}
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                  headers={"Content-Type": "application/json"})
    data = json.loads(urllib.request.urlopen(req).read().decode())
    scroll_id = data["_scroll_id"]
    events = [h["_source"] for h in data["hits"]["hits"]]
    while True:
        req = urllib.request.Request(
            "http://elasticsearch:9200/_search/scroll",
            data=json.dumps({"scroll": "2m", "scroll_id": scroll_id}).encode(),
            headers={"Content-Type": "application/json"})
        data = json.loads(urllib.request.urlopen(req).read().decode())
        hits = data["hits"]["hits"]
        if not hits: break
        events.extend(h["_source"] for h in hits)
    return events


def main():
    model = load_frozen_model()
    print("[1/2] Fetching events...")
    events = fetch_all()
    random.seed(42)
    sample = random.sample(events, 5000)

    print("[2/2] Running pipeline...")
    sessions = reconstruct_sessions(adapt_input({"events": sample}))
    print(f"  {len(sessions)} sessions\n")

    # Collect all feature diffs from cluster 37 sessions
    cluster37_diffs = {}  # feature_name -> list of abs(scaled - centroid)
    sample_count = 0

    for session in sessions:
        fg = {}
        fg.update(generate_base_features(session))
        fg.update(generate_diversity_features(session))
        fg.update(generate_temporal_features(session))
        fg.update(generate_density_features(session))
        fg.update(generate_geo_availability_features(session))
        features = assemble_48_features(fg)
        scaled = model.scale_features(features)
        cluster, distance = model.nearest_centroid(scaled)

        if cluster == 37 and sample_count < 200:
            # Find cluster 37 centroid
            for c in model.centroids:
                if c["dbscan_cluster"] == 37:
                    centroid_vec = c["vector"]
                    break
            for i, name in enumerate(model.feature_names):
                diff = abs(scaled[i] - centroid_vec[i])
                cluster37_diffs.setdefault(name, []).append(diff)
            sample_count += 1

    print(f"Analyzed {sample_count} cluster-37 sessions\n")
    print("=" * 80)
    print("TOP 15 FEATURES CAUSING THE ~33 DISTANCE (cluster 37)")
    print("=" * 80)
    print(f"{'feature':35s} {'avg|diff|':>12s} {'contrib²':>12s}")
    print("-" * 80)

    ranked = sorted(
        cluster37_diffs.items(),
        key=lambda x: -sum(d*d for d in x[1]) / len(x[1]),
    )
    total_var = 0
    for name, diffs in ranked:
        avg_abs = sum(diffs) / len(diffs)
        contrib_sq = sum(d*d for d in diffs) / len(diffs)
        total_var += contrib_sq

    for name, diffs in ranked[:15]:
        avg_abs = sum(diffs) / len(diffs)
        contrib_sq = sum(d*d for d in diffs) / len(diffs)
        pct = 100 * contrib_sq / total_var
        print(f"{name:35s} {avg_abs:12.4f} {contrib_sq:12.4f}  ({pct:5.1f}%)")


if __name__ == "__main__":
    main()
