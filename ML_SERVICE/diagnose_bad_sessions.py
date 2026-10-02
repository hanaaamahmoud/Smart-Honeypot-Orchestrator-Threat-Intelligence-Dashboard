"""Find the worst sessions and their features."""
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
        if not hits:
            break
        events.extend(h["_source"] for h in hits)
    return events


def main():
    model = load_frozen_model()
    with open("/app/models/frozen_production_reference/standard_scaler_params.json") as f:
        scaler = json.load(f)

    print("[1/2] Fetching events...")
    all_events = fetch_all_events()
    print(f"  {len(all_events)} events")

    random.seed(42)
    sample = random.sample(all_events, 5000)

    print("[2/2] Running pipeline...")
    sessions = reconstruct_sessions(adapt_input({"events": sample}))
    print(f"  {len(sessions)} sessions")

    results = []
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
        results.append((distance, cluster, session, features, scaled))

    results.sort(reverse=True, key=lambda x: x[0])

    print("\n" + "=" * 80)
    print("TOP 5 WORST SESSIONS")
    print("=" * 80)

    key_features = [
        "event_count", "session_duration_seconds",
        "inter_event_gap_mean", "inter_event_gap_max",
        "session_duration_log1p", "inter_event_gap_mean_log1p",
        "inter_event_gap_max_log1p", "events_per_second",
        "auth_attempt_total", "unique_source_ips",
        "unique_countries", "unique_destinations",
    ]

    for i, (dist, cluster, session, features, scaled) in enumerate(results[:5]):
        print(f"\n{'='*80}")
        print(f"#{i+1}  DISTANCE: {dist:.2f}  →  CLUSTER: {cluster}")
        print(f"{'='*80}")
        print(f"  session_id:     {session['session_id']}")
        print(f"  event_count:    {session['event_count']}")
        print(f"  start_time:     {session['start_time']}")
        print(f"  end_time:       {session['end_time']}")
        print(f"  duration (s):   {session['duration_seconds']:.2f}")
        print(f"\n  {'feature':35s} {'raw':>15s} {'scaled':>12s}")
        print(f"  {'-'*35} {'-'*15} {'-'*12}")
        for name in key_features:
            raw = features[name]
            idx = list(scaler["features"]).index(name)
            sc = scaled[idx]
            print(f"  {name:35s} {raw:15.2f} {sc:+12.2f}")

    # Distance histogram
    print("\n" + "=" * 80)
    print("DISTANCE DISTRIBUTION")
    print("=" * 80)
    buckets = [0, 5, 10, 15, 20, 30, 50, 100, 500, 1000, 10000, float('inf')]
    labels = ["0-5", "5-10", "10-15", "15-20", "20-30", "30-50",
              "50-100", "100-500", "500-1000", "1000-10000", ">10000"]
    counts = [0] * len(labels)
    for dist, *_ in results:
        for i in range(len(labels)):
            if buckets[i] <= dist < buckets[i+1]:
                counts[i] += 1
                break
    total = len(results)
    for label, cnt in zip(labels, counts):
        pct = 100 * cnt / total
        bar = "█" * int(pct / 2)
        print(f"  {label:>12s}: {cnt:5d}  ({pct:5.1f}%)  {bar}")


if __name__ == "__main__":
    main()
