#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
LEAN_FILE="$ROOT/P5MovingMetricContraction.lean"
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
  pullback_quadratic_eq_bilinear \
  physical_variation_rate_identity \
  moving_metric_contraction_tensor_congruence \
  contraction_rate_pullback \
  normalized_rate_of_congruence \
  dropping_material_metric_derivative_counterexample \
  moving_affine_chart_material_cancellation; do
  grep -F "'RouteBP5MovingMetricContraction.$theorem' depends on axioms:" "$OUT" >/dev/null || {
    echo "missing axiom report for $theorem" >&2
    exit 3
  }
done

if grep -F "sorryAx" "$OUT" >/dev/null; then
  echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2
  exit 4
fi

echo "AXIOM_AUDIT=PASS"
echo "P5_MOVING_METRIC_CONTRACTION_FOCUSED_CHECK=PASS"
echo "EXACT_REAL_2X2_ALGEBRA=true"
echo "MATERIAL_METRIC_TERM_RETAINED=true"
echo "MOVING_FRAME_CONNECTION_RETAINED=true"
echo "SAME_CONTRACTION_RATE=true"
echo "DIVISION_FREE_FORWARD_TRANSPORT=true"
echo "DIFFERENTIAL_COVARIANCE_DERIVATION=OPEN"
echo "DEPLOYED_SOURCE_BINDING=OPEN"
echo "FLOAT64_FD_CONTROLLER_SOLVE=OPEN"
echo "P8_ODE_COVERAGE=OPEN"
echo "REGISTRY_MUTATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_p5_moving_metric_contraction_lean/verify.sh"
