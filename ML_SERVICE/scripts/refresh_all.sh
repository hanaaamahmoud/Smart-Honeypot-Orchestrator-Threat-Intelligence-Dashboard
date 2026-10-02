#!/bin/bash
# ============================================================
# refresh_all.sh — Full ML Service refresh in one command
# ============================================================

set -e

CONTAINER="honeypot-ml-service"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
ZIP_NAME="ml_analytics_data_${TIMESTAMP}.zip"

# Host folder where this script lives
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ML_SERVICE_DIR="$(dirname "$SCRIPT_DIR")"
HOST_ZIP="$ML_SERVICE_DIR/backend_handoff/$ZIP_NAME"

echo ""
echo "============================================================"
echo "ML SERVICE — FULL REFRESH"
echo "Started: $(date '+%Y-%m-%d %H:%M:%S')"
echo "============================================================"
echo ""

# [1/5] Docker
echo "[1/5] Checking Docker daemon..."
if ! docker info > /dev/null 2>&1; then
    echo "   ERROR: Docker daemon is not running."
    exit 1
fi
echo "   OK — Docker is running."

# [2/5] Container
echo ""
echo "[2/5] Checking container: $CONTAINER"
if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER}$"; then
    echo "   Starting container..."
    docker start $CONTAINER > /dev/null 2>&1
    sleep 15
fi

HEALTH=$(curl -s http://localhost:8000/health 2>/dev/null || echo "")
if ! echo "$HEALTH" | grep -q '"status":"ok"'; then
    sleep 15
    HEALTH=$(curl -s http://localhost:8000/health 2>/dev/null || echo "")
fi

if echo "$HEALTH" | grep -q '"status":"ok"'; then
    echo "   OK — Container is healthy."
else
    echo "   ERROR: Container is not healthy."
    exit 1
fi

# [3/5] Elasticsearch
echo ""
echo "[3/5] Checking Elasticsearch..."
ES_COUNT=$(docker exec $CONTAINER python -c "
from app.ingestion.elasticsearch import ElasticsearchReader
from app.config import Settings
r = ElasticsearchReader(Settings.ELASTICSEARCH_URL, Settings.ELASTICSEARCH_INDEX)
print(r.count())
" 2>/dev/null || echo "ERROR")

if [ "$ES_COUNT" = "ERROR" ]; then
    echo "   ERROR: Cannot reach Elasticsearch."
    exit 1
fi
echo "   OK — $ES_COUNT events in honeypot-events."

# [4/5] Pipeline
echo ""
echo "[4/5] Running full ML pipeline (1-3 minutes)..."
echo ""
docker exec -it $CONTAINER bash -c "cd /app && bash scripts/run_ml_pipeline.sh"
echo ""
echo "   OK — Pipeline completed."

# [5/5] Package
echo ""
echo "[5/5] Packaging handoff ZIP..."
docker exec -it $CONTAINER bash -c "cd /app && bash scripts/package_handoff.sh"
echo ""
echo "   OK — Package created."

# Copy ZIP to host
echo ""
echo "Copying ZIP to host..."
mkdir -p "$(dirname "$HOST_ZIP")"

if docker cp "$CONTAINER:/app/backend_handoff/ml_analytics_files.zip" "$HOST_ZIP" 2>/dev/null; then
    SIZE=$(du -h "$HOST_ZIP" | cut -f1)
    echo "   OK — $HOST_ZIP ($SIZE)"
else
    echo "   WARNING: Copy failed. ZIP stays in container at:"
    echo "         /app/backend_handoff/ml_analytics_files.zip"
fi

echo ""
echo "============================================================"
echo "REFRESH COMPLETE"
echo "============================================================"
echo "  Events:      $ES_COUNT"
echo "  ZIP:         $HOST_ZIP"
echo "  Finished:    $(date '+%Y-%m-%d %H:%M:%S')"
echo "============================================================"
