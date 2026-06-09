#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_DIR="$(cd "$SKILL_DIR/../.." && pwd)"
DIST_DIR="$REPO_DIR/dist"
OUT="$DIST_DIR/world-cup-digest.skill"

mkdir -p "$DIST_DIR"
rm -f "$OUT"

cd "$SKILL_DIR"
zip -qr "$OUT" . -x "*/__pycache__/*" "*.pyc" ".DS_Store"

echo "$OUT"
