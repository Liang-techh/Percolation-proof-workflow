#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
LEAN_FILE="$ROOT/P5InitialReferenceBridge.lean"
EXPECTED_TOOLCHAIN="$(tr -d '\r\n' < "$ROOT/lean-toolchain")"

command -v lake >/dev/null 2>&1 || { echo "lake not found on PATH" >&2; exit 2; }
command -v lean >/dev/null 2>&1 || { echo "lean not found on PATH" >&2; exit 2; }
[[ -d "$LAKE_ROOT" ]] || { echo "local_fkg Lake environment not found at $LAKE_ROOT" >&2; exit 2; }
[[ -f "$LAKE_ROOT/lake-manifest.json" ]] || { echo "pinned lake-manifest.json missing at $LAKE_ROOT" >&2; exit 2; }

ACTUAL_TOOLCHAIN="$(tr -d '\r\n' < "$LAKE_ROOT/lean-toolchain")"
[[ "$ACTUAL_TOOLCHAIN" == "$EXPECTED_TOOLCHAIN" ]] || {
  echo "toolchain mismatch: sidecar=$EXPECTED_TOOLCHAIN local_fkg=$ACTUAL_TOOLCHAIN" >&2
  exit 2
}

if grep -nE '\b(sorry|admit)\b' "$LEAN_FILE"; then
  echo "PLACEHOLDER_SCAN=FAIL" >&2
  exit 4
fi
echo "PLACEHOLDER_SCAN=PASS"

OUT="$(mktemp)"
trap 'rm -f "$OUT"' EXIT
(
  cd "$LAKE_ROOT"
  lake env lean -DwarningAsError=true "$LEAN_FILE"
) 2>&1 | tee "$OUT"

for theorem in \
  qEnergy_nonneg \
  vEnergy_nonneg \
  pFull_split \
  hybridBudget_eq_full_of_block_match \
  weighted_initial_ball_bound \
  pFull_le_27_over_800_of_ball \
  pFull_lt_28_over_5_of_ball \
  hybridBudget_le_27_over_800_of_initial_match \
  hybridBudget_lt_28_over_5_of_initial_match \
  anchor_eq_self_of_block_match \
  centeredResidual_eq_zero_of_initial_match \
  anchorBias_eq_actual_minus_lbar_of_initial_match \
  nominalResidual_eq_zero_of_graph \
  same_qv_input_different_acceleration_residual; do
  if ! grep -F "'RouteBP5InitialReferenceBridge.$theorem' depends on axioms:" "$OUT" >/dev/null \
      && ! grep -F "'RouteBP5InitialReferenceBridge.$theorem' does not depend on any axioms" "$OUT" >/dev/null; then
    echo "missing axiom report for $theorem" >&2
    exit 3
  fi
done

if grep -F "sorryAx" "$OUT" >/dev/null; then
  echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2
  exit 4
fi

echo "AXIOM_AUDIT=PASS"
echo "P5_INITIAL_REFERENCE_BRIDGE_FOCUSED_CHECK=PASS"
echo "INITIAL_HYBRID_EQUALS_FULL=true"
echo "INITIAL_BALL_27_OVER_800=true"
echo "SAME_SOURCE_ANCHOR_SELF=true"
echo "CENTERED_RESIDUAL_INITIAL_ZERO=true"
echo "NOMINAL_GRAPH_IMPLIES_LBAR_ZERO=true"
echo "POINTWISE_QV_WITHOUT_ACCELERATION_IS_INSUFFICIENT=true"
echo "GENERAL_TIME_ODE_UNIQUENESS=OPEN"
echo "REFERENCE_KEY_SOURCE_BINDING=OPEN"
echo "FLOAT64_CONTROLLER_BINDING=OPEN"
echo "P8_FLOWPIPE_COVERAGE=OPEN"
echo "P5_M4_FINAL_INTEGRATION=false"
echo "REGISTRY_MUTATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_p5_initial_reference_bridge_lean/verify.sh"
