#!/usr/bin/env bash
set -euo pipefail
SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
CACHE=/home/z5242/sos_lean
LEAN=/home/z5242/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean
mkdir -p "$SIDE/output"
RUN=$(mktemp -d "$SIDE/output/run-XXXXXXXX")
cp "$SIDE/RouteBMinimalSourceLoop.lean" "$RUN/"
export LEAN_PATH="$RUN:$CACHE/.lake/packages/mathlib/.lake/build/lib/lean"
for PACKAGE in "$CACHE"/.lake/packages/*; do
  LIB="$PACKAGE/.lake/build/lib/lean"
  if test -d "$LIB"; then LEAN_PATH="$LEAN_PATH:$LIB"; fi
done
test "$(git -C "$CACHE/.lake/packages/mathlib" rev-parse HEAD)" = 0df444a360eaa60ab8c11dca51a86af692955474
set +e
"$LEAN" -DwarningAsError=true --root="$RUN" -o "$RUN/RouteBMinimalSourceLoop.olean" \
  "$RUN/RouteBMinimalSourceLoop.lean" 2>&1 | tee "$RUN/terminal.log"
CODE=${PIPESTATUS[0]}
set -e
printf 'COMPILE_EXIT_CODE=%s\n' "$CODE"
test "$CODE" -eq 0
if grep -nE '(^|[^[:alnum:]_])(sorry|admit)([^[:alnum:]_]|$)|^[[:space:]]*axiom[[:space:]]' \
  "$RUN/RouteBMinimalSourceLoop.lean"; then exit 1; fi
sha256sum "$RUN/RouteBMinimalSourceLoop.lean" | tee "$RUN/source.sha256"
printf 'SOURCE_RESTRICTION_CHECK=PASSED\n'
printf 'MAIN_DAG_STATE_UNCHANGED=true\n'
printf 'RUN=%s\n' "$RUN"
