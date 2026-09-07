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
  "$LAKE" env lean -DwarningAsError=true "$ROOT/P5FiniteHorizonBudget.lean"
) 2>&1 | tee "$LOG"

for DECL in \
  abs_le_of_sq_le_sq_nonneg \
  cubic_absorption_from_energy_barrier \
  dual_work_budget \
  mixed_energy_rate \
  linear_growth_stays_below_barrier \
  t1_fifty_fifty_headroom_from_rational \
  upper_storage_coercivity_counterexample; do
  grep -q "RouteBP5FiniteHorizonBudget.$DECL" "$LOG" || {
    echo "FAIL: missing axiom report for $DECL" >&2
    exit 1
  }
done

if grep -Eiq 'sorryAx|declaration uses.*axiom|unknown module|error:' "$LOG"; then
  echo "AXIOM_AUDIT=FAIL"
  exit 1
fi

echo "AXIOM_AUDIT=PASS"
echo "P5_FINITE_HORIZON_POINTWISE_FOCUSED_CHECK=PASS"
echo "FIRST_EXIT_CALCULUS=OPEN"
echo "WEIGHTED_DUAL_SOURCE_ADAPTER=T-P5-014"
echo "FOURIER_SF_SOURCE_BINDING=OPEN"
echo "RAMP_WORK_HBAR_SOURCE_BINDING=OPEN"
echo "WEIGHTED_DUAL_RBAR_SOURCE_BINDING=OPEN"
echo "NONKINETIC_STORAGE_LOWER_BOUND=OPEN"
echo "P8_RAMP_GRAPH_DOMAIN_COVERAGE=OPEN"
echo "REGISTRY_MUTATION=false"
