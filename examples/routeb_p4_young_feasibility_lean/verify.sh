#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
LEAN_FILE="$ROOT/P4YoungFeasibility.lean"
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

OUT="$(mktemp)"
trap 'rm -f "$OUT"' EXIT

(
  cd "$LAKE_ROOT"
  lake env lean -DwarningAsError=true "$LEAN_FILE"
) 2>&1 | tee "$OUT"

for theorem in \
  young_gap_mul_identity \
  young_scalar_budget_mul_iff \
  young_scalar_discriminant_necessary \
  young_theta_gap_identity \
  young_scalar_discriminant_constructive \
  young_lambda_gap_identity \
  young_scalar_lambda_constructive \
  young_scalar_strict_margin_constructive \
  young_scalar_strict_extra_reserve \
  rational_example_sharp_vs_theta_one \
  obstruction_example_no_theta; do
  grep -F "'RouteBP4YoungFeasibility.$theorem' depends on axioms:" "$OUT" >/dev/null || {
    echo "missing axiom report for $theorem" >&2
    exit 3
  }
done

if grep -F "sorryAx" "$OUT" >/dev/null; then
  echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2
  exit 4
fi

echo "AXIOM_AUDIT=PASS"
echo "P4_YOUNG_FEASIBILITY_FOCUSED_CHECK=PASS"
echo "P4_CONCRETE_A_P_D_M_SOURCE_BINDING=OPEN"
echo "P4_SHARED_LAMBDA_MULTIROW=OPEN"
echo "TRUE_DH_FLOAT64_SEMANTICS=OPEN"
echo "P8_DOMAIN_TRAJECTORY_COVERAGE=OPEN"
echo "P4_M4_FINAL_INTEGRATION=false"
echo "REGISTRY_MUTATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_p4_young_feasibility_lean/verify.sh"
