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
  echo "EXPECTED_TOOLCHAIN=$EXPECTED_TOOLCHAIN" >&2
  echo "ACTUAL_TOOLCHAIN=$ACTUAL_TOOLCHAIN" >&2
  exit 2
fi

echo "LEAN_TOOLCHAIN=$EXPECTED_TOOLCHAIN"
LOG="$(mktemp)"
trap 'rm -f "$LOG"' EXIT

(
  cd "$LAKE_ROOT"
  "$LAKE" env lean -DwarningAsError=true "$ROOT/P5CubicSmallGain.lean"
) 2>&1 | tee "$LOG"

for DECL in \
  scaled_young_division_free \
  cubic_relative_small_gain \
  cubic_relative_small_gain_strict \
  abs_le_of_sq_le_sq_nonneg \
  cubic_absorption_of_energy_sublevel \
  nonzero_cubic_ray_not_globally_quadratic_absorbable; do
  grep -q "RouteBP5CubicSmallGain.$DECL" "$LOG" || {
    echo "FAIL: missing axiom report for $DECL" >&2
    exit 1
  }
done

if grep -Eiq 'sorryAx|declaration uses.*axiom|unknown module|error:' "$LOG"; then
  echo "AXIOM_AUDIT=FAIL"
  exit 1
fi

echo "AXIOM_AUDIT=PASS"
echo "P5_CUBIC_SMALL_GAIN_FOCUSED_CHECK=PASS"
echo "FD_TENSOR_SOURCE_BINDING=OPEN"
echo "P8_VELOCITY_SUBLEVEL_COVERAGE=OPEN"
echo "CONTROLLER_SOLVE_BIAS_CLOSURE=OPEN"
echo "REGISTRY_MUTATION=false"
