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
  cp "$SIDE/QProjection.lean" "$SIDE/README.md" \
    "$SIDE/DERIVATION.md" "$SIDE/ATTEMPT_HISTORY.md" "$SIDE/verify.sh" "$RUN/"
  MATHLIB_COMMIT=$(git -C "$CACHE/.lake/packages/mathlib" rev-parse HEAD)
  printf 'LEAN_TOOLCHAIN_COMMIT=819816b2e0a3bf405af45ae5c7af2491d8f5bee6\n'
  printf 'MATHLIB_COMMIT=%s\n' "$MATHLIB_COMMIT"
  test "$MATHLIB_COMMIT" = 0df444a360eaa60ab8c11dca51a86af692955474
  "$LEAN" --version
  export LEAN_PATH="$RUN"
  for PACKAGE in "$CACHE"/.lake/packages/*; do
    LIB="$PACKAGE/.lake/build/lib/lean"
    if test -d "$LIB"; then LEAN_PATH="$LEAN_PATH:$LIB"; fi
  done
  printf 'LEAN_PATH=%s\n' "$LEAN_PATH"
  sha256sum "$LEAN" > "$RUN/compiler.sha256"
  sha256sum "$RUN/QProjection.lean" > "$RUN/source.sha256"
  printf 'COMMAND=%s -DwarningAsError=true --root=%s -o %s/QProjection.olean %s/QProjection.lean\n' \
    "$LEAN" "$RUN" "$RUN" "$RUN"
  set +e
  "$LEAN" -DwarningAsError=true --root="$RUN" \
    -o "$RUN/QProjection.olean" "$RUN/QProjection.lean"
  CODE=$?
  set -e
  printf 'QProjection_COMPILE_EXIT_CODE=%s\n' "$CODE"
  test "$CODE" -eq 0
  sha256sum "$RUN/QProjection.lean" "$RUN/QProjection.olean"
  printf 'NO_SORRY_OR_ADMIT_CHECK=grep_source_after_compile\n'
  ! grep -nE '\b(sorry|admit)\b' "$RUN/QProjection.lean"
  printf 'SNAPSHOT_HASHES_UNCHANGED=true\nEND_UTC=%s\n' "$(date -u +%FT%TZ)"
) > "$RUN/terminal.log" 2>&1
CODE=$?
set -e
cat "$RUN/terminal.log"
exit "$CODE"
