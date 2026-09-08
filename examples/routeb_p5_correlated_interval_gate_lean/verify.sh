#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
LEAN_FILE="$ROOT/P5CorrelatedIntervalGate.lean"
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

if grep -nE '\b(sorry|admit)\b' "$LEAN_FILE"; then
  echo "PLACEHOLDER_SCAN=FAIL" >&2
  exit 3
fi
echo "PLACEHOLDER_SCAN=PASS"

OUT="$(mktemp)"
trap 'rm -f "$OUT"' EXIT

(
  cd "$LAKE_ROOT"
  lake env lean -DwarningAsError=true "$LEAN_FILE"
) 2>&1 | tee "$OUT"

for theorem in \
  signed_sum_interval_transport \
  signed_sum_abs_transport \
  skew_family_signed_sum_zero \
  skew_family_signed_sum_abs_zero; do
  grep -F "'RouteBP5SignedSumIntervalTransport.$theorem' depends on axioms:" "$OUT" >/dev/null || {
    echo "missing axiom report for $theorem" >&2
    exit 4
  }
done

if grep -F "sorryAx" "$OUT" >/dev/null; then
  echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2
  exit 5
fi

echo "AXIOM_AUDIT=PASS"
echo "P5_SIGNED_SUM_INTERVAL_TRANSPORT_FOCUSED_CHECK=PASS"
echo "SIGNED_INTERVAL_ADDITION_BEFORE_ABS=true"
echo "SKEW_COORDINATE_CHARGED=false"
echo "MAIN_T_P5_045_FORMALIZATION_OWNER=苏梦辰"
echo "SOURCE_BINDING=OPEN"
echo "P8_SAME_DOMAIN_COVERAGE=OPEN"
echo "P5_P8_M4_FINAL_INTEGRATION=false"
echo "REGISTRY_MUTATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_p5_correlated_interval_gate_lean/verify.sh"
