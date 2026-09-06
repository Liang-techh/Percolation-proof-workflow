#!/usr/bin/env bash
set -euo pipefail
SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
CACHE=/home/z5242/sos_lean
LEAN=/home/z5242/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean
mkdir -p "$SIDE/output"
RUN=$(mktemp -d "$SIDE/output/run-XXXXXXXX")
for NAME in GainBridge.lean verify.sh DERIVATION.md ATTEMPT_HISTORY.md; do
  if test -f "$SIDE/$NAME"; then cp "$SIDE/$NAME" "$RUN/$NAME"; fi
done
sha256sum "$RUN/GainBridge.lean" "$RUN/verify.sh" > "$RUN/before_run.sha256"
printf 'ATTEMPT_DIRECTORY=%s\n' "$RUN"
# No asynchronous tee: the whole subprocess log is closed before it is read.
set +e
(
  set -euo pipefail
  trap 'code=$?; printf "VERIFY_EXIT_CODE=%s\n" "$code"' EXIT
  printf 'PRE_RUN_SNAPSHOTS_COMPLETE\n'
  test "$(git -C "$CACHE/.lake/packages/mathlib" rev-parse HEAD)" = 0df444a360eaa60ab8c11dca51a86af692955474
  "$LEAN" --version
  export LEAN_PATH="$RUN"
  for PACKAGE in "$CACHE"/.lake/packages/*; do
    LIB="$PACKAGE/.lake/build/lib/lean"
    if test -d "$LIB"; then LEAN_PATH="$LEAN_PATH:$LIB"; fi
  done
  set +e
  "$LEAN" -DwarningAsError=true --root="$RUN" -o "$RUN/GainBridge.olean" "$RUN/GainBridge.lean"
  CODE=$?
  set -e
  printf 'LEAN_COMPILE_EXIT_CODE=%s\n' "$CODE"
  test "$CODE" -eq 0
  sha256sum "$RUN/GainBridge.olean"
) > "$RUN/terminal.log" 2>&1
CODE=$?
set -e
cat "$RUN/terminal.log"
exit "$CODE"
