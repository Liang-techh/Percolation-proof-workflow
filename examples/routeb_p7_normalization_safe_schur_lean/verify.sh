#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
LEAN_FILE="$ROOT/P7NormalizationSafeSchur.lean"
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
  weighted_completion_one \
  schur_cost_from_physical_box \
  transported_cost_identity \
  r11_nonneg \
  r22_nonneg \
  transported_box_quadratic_cost \
  box_vertex_attains_of_nonneg_cross \
  box_vertex_attains_of_neg_cross \
  box_cost_attained \
  normalization_safe_schur_consumer \
  scalar_normalization_cost \
  scalar_normalization_rho_cost \
  normalized_certificate_no_uniform_cost \
  normalized_component_abs_le \
  interval_normalization_schur_cost; do
  grep -F "'RouteBP7NormalizationSafeSchur.$theorem' depends on axioms:" "$OUT" >/dev/null || {
    echo "missing axiom report for $theorem" >&2
    exit 3
  }
done

if grep -F "sorryAx" "$OUT" >/dev/null; then
  echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2
  exit 4
fi

echo "AXIOM_AUDIT=PASS"
echo "P7_NORMALIZATION_SAFE_SCHUR_FOCUSED_CHECK=PASS"
