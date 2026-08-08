#!/usr/bin/env bash
# Compatibility wrapper. The compliance engine is `atlas check`.
#
# Kept because CI, hooks, and muscle memory point here. It forwards every
# argument, so `atlas check --json` works exactly as
# `atlas check --json` does.
set -euo pipefail
cd "$(dirname "$0")/.."
exec python3 scripts/atlas check "$@"
