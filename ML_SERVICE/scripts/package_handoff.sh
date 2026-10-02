#!/bin/bash
# Package ML Analytics Handoff
# Usage: bash package_handoff.sh

set -e

SRC="/app/analytics_output"
DEST="/app/backend_handoff/ml_analytics_files"

echo "═══════════════════════════════════════════════"
echo "📦 PACKAGING ML ANALYTICS HANDOFF"
echo "═══════════════════════════════════════════════"

# Clear and recreate
rm -rf "$DEST"
mkdir -p "$DEST"

echo ""
echo "[1/4] Copying files..."

cp "$SRC/02_cluster_analytics_enriched.json" "$DEST/cluster_analytics.json"
cp "$SRC/03_temporal_analytics.json" "$DEST/temporal_analytics.json"
cp "$SRC/04_session_analytics.json" "$DEST/session_analytics.json"
cp "$SRC/05_mitre_analytics_lite.json" "$DEST/mitre_analytics.json"
cp "$SRC/06_mitre_statistics.json" "$DEST/mitre_statistics.json"
cp "$SRC/07_mitre_trends.json" "$DEST/mitre_trends.json"
cp "$SRC/08_session_replay_list.json" "$DEST/session_replay_list.json"
cp -r "$SRC/session_replay_details" "$DEST/"

echo "   ✅ Files copied"

echo ""
echo "[2/4] Creating ZIP..."
cd /app/backend_handoff
rm -f ml_analytics_files.zip
zip -r -q ml_analytics_files.zip ml_analytics_files/

echo "   ✅ ZIP created"

echo ""
echo "[3/4] Verifying..."
ls -lh ml_analytics_files.zip
echo ""
echo "ZIP contents:"
unzip -l ml_analytics_files.zip | tail -20

echo ""
echo "[4/4] Summary"
echo "═══════════════════════════════════════════════"
echo "✅ HANDOFF PACKAGE READY"
echo "═══════════════════════════════════════════════"
echo ""
echo "📁 ZIP: /app/backend_handoff/ml_analytics_files.zip"
echo ""
echo "Next: Send this ZIP to Backend team"
