#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
LEAN_FILE="$ROOT/P5SignedTwoCycleContact.lean"
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

OUT="$(mktemp)"
trap 'rm -f "$OUT"' EXIT

(
  cd "$LAKE_ROOT"
  lake env lean -DwarningAsError=true "$LEAN_FILE"
) 2>&1 | tee "$OUT"

for theorem in \
  cyclePhi_antitone_of_monotone_antitone \
  cyclePhi_antitone_of_antitone_monotone \
  sub_antitone_strongMono_one \
  sub_antitone_abs_coercive_one \
  sub_antitone_injective \
  coercive_inverse_perturbation \
  negative_feedback_coordinate_bound \
  two_cycle_negative_feedback_inverse_bound_monotone_antitone \
  two_cycle_negative_feedback_inverse_bound_antitone_monotone \
  two_cycle_small_gain_cleared \
  two_cycle_small_gain_cleared_with_reserve \
  root_antitone_of_active_increasing_cross_up \
  root_monotone_of_active_increasing_cross_down \
  identity_two_cycle_boundary_nonunique \
  small_gain_near_boundary_sharp_99_100; do
  grep -F "'RouteBP5SignedTwoCycleContact.$theorem' depends on axioms:" "$OUT" >/dev/null || {
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
echo "NEGATIVE_FEEDBACK_NO_SMALL_GAIN=true"
echo "UNSIGNED_CLEARED_RESERVE=true"
echo "SOURCE_CROSS_SIGN_ROOT_ORIENTATION=true"
echo "INTERVAL_SELF_MAP_EXISTENCE_LEAF=OPEN"
echo "BASE_PARAMETER_D_TRANSPORT=OPEN"
echo "CONCRETE_SOURCE_BINDING=OPEN"
echo "P8_ODE_COVERAGE=OPEN"
echo "P5_M4_FINAL_INTEGRATION=false"
echo "REGISTRY_MUTATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_p5_signed_two_cycle_contact_lean/verify.sh"
