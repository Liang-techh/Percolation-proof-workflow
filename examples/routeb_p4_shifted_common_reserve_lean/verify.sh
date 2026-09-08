#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
LEAN_FILE="$ROOT/P4ShiftedCommonReserve.lean"
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
  quadratic_chord_identity \
  quadratic_below_endpoint_chord \
  shifted_charge_complete_square \
  common_interval_shifted_reserve_mul \
  common_interval_shifted_feasible \
  common_interval_shifted_strict \
  common_interval_shifted_reserve_family \
  shifted_witness_mem_interval \
  midpoint_fails_shifted_passes_1_4_19_20 \
  large_discriminant_wrong_branch_counterexample \
  shifted_boundary_1_4_1 \
  charge_above_one_impossible_1_4; do
  grep -F "'RouteBP4ShiftedCommonReserve.$theorem' depends on axioms:" "$OUT" >/dev/null || {
    echo "missing axiom report for $theorem" >&2
    exit 3
  }
done

if grep -F "sorryAx" "$OUT" >/dev/null; then
  echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2
  exit 4
fi

if grep -E '\bsorry\b|\badmit\b' "$LEAN_FILE" >/dev/null; then
  echo "PLACEHOLDER_SCAN=FAIL" >&2
  exit 5
fi

echo "PLACEHOLDER_SCAN=PASS"
echo "AXIOM_AUDIT=PASS"
echo "P4_SHIFTED_COMMON_RESERVE_FOCUSED_CHECK=PASS"
echo "COMMON_ENDPOINT_CERTIFICATE=REQUIRED"
echo "CONCRETE_SOURCE_BINDING=OPEN"
echo "TRUE_DH_FLOAT64_SEMANTICS=OPEN"
echo "P8_COVERAGE=OPEN"
echo "P4_M4_FINAL_INTEGRATION=false"
echo "REGISTRY_MUTATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_p4_shifted_common_reserve_lean/verify.sh"
