#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
LEAN_FILE="$ROOT/P5InvariantPathSheetCoverage.lean"
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
  affine_center_identity \
  affine_abs_le_of_endpoint_abs_le \
  straight_segment_mem_box \
  outer_abs_of_inner_and_displacement \
  pointwise_outer_box_of_inner_and_displacement \
  abs_le_of_sq_le_aux_sq \
  pointwise_abs_speed_cap_of_square_packet \
  flowed_path_sheet_mem_of_initial_path_mem_and_forward_invariant \
  robust_storage_shift_deriv_algebra \
  inner_level_strictly_inside_outer \
  storage_shift_nonpos_iff \
  endpoint_counter_endpoints_zero \
  endpoint_counter_midpoint \
  endpoint_counter_midpoint_exits_unit_box \
  zero_tangent_energy_everywhere \
  zero_tangent_energy_does_not_certify_base_box; do
  if ! grep -F "'RouteBP5InvariantPathSheetCoverage.$theorem' depends on axioms:" "$OUT" >/dev/null \
      && ! grep -F "'RouteBP5InvariantPathSheetCoverage.$theorem' does not depend on any axioms" "$OUT" >/dev/null; then
    echo "missing axiom report for $theorem" >&2
    exit 3
  fi
done

if grep -F "sorryAx" "$OUT" >/dev/null; then
  echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2
  exit 4
fi

echo "AXIOM_AUDIT=PASS"
echo "P5_INVARIANT_PATH_SHEET_FOCUSED_CHECK=PASS"
echo "ROUTE_A_BOX_MARGIN_ALGEBRA=true"
echo "SQUARE_ONLY_SPEED_CAP=true"
echo "POINTWISE_SHEET_LIFT=true"
echo "ROUTE_B_DIVISION_FREE_SHIFT_ALGEBRA=true"
echo "ANALYTIC_SCALAR_INTEGRATION=OPEN"
echo "FIRST_EXIT_BOOTSTRAP=OPEN"
echo "GRONWALL_BASE_STORAGE_INVARIANCE=OPEN"
echo "SOURCE_TUBE_BINDING=OPEN"
echo "FLOAT64_FD_CONTROLLER_BINDING=OPEN"
echo "P8_ODE_COVERAGE=OPEN"
echo "P5_M4_FINAL_INTEGRATION=false"
echo "REGISTRY_MUTATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_p5_invariant_path_sheet_lean/verify.sh"
