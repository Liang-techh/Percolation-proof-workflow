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
  "$LAKE" env lean -DwarningAsError=true "$ROOT/P5WeightedDualAdapter.lean"
) 2>&1 | tee "$LOG"

for DECL in \
  weightedDual_nonneg \
  box_to_weightedDual \
  box_to_rate_budget \
  diagonal_normalization_dual_identity \
  diagonal_box_to_weightedDual \
  local_relative_to_weightedDual \
  fixed_bias_not_uniformly_relative_scalar \
  undamped_direction_obstruction_scalar; do
  grep -q "RouteBP5WeightedDualAdapter.$DECL" "$LOG" || {
    echo "FAIL: missing axiom report for $DECL" >&2
    exit 1
  }
done

if grep -Eiq 'sorryAx|declaration uses.*axiom|unknown module|error:' "$LOG"; then
  echo "AXIOM_AUDIT=FAIL"
  exit 1
fi

echo "AXIOM_AUDIT=PASS"
echo "P5_WEIGHTED_DUAL_ADAPTER_FOCUSED_CHECK=PASS"
echo "SOURCE_FORCE_COORDINATE_MAP=OPEN"
echo "SOURCE_COMPONENT_INTERVALS=OPEN"
echo "DAMPING_COEFFICIENT_SOURCE_BINDING=OPEN"
echo "P8_SAME_DOMAIN_COVERAGE=OPEN"
echo "REGISTRY_MUTATION=false"
