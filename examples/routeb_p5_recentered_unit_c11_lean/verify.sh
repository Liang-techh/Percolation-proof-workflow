#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
LEAN_FILE="$ROOT/P5RecenteredUnitC11.lean"
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
  segment_argument_sub \
  abs_segment_argument_sub \
  segmentAverage_at_root \
  sigma_mul_segmentAverage \
  segment_average_bounds \
  segment_average_signed_bounds \
  segment_average_lipschitz_twice \
  recentered_unit_exact_factorization \
  recentered_unit_eq_segmentAverage_of_increment \
  root_graph_division_free_to_lipschitz \
  parameterized_segment_argument_bound \
  sharp_half_quadratic_regression; do
  grep -F "'RouteBP5RecenteredUnitC11.$theorem' depends on axioms:" "$OUT" >/dev/null || {
    echo "missing axiom report for $theorem" >&2
    exit 3
  }
done

if grep -F "sorryAx" "$OUT" >/dev/null; then
  echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2
  exit 4
fi

echo "AXIOM_AUDIT=PASS"
echo "P5_RECENTERED_UNIT_C11_FOCUSED_CHECK=PASS"
echo "SHARP_HALF_LIPSCHITZ_MULTIPLICATION_ONLY=true"
echo "FTC_INCREMENT_IDENTITY_REQUIRED=true"
echo "DEPLOYED_SOURCE_CSE_BINDING=OPEN"
echo "FLOAT64_FD_CONTROLLER_BINDING=OPEN"
echo "P8_COVERAGE=OPEN"
echo "P5_M4_FINAL_INTEGRATION=false"
echo "REGISTRY_MUTATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_p5_recentered_unit_c11_lean/verify.sh"
