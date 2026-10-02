#!/bin/bash
# ============================================================
# package_handoff.sh — Package ML analytics into a ZIP
#
# Uses Python's zipfile module (no dependency on the `zip`
# command being installed).
#
# Output:
#   /app/backend_handoff/ml_analytics_files.zip
# ============================================================

set -e

SRC="/app/analytics_output"
DEST="/app/backend_handoff/ml_analytics_files"
ZIP_OUT="/app/backend_handoff/ml_analytics_files.zip"

echo "============================================================"
echo "PACKAGING ML ANALYTICS HANDOFF"
echo "============================================================"

# ─── 1. Prepare folder ───
echo ""
echo "[1/4] Preparing folder..."
rm -rf "$DEST"
mkdir -p "$DEST"

# ─── 2. Copy files ───
echo ""
echo "[2/4] Copying files..."

cp "$SRC/02_cluster_analytics_enriched.json"   "$DEST/cluster_analytics.json"
cp "$SRC/03_temporal_analytics.json"           "$DEST/temporal_analytics.json"
cp "$SRC/04_session_analytics.json"            "$DEST/session_analytics.json"
cp "$SRC/05_mitre_analytics_lite.json"         "$DEST/mitre_analytics.json"
cp "$SRC/06_mitre_statistics.json"             "$DEST/mitre_statistics.json"
cp "$SRC/07_mitre_trends.json"                 "$DEST/mitre_trends.json"
cp "$SRC/08_session_replay_list.json"          "$DEST/session_replay_list.json"

# Copy session details if they exist
if [ -d "$SRC/session_replay_details" ]; then
    cp -r "$SRC/session_replay_details" "$DEST/"
fi

# Copy the README from the existing location
if [ -f "/app/backend_handoff/ml_analytics_files/README.md" ]; then
    cp "/app/backend_handoff/ml_analytics_files/README.md" "$DEST/" 2>/dev/null || true
fi

echo "   OK — Files copied"

# ─── 3. Create ZIP with Python ───
echo ""
echo "[3/4] Creating ZIP (Python zipfile)..."

rm -f "$ZIP_OUT"

python3 -c "
import zipfile
import os

zip_path = '$ZIP_OUT'
source_dir = '$DEST'

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(source_dir):
        for f in files:
            full_path = os.path.join(root, f)
            arcname = os.path.relpath(full_path, os.path.dirname(source_dir))
            zf.write(full_path, arcname)

size_mb = os.path.getsize(zip_path) / (1024 * 1024)
print(f'   OK — ZIP created ({size_mb:.2f} MB)')
"

# ─── 4. Summary ───
echo ""
echo "[4/4] Summary"
echo "============================================================"
echo "✅ HANDOFF PACKAGE READY"
echo "============================================================"
echo ""
echo "   ZIP path:    $ZIP_OUT"
echo "   Contents:    $(python3 -c "import zipfile; print(len(zipfile.ZipFile('$ZIP_OUT').namelist()))" 2>/dev/null || echo "?") files"
echo ""
echo "   Next: run refresh_all.sh to copy the ZIP to the host."
echo "============================================================"
