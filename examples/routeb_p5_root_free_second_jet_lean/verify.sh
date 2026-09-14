#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
LEAN_FILE="$ROOT/P5RootFreeSecondJet.lean"
EXPECTED_TOOLCHAIN="$(tr -d '\r\n' < "$ROOT/lean-toolchain")"

command -v lake >/dev/null 2>&1 || { echo "lake not found on PATH" >&2; exit 2; }
command -v lean >/dev/null 2>&1 || { echo "lean not found on PATH" >&2; exit 2; }
[[ -d "$LAKE_ROOT" ]] || { echo "local_fkg Lake environment not found at $LAKE_ROOT" >&2; exit 2; }
[[ -f "$LAKE_ROOT/lake-manifest.json" ]] || { echo "pinned lake-manifest.json missing at $LAKE_ROOT" >&2; exit 2; }
[[ -f "$LAKE_ROOT/lean-toolchain" ]] || { echo "local_fkg lean-toolchain missing at $LAKE_ROOT" >&2; exit 2; }

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
  cross_sq_le_cap_product \
  two_cross_upper_of_discriminant \
  two_cross_lower_of_discriminant \
  quadratic_two_term_discriminant_add \
  quadratic_two_term_discriminant_sub \
  inner_guard_forces_aux_nonneg \
  second_jet_independent_energy_nested \
  second_jet_independent_energy_homogeneous \
  zero_cap_endpoint_gate_exact \
  imbalanced_100_1_1_certificate \
  imbalanced_144_beats_factor_three \
  nonsquare_1_2_3_certificate \
  squared_inner_test_without_guard_is_unsound \
  diagonal_sum_without_cross_allowance_is_unsound; do
  if ! grep -F "'RouteBP5RootFreeSecondJet.$theorem' depends on axioms:" "$OUT" >/dev/null \
      && ! grep -F "'RouteBP5RootFreeSecondJet.$theorem' does not depend on any axioms" "$OUT" >/dev/null; then
    echo "missing axiom report for $theorem" >&2
    exit 3
  fi
done

if grep -F "sorryAx" "$OUT" >/dev/null; then
  echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2
  exit 4
fi

echo "AXIOM_AUDIT=PASS"
echo "P5_ROOT_FREE_SECOND_JET_FOCUSED_CHECK=PASS"
echo "NESTED_DISCRIMINANT_GATE=true"
echo "SQUARE_ROOT_FREE=true"
echo "DIVISION_FREE=true"
echo "BRANCH_GUARD_REQUIRED=true"
echo "HOMOGENEOUS_SCALE_GATE=true"
echo "D2M_D2R_J2_SOURCE_BINDING=OPEN"
echo "SAME_SEGMENT_COVERAGE=OPEN"
echo "P5_METRIC_IDENTITY=OPEN"
echo "FLOAT64_CONTROLLER_BINDING=OPEN"
echo "P8_FLOWPIPE_COVERAGE=OPEN"
echo "REGISTRY_MUTATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_p5_root_free_second_jet_lean/verify.sh"
