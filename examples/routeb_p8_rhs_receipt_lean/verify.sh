#!/usr/bin/env bash
set -euo pipefail

SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
PARENT=$(cd -- "$SIDE/../routeb_p8_picard_step_lean" && pwd -P)
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

RUN=$(mktemp -d)
trap 'rm -rf "$RUN"' EXIT
mkdir -p "$RUN/parent"
cp "$PARENT/RouteBP8PicardStep.lean" "$RUN/parent/"
cp "$SIDE/P8RhsReceipt.lean" "$RUN/"

(
  cd "$LAKE_ROOT"
  "$LAKE" env lean -DwarningAsError=true --root="$RUN/parent" \
    -o "$RUN/parent/RouteBP8PicardStep.olean" \
    "$RUN/parent/RouteBP8PicardStep.lean"
  export LEAN_PATH="$RUN/parent${LEAN_PATH:+:$LEAN_PATH}"
  "$LAKE" env lean -DwarningAsError=true --root="$RUN" \
    -o "$RUN/P8RhsReceipt.olean" "$RUN/P8RhsReceipt.lean"
)

if grep -nE '(^|[^[:alnum:]_])(sorry|admit|axiom)([^[:alnum:]_]|$)|^[[:space:]]*(unsafe|partial)[[:space:]]' \
    "$SIDE/P8RhsReceipt.lean" "$PARENT/RouteBP8PicardStep.lean"; then
  echo "SOURCE_RESTRICTION_CHECK=FAILED" >&2
  exit 1
fi

echo "SOURCE_RESTRICTION_CHECK=PASSED"
echo "P8_RHS_RECEIPT_LOCAL_COMPILE=PASSED"
echo "JULIA_FULL_RHS_BINDING=OPEN"
