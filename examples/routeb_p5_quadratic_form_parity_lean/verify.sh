#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
LEAN_FILE="$ROOT/P5QuadraticFormParity.lean"
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
  balanced_pair_same_parity_cancel \
  balanced_pair_opposite_parity_flip \
  positive_excess_pair_vanishes_at_zero \
  opposite_parity_quadratic_jump \
  opposite_parity_cross_zero_invariant \
  particular_contact_invariance_iff \
  opposite_parity_gate_iff_universal_invariant \
  all_odd_quadratic_invariant \
  diagonal_squares_ignore_sign \
  counterexample_matrix_coercive \
  quadratic_form_parity_counterexample \
  square_only_pass_does_not_imply_mixed_invariance \
  accidental_contact_cancellation_not_structural \
  mixed_quadratic_consumer_of_parity_gate; do
  grep -F "'RouteBP5QuadraticFormParity.$theorem' depends on axioms:" "$OUT" >/dev/null || {
    echo "missing axiom report for $theorem" >&2
    exit 3
  }
done

if grep -F "sorryAx" "$OUT" >/dev/null; then
  echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2
  exit 4
fi

echo "AXIOM_AUDIT=PASS"
echo "P5_QUADRATIC_FORM_PARITY_FOCUSED_CHECK=PASS"
echo "TWO_CHANNEL_STRUCTURAL_IFF=true"
echo "MIXED_CROSS_TERM_GATE_EXPLICIT=true"
echo "DIAGONAL_SQUARE_LIFT_UNSOUND_WITHOUT_GATE=true"
echo "FINITE_INDEX_MATRIX_THEOREM=OPEN"
echo "QUANTITATIVE_LIPSCHITZ_TRANSPORT=OPEN"
echo "DEPLOYED_SOURCE_FLOAT64_BINDING=OPEN"
echo "P8_ODE_COVERAGE=OPEN"
echo "P5_M4_FINAL_INTEGRATION=false"
echo "REGISTRY_MUTATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_p5_quadratic_form_parity_lean/verify.sh"
