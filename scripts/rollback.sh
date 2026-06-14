#!/usr/bin/env bash
set -euo pipefail

CURRENT="$(tr -d '\r\n' < nginx/active-environment 2>/dev/null || echo green)"
TARGET="blue"

if [[ "$CURRENT" == "blue" ]]; then
  TARGET="green"
fi

echo "Rollback desde $CURRENT hacia $TARGET"
./scripts/promote.sh "$TARGET"
