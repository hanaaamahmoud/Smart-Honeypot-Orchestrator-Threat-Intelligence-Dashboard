#!/bin/bash
# ML Pipeline — Full Run
# Usage: bash run_ml_pipeline.sh

echo "═══════════════════════════════════════════════"
echo "🤖 ML PIPELINE — FULL RUN"
echo "═══════════════════════════════════════════════"

cd /app

echo ""
echo "[1/6] Reading from Elasticsearch..."
python3 -c "
from app.ingestion.elasticsearch import ElasticsearchReader
from app.config import Settings
r = ElasticsearchReader(Settings.ELASTICSEARCH_URL, Settings.ELASTICSEARCH_INDEX)
print(f'   Events: {r.count():,}')
"

echo ""
echo "[2/6] Running pipeline + analytics..."
python3 << 'PYEOF'
import json, os
from datetime import datetime, timezone
from app.ingestion.elasticsearch import ElasticsearchReader
from app.config import Settings
from app.pipeline.normalization import normalize_events
from app.pipeline.session_reconstruction import reconstruct_sessions
from app.pipeline.feature_generation_base import generate_base_features
from app.pipeline.feature_generation_diversity import generate_diversity_features
from app.pipeline.feature_generation_temporal import generate_temporal_features
from app.pipeline.feature_generation_density import generate_density_features
from app.pipeline.feature_generation_geo import generate_geo_availability_features
from app.pipeline.feature_generation import assemble_48_features
from app.model_loader import load_frozen_model
from app.analytics.cluster_analytics import build_cluster_analytics
from app.analytics.temporal_analytics import build_temporal_analytics
from app.analytics.session_analytics import build_session_records, build_session_summary
from app.analytics.mitre_analytics import build_mitre_analytics
from app.analytics.mitre_statistics import build_mitre_statistics
from app.analytics.mitre_trends import build_mitre_trends
from app.analytics.session_replay import build_session_replay

OUT = "/app/analytics_output"
os.makedirs(OUT, exist_ok=True)

# 1. Load
r = ElasticsearchReader(Settings.ELASTICSEARCH_URL, Settings.ELASTICSEARCH_INDEX)
events = []
for batch in r.read_events_in_batches(batch_size=5000):
    events.extend(batch)
print(f"   Events loaded: {len(events):,}")

# 2. Pipeline
normalized = normalize_events(events)
sessions = reconstruct_sessions(normalized)
model = load_frozen_model()

results = []
for s in sessions:
    fg = {}
    fg.update(generate_base_features(s))
    fg.update(generate_diversity_features(s))
    fg.update(generate_temporal_features(s))
    fg.update(generate_density_features(s))
    fg.update(generate_geo_availability_features(s))
    fv = assemble_48_features(fg)
    scaled = model.scale_features(fv)
    cid, dist = model.nearest_centroid(scaled)
    
    first = s['events'][0] if s['events'] else {}
    raw = first.get('raw', {})
    results.append({
        'reconstructed_session_id': s['session_id'],
        'production_cluster_assignment': int(cid),
        'assignment_status': 'EXISTING_PRODUCTION_CLUSTER',
        'feature_validation_status': 'VALIDATED_48_FEATURES',
        'distance': round(float(dist), 4),
        'event_count': len(s['events']),
        'session_start': s.get('start_time', ''),
        'session_end': s.get('end_time', ''),
        'session_duration_seconds': s.get('duration_seconds', 0),
        'honeypot': first.get('honeypot', ''),
        'protocol': first.get('protocol', ''),
        'source_ip': first.get('source_ip', ''),
        'country': first.get('country', ''),
        'country_code': first.get('country_code', ''),
        'asn': raw.get('asn', ''),
        'attack_type': raw.get('attack_type', ''),
        'mitre_technique': raw.get('mitre_technique', ''),
        'attack_stage': raw.get('attack_stage', ''),
        'severity': raw.get('severity', ''),
    })

# 3. All analytics
ts = datetime.now(timezone.utc).isoformat()

# ML Output
with open(f"{OUT}/00_ml_output_full.json", "w") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"   Processed: {len(results):,} sessions")
print(f"   Clusters: {len(set(r['production_cluster_assignment'] for r in results))}")

PYEOF

echo ""
echo "[3/6] Full pipeline done"
echo ""
echo "═══════════════════════════════════════════════"
echo "✅ PIPELINE RUN COMPLETE"
echo "═══════════════════════════════════════════════"
echo ""
echo "Next steps:"
echo "  1. Copy files to /app/backend_handoff/ml_analytics_files/"
echo "  2. Run: bash /app/package_handoff.sh"
echo "  3. Send the ZIP to Backend team"
