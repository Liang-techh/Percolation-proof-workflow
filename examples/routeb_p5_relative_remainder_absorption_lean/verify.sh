#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
LEAN_FILE="$ROOT/P5RelativeRemainderAbsorption.lean"
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
  same_monomial_exact_factorization \
  same_monomial_remainder_absorption \
  absorbed_unit_has_strict_sign \
  higher_order_normalized_charge \
  higher_order_remainder_unit_margin \
  relative_remainder_abs_lt \
  relative_remainder_same_sign \
  alpha_one_cancellation_boundary \
  lower_order_contamination_factorization \
  additive_normalized_remainder_difference_budget \
  source_family_same_monomial_absorption; do
  grep -F "'RouteBP5RelativeRemainderAbsorption.$theorem' depends on axioms:" "$OUT" >/dev/null || {
    echo "missing axiom report for $theorem" >&2
    exit 3
  }
done

if grep -F "sorryAx" "$OUT" >/dev/null; then
  echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2
  exit 4
fi

echo "AXIOM_AUDIT=PASS"
echo "P5_RELATIVE_REMAINDER_ABSORPTION_FOCUSED_CHECK=PASS"
echo "EXACT_DIVISIBILITY_INTERFACE_REQUIRED=true"
echo "HIGHER_ORDER_MONOMIAL_ENVELOPE_REQUIRED=true"
echo "RELATIVE_ALPHA_STRICTLY_LT_ONE_REQUIRED=true"
echo "LIPSCHITZ_QUOTIENT_EXTENSION_NOT_INFERRED=true"
echo "SOURCE_CSE_BINDING=OPEN"
echo "FLOAT64_FD_CONTROLLER_BINDING=OPEN"
echo "P8_COVERAGE=OPEN"
echo "P5_M4_FINAL_INTEGRATION=false"
echo "REGISTRY_MUTATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_p5_relative_remainder_absorption_lean/verify.sh"
