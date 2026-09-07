#!/usr/bin/env bash
set -euo pipefail

SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
LAKE_ROOT=${LAKE_ROOT:-/home/z5242/sos_lean}
LAKE=${LAKE:-/home/z5242/.elan/bin/lake}

if [[ ! -d "$LAKE_ROOT" ]]; then
  echo "missing pinned Lake environment: $LAKE_ROOT" >&2
  exit 1
fi
if [[ ! -x "$LAKE" ]]; then
  echo "missing pinned Lake executable: $LAKE" >&2
  exit 1
fi

(cd "$LAKE_ROOT" && "$LAKE" env lean -DwarningAsError=true \
  "$SIDE/RouteBP8PicardStep.lean")
if grep -nE '(^|[^[:alnum:]_])(sorry|admit)([^[:alnum:]_]|$)|^[[:space:]]*axiom[[:space:]]' \
    "$SIDE/RouteBP8PicardStep.lean"; then
  echo "SOURCE_RESTRICTION_CHECK=FAILED" >&2
  exit 1
fi

echo "SOURCE_RESTRICTION_CHECK=PASSED"
echo "P8_PICARD_STEP_LOCAL_COMPILE=PASSED"
