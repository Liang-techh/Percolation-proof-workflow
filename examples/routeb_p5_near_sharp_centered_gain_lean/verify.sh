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
  "$LAKE" env lean -DwarningAsError=true "$ROOT/P5NearSharpCenteredGain.lean"
) 2>&1 | tee "$LOG"

for DECL in \
  weighted_joint_quadratic_bound_block45 \
  weighted_amgm_75_106 \
  qDissipation_nonneg \
  near_sharp_joint_centered_gain \
  abs_le_of_sq_le_sq_nonneg \
  near_sharp_scalar_residual_consumer \
  block45_near_sharp_scalar_residual_consumer \
  old_minus_new_constant_corrected \
  sharpness_bracket_width \
  lower_witness_rejects_57562365_over_1e7; do
  grep -q "RouteBP5NearSharpCenteredGain.$DECL" "$LOG" || {
    echo "FAIL: missing axiom report for $DECL" >&2
    exit 1
  }
done

if grep -Eiq 'sorryAx|declaration uses.*axiom|unknown module|error:' "$LOG"; then
  echo "AXIOM_AUDIT=FAIL"
  exit 1
fi

echo "AXIOM_AUDIT=PASS"
echo "P5_NEAR_SHARP_CENTERED_GAIN_FOCUSED_CHECK=PASS"
echo "T_P5_023_CELL_PATH_BINDING=OPEN"
echo "SOURCE_FLOAT64_JACOBIAN_BINDING=OPEN"
echo "ANCHOR_BIAS_LEDGER=OPEN"
echo "P8_SAME_DOMAIN_COVERAGE=OPEN"
echo "ODE_CONTINUATION=OPEN"
echo "P5_P8_M4_FINAL_INTEGRATION=false"
echo "REGISTRY_MUTATION=false"
