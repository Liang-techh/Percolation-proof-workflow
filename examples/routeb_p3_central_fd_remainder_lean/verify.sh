#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
LEAN_FILE="$ROOT/P3CentralFDRemainder.lean"
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
  rawDefect_eq_remainder_diff \
  rawDefect_abs_le_third \
  central_fd_raw_defect_le_of_taylor_pair \
  centralFD_error_eq_raw_div \
  central_fd_error_le_sixth_third_deriv \
  shifted_stencil_contained \
  central_fd_error_uniform_of_step_cap \
  central_fd_x_cube_sharp \
  raw_defect_x_cube_sharp \
  cubic_family_same_center_two_jet \
  cubic_family_center_fd_error \
  central_fd_two_term_linear_residual_budget; do
  grep -F "'RouteBP3CentralFDRemainder.$theorem' depends on axioms:" "$OUT" >/dev/null || {
    echo "missing axiom report for $theorem" >&2
    exit 3
  }
done

if grep -F "sorryAx" "$OUT" >/dev/null; then
  echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2
  exit 4
fi

echo "AXIOM_AUDIT=PASS"
echo "P3_CENTRAL_FD_REMAINDER_FOCUSED_CHECK=PASS"
echo "TAYLOR_PACKET_ALGEBRA=true"
echo "SHARP_ONE_SIXTH_CONSTANT=true"
echo "SHIFTED_STENCIL_CONTAINMENT=true"
echo "X3_SHARPNESS_REGRESSION=true"
echo "POINTWISE_C2_OBSTRUCTION_FAMILY=true"
echo "TWO_TERM_LINEAR_RESIDUAL_HANDOFF=true"
echo "ANALYTIC_C3_TO_TAYLOR=OPEN"
echo "DEPLOYED_EVALUATOR_SOURCE_BINDING=OPEN"
echo "FLOAT64_LIBM_ROUNDING=OPEN"
echo "DOWNSTREAM_P4_P5_P8_COVERAGE=OPEN"
echo "REGISTRY_MUTATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_p3_central_fd_remainder_lean/verify.sh"
