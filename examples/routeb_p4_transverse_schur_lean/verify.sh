#!/usr/bin/env bash
set -euo pipefail
# CI_PORTABLE=1

ROOT="$(cd "$(dirname "$0")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"

if [[ -z "${LAKE:-}" ]]; then
  LAKE="$(command -v lake || true)"
fi

if [[ -z "$LAKE" ]]; then
  echo "BUILD_ENV_BLOCKED: cannot locate lake on PATH" >&2
  exit 2
fi

if [[ ! -f "$LAKE_ROOT/lakefile.toml" && ! -f "$LAKE_ROOT/lakefile.lean" ]]; then
  echo "BUILD_ENV_BLOCKED: local Lake root missing at $LAKE_ROOT" >&2
  exit 2
fi

EXPECTED_TOOLCHAIN="$(tr -d '\r\n' < "$ROOT/lean-toolchain")"
ACTUAL_TOOLCHAIN="$(tr -d '\r\n' < "$LAKE_ROOT/lean-toolchain")"
if [[ "$ACTUAL_TOOLCHAIN" != "$EXPECTED_TOOLCHAIN" ]]; then
  echo "BUILD_ENV_BLOCKED: toolchain mismatch" >&2
  echo "EXPECTED_TOOLCHAIN=$EXPECTED_TOOLCHAIN" >&2
  echo "ACTUAL_TOOLCHAIN=$ACTUAL_TOOLCHAIN" >&2
  exit 2
fi

if [[ ! -f "$LAKE_ROOT/lake-manifest.json" ]]; then
  echo "BUILD_ENV_BLOCKED: pinned lake-manifest.json missing at $LAKE_ROOT" >&2
  exit 2
fi

echo "LEAN_TOOLCHAIN=$EXPECTED_TOOLCHAIN"
echo "LAKE_MANIFEST=$LAKE_ROOT/lake-manifest.json"
LOG="$(mktemp)"
trap 'rm -f "$LOG"' EXIT

(
  cd "$LAKE_ROOT"
  "$LAKE" env lean -DwarningAsError=true "$ROOT/P4TransverseSchur.lean"
) 2>&1 | tee "$LOG"

for DECL in \
  combined_residual_abs \
  transverse_square_budget \
  residual_square_budget \
  relative_plus_transverse_schur \
  additive_bias_with_slack \
  transverse_reserve_failure_witness \
  block4_delta_identity \
  block4_delta_pos \
  block4_reserve_from_integer_budget \
  block4_quarter_plus_transverse; do
  grep -q "RouteBP4TransverseSchur.$DECL" "$LOG" || {
    echo "FAIL: missing axiom report for $DECL" >&2
    exit 1
  }
done

if grep -Eiq 'sorryAx|declaration uses.*axiom|unknown module|error:' "$LOG"; then
  echo "AXIOM_AUDIT=FAIL"
  exit 1
fi

echo "AXIOM_AUDIT=PASS"
echo "P4_TRANSVERSE_SCHUR_FOCUSED_CHECK=PASS"
echo "EXECUTION_REMAINDER_TYPED_BINDING=OPEN"
echo "TRANSVERSE_POSITIVE_RESERVE_BINDING=OPEN"
echo "FLOAT64_IEEE_BOUNDS=OPEN"
echo "REGISTRY_MUTATION=false"
