#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
LEAN_FILE="$ROOT/P5SimilarityNormalization.lean"
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
  quadraticForm_congruence \
  bilinear_congruence \
  strongMonotone_similarity_iff \
  sqLipschitz_similarity_iff \
  corrector_step_similarity \
  jacobian_sym_congruence \
  jacobian_gram_congruence \
  frozen_metric_monotonicity_counterexample \
  transported_metric_sym_regression \
  transported_metric_gram_regression; do
  grep -F "'RouteBP5SimilarityNormalization.$theorem' depends on axioms:" "$OUT" >/dev/null || {
    echo "missing axiom report for $theorem" >&2
    exit 3
  }
done

if grep -F "sorryAx" "$OUT" >/dev/null; then
  echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2
  exit 4
fi

echo "AXIOM_AUDIT=PASS"
echo "P5_SIMILARITY_NORMALIZATION_FOCUSED_CHECK=PASS"
echo "GENERAL_SYMMETRIC_METRIC_2X2=true"
echo "DIAGONAL_AFFINE_CHART=true"
echo "SAME_MU_LAMBDA=true"
echo "SAME_CORRECTOR_STEP=true"
echo "JACOBIAN_ACTION_INTERTWINING=true"
echo "WRONG_METRIC_COUNTEREXAMPLE=true"
echo "ARBITRARY_MATRIX_GENERALIZATION=OPEN"
echo "DEPLOYED_SOURCE_CHART_BINDING=OPEN"
echo "FLOAT64_FD_CONTROLLER_SOLVE=OPEN"
echo "P8_ODE_COVERAGE=OPEN"
echo "REGISTRY_MUTATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_p5_similarity_normalization_lean/verify.sh"
