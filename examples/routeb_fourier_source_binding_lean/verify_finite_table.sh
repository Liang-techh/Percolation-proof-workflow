#!/usr/bin/env bash
set -euo pipefail

SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
CACHE=/home/z5242/sos_lean
LEAN=/home/z5242/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean
RUN=$(mktemp -d "$SIDE/output/finite-table-XXXXXXXX")
printf 'ATTEMPT_DIRECTORY=%s\n' "$RUN"
set +e
(
  set -euo pipefail
  trap 'code=$?; printf "VERIFY_EXIT_CODE=%s\\n" "$code"' EXIT
  REV=$(git -C "$CACHE/.lake/packages/mathlib" rev-parse HEAD)
  test "$REV" = 0df444a360eaa60ab8c11dca51a86af692955474
  export LEAN_PATH="$RUN"
  for PACKAGE in "$CACHE"/.lake/packages/*; do
    LIB="$PACKAGE/.lake/build/lib/lean"
    if test -d "$LIB"; then LEAN_PATH="$LEAN_PATH:$LIB"; fi
  done
  cp "$SIDE/ExactCoefficientBridge.lean" "$SIDE/FiniteTableReification.lean" "$RUN/"
  "$LEAN" -DwarningAsError=true --root="$RUN" \
    -o "$RUN/ExactCoefficientBridge.olean" "$RUN/ExactCoefficientBridge.lean"
  "$LEAN" -DwarningAsError=true --root="$RUN" \
    -o "$RUN/FiniteTableReification.olean" "$RUN/FiniteTableReification.lean"
  sha256sum "$RUN/FiniteTableReification.lean" "$RUN/FiniteTableReification.olean"
) > "$RUN/terminal.log" 2>&1
CODE=$?
set -e
cat "$RUN/terminal.log"
exit "$CODE"
