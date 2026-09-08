#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
LEAN_FILE="$ROOT/P5CorrelatedIntervalGate.lean"
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

if grep -nE '\b(sorry|admit)\b' "$LEAN_FILE"; then
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
  scaled_correlated_invariants \
  signed_sum_interval_transport \
  square_le_square_of_abs_le \
  scaled_symmetric_det_lower_of_interval \
  scaled_adjugate_bias_le_box \
  scaled_adjugate_bias_le_cross_cap \
  correlated_quarter_gate_of_interval_box \
  correlated_one_twelfth_parameter_gate_of_interval_box \
  whole_cell_quarter_integer_gate_iff \
  whole_cell_one_twelfth_integer_gate_iff; do
  grep -F "'RouteBP5CorrelatedIntervalGate.$theorem' depends on axioms:" "$OUT" >/dev/null || {
    echo "missing axiom report for $theorem" >&2
    exit 4
  }
done

if grep -F "sorryAx" "$OUT" >/dev/null; then
  echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2
  exit 5
fi

echo "AXIOM_AUDIT=PASS"
echo "P5_CORRELATED_INTERVAL_GATE_FOCUSED_CHECK=PASS"
echo "SOURCE_SIGNED_JACOBIAN_EXPORTER=OPEN"
echo "SOURCE_COMPONENT_OR_CORRELATED_BIAS_BOUNDS=OPEN"
echo "SOURCE_PARAMETER_SENSITIVITY_BOUNDS=OPEN"
echo "SOURCE_FLOAT64_CONTROLLER_SOLVE_SEMANTICS=OPEN"
echo "P8_SAME_DOMAIN_COVERAGE=OPEN"
echo "P5_P8_M4_FINAL_INTEGRATION=false"
echo "REGISTRY_MUTATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_p5_correlated_interval_gate_lean/verify.sh"
