#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
LEAN_FILE="$ROOT/P5SquareOnlyRadical.lean"
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
if [[ ! -f "$LAKE_ROOT/lean-toolchain" ]]; then
  echo "pinned lean-toolchain missing at $LAKE_ROOT" >&2
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
  pointwise_square_is_square_only_admissible \
  centered_signed_is_not_square_only_admissible \
  normalized_square_eq_ratio \
  normalized_square_factor_cancel \
  balanced_square_extension_no_parity \
  common_factor_square_cancel \
  cancelled_square_pointwise_bound \
  balanced_square_pointwise_bound \
  balanced_square_difference_identity \
  cancelled_square_difference_identity \
  square_difference_abs_bound \
  cancelled_square_zero_at_factor_zero \
  balanced_odd_pointwise_square_constant \
  balanced_odd_centered_signed_jump \
  balanced_odd_square_variation_zero; do
  grep -F "'RouteBP5SquareOnlyRadical.$theorem' depends on axioms:" "$OUT" >/dev/null || {
    echo "missing axiom report for $theorem" >&2
    exit 3
  }
done

if grep -F "sorryAx" "$OUT" >/dev/null; then
  echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2
  exit 4
fi

echo "AXIOM_AUDIT=PASS"
echo "P5_SQUARE_ONLY_RADICAL_FOCUSED_CHECK=PASS"
echo "POINTWISE_SQUARE_VS_CENTERED_SIGNED_TYPED_SPLIT=PRESERVED"
echo "FACTOR_PACKET_SOURCE_BINDING=OPEN"
echo "EXECUTABLE_ZERO_REWRITE=OPEN"
echo "FLOAT64_LIBM_SEMANTICS=OPEN"
echo "P8_ODE_COVERAGE=OPEN"
echo "P5_M4_FINAL_INTEGRATION=false"
echo "REGISTRY_MUTATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_p5_square_only_radical_lean/verify.sh"
