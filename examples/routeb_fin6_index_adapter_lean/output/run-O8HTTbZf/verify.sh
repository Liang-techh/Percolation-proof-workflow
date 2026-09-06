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
  printf 'START_UTC=%s\n' "$(date -u +%FT%TZ)"
  cp "$SIDE/Fin6IndexAdapter.lean" "$SIDE/README.md" "$SIDE/verify.sh" "$RUN/"

  MATHLIB_COMMIT=$(git -C "$CACHE/.lake/packages/mathlib" rev-parse HEAD)
  printf 'MATHLIB_COMMIT=%s\n' "$MATHLIB_COMMIT"
  test "$MATHLIB_COMMIT" = 0df444a360eaa60ab8c11dca51a86af692955474
  "$LEAN" --version

  export LEAN_PATH="$RUN"
  for PACKAGE in "$CACHE"/.lake/packages/*; do
    LIB="$PACKAGE/.lake/build/lib/lean"
    if test -d "$LIB"; then LEAN_PATH="$LEAN_PATH:$LIB"; fi
  done
  printf 'LEAN_PATH=%s\n' "$LEAN_PATH"

  sha256sum "$SIDE/Fin6IndexAdapter.lean" "$SIDE/README.md" "$SIDE/verify.sh" \
    > "$RUN/input.sha256"
  printf 'SOURCE_SNAPSHOT_COMPLETE\n'

  set +e
  "$LEAN" -DwarningAsError=true --root="$RUN" \
    -o "$RUN/Fin6IndexAdapter.olean" "$RUN/Fin6IndexAdapter.lean"
  CODE=$?
  set -e
  printf 'Fin6IndexAdapter_COMPILE_EXIT_CODE=%s\n' "$CODE"
  if test "$CODE" -ne 0; then exit "$CODE"; fi

  if rg -n --glob 'Fin6IndexAdapter.lean' '\b(sorry|admit)\b|axiom[[:space:]]' "$RUN"; then
    printf 'SOURCE_RESTRICTION_CHECK=FAILED\n'
    exit 1
  fi
  printf 'SOURCE_RESTRICTION_CHECK=PASSED\n'
  sha256sum "$RUN/Fin6IndexAdapter.lean" "$RUN/Fin6IndexAdapter.olean"
  printf 'FUNCTION_LEVEL_FRAME_BINDING=OPEN\n'
  printf 'FUNCTION_LEVEL_MASS_BINDING=OPEN\n'
  printf 'END_UTC=%s\n' "$(date -u +%FT%TZ)"
) > "$RUN/terminal.log" 2>&1
CODE=$?
set -e
cat "$RUN/terminal.log"
exit "$CODE"
