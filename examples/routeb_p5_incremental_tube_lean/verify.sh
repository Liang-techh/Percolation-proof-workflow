#!/usr/bin/env bash
set -euo pipefail
# CI_PORTABLE=1

ROOT="$(cd "$(dirname "$0")" && pwd)"
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
  exit 2
fi
if [[ ! -f "$LAKE_ROOT/lake-manifest.json" ]]; then
  echo "BUILD_ENV_BLOCKED: pinned lake-manifest.json missing at $LAKE_ROOT" >&2
  exit 2
fi

echo "LEAN_TOOLCHAIN=$EXPECTED_TOOLCHAIN"
echo "LAKE_MANIFEST=$LAKE_ROOT/lake-manifest.json"
LOG="$(mktemp)"
trap 'rm -f "$LOG"' EXIT
(
  cd "$LAKE_ROOT"
  "$LAKE" env lean -DwarningAsError=true "$ROOT/P5IncrementalTube.lean"
) 2>&1 | tee "$LOG"

for DECL in \
  common_forcing_cancels \
  block45_common_forcing_cancels \
  storage_completed_square \
  mass_lower \
  mass_upper \
  h_lower \
  storage_lower_completed \
  k_upper \
  damp_upper \
  mass_cross_upper \
  storage_upper_coefficients \
  storage_upper_gap \
  storage_upper_21_25 \
  position_sq_bound \
  velocity_completion_identity \
  velocity_sq_bound \
  matching_initial_storage \
  iss_storage_refinement \
  division_free_barrier_inward \
  barrier_integer_constants; do
  grep -q "RouteBP5IncrementalTube.$DECL" "$LOG" || {
    echo "FAIL: missing axiom report for $DECL" >&2
    exit 1
  }
done

if grep -Eiq 'sorryAx|declaration uses.*axiom|unknown module|error:' "$LOG"; then
  echo "AXIOM_AUDIT=FAIL"
  exit 1
fi

echo "AXIOM_AUDIT=PASS"
echo "P5_INCREMENTAL_TUBE_FOCUSED_CHECK=PASS"
echo "SOURCE_FLOAT64_BINDING=OPEN"
echo "P8_NOMINAL_FLOWPIPE=OPEN"
echo "ODE_COVERAGE=OPEN"
echo "P5_P8_M4_FINAL_INTEGRATION=false"
echo "REGISTRY_MUTATION=false"
