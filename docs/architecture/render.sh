#!/usr/bin/env bash
# Renders every view in workspace.dsl to docs/architecture/svg/<view-key>.svg. Needs Docker.
set -euo pipefail

STRUCTURIZR_IMAGE="structurizr/structurizr:2026.09.19"
PLANTUML_IMAGE="plantuml/plantuml:1.2026.8"

DIR="$(cd "$(dirname "$0")" && pwd)"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

cp "$DIR/workspace.dsl" "$WORK/"

# Host user, so the exported files can be cleaned up on Linux.
docker run --rm --user "$(id -u):$(id -g)" -v "$WORK:/usr/local/structurizr" "$STRUCTURIZR_IMAGE" \
  export -workspace workspace.dsl -format plantuml/c4plantuml -output puml

mkdir -p "$DIR/svg"
rm -f "$DIR/svg/"*.svg

for puml in "$WORK"/puml/*.puml; do
  name="$(basename "$puml" .puml)"
  name="${name#structurizr-}"
  name="${name#c4plantuml-}"
  docker run --rm -i "$PLANTUML_IMAGE" -tsvg -pipe < "$puml" > "$DIR/svg/$name.svg"
  echo "rendered svg/$name.svg"
done
