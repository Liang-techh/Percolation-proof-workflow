#!/usr/bin/env bash
set -euo pipefail
# CI_PORTABLE=1

ROOT="$(cd "$(dirname "$0")" && pwd)"
PARENT="$(cd "$ROOT/../routeb_p8_picard_step_lean" && pwd)"
CONTRACT="$(cd "$ROOT/../routeb_p8_contract_adapter" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"

if [[ -z "${LAKE:-}" ]]; then
  LAKE="$(command -v lake || true)"
fi

if [[ -z "$LAKE" ]]; then
  echo "BUILD_ENV_BLOCKED: cannot locate lake on PATH" >&2
  exit 2
fi

if [[ ! -f "$LAKE_ROOT/lakefile.toml" && ! -f "$LAKE_ROOT/lakefile.lean" ]]; then
  echo "BUILD_ENV_BLOCKED: local Lake root missing at $LAKE_ROOT" >&2
  exit 2
fi

EXPECTED_TOOLCHAIN="$(tr -d '\r\n' < "$ROOT/lean-toolchain")"
ACTUAL_TOOLCHAIN="$(tr -d '\r\n' < "$LAKE_ROOT/lean-toolchain")"
if [[ "$ACTUAL_TOOLCHAIN" != "$EXPECTED_TOOLCHAIN" ]]; then
  echo "BUILD_ENV_BLOCKED: toolchain mismatch" >&2
  echo "EXPECTED_TOOLCHAIN=$EXPECTED_TOOLCHAIN" >&2
  echo "ACTUAL_TOOLCHAIN=$ACTUAL_TOOLCHAIN" >&2
  exit 2
fi

echo "LEAN_TOOLCHAIN=$EXPECTED_TOOLCHAIN"
RUN="$(mktemp -d)"
LOG="$(mktemp)"
trap 'rm -rf "$RUN"; rm -f "$LOG"' EXIT
mkdir -p "$RUN/parent" "$RUN/contract" "$RUN/child"
cp "$PARENT/RouteBP8PicardStep.lean" "$RUN/parent/"
cp "$CONTRACT/P8ContractAdapter.lean" "$RUN/contract/"
cp "$ROOT/P8First12Adapter.lean" "$RUN/child/"

(
  cd "$LAKE_ROOT"
  "$LAKE" env lean -DwarningAsError=true --root="$RUN/parent" \
    -o "$RUN/parent/RouteBP8PicardStep.olean" \
    "$RUN/parent/RouteBP8PicardStep.lean"

  BASE_LEAN_PATH="${LEAN_PATH:-}"
  export LEAN_PATH="$RUN/parent${BASE_LEAN_PATH:+:$BASE_LEAN_PATH}"
  "$LAKE" env lean -DwarningAsError=true --root="$RUN/contract" \
    -o "$RUN/contract/P8ContractAdapter.olean" \
    "$RUN/contract/P8ContractAdapter.lean"

  export LEAN_PATH="$RUN/contract:$RUN/parent${BASE_LEAN_PATH:+:$BASE_LEAN_PATH}"
  "$LAKE" env lean -DwarningAsError=true --root="$RUN/child" \
    -o "$RUN/child/P8First12Adapter.olean" \
    "$RUN/child/P8First12Adapter.lean"
) 2>&1 | tee "$LOG"

grep -q "forgetTail_rampLift" "$LOG"
grep -q "timeLift_first12_on_ramp" "$LOG"
grep -q "timeLift_tail_on_ramp" "$LOG"
grep -q "repair13_preserves_first12" "$LOG"
grep -q "repair13_eq_source_at_iff_c_zero" "$LOG"
grep -q "repair13_eq_source_iff_c_zero" "$LOG"
grep -q "repair13_ne_source_of_c_ne_zero" "$LOG"

if grep -Eiq 'sorryAx|unknown module|error:' "$LOG"; then
  echo "AXIOM_AUDIT=FAIL"
  exit 1
fi

echo "AXIOM_AUDIT=PASS"
echo "P8_FIRST12_ADAPTER_FOCUSED_CHECK=PASS"
echo "SOURCE_MECHANICAL_BINDING=OPEN"
echo "ODE_CONTINUATION=OPEN"
echo "FLOWPIPE_COVERAGE=OPEN"
echo "REGISTRY_MUTATION=false"
