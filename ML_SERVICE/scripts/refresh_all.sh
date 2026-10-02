#!/bin/bash
# ============================================================
# refresh_all.sh — Full ML Service refresh in one command
#
# Usage:
#   bash scripts/refresh_all.sh
#
# Steps:
#   1. Verify Docker + Container are healthy
#   2. Verify Elasticsearch is reachable
#   3. Run the full ML pipeline
#   4. Package results into ml_analytics_files.zip
#   5. Copy the ZIP to the Windows Desktop
#   6. Print a summary
# ============================================================

set -e

CONTAINER="honeypot-ml-service"
DESKTOP="/mnt/c/Users/Al-Huda/Desktop"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
ZIP_NAME="ml_analytics_data_${TIMESTAMP}.zip"

echo ""
echo "============================================================"
echo "ML SERVICE — FULL REFRESH"
echo "Started: $(date '+%Y-%m-%d %H:%M:%S')"
echo "============================================================"
echo ""

# [1/5] Docker daemon
echo "[1/5] Checking Docker daemon..."
if ! docker info > /dev/null 2>&1; then
    echo "   ERROR: Docker daemon is not running."
    echo "   Start Docker Desktop and try again."
    exit 1
fi
echo "   OK — Docker is running."

# [2/5] Container
echo ""
echo "[2/5] Checking container: $CONTAINER"
if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER}$"; then
    echo "   Container is not running. Attempting to start..."
    docker start $CONTAINER > /dev/null 2>&1 || {
        echo "   ERROR: Failed to start $CONTAINER."
        echo "   Run: docker compose up -d"
        exit 1
    }
    echo "   Waiting 15s for health check..."
    sleep 15
fi

HEALTH=$(curl -s http://localhost:8000/health 2>/dev/null || echo "")
if ! echo "$HEALTH" | grep -q '"status":"ok"'; then
    echo "   Waiting another 15s for health..."
    sleep 15
    HEALTH=$(curl -s http://localhost:8000/health 2>/dev/null || echo "")
fi

if echo "$HEALTH" | grep -q '"status":"ok"'; then
    echo "   OK — Container is healthy."
else
    echo "   ERROR: Container is not healthy."
    echo "   Check: docker logs $CONTAINER --tail 30"
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

# Copy to Desktop
echo ""
echo "Copying to Desktop..."
if [ ! -d "$DESKTOP" ]; then
    echo "   WARNING: Desktop path not found: $DESKTOP"
    echo "   ZIP stays at: /app/backend_handoff/ml_analytics_files.zip"
else
    docker cp "$CONTAINER:/app/backend_handoff/ml_analytics_files.zip" \
              "$DESKTOP/$ZIP_NAME" 2>/dev/null
    if [ -f "$DESKTOP/$ZIP_NAME" ]; then
        SIZE=$(du -h "$DESKTOP/$ZIP_NAME" | cut -f1)
        echo "   OK — $DESKTOP/$ZIP_NAME ($SIZE)"
    fi
fi

echo ""
echo "============================================================"
echo "REFRESH COMPLETE"
echo "============================================================"
echo "  Events:      $ES_COUNT"
echo "  ZIP:         $DESKTOP/$ZIP_NAME"
echo "  Finished:    $(date '+%Y-%m-%d %H:%M:%S')"
echo "============================================================"
