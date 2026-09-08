#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
LEAN_FILE="$ROOT/P5TargetDomainObstruction.lean"
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
  witness_fullP_zero \
  witness_growth_caps \
  witness_in_broad_target \
  witness_has_strict_displayed_reserve \
  witness_ramp_realization \
  gapG_gt_eleven_percent \
  gapG_pos \
  beta_increment_iff \
  exact_gap_beta_increment_iff \
  exact_gap_target_negative \
  floor_weakening_iff \
  witness_beta_coeff_halfspace_iff \
  witness_qv_weights_vanish \
  witness_lambda2_budget_iff \
  broad_target_universal_nonnegative_false; do
  grep -F "'RouteBP5TargetDomainObstruction.$theorem' depends on axioms:" "$OUT" >/dev/null || {
    echo "missing axiom report for $theorem" >&2
    exit 3
  }
done

if grep -F "sorryAx" "$OUT" >/dev/null; then
  echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2
  exit 4
fi

echo "AXIOM_AUDIT=PASS"
echo "P5_TARGET_DOMAIN_OBSTRUCTION_FOCUSED_CHECK=PASS"
echo "BROAD_WITNESS_TYPED=true"
echo "EXACT_GAP_GT_11_OVER_100=true"
echo "POINTWISE_BETA_REPAIR_IFF=true"
echo "QV_WEIGHT_VANISHING_AT_WITNESS=true"
echo "LAMBDA2_DEBIT_ALGEBRA=true"
echo "DEPLOYED_DH_SOURCE_EQUALITY=OPEN"
echo "PHYSICAL_REACHABLE_DOMAIN_EXCLUSION=OPEN"
echo "FULL_CELL_REPAIR_SUFFICIENCY=OPEN"
echo "FLOAT64_CONTROLLER_BINDING=OPEN"
echo "P8_ODE_COVERAGE=OPEN"
echo "P5_M4_FINAL_INTEGRATION=false"
echo "REGISTRY_MUTATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_p5_target_domain_obstruction_lean/verify.sh"
