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
  trap 'code=$?; printf "VERIFY_EXIT_CODE=%s\n" "$code"' EXIT
  printf 'START_UTC=%s\n' "$(date -u +%FT%TZ)"
  cp "$SIDE/TerminalGate.lean" "$RUN/"
  cp "$SIDE/verify.sh" "$RUN/"
  cp "$SIDE/lean-toolchain" "$RUN/"
  REV=$(git -C "$CACHE/.lake/packages/mathlib" rev-parse HEAD)
  printf 'MATHLIB_COMMIT=%s\n' "$REV"
  test "$REV" = 0df444a360eaa60ab8c11dca51a86af692955474
  "$LEAN" --version
  export LEAN_PATH="$RUN"
  for PACKAGE in "$CACHE"/.lake/packages/*; do
    LIB="$PACKAGE/.lake/build/lib/lean"
    if test -d "$LIB"; then LEAN_PATH="$LEAN_PATH:$LIB"; fi
  done
  printf 'LEAN_PATH=%s\n' "$LEAN_PATH"
  find "$RUN" -type f ! -name terminal.log ! -name before_run.sha256 -print0 |
    sort -z | xargs -0 sha256sum > "$RUN/before_run.sha256"
  printf 'PROSPECTIVE_SNAPSHOT_COMPLETE\n'
  printf 'COMMAND=%s -DwarningAsError=true --root=%s -o %s/TerminalGate.olean %s/TerminalGate.lean\n' \
    "$LEAN" "$RUN" "$RUN" "$RUN"
  set +e
  "$LEAN" -DwarningAsError=true --root="$RUN" \
    -o "$RUN/TerminalGate.olean" "$RUN/TerminalGate.lean"
  CODE=$?
  set -e
  printf 'TerminalGate_COMPILE_EXIT_CODE=%s\n' "$CODE"
  test "$CODE" -eq 0
  sha256sum "$RUN/TerminalGate.lean" "$RUN/TerminalGate.olean"
  printf 'END_UTC=%s\n' "$(date -u +%FT%TZ)"
) > "$RUN/terminal.log" 2>&1
CODE=$?
set -e
cat "$RUN/terminal.log"
exit "$CODE"
