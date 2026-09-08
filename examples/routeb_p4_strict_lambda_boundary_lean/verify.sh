#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
LEAN_FILE="$ROOT/P4StrictLambdaBoundary.lean"
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

if grep -nE '(^|[^A-Za-z])(sorry|admit)([^A-Za-z]|$)' "$LEAN_FILE"; then
  echo "PLACEHOLDER_SCAN=FAIL" >&2
  exit 3
fi

echo "PLACEHOLDER_SCAN=PASS"

OUT="$(mktemp)"
trap 'rm -f "$OUT"' EXIT

(
  cd "$LAKE_ROOT"
  lake env lean -DwarningAsError=true "$LEAN_FILE"
) 2>&1 | tee "$OUT"

for theorem in \
  strictPair_implies_weakPair \
  boundaryPair_implies_weakPair \
  boundaryPair_not_strict \
  weak_not_strict_iff_boundary \
  touching_pair_is_boundary \
  touching_pair_weak_not_strict \
  touching_rows_common_weak_forces_two \
  touching_rows_at_two \
  touching_rows_no_positive_common_reserve \
  perturb_gap_identity \
  positive_perturbation_strict \
  zero_perturbation_boundary \
  negative_perturbation_not_weak \
  perturbation_discriminant_identity \
  positive_tenth_exact_reserve; do
  grep -F "'RouteBP4StrictLambdaBoundary.$theorem'" "$OUT" >/dev/null || {
    echo "missing axiom report for $theorem" >&2
    exit 4
  }
done

if grep -F "sorryAx" "$OUT" >/dev/null; then
  echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2
  exit 5
fi

echo "AXIOM_AUDIT=PASS"
echo "P4_STRICT_LAMBDA_BOUNDARY_FOCUSED_CHECK=PASS"
echo "FINITE_FAMILY_OPEN_INTERVAL_HELLY=OPEN"
echo "CONCRETE_P4_SOURCE_FLOAT64_BINDING=OPEN"
echo "P8_DOMAIN_TRAJECTORY_COVERAGE=OPEN"
echo "P4_M4_FINAL_INTEGRATION=false"
echo "REGISTRY_MUTATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_p4_strict_lambda_boundary_lean/verify.sh"
