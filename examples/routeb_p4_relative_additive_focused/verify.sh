#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXAMPLES="$(cd "$ROOT/.." && pwd)"
SRC="${P4_RELATIVE_ADDITIVE_SRC:-$EXAMPLES/routeb_p5_feasible_cone_spn_proof_attempt}"
LAKE_ROOT="${LAKE_ROOT:-$EXAMPLES/local_fkg}"

command -v lake >/dev/null 2>&1 || { echo "lake not found on PATH" >&2; exit 2; }
command -v lean >/dev/null 2>&1 || { echo "lean not found on PATH" >&2; exit 2; }
[[ -d "$LAKE_ROOT" ]] || { echo "local_fkg Lake environment not found at $LAKE_ROOT" >&2; exit 2; }
[[ -f "$LAKE_ROOT/lean-toolchain" ]] || { echo "pinned lean-toolchain missing at $LAKE_ROOT/lean-toolchain" >&2; exit 2; }
[[ -f "$LAKE_ROOT/lake-manifest.json" ]] || { echo "pinned lake-manifest missing at $LAKE_ROOT/lake-manifest.json" >&2; exit 2; }

echo "LEAN_TOOLCHAIN=$(tr -d '\r\n' < "$LAKE_ROOT/lean-toolchain")"
echo "LAKE_MANIFEST=$LAKE_ROOT/lake-manifest.json"

for f in \
  NEW_P4_032_BlockDefects.lean \
  NEW_P4_032_DefectNormBudget.lean \
  NEW_P4_032_WeightedThreeTerm.lean \
  NEW_P4_032_RelativeAdditive.lean; do
  [[ -f "$SRC/$f" ]] || { echo "missing source $SRC/$f" >&2; exit 2; }
done

if grep -nE '\b(sorry|admit)\b' "$SRC/NEW_P4_032_RelativeAdditive.lean"; then
  echo "PLACEHOLDER_SCAN=FAIL" >&2
  exit 4
fi
echo "PLACEHOLDER_SCAN=PASS"

BUILD="$(mktemp -d)"
OUT="$(mktemp)"
trap 'rm -rf "$BUILD" "$OUT"' EXIT
BASE_LEAN_PATH="$(cd "$LAKE_ROOT" && lake env printenv LEAN_PATH)"

compile_module() {
  local module="$1"
  (
    cd "$SRC"
    LEAN_PATH="$BUILD:$BASE_LEAN_PATH" \
      lean -DwarningAsError=true -o "$BUILD/${module%.lean}.olean" "$module"
  )
}

compile_module NEW_P4_032_BlockDefects.lean
compile_module NEW_P4_032_DefectNormBudget.lean
compile_module NEW_P4_032_WeightedThreeTerm.lean
(
  cd "$SRC"
  LEAN_PATH="$BUILD:$BASE_LEAN_PATH" \
    lean -DwarningAsError=true NEW_P4_032_RelativeAdditive.lean
) 2>&1 | tee "$OUT"

for theorem in \
  effective_coefficients_nonnegative \
  affine_budget_identity \
  weighted_budget_le_relative_additive \
  relative_additive_budget_nonnegative \
  consume_weighted_budget \
  force_relative_additive \
  accel_relative_additive \
  zero_bias_corollary; do
  grep -F "'RouteBP4032RelativeAdditive.$theorem' depends on axioms:" "$OUT" >/dev/null || {
    echo "missing axiom report for $theorem" >&2
    exit 3
  }
done

if grep -F "sorryAx" "$OUT" >/dev/null; then
  echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2
  exit 4
fi

echo "AXIOM_AUDIT=PASS"
echo "P4_RELATIVE_ADDITIVE_FOCUSED_CHECK=PASS"
echo "RHO_EFF_BIAS_EFF_TYPED=CHECKED"
echo "SQRT_DEPENDENCE=false"
echo "SOURCE_BINDING=OPEN"
echo "COVERAGE=OPEN"
echo "ADMISSION_MUTATION=false"
echo "P4_M4_FINAL_INTEGRATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_p4_relative_additive_focused/verify.sh"
