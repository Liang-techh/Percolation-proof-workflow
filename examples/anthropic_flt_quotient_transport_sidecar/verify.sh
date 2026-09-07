#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-../local_fkg}"

if [[ -z "${LAKE:-}" ]]; then
  if command -v lake >/dev/null 2>&1; then
    LAKE="$(command -v lake)"
  else
    echo "BUILD_ENV_BLOCKED: lake not found" >&2
    exit 2
  fi
fi

test "$(tr -d '\r\n' < "$ROOT/lean-toolchain")" = "leanprover/lean4:v4.33.1"
LOG="$(mktemp)"
trap 'rm -f "$LOG"' EXIT
(cd "$LAKE_ROOT" && "$LAKE" env lean -DwarningAsError=true \
  "$ROOT/AnthropicFLTQuotientTransport.lean") 2>&1 | tee "$LOG"

grep -q "quotientContinuousLinearEquiv" "$LOG"
grep -q "quotientPiContinuousLinearEquiv" "$LOG"
grep -q "quotient_transport_mk" "$LOG"
if grep -Eiq 'sorryAx|declaration uses.*axiom|unknown module|error:' "$LOG"; then
  echo "AXIOM_AUDIT=FAIL" >&2
  exit 1
fi
echo "AXIOM_AUDIT=PASS"
echo "FLT_QUOTIENT_TRANSPORT_FOCUSED_CHECK=PASS"
