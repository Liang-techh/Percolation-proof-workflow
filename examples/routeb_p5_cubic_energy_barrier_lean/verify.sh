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
  "$LAKE" env lean -DwarningAsError=true "$ROOT/P5CubicEnergyBarrier.lean"
) 2>&1 | tee "$LOG"

for DECL in \
  abs_le_of_sq_le_sq_nonneg \
  cubic_square_absorption_from_energy_barrier \
  cubic_square_strict_absorption_from_energy_barrier \
  cubic_energy_barrier_dissipation \
  cubic_energy_barrier_strict_dissipation \
  regularizer_to_damping_coercivity \
  fdLambda_mul_K_exact \
  fourier_barrier_from_division_free \
  fourier_cubic_absorption_from_division_free_barrier; do
  grep -q "RouteBP5CubicEnergyBarrier.$DECL" "$LOG" || {
    echo "FAIL: missing axiom report for $DECL" >&2
    exit 1
  }
done

if grep -Eiq 'sorryAx|declaration uses.*axiom|unknown module|error:' "$LOG"; then
  echo "AXIOM_AUDIT=FAIL"
  exit 1
fi

echo "AXIOM_AUDIT=PASS"
echo "P5_CUBIC_ENERGY_BARRIER_FOCUSED_CHECK=PASS"
echo "FOURIER_SF_SOURCE_BINDING=OPEN"
echo "NONKINETIC_STORAGE_LOWER_BOUND=OPEN"
echo "IEEE_CUBIC_REMAINDER=OPEN"
echo "CONTROLLER_SOLVE_BIAS_CLOSURE=OPEN"
echo "FIRST_EXIT_ODE_COVERAGE=OPEN"
echo "REGISTRY_MUTATION=false"
