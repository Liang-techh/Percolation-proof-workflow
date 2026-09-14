#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
LEAN_FILE="$ROOT/P5CenterBiasMixedSmallGain.lean"
EXPECTED_TOOLCHAIN="$(tr -d '\r\n' < "$ROOT/lean-toolchain")"

command -v lake >/dev/null 2>&1 || { echo "lake not found on PATH" >&2; exit 2; }
command -v lean >/dev/null 2>&1 || { echo "lean not found on PATH" >&2; exit 2; }
[[ -d "$LAKE_ROOT" ]] || { echo "local_fkg Lake environment not found at $LAKE_ROOT" >&2; exit 2; }
[[ -f "$LAKE_ROOT/lake-manifest.json" ]] || { echo "pinned lake-manifest.json missing at $LAKE_ROOT" >&2; exit 2; }
[[ -f "$LAKE_ROOT/lean-toolchain" ]] || { echo "local_fkg lean-toolchain missing at $LAKE_ROOT" >&2; exit 2; }

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
  weighted_quadratic_bias_identity \
  quadratic_add_weighted \
  biased_displacement_linear_le \
  biased_displacement_sq_le \
  mixed_power_square_bound \
  square_completion_power_absorption \
  biased_anchor_power_absorption \
  biased_anchor_mixed_small_gain \
  mixed_small_gain_strict_reserves \
  mixed_small_gain_boundary_inward \
  nonzero_bias_zero_floor_counterexample; do
  if ! grep -F "'RouteBP5CenterBiasMixedSmallGain.$theorem' depends on axioms:" "$OUT" >/dev/null \
      && ! grep -F "'RouteBP5CenterBiasMixedSmallGain.$theorem' does not depend on any axioms" "$OUT" >/dev/null; then
    echo "missing axiom report for $theorem" >&2
    exit 3
  fi
done

if grep -F "sorryAx" "$OUT" >/dev/null; then
  echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2
  exit 4
fi

echo "AXIOM_AUDIT=PASS"
echo "P5_CENTER_BIAS_MIXED_SMALL_GAIN_FOCUSED_CHECK=PASS"
echo "WEIGHTED_PSD_BIAS_SPLIT=true"
echo "MIXED_RELATIVE_ADDITIVE_GATE=true"
echo "DIVISION_FREE_ULTIMATE_RADIUS_GATE=true"
echo "NONZERO_BIAS_ZERO_FLOOR_OBSTRUCTION=true"
echo "DEPLOYED_SOURCE_BINDING=OPEN"
echo "SAME_DOMAIN_COVERAGE=OPEN"
echo "FLOAT64_CONTROLLER_BINDING=OPEN"
echo "P8_FLOWPIPE_COVERAGE=OPEN"
echo "REGISTRY_MUTATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_p5_center_bias_mixed_small_gain_lean/verify.sh"
