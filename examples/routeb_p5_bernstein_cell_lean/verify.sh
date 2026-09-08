#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
LEAN_FILE="$ROOT/P5BernsteinCell.lean"
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
  quad_bernstein_identity \
  cubic_bernstein_identity \
  quad_bernstein_weights_sum \
  cubic_bernstein_weights_sum \
  quadBern_nonneg_of_controls \
  cubicBern_nonneg_of_controls \
  quadPoly_nonneg_of_controls \
  cubicPoly_nonneg_of_controls \
  quad_decasteljau_left_half \
  quad_decasteljau_right_half \
  cubic_decasteljau_left_half \
  cubic_decasteljau_right_half \
  quad_left_controls_nonneg \
  quad_right_controls_nonneg \
  cubic_left_controls_nonneg \
  cubic_right_controls_nonneg \
  endpoint_only_unsound_regression \
  negative_control_positive_polynomial_identity \
  negative_control_positive_polynomial_lower_bound \
  negative_control_positive_polynomial_middle_control \
  cubic_packets_feed_two_remainder_consumer; do
  grep -F "'RouteBP5BernsteinCell.$theorem' depends on axioms:" "$OUT" >/dev/null || {
    echo "missing axiom report for $theorem" >&2
    exit 3
  }
done

if grep -F "sorryAx" "$OUT" >/dev/null; then
  echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2
  exit 4
fi

echo "AXIOM_AUDIT=PASS"
echo "P5_BERNSTEIN_CELL_FOCUSED_CHECK=PASS"
echo "BERNSTEIN_QUAD_CUBIC_CORE=true"
echo "DYADIC_DECASTELJAU_HALF=true"
echo "NEGATIVE_CONTROL_IS_NOT_REJECTION=true"
echo "EVENTUAL_STRICT_POSITIVITY_SUBDIVISION_THEOREM=OPEN"
echo "DEPLOYED_SOURCE_FLOAT64_BINDING=OPEN"
echo "P8_ODE_COVERAGE=OPEN"
echo "P5_M4_FINAL_INTEGRATION=false"
echo "REGISTRY_MUTATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_p5_bernstein_cell_lean/verify.sh"
