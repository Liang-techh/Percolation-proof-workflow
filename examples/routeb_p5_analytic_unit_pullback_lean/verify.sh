#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
LEAN_FILE="$ROOT/P5AnalyticUnitPullback.lean"
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
  positive_multiplier_zero_iff \
  positive_unit_does_not_cancel_jump \
  lower_margin_implies_nonzero \
  worked_unit_pullback_identity \
  worked_unit_den_pos \
  worked_unit_lower \
  worked_unit_upper \
  worked_unit_difference_identity \
  worked_unit_lipschitz \
  triple_product_abs_bound \
  triple_product_difference_identity \
  unit_contact_times_reduced_lipschitz \
  hidden_zero_no_uniform_margin \
  hidden_zero_not_unit_counterexample; do
  grep -F "'RouteBP5AnalyticUnitPullback.$theorem' depends on axioms:" "$OUT" >/dev/null || {
    echo "missing axiom report for $theorem" >&2
    exit 3
  }
done

if grep -F "sorryAx" "$OUT" >/dev/null; then
  echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2
  exit 4
fi

echo "AXIOM_AUDIT=PASS"
echo "P5_ANALYTIC_UNIT_PULLBACK_FOCUSED_CHECK=PASS"
echo "POSITIVE_UNIT_CANNOT_HIDE_ZERO_OR_JUMP=true"
echo "WORKED_RATIONAL_UNIT_ENVELOPE=true"
echo "THREE_FACTOR_LIPSCHITZ_CONSUMER=true"
echo "HIDDEN_ZERO_FAIL_CLOSED_REGRESSION=true"
echo "GENERAL_ZPOW_FINSET_PULLBACK=OPEN"
echo "DEPLOYED_CSE_FACTOR_SOURCE_BINDING=OPEN"
echo "FLOAT64_CONTROLLER_SEMANTICS=OPEN"
echo "P8_ODE_COVERAGE=OPEN"
echo "P5_M4_FINAL_INTEGRATION=false"
echo "REGISTRY_MUTATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_p5_analytic_unit_pullback_lean/verify.sh"
