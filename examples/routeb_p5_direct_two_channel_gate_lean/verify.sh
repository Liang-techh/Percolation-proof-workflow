#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
LEAN_FILE="$ROOT/P5DirectTwoChannelGate.lean"
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
  positive_scale_lt_zero_iff \
  scaled_sqrt_lt_iff_signed_square \
  sqrt_lt_iff_signed_square \
  two_scaled_sqrt_lt_iff_signed_square \
  ee_direct_gate_iff \
  ie_cost_scaled_iff \
  ei_cost_scaled_iff \
  ii_cost_scaled_iff \
  ie_direct_gate_iff \
  ei_direct_gate_iff \
  ii_direct_gate_iff \
  ii_gate_fail_blocks_branch_cost \
  ii_strict_success_regression \
  ii_boundary_regression \
  omit_T_positive_guard_counterexample \
  omit_S_positive_guard_counterexample; do
  grep -F "'RouteBP5DirectTwoChannelGate.$theorem' depends on axioms:" "$OUT" >/dev/null || {
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
echo "P5_DIRECT_TWO_CHANNEL_GATE_FOCUSED_CHECK=PASS"
echo "T_P5_042_OPTIMIZER_BRIDGE=REQUIRED_FOR_NO_RHO_OBSTRUCTION"
echo "CONCRETE_SOURCE_BINDING=OPEN"
echo "TRUE_DH_FLOAT64_SEMANTICS=OPEN"
echo "P8_COVERAGE=OPEN"
echo "P5_P8_M4_FINAL_INTEGRATION=false"
echo "REGISTRY_MUTATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_p5_direct_two_channel_gate_lean/verify.sh"
