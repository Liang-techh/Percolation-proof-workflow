#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
LEAN_FILE="$ROOT/P5SignedTwoCycle.lean"
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
  unsigned_two_cycle_budget_x1 \
  unsigned_two_cycle_budget_x2 \
  unsigned_two_cycle_injective_zero_budget \
  cleared_two_cycle_budget_x1 \
  cleared_two_cycle_budget_x2 \
  composition_antitone_of_monotone_antitone \
  composition_antitone_of_antitone_monotone \
  antitone_unit_coercivity \
  antitone_abs_coercivity \
  negative_feedback_scalar_budget \
  nested_variation_budget \
  strictMono_zero_le_of_nonneg_sample \
  strictMono_le_zero_of_nonpos_sample \
  same_orientation_unit_gain_obstruction \
  negative_feedback_linear_injective; do
  grep -F "'RouteBP5SignedTwoCycle.$theorem' depends on axioms:" "$OUT" >/dev/null || {
    echo "missing axiom report for $theorem" >&2
    exit 3
  }
done

if grep -F "sorryAx" "$OUT" >/dev/null; then
  echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2
  exit 4
fi

echo "AXIOM_AUDIT=PASS"
echo "P5_SIGNED_TWO_CYCLE_FOCUSED_CHECK=PASS"
echo "UNSIGNED_SMALL_GAIN_BRANCH=true"
echo "NEGATIVE_FEEDBACK_NO_SMALL_GAIN_BRANCH=true"
echo "FAIL_BOTH_BRANCHES_IS_NOT_APPLICABLE=true"
echo "INTERVAL_FIXED_POINT_EXISTENCE=OPEN"
echo "DEPLOYED_ROOT_SOURCE_FLOAT64_BINDING=OPEN"
echo "P8_ODE_COVERAGE=OPEN"
echo "P5_M4_FINAL_INTEGRATION=false"
echo "REGISTRY_MUTATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_p5_signed_two_cycle_lean/verify.sh"
