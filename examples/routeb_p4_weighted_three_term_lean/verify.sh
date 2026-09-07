#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$ROOT/../.." && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$REPO_ROOT/examples/local_fkg}"
SRC_DIR="$REPO_ROOT/examples/routeb_p5_feasible_cone_spn_proof_attempt"
LEAN_BASENAME="NEW_P4_032_WeightedThreeTerm.lean"
LEAN_FILE="$SRC_DIR/$LEAN_BASENAME"
EXPECTED_TOOLCHAIN="$(tr -d '\r\n' < "$REPO_ROOT/lean-toolchain")"

command -v lake >/dev/null 2>&1 || {
  echo "lake not found on PATH" >&2
  exit 2
}
command -v lean >/dev/null 2>&1 || {
  echo "lean not found on PATH" >&2
  exit 2
}

for required in "$LAKE_ROOT/lake-manifest.json" "$LAKE_ROOT/lean-toolchain" "$LEAN_FILE"; do
  [[ -f "$required" ]] || {
    echo "required pinned input missing: $required" >&2
    exit 2
  }
done

ACTUAL_TOOLCHAIN="$(tr -d '\r\n' < "$LAKE_ROOT/lean-toolchain")"
if [[ "$ACTUAL_TOOLCHAIN" != "$EXPECTED_TOOLCHAIN" ]]; then
  echo "toolchain mismatch: repo=$EXPECTED_TOOLCHAIN local_fkg=$ACTUAL_TOOLCHAIN" >&2
  exit 2
fi

OUT="$(mktemp)"
trap 'rm -f "$OUT"' EXIT

(
  cd "$LAKE_ROOT"
  lake env bash -eu -c 'cd "$1"; lean -DwarningAsError=true "$2"' _ "$SRC_DIR" "$LEAN_BASENAME"
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

if grep -nE '(^|[^[:alnum:]_])(sorry|admit)([^[:alnum:]_]|$)' "$LEAN_FILE" >/dev/null; then
  echo "PLACEHOLDER_SCAN=FAIL target contains sorry/admit" >&2
  exit 5
fi

echo "AXIOM_AUDIT=PASS"
echo "PLACEHOLDER_SCAN=PASS"
echo "P4_WEIGHTED_THREE_TERM_FOCUSED_CHECK=PASS"
echo "FORCE_ACCEL_TYPES_PRESERVED=true"
echo "SOURCE_IDENTITY_COVERAGE_FLOAT64=OPEN"
echo "P4_M4_FINAL_INTEGRATION=false"
echo "REGISTRY_MUTATION=false"
