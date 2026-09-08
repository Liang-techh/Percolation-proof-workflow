#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
LEAN_FILE="$ROOT/P5CorrelatedMatrixPerturbation.lean"
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
if [[ ! -f "$LAKE_ROOT/lake-manifest.json" ]]; then
  echo "pinned lake-manifest.json missing at $LAKE_ROOT" >&2
  exit 2
fi
if [[ ! -f "$LAKE_ROOT/lean-toolchain" ]]; then
  echo "pinned lean-toolchain missing at $LAKE_ROOT" >&2
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
  branchfree_packet_trace_identity \
  branchfree_packet_det_identity \
  det2_add_exact \
  trace2_add_exact \
  mul_abs_cap \
  det2_add_lower_of_abs_bounds \
  trace2_add_lower_of_abs_bounds \
  abs_sub_sub_le \
  abs_sub_sub_sub_le \
  branchfree_packet_error_entries \
  branchfree_packet_error_abs_bounds \
  sym2_scaled_qf_completion_identity \
  sym2_scaled_qf_nonneg_of_trace_det4 \
  affine_packet_identity \
  affine_energy_le_of_packet_trace_det \
  branchfree_of_nominal_correlated_reserve \
  branchfree_of_nominal_entry_radius_reserve \
  rank_one_correlated_error_regression \
  rank_one_entry_radius_penalty; do
  grep -F "'RouteBP5CorrelatedMatrixPerturbation.$theorem' depends on axioms:" "$OUT" >/dev/null || {
    echo "missing axiom report for $theorem" >&2
    exit 3
  }
done

if grep -F "sorryAx" "$OUT" >/dev/null; then
  echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2
  exit 4
fi

echo "AXIOM_AUDIT=PASS"
echo "P5_CORRELATED_MATRIX_PERTURBATION_FOCUSED_CHECK=PASS"
echo "CORRELATED_CDET_LANE_PRESERVED=true"
echo "ENTRY_RADIUS_FALLBACK_ONLY=true"
echo "SIGNED_SIGMA_REQUIRED=true"
echo "SAME_KEY_COMPOSITION_REQUIRED=true"
echo "SOURCE_NOMINAL_ERROR_BINDING=OPEN"
echo "FLOAT64_OUTWARD_ROUNDING=OPEN"
echo "P8_ODE_COVERAGE=OPEN"
echo "P5_M4_FINAL_INTEGRATION=false"
echo "REGISTRY_MUTATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_p5_correlated_matrix_perturbation_lean/verify.sh"
