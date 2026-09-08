#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
LEAN_FILE="$ROOT/P5ZeroContactFactor.lean"
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
  quadratic_repeated_root_factor_identity \
  quadratic_repeated_root_nonneg \
  quadratic_repeated_root_contact \
  affine_nonneg_of_endpoint_values \
  cubic_repeated_root_factor_identity \
  cubic_repeated_root_contact \
  cubic_repeated_root_nonneg_on_unit \
  left_endpoint_factor_identity \
  left_endpoint_factor_nonneg \
  right_endpoint_factor_identity \
  right_endpoint_factor_nonneg \
  one_third_square_regression \
  one_third_square_nonneg_regression \
  simple_root_negative_regression \
  endpoint_simple_root_regression \
  zero_contact_packets_feed_two_remainder_consumer; do
  grep -F "'RouteBP5ZeroContactFactor.$theorem' depends on axioms:" "$OUT" >/dev/null || {
    echo "missing axiom report for $theorem" >&2
    exit 3
  }
done

if grep -F "sorryAx" "$OUT" >/dev/null; then
  echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2
  exit 4
fi

echo "AXIOM_AUDIT=PASS"
echo "P5_ZERO_CONTACT_FACTOR_FOCUSED_CHECK=PASS"
echo "QUADRATIC_REPEATED_ROOT_CERT=true"
echo "CUBIC_REPEATED_ROOT_CERT=true"
echo "ENDPOINT_ZERO_BRANCH_SEPARATE=true"
echo "ROOT_DISCOVERY_TRUSTED=false"
echo "CERTIFICATE_LEVEL_COMPLETENESS_THEOREM=OPEN"
echo "DEPLOYED_SOURCE_FLOAT64_BINDING=OPEN"
echo "P8_ODE_COVERAGE=OPEN"
echo "P5_M4_FINAL_INTEGRATION=false"
echo "REGISTRY_MUTATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_p5_zero_contact_factor_lean/verify.sh"
