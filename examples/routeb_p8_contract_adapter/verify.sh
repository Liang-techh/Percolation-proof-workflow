#!/usr/bin/env bash
set -euo pipefail

SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
PARENT=$(cd -- "$SIDE/../routeb_p8_picard_step_lean" && pwd -P)
LAKE_ROOT=${LAKE_ROOT:-/home/z5242/sos_lean}
LAKE=${LAKE:-/home/z5242/.elan/bin/lake}

if [[ ! -d "$LAKE_ROOT" || ! -x "$LAKE" ]]; then
  echo "BUILD_ENV_BLOCKED: missing pinned Lake environment or executable" >&2
  exit 1
fi

RUN=$(mktemp -d)
trap 'rm -rf "$RUN"' EXIT
mkdir -p "$RUN/parent"
cp "$PARENT/RouteBP8PicardStep.lean" "$RUN/parent/"
cp "$SIDE/P8ContractAdapter.lean" "$RUN/"

(
  cd "$LAKE_ROOT"
  "$LAKE" env lean -DwarningAsError=true --root="$RUN/parent" \
    -o "$RUN/parent/RouteBP8PicardStep.olean" \
    "$RUN/parent/RouteBP8PicardStep.lean"
  export LEAN_PATH="$RUN/parent${LEAN_PATH:+:$LEAN_PATH}"
  "$LAKE" env lean -DwarningAsError=true --root="$RUN" \
    -o "$RUN/P8ContractAdapter.olean" "$RUN/P8ContractAdapter.lean"
)

if grep -nE '(^|[^[:alnum:]_])(sorry|admit|axiom)([^[:alnum:]_]|$)|^[[:space:]]*(unsafe|partial)[[:space:]]' \
    "$SIDE/P8ContractAdapter.lean" "$PARENT/RouteBP8PicardStep.lean"; then
  echo "SOURCE_RESTRICTION_CHECK=FAILED" >&2
  exit 1
fi

echo "SOURCE_RESTRICTION_CHECK=PASSED"
echo "P8_CONTRACT_ADAPTER_COMPILE=PASSED"
echo "TRUE_DH_BINDING=OPEN"
