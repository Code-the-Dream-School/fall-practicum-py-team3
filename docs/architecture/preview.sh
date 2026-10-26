#!/usr/bin/env bash
# Live preview of workspace.dsl in the browser. Save the file, refresh the page. Needs Docker.
set -euo pipefail

IMAGE="structurizr/structurizr:2026.09.19"
PORT="${PORT:-8080}"
DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Open http://localhost:$PORT (Ctrl+C to stop)"
docker run -it --rm --user "$(id -u):$(id -g)" -p "$PORT:8080" \
  -v "$DIR:/usr/local/structurizr" "$IMAGE" local
