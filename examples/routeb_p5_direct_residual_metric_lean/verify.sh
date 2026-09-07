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
  "$LAKE" env lean -DwarningAsError=true "$ROOT/P5DirectResidualMetric.lean"
) 2>&1 | tee "$LOG"

for DECL in \
  q_lower_diagonal \
  axis4_metric_gap \
  axis5_metric_gap \
  axis4_direct_metric \
  axis5_direct_metric \
  block45_direct_metric \
  abs_le_of_sq_le_sq_nonneg \
  residual_square_absorption \
  derivative_after_residual_absorption \
  iss_direct_metric_refinement \
  ultimate_gain_constants \
  direct_metric_barrier_inward \
  quarter_barrier_inward \
  common_margin_barrier_inward \
  barrier_constant_checks; do
  grep -q "RouteBP5DirectResidualMetric.$DECL" "$LOG" || {
    echo "FAIL: missing axiom report for $DECL" >&2
    exit 1
  }
done

if grep -Eiq 'sorryAx|declaration uses.*axiom|unknown module|error:' "$LOG"; then
  echo "AXIOM_AUDIT=FAIL"
  exit 1
fi

echo "AXIOM_AUDIT=PASS"
echo "P5_DIRECT_RESIDUAL_METRIC_FOCUSED_CHECK=PASS"
echo "SOURCE_FLOAT64_BINDING=OPEN"
echo "RESIDUAL_L2_SOURCE_BOUND=OPEN"
echo "P8_NOMINAL_FLOWPIPE=OPEN"
echo "ODE_COVERAGE=OPEN"
echo "P5_P8_M4_FINAL_INTEGRATION=false"
echo "REGISTRY_MUTATION=false"
