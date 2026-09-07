#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXAMPLES="$(cd "$ROOT/.." && pwd)"
SRC="${P4_WEIGHTED_SRC:-$EXAMPLES/routeb_p5_feasible_cone_spn_proof_attempt}"
LAKE_ROOT="${LAKE_ROOT:-$EXAMPLES/local_fkg}"
EXPECTED_TOOLCHAIN="$(tr -d '\r\n' < "$ROOT/lean-toolchain")"

command -v lake >/dev/null 2>&1 || { echo "lake not found on PATH" >&2; exit 2; }
command -v lean >/dev/null 2>&1 || { echo "lean not found on PATH" >&2; exit 2; }
[[ -d "$LAKE_ROOT" ]] || { echo "local_fkg Lake environment not found at $LAKE_ROOT" >&2; exit 2; }
[[ -f "$LAKE_ROOT/lake-manifest.json" ]] || { echo "pinned lake-manifest missing at $LAKE_ROOT/lake-manifest.json" >&2; exit 2; }

ACTUAL_TOOLCHAIN="$(tr -d '\r\n' < "$LAKE_ROOT/lean-toolchain")"
[[ "$ACTUAL_TOOLCHAIN" == "$EXPECTED_TOOLCHAIN" ]] || {
  echo "toolchain mismatch: focused=$EXPECTED_TOOLCHAIN local_fkg=$ACTUAL_TOOLCHAIN" >&2
  exit 2
}

for f in NEW_P4_032_BlockDefects.lean NEW_P4_032_DefectNormBudget.lean NEW_P4_032_WeightedThreeTerm.lean; do
  [[ -f "$SRC/$f" ]] || { echo "missing source $SRC/$f" >&2; exit 2; }
done

BUILD="$(mktemp -d)"
OUT="$(mktemp)"
trap 'rm -rf "$BUILD" "$OUT"' EXIT
BASE_LEAN_PATH="$(cd "$LAKE_ROOT" && lake env printenv LEAN_PATH)"

compile_module() {
  local module="$1"
  (
    cd "$LAKE_ROOT"
    LEAN_PATH="$BUILD:$BASE_LEAN_PATH" \
      lean -DwarningAsError=true -o "$BUILD/${module%.lean}.olean" "$SRC/$module"
  )
}

compile_module NEW_P4_032_BlockDefects.lean
compile_module NEW_P4_032_DefectNormBudget.lean
(
  cd "$LAKE_ROOT"
  LEAN_PATH="$BUILD:$BASE_LEAN_PATH" \
    lean -DwarningAsError=true "$SRC/NEW_P4_032_WeightedThreeTerm.lean"
) 2>&1 | tee "$OUT"

for theorem in \
  reciprocal_iff_polynomial \
  ofPolynomial \
  weighted_scalar \
  weighted_three_term_norm_sq \
  routeB_port_defect_quadratic_budget \
  action_squared_budget \
  force_accel_term_identity \
  force_defect_budget \
  accel_defect_budget; do
  grep -F "'RouteBP4032WeightedThreeTerm.$theorem' depends on axioms:" "$OUT" >/dev/null || {
    echo "missing axiom report for $theorem" >&2
    exit 3
  }
done

if grep -F "sorryAx" "$OUT" >/dev/null; then
  echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2
  exit 4
fi

echo "AXIOM_AUDIT=PASS"
echo "P4_WEIGHTED_THREE_TERM_FOCUSED_CHECK=PASS"
echo "FORCE_ACCEL_TYPED_DISTINCTION=PRESERVED"
echo "SOURCE_BINDING=OPEN"
echo "COVERAGE=OPEN"
echo "ADMISSION_MUTATION=false"
echo "P4_M4_FINAL_INTEGRATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_p4_weighted_three_term_focused/verify.sh"
