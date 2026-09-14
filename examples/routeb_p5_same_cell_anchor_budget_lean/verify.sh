#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
LEAN_FILE="$ROOT/P5SameCellAnchorBudget.lean"
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
  second_jet_energy_le_of_lower_gain \
  same_cell_graph_affine_anchor_budget_of_four_mul \
  cell_radius_anchor_budget \
  abs_lower_of_approx_left_inverse \
  scalar_lower_gain_sq_of_approx_left_inverse \
  preconditioned_anchor_budget \
  cubic_anchor_second_zero \
  cubic_anchor_affine_remainder_one \
  anchor_only_second_jet_is_insufficient_regression \
  scalar_eps_anchor_affine_remainder_exact \
  nonsingularity_alone_no_uniform_anchor_budget; do
  if ! grep -F "'RouteBP5SameCellAnchorBudget.$theorem' depends on axioms:" "$OUT" >/dev/null \
      && ! grep -F "'RouteBP5SameCellAnchorBudget.$theorem' does not depend on any axioms" "$OUT" >/dev/null; then
    echo "missing axiom report for $theorem" >&2
    exit 3
  fi
done

if grep -F "sorryAx" "$OUT" >/dev/null; then
  echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2
  exit 4
fi

echo "AXIOM_AUDIT=PASS"
echo "P5_SAME_CELL_ANCHOR_BUDGET_FOCUSED_CHECK=PASS"
echo "DIVISION_FREE_ANCHOR_GATE=true"
echo "SCALAR_PRECONDITIONER_LOWER_GAIN=true"
echo "ANCHOR_ONLY_CURVATURE_REJECTED=true"
echo "NONSINGULARITY_ONLY_BUDGET_REJECTED=true"
echo "D2M_D2R_J2_SOURCE_BINDING=OPEN"
echo "WHOLE_PHYSICAL_SEGMENT_C2_COVERAGE=OPEN"
echo "TAYLOR_JENSEN_ANALYTIC_REMAINDER=OPEN"
echo "FLOAT64_CONTROLLER_BINDING=OPEN"
echo "P8_FLOWPIPE_COVERAGE=OPEN"
echo "REGISTRY_MUTATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_p5_same_cell_anchor_budget_lean/verify.sh"
