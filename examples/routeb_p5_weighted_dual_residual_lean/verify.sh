#!/usr/bin/env bash
set -euo pipefail
# CI_PORTABLE=1

ROOT="$(cd "$(dirname "$0")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
LAKE="${LAKE:-$(command -v lake || true)}"

if [[ -z "$LAKE" ]]; then
  echo "BUILD_ENV_BLOCKED: cannot locate lake on PATH" >&2
  exit 2
fi

EXPECTED_TOOLCHAIN="$(tr -d '\r\n' < "$ROOT/lean-toolchain")"
ACTUAL_TOOLCHAIN="$(tr -d '\r\n' < "$LAKE_ROOT/lean-toolchain")"
if [[ "$EXPECTED_TOOLCHAIN" != "$ACTUAL_TOOLCHAIN" ]]; then
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
  "$LAKE" env lean -DwarningAsError=true "$ROOT/WeightedDualResidual.lean"
) 2>&1 | tee "$LOG"

for DECL in \
  weighted_young_component \
  weighted_dot_le_of_dualSq \
  weighted_residual_decay \
  dualSq_nonneg \
  dualSq_eq_zero_forces_component_zero \
  weighted_residual_decay_kappa_zero \
  generic_force_error_not_velocity_relative; do
  grep -q "$DECL" "$LOG"
done

if grep -Eiq 'sorryAx|declaration uses.*axiom|unknown module|error:' "$LOG"; then
  echo "AXIOM_AUDIT=FAIL"
  exit 1
fi

echo "AXIOM_AUDIT=PASS"
echo "P5_WEIGHTED_DUAL_RESIDUAL_FOCUSED_CHECK=PASS"
echo "PHYSICAL_SOURCE_BINDING=OPEN"
echo "FINAL_INTEGRATION=梁智炜"
