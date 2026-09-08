#!/usr/bin/env bash
# CI_PORTABLE=1
# focused branch CI replay for 巨阳仙尊 / T-P4-034
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
LEAN_FILE="$ROOT/O2SignedRectangleEnergyConsumer.lean"
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
  second_diagonal_pos \
  energy_sos_identity \
  energy_quadratic_nonnegative \
  dual_sos_identity \
  dual_quadratic_nonnegative \
  retained_dissipation_completion_identity \
  o2_error_power_retained_dissipation_completion_2x2 \
  quadratic_interval_le_endpoints \
  dual_quadratic_rectangle_le_corners \
  o2_signed_rectangle_energy_consumer \
  o2_signed_rectangle_first_exit_with_reserve \
  global_sign_dual_invariant \
  global_sign_rectangle_transport \
  absolute_bias_small_scale_identity \
  absolute_evaluator_bias_blocks_homogeneous_decay; do
  grep -F "'RouteBP4O2SignedRectangleEnergy.$theorem' depends on axioms:" "$OUT" >/dev/null || {
    echo "missing axiom report for $theorem" >&2
    exit 3
  }
done

if grep -F "sorryAx" "$OUT" >/dev/null; then
  echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2
  exit 4
fi

echo "AXIOM_AUDIT=PASS"
echo "P4_O2_SIGNED_RECTANGLE_ENERGY_FOCUSED_CHECK=PASS"
echo "FOUR_CORNER_DIVISION_FREE_GATE=true"
echo "SIGNED_INTERVAL_CORRELATION_PRESERVED=true"
echo "ACCELERATION_TO_FORCE_BRIDGE=OPEN"
echo "DEPLOYED_FLOAT64_FINAL_RESIDUAL_EXPORT=OPEN"
echo "SINGULAR_RANK_COMPATIBILITY=OPEN"
echo "P8_SAME_DOMAIN_COVERAGE=OPEN"
echo "P4_M4_FINAL_INTEGRATION=false"
echo "REGISTRY_MUTATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_p4_o2_signed_rectangle_energy_lean/verify.sh"
