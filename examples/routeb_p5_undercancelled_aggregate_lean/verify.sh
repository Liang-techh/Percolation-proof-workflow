#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
LEAN_FILE="$ROOT/P5UndercancelledAggregate.lean"
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
  net_order_nonnegative_iff \
  net_order_negative_iff \
  aggregate_integer_excess_identity \
  aggregate_extension_agrees_off_contact \
  aggregate_contact_safe_of_net_nonnegative \
  zero_net_order_finite_scale \
  positive_net_order_zero_extension \
  negative_net_order_reciprocal_form \
  reciprocal_power_unbounded_right \
  negative_net_order_unbounded \
  undercancelled_product_exact_rescue \
  zero_net_order_exact_example \
  negative_net_order_exact_example \
  monomial_pullback_exponent_transport \
  additive_cancellation_bounded_iff \
  additive_noncancellation_unbounded \
  exact_vanishing_atom_rescue; do
  grep -F "'RouteBP5UndercancelledAggregate.$theorem' depends on axioms:" "$OUT" >/dev/null || {
    echo "missing axiom report for $theorem" >&2
    exit 3
  }
done

if grep -F "sorryAx" "$OUT" >/dev/null; then
  echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2
  exit 4
fi

echo "AXIOM_AUDIT=PASS"
echo "P5_UNDERCANCELLED_AGGREGATE_FOCUSED_CHECK=PASS"
echo "AGGREGATE_FIRST_CONTACT_ORDER_GATE=true"
echo "NEGATIVE_NET_ORDER_UNBOUNDED=true"
echo "ADDITIVE_PRINCIPAL_CANCELLATION_EXACT=true"
echo "FINITE_ORDER_ASYMPTOTIC_BINDING=OPEN"
echo "ALGEBRAIC_GCD_DEPENDENCE=OPEN"
echo "DEPLOYED_SOURCE_FLOAT64_BINDING=OPEN"
echo "P8_ODE_COVERAGE=OPEN"
echo "P5_M4_FINAL_INTEGRATION=false"
echo "REGISTRY_MUTATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_p5_undercancelled_aggregate_lean/verify.sh"
