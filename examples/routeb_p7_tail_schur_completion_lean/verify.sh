#!/usr/bin/env bash
set -euo pipefail
# CI_PORTABLE=1

ROOT="$(cd "$(dirname "$0")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
LAKE="${LAKE:-$(command -v lake || true)}"
if [[ -z "$LAKE" ]]; then
  echo "BUILD_ENV_BLOCKED: cannot locate lake on PATH" >&2
  exit 2
fi

EXPECTED_TOOLCHAIN="$(tr -d '\r\n' < "$ROOT/lean-toolchain")"
ACTUAL_TOOLCHAIN="$(tr -d '\r\n' < "$LAKE_ROOT/lean-toolchain")"
if [[ "$EXPECTED_TOOLCHAIN" != "$ACTUAL_TOOLCHAIN" ]]; then
  echo "BUILD_ENV_BLOCKED: toolchain mismatch" >&2
  exit 2
fi

LOG="$(mktemp)"
trap 'rm -f "$LOG"' EXIT
(
  cd "$LAKE_ROOT"
  "$LAKE" env lean -DwarningAsError=true "$ROOT/TailSchurCompletion.lean"
) 2>&1 | tee "$LOG"

for DECL in schur_completion_identity robust_inverse_quadratic_bound_2x2 schur_tail_absorption; do
  grep -q "$DECL" "$LOG"
done
if grep -Eiq 'sorryAx|declaration uses.*axiom|unknown module|error:' "$LOG"; then
  echo "AXIOM_AUDIT=FAIL"
  exit 1
fi
echo "AXIOM_AUDIT=PASS"
echo "P7_TAIL_SCHUR_FOCUSED_CHECK=PASS"
echo "P7_PHYSICAL_SOURCE_BINDING=OPEN"
echo "FINAL_INTEGRATION=梁智炜"
