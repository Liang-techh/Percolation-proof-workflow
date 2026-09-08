#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
LEAN_FILE="$ROOT/P5SharedROptimizer.lean"
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
  same_curvature_difference_affine \
  same_curvature_vertex_square \
  scaled_vertex_value \
  scaled_difference_at_vertex_one \
  scaled_difference_at_vertex_two \
  shared_positive_of_active_vertex_one \
  shared_positive_of_active_vertex_two \
  crossover_inside_of_endpoint_sign_change \
  crossover_value_scaled \
  crossover_gate_equality \
  shared_positive_of_crossover \
  p5_barrier_parameter_difference_cancels \
  separated_regression_each_passes \
  shared_regression_positive_implies_eps_gt_sixteenth \
  eps_one_hundred_no_shared_witness \
  eps_one_sixteenth_boundary \
  eps_one_tenth_crossover_margin; do
  grep -F "'RouteBP5SharedROptimizer.$theorem' depends on axioms:" "$OUT" >/dev/null || {
    echo "missing axiom report for $theorem" >&2
    exit 4
  }
done

if grep -F "sorryAx" "$OUT" >/dev/null; then
  echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2
  exit 5
fi

echo "AXIOM_AUDIT=PASS"
echo "P5_SHARED_R_OPTIMIZER_FOCUSED_CHECK=PASS"
echo "FIVE_CANDIDATE_SUFFICIENCY_SEAMS=true"
echo "FIVE_CANDIDATE_NECESSITY_COMPLETENESS=OPEN"
echo "SEPARATE_PASS_DOES_NOT_IMPLY_SHARED_PASS=true"
echo "SOURCE_BINDING=OPEN"
echo "FLOAT64_CONTROLLER_SEMANTICS=OPEN"
echo "P8_SAME_DOMAIN_COVERAGE=OPEN"
echo "P5_P8_M4_FINAL_INTEGRATION=false"
echo "REGISTRY_MUTATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_p5_shared_r_optimizer_lean/verify.sh"
