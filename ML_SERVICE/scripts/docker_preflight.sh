#!/usr/bin/env bash
set -euo pipefail

echo "=== ML_SERVICE Docker preflight ==="

required_files=(
  "Dockerfile"
  "docker-compose.yml"
  "requirements.txt"
  ".dockerignore"
)

required_dirs=(
  "app"
  "app/analytics"
  "analytics"
  "models"
  "tests"
)

for f in "${required_files[@]}"; do
  [[ -f "$f" ]] || { echo "MISSING FILE: $f"; exit 1; }
done

for d in "${required_dirs[@]}"; do
  [[ -d "$d" ]] || { echo "MISSING DIR: $d"; exit 1; }
done

echo
echo "=== Host source inventory ==="
find app analytics models tests -type f \
  -not -path '*/__pycache__/*' \
  -not -name '*.pyc' \
  | sort

echo
echo "=== Compose validation ==="
docker compose config >/tmp/ml_service_compose_config.yml
echo "docker compose config: OK"

echo
echo "=== Docker build context check ==="
echo "The Dockerfile uses COPY . . and .dockerignore controls exclusions."
echo "No image/container rebuild is performed by this script."

echo
echo "=== Existing container mounts (if container exists) ==="
docker inspect honeypot-ml-service \
  --format '{{range .Mounts}}{{println .Source "->" .Destination}}{{end}}' \
  2>/dev/null || echo "Container not found; this is OK before first rebuild."

echo
echo "=== Preflight complete: NO BUILD PERFORMED ==="
