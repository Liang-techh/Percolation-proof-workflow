#!/usr/bin/env bash
set -euo pipefail

SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
CACHE=/home/z5242/sos_lean
LEAN=/home/z5242/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean
mkdir -p "$SIDE/output"
RUN=$(mktemp -d "$SIDE/output/run-XXXXXXXX")
printf 'ATTEMPT_DIRECTORY=%s\n' "$RUN"

set +e
(
  set -euo pipefail
  trap 'code=$?; printf "VERIFY_EXIT_CODE=%s\\n" "$code"' EXIT
  printf 'LEAN_TOOLCHAIN='; cat "$SIDE/lean-toolchain"
  REV=$(git -C "$CACHE/.lake/packages/mathlib" rev-parse HEAD)
  printf 'MATHLIB_COMMIT=%s\n' "$REV"
  test "$REV" = 0df444a360eaa60ab8c11dca51a86af692955474
  "$LEAN" --version
  export LEAN_PATH="$RUN"
  for PACKAGE in "$CACHE"/.lake/packages/*; do
    LIB="$PACKAGE/.lake/build/lib/lean"
    if test -d "$LIB"; then LEAN_PATH="$LEAN_PATH:$LIB"; fi
  done
  cp "$SIDE/ExactCoefficientBridge.lean" \
     "$SIDE/FiniteTableReification.lean" \
     "$SIDE/PayloadRows.lean" \
     "$SIDE/Payload.lean" "$RUN/"
  "$LEAN" -DwarningAsError=true --root="$RUN" \
    -o "$RUN/ExactCoefficientBridge.olean" "$RUN/ExactCoefficientBridge.lean"
  "$LEAN" -DwarningAsError=true --root="$RUN" \
    -o "$RUN/FiniteTableReification.olean" "$RUN/FiniteTableReification.lean"
  "$LEAN" -DwarningAsError=true --root="$RUN" \
    -o "$RUN/PayloadRows.olean" "$RUN/PayloadRows.lean"
  "$LEAN" -DwarningAsError=true --root="$RUN" \
    -o "$RUN/Payload.olean" "$RUN/Payload.lean"
  printf 'FOCUSED_FILES=ExactCoefficientBridge.lean,FiniteTableReification.lean,PayloadRows.lean,Payload.lean\n'
  sha256sum "$SIDE/lean-toolchain" "$SIDE/PayloadRows.lean" \
    "$RUN/Payload.olean"
) > "$RUN/terminal.log" 2>&1
CODE=$?
set -e
cat "$RUN/terminal.log"
exit "$CODE"
