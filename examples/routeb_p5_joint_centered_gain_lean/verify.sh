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
  "$LAKE" env lean -DwarningAsError=true "$ROOT/P5JointCenteredGain.lean"
) 2>&1 | tee "$LOG"

for DECL in \
  joint_quadratic_comparison \
  weighted_amgm_7_10 \
  qDissipation_nonneg \
  block45_joint_residual_metric \
  abs_le_of_sq_le_sq_nonneg \
  centered_small_gain_joint \
  block45_centered_small_gain \
  centered_no_bias_decay \
  centered_no_bias_strict_decay \
  gain_improvement_exact \
  half_gain_checker_constants \
  counterexample_23_quarter; do
  grep -q "RouteBP5JointCenteredGain.$DECL" "$LOG" || {
    echo "FAIL: missing axiom report for $DECL" >&2
    exit 1
  }
done

if grep -Eiq 'sorryAx|declaration uses.*axiom|unknown module|error:' "$LOG"; then
  echo "AXIOM_AUDIT=FAIL"
  exit 1
fi

echo "AXIOM_AUDIT=PASS"
echo "P5_JOINT_CENTERED_GAIN_FOCUSED_CHECK=PASS"
echo "T_P5_023_CELL_PATH_BINDING=OPEN"
echo "SOURCE_FLOAT64_JACOBIAN_BINDING=OPEN"
echo "ANCHOR_BIAS_LEDGER=OPEN"
echo "P8_SAME_DOMAIN_COVERAGE=OPEN"
echo "ODE_CONTINUATION=OPEN"
echo "P5_P8_M4_FINAL_INTEGRATION=false"
echo "REGISTRY_MUTATION=false"
