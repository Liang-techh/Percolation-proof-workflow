#!/usr/bin/env bash
set -euo pipefail
# CI_PORTABLE=1

ROOT="$(cd "$(dirname "$0")" && pwd)"
PARENT="$(cd "$ROOT/../routeb_p8_picard_step_lean" && pwd)"
CONTRACT="$(cd "$ROOT/../routeb_p8_contract_adapter" && pwd)"
FIRST12="$(cd "$ROOT/../routeb_p8_first12_adapter_lean" && pwd)"
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
mkdir -p "$RUN/parent" "$RUN/contract" "$RUN/first12" "$RUN/child"
cp "$PARENT/RouteBP8PicardStep.lean" "$RUN/parent/"
cp "$CONTRACT/P8ContractAdapter.lean" "$RUN/contract/"
cp "$FIRST12/P8First12Adapter.lean" "$RUN/first12/"
cp "$ROOT/P8RampTubeTransport.lean" "$RUN/child/"

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
  "$LAKE" env lean -DwarningAsError=true --root="$RUN/first12" \
    -o "$RUN/first12/P8First12Adapter.olean" \
    "$RUN/first12/P8First12Adapter.lean"

  export LEAN_PATH="$RUN/first12:$RUN/contract:$RUN/parent${BASE_LEAN_PATH:+:$BASE_LEAN_PATH}"
  "$LAKE" env lean -DwarningAsError=true --root="$RUN/child" \
    -o "$RUN/child/P8RampTubeTransport.olean" \
    "$RUN/child/P8RampTubeTransport.lean"
) 2>&1 | tee "$LOG"

grep -q "rampLift_injective_mc" "$LOG"
grep -q "rampTube_on_ramp_iff" "$LOG"
grep -q "mechanical_coverage_lifts" "$LOG"
grep -q "pullbackDomain_iff" "$LOG"
grep -q "ramp_tail_sq_cap" "$LOG"
grep -q "current_w_box_not_T1" "$LOG"
grep -q "ramp_tail_distance" "$LOG"
grep -q "explicitMechanical_lipschitz_transport" "$LOG"

if grep -Eiq 'sorryAx|unknown module|error:' "$LOG"; then
  echo "AXIOM_AUDIT=FAIL"
  exit 1
fi

echo "AXIOM_AUDIT=PASS"
echo "P8_RAMP_TUBE_TRANSPORT_FOCUSED_CHECK=PASS"
echo "SOURCE_MECHANICAL_BINDING=OPEN"
echo "ODE_CONTINUATION=OPEN"
echo "FLOWPIPE_COVERAGE=OPEN"
echo "REGISTRY_MUTATION=false"
