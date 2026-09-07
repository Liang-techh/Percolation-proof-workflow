#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
LEAN_FILE="$ROOT/P5EightNinthsCoercivity.lean"
EXPECTED_TOOLCHAIN="$(tr -d '\r\n' < "$ROOT/lean-toolchain")"

command -v lake >/dev/null 2>&1 || {
  echo "lake not found on PATH" >&2
  exit 2
}
command -v lean >/dev/null 2>&1 || {
  echo "lean not found on PATH" >&2
  exit 2
}

if [[ ! -d "$LAKE_ROOT" ]]; then
  echo "local_fkg Lake environment not found at $LAKE_ROOT" >&2
  exit 2
fi

ACTUAL_TOOLCHAIN="$(tr -d '\r\n' < "$LAKE_ROOT/lean-toolchain")"
if [[ "$ACTUAL_TOOLCHAIN" != "$EXPECTED_TOOLCHAIN" ]]; then
  echo "toolchain mismatch: sidecar=$EXPECTED_TOOLCHAIN local_fkg=$ACTUAL_TOOLCHAIN" >&2
  exit 2
fi

OUT="$(mktemp)"
trap 'rm -f "$OUT"' EXIT

(
  cd "$LAKE_ROOT"
  lake env lean -DwarningAsError=true "$LEAN_FILE"
) 2>&1 | tee "$OUT"

for theorem in \
  nine_square_gap_identity \
  nine_square_coefficients_positive \
  q_ge_eight_ninths_storage \
  improved_iss_refinement \
  ultimate_gain_constant \
  decay_improvement_factor \
  improved_barrier_inward \
  quarter_barrier_inward \
  initial_coefficient_lt_one_twelfth \
  parameter_tube_boundary_inward \
  one_twelfth_parameter_tube_gate \
  physical_slack_to_one_twelfth_gate \
  slack_feasibility_necessity \
  exact_feasibility_factor; do
  grep -F "'RouteBP5EightNinthsCoercivity.$theorem' depends on axioms:" "$OUT" >/dev/null || {
    echo "missing axiom report for $theorem" >&2
    exit 3
  }
done

if grep -F "sorryAx" "$OUT" >/dev/null; then
  echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2
  exit 4
fi

echo "AXIOM_AUDIT=PASS"
echo "P5_EIGHT_NINTHS_COERCIVITY_FOCUSED_CHECK=PASS"
echo "SOURCE_RESIDUAL_GAIN_TABLE=OPEN"
echo "SOURCE_FLOAT64_INCREMENTAL_SEMANTICS=OPEN"
echo "P8_SAME_DOMAIN_COVERAGE=OPEN"
echo "ODE_FIRST_EXIT_CONTINUATION=OPEN"
echo "P5_P8_M4_FINAL_INTEGRATION=false"
echo "REGISTRY_MUTATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_p5_eight_ninths_coercivity_lean/verify.sh"
