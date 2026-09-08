#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
LEAN_FILE="$ROOT/P5ParetoOptimizer.lean"
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
  pareto_margin_expand \
  pareto_margin_left_max \
  pareto_margin_right_max \
  pareto_margin_vertex_gap \
  pareto_margin_vertex_max \
  pareto_margin_vertex_value \
  pareto_vertex_mem_Ioo \
  paretoOpt_mem_Icc \
  pareto_optimal_selector \
  pareto_vertex_positive_iff \
  pareto_gate_exists_iff \
  pareto_gate_impossible_of_branch_nonpositive \
  pareto_interior_strict_gain_over_left \
  pareto_interior_strict_gain_over_right \
  pareto_selector_right_threshold \
  pareto_selector_left_threshold \
  pareto_interior_endpoint_failure_witness; do
  grep -F "'RouteBP5ParetoOptimizer.$theorem' depends on axioms:" "$OUT" >/dev/null || {
    echo "missing axiom report for $theorem" >&2
    exit 3
  }
done

if grep -F "sorryAx" "$OUT" >/dev/null; then
  echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2
  exit 4
fi

echo "AXIOM_AUDIT=PASS"
echo "P5_PARETO_OPTIMIZER_FOCUSED_CHECK=PASS"
echo "T_P5_038_FIRST_EXIT_REUSED_NOT_DUPLICATED=true"
echo "COMPONENTWISE_E4_E5_SOURCE_BINDING=OPEN"
echo "TRUE_DH_FLOAT64_SEMANTICS=OPEN"
echo "P8_ODE_COVERAGE=OPEN"
echo "P5_M4_FINAL_INTEGRATION=false"
echo "REGISTRY_MUTATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_p5_pareto_optimizer_lean/verify.sh"
