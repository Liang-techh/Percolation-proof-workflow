#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
LEAN_FILE="$ROOT/P4RationalLambdaGuard.lean"
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
  quadratic_chord_identity \
  convex_quadratic_endpoint_interval \
  convex_quadratic_on_interval \
  common_lambda_interval \
  common_fixed_lambda_interval \
  quadratic_center_plus_identity \
  quadratic_center_minus_identity \
  symmetric_rounding_guard \
  rounding_preserves_lambda_gt_one \
  source_envelope_quadratic_le \
  source_envelope_common_lambda_interval \
  concave_endpoint_failure \
  midpoint_margin_not_global \
  negative_shift_envelope_failure; do
  grep -F "'RouteBP4RationalLambdaGuard.$theorem'" "$OUT" >/dev/null || {
    echo "missing axiom report for $theorem" >&2
    exit 4
  }
done

if grep -F "sorryAx" "$OUT" >/dev/null; then
  echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2
  exit 5
fi

echo "AXIOM_AUDIT=PASS"
echo "P4_RATIONAL_LAMBDA_GUARD_FOCUSED_CHECK=PASS"
echo "P4_CONCRETE_DH_SOURCE_COEFFICIENT_BINDING=OPEN"
echo "FLOAT64_REALIZATION_CONTAINMENT=OPEN"
echo "P8_DOMAIN_TRAJECTORY_COVERAGE=OPEN"
echo "P4_M4_FINAL_INTEGRATION=false"
echo "REGISTRY_MUTATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_p4_rational_lambda_guard_lean/verify.sh"
