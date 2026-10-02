"""Random-sample pipeline diagnostic."""
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


def fetch_all_events():
    """Fetch ALL events from ES via scroll API."""
    url = "http://elasticsearch:9200/honeypot-events/_search?scroll=2m"
    body = {"size": 5000, "query": {"match_all": {}}}
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
    )
    data = json.loads(urllib.request.urlopen(req).read().decode())
    scroll_id = data["_scroll_id"]
    events = [h["_source"] for h in data["hits"]["hits"]]

    while True:
        req = urllib.request.Request(
            "http://elasticsearch:9200/_search/scroll",
            data=json.dumps({"scroll": "2m", "scroll_id": scroll_id}).encode(),
            headers={"Content-Type": "application/json"},
        )
        data = json.loads(urllib.request.urlopen(req).read().decode())
        hits = data["hits"]["hits"]
        if not hits:
            break
        events.extend(h["_source"] for h in hits)

    return events


def main():
    print("=" * 70)
    print("RANDOM SAMPLE DIAGNOSTIC")
    print("=" * 70)

    print("\n[1/3] Loading frozen model...")
    model = load_frozen_model()
    print(f"  Model loaded: {len(model.feature_names)} features")

    print("\n[2/3] Fetching all events from Elasticsearch (scroll)...")
    all_events = fetch_all_events()
    print(f"  Fetched {len(all_events)} events")

    print("\n[3/3] Sampling 5000 random events...")
    random.seed(42)
    sample = random.sample(all_events, min(5000, len(all_events)))
    print(f"  Sample size: {len(sample)}")

    # Show honeypot distribution in sample
    honeypots = {}
    for e in sample:
        hp = e.get("honeypot", "?")
        honeypots[hp] = honeypots.get(hp, 0) + 1
    print(f"\n  Sample honeypot distribution:")
    for hp, cnt in sorted(honeypots.items(), key=lambda x: -x[1]):
        print(f"    {hp:20s}: {cnt}")

    protocols = {}
    for e in sample:
        p = e.get("protocol", "?")
        protocols[p] = protocols.get(p, 0) + 1
    print(f"\n  Sample protocol distribution:")
    for p, cnt in sorted(protocols.items(), key=lambda x: -x[1]):
        print(f"    {p:20s}: {cnt}")

    print("\n" + "=" * 70)
    print("RUNNING PIPELINE")
    print("=" * 70)

    normalized = adapt_input({"events": sample})
    sessions = reconstruct_sessions(normalized)
    print(f"Sessions built: {len(sessions)}")

    cluster_counts = {}
    distances = []

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

        cluster_counts[cluster] = cluster_counts.get(cluster, 0) + 1
        distances.append(distance)

    print("\n" + "=" * 70)
    print("CLUSTER DISTRIBUTION")
    print("=" * 70)
    for cid in sorted(cluster_counts.keys()):
        cnt = cluster_counts[cid]
        pct = 100 * cnt / len(sessions)
        bar = "█" * int(pct / 2)
        print(f"  Cluster {cid:2d}: {cnt:5d}  ({pct:5.1f}%)  {bar}")

    print(f"\nTotal clusters used: {len(cluster_counts)} (out of 38)")

    print("\n" + "=" * 70)
    print("DISTANCE STATISTICS")
    print("=" * 70)
    distances.sort()
    n = len(distances)
    print(f"  min:    {distances[0]:.4f}")
    print(f"  p25:    {distances[n//4]:.4f}")
    print(f"  median: {distances[n//2]:.4f}")
    print(f"  p75:    {distances[3*n//4]:.4f}")
    print(f"  p95:    {distances[int(n*0.95)]:.4f}")
    print(f"  max:    {distances[-1]:.4f}")
    print(f"  mean:   {sum(distances)/n:.4f}")

    print(f"\n  Training reference:")
    print(f"    min: 0.0002, median: 0.2432, p95: 7.154, max: 200.07, mean: 1.457")


if __name__ == "__main__":
    main()
