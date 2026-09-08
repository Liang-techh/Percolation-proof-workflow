#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
LEAN_FILE="$ROOT/P5MultipleRootCluster.lean"
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
  signed_error_bounds \
  multiple_contact_root_mul_pow_le \
  multiple_contact_root_inside_of_strict \
  multiple_contact_root_cluster \
  multiple_contact_right_outer_reserve \
  multiple_contact_left_outer_reserve_even \
  multiple_contact_left_outer_reserve_odd \
  equality_boundary_can_touch \
  double_contact_positive_shift_no_root \
  double_contact_negative_shift_factor \
  double_contact_negative_shift_roots \
  lower_order_perturbation_factor \
  double_contact_linear_unfolding \
  double_contact_linear_unfolding_roots; do
  grep -F "'RouteBP5MultipleRootCluster.$theorem' depends on axioms:" "$OUT" >/dev/null || {
    echo "missing axiom report for $theorem" >&2
    exit 3
  }
done

if grep -F "sorryAx" "$OUT" >/dev/null; then
  echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2
  exit 4
fi

echo "AXIOM_AUDIT=PASS"
echo "P5_MULTIPLE_ROOT_CLUSTER_FOCUSED_CHECK=PASS"
echo "RADICAL_FREE_CLUSTER_GATE=true"
echo "OUTER_SIGN_PARITY_GATE=true"
echo "UNRESOLVED_MIDDLE_CLUSTER=true"
echo "UNIQUE_RECENTERING_CLAIM=false"
echo "IVT_EXISTENCE_LAYER=OPEN"
echo "DEPLOYED_SOURCE_FLOAT64_BINDING=OPEN"
echo "P8_ODE_COVERAGE=OPEN"
echo "P5_M4_FINAL_INTEGRATION=false"
echo "REGISTRY_MUTATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_p5_multiple_root_cluster_lean/verify.sh"
