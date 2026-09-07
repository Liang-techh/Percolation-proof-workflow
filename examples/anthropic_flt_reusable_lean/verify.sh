#!/usr/bin/env bash
set -euo pipefail

SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
cd "$SIDE"

if command -v lake >/dev/null 2>&1; then
  LAKE=$(command -v lake)
elif test -x /home/z5242/.elan/bin/lake; then
  LAKE=/home/z5242/.elan/bin/lake
else
  echo 'lake not found; checked PATH and /home/z5242/.elan/bin/lake' >&2
  exit 127
fi

test "$(tr -d '\r\n' < lean-toolchain)" = "leanprover/lean4:v4.33.1"
test "$(grep -hEc 'db584cd6d46c92f209a44c0f1c829460d327499d' README.md REPORT.md ATTRIBUTION.md | awk '{s += $1} END {print s + 0}')" -ge 1
if grep -En '(^|[[:space:]])(axiom|sorry|native_decide|unsafe)([[:space:]]|$)' AnthropicFLTReusable.lean; then
  echo 'forbidden Lean construct found' >&2
  exit 2
fi

set +e
"$LAKE" build
CODE=$?
set -e
echo "LEAN_BUILD_EXIT_CODE=$CODE"
if test "$CODE" -ne 0; then exit "$CODE"; fi

AXIOM_OUT=$(mktemp)
trap 'rm -f "$AXIOM_OUT"' EXIT
"$LAKE" env lean AnthropicFLTReusable.lean 2>&1 | tee "$AXIOM_OUT"
if grep -En 'declaration uses.*axiom|contains.*axiom|sorryAx|axiom' "$AXIOM_OUT"; then
  echo 'axiom audit failed' >&2
  exit 3
fi
echo 'AXIOM_AUDIT=PASS (no axiom/sorry diagnostics)'
echo 'FOCUSED_BUILD=AnthropicFLTReusable.lean only'
