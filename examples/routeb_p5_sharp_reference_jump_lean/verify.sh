#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
LEAN_FILE="$ROOT/P5SharpReferenceJump.lean"
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
  reference_jump_observable_eq_storage_mul_direction \
  reference_jump_direction_energy_exact \
  current_sharp_coefficient_strictly_better_than_old \
  current_eight_n_d_exact \
  storage_representer_observable_sq_le \
  le_of_sq_le_sq_of_nonneg_right \
  quadratic_translation_ball_inclusion_sq_gate \
  current_reference_jump_gate \
  reference_dwell_jump_direct_gate \
  direct_contracted_packet_strict_margin \
  outer_collar_prebudget_fails_same_packet \
  boundary_gate_equality_regression; do
  if ! grep -F "'RouteBP5SharpReferenceJump.$theorem' depends on axioms:" "$OUT" >/dev/null \
      && ! grep -F "'RouteBP5SharpReferenceJump.$theorem' does not depend on any axioms" "$OUT" >/dev/null; then
    echo "missing axiom report for $theorem" >&2
    exit 3
  fi
done

if grep -F "sorryAx" "$OUT" >/dev/null; then
  echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2
  exit 4
fi

echo "AXIOM_AUDIT=PASS"
echo "P5_SHARP_REFERENCE_JUMP_FOCUSED_CHECK=PASS"
echo "REFERENCE_REPRESENTER_BLOCK_EXPANSION=true"
echo "DIRECTION_ENERGY_A_EXACT=true"
echo "DENOMINATOR_CLEARED_JUMP_GATE=true"
echo "DIRECT_DWELL_JUMP_GATE=true"
echo "OUTER_COLLAR_PREBUDGET_STRICTLY_WEAKER_REGRESSION=true"
echo "GATE_EQUALITY_IS_BOUNDARY_ONLY=true"
echo "REFERENCE_KEY_SOURCE_BINDING=OPEN"
echo "FLOAT64_CONTROLLER_BINDING=OPEN"
echo "P8_FLOWPIPE_COVERAGE=OPEN"
echo "P5_M4_FINAL_INTEGRATION=false"
echo "REGISTRY_MUTATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_p5_sharp_reference_jump_lean/verify.sh"
