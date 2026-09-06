#!/usr/bin/env bash
set -euo pipefail

SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
LEAN=/home/z5242/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean
CACHE=/home/z5242/sos_lean
MATHLIB_COMMIT=0df444a360eaa60ab8c11dca51a86af692955474

mkdir -p "$SIDE/output"
RUN=$(mktemp -d "$SIDE/output/run-XXXXXXXX")
printf 'ATTEMPT_DIRECTORY=%s\n' "$RUN"

set +e
(
  set -euo pipefail
  trap 'code=$?; printf "VERIFY_EXIT_CODE=%s\n" "$code"' EXIT
  printf 'START_UTC=%s\n' "$(date -u +%FT%TZ)"
  cp "$SIDE/OriginQuadratic.lean" "$SIDE/verify.sh" "$RUN/"
  REV=$(git -C "$CACHE/.lake/packages/mathlib" rev-parse HEAD)
  printf 'MATHLIB_COMMIT=%s\n' "$REV"
  test "$REV" = "$MATHLIB_COMMIT"
  "$LEAN" --version
  export LEAN_PATH="$CACHE/.lake/packages/mathlib/.lake/build/lib/lean:$CACHE/.lake/packages/batteries/.lake/build/lib/lean:$CACHE/.lake/packages/aesop/.lake/build/lib/lean:$CACHE/.lake/packages/Qq/.lake/build/lib/lean:$CACHE/.lake/packages/proofwidgets/.lake/build/lib/lean:$CACHE/.lake/packages/LeanSearchClient/.lake/build/lib/lean:$CACHE/.lake/packages/importGraph/.lake/build/lib/lean:$CACHE/.lake/packages/plausible/.lake/build/lib/lean"
  printf 'LEAN_PATH=%s\n' "$LEAN_PATH"
  sha256sum "$LEAN" > "$RUN/compiler.sha256"
  find "$RUN" -type f ! -name terminal.log ! -name before_run.sha256 -print0 |
    sort -z | xargs -0 sha256sum > "$RUN/before_run.sha256"
  printf 'PRE_RUN_SNAPSHOTS_COMPLETE\n'
  printf 'COMMAND=%s -DwarningAsError=true --root=%s -o %s/OriginQuadratic.olean %s/OriginQuadratic.lean\n' "$LEAN" "$RUN" "$RUN" "$RUN"
  set +e
  "$LEAN" -DwarningAsError=true --root="$RUN" -o "$RUN/OriginQuadratic.olean" "$RUN/OriginQuadratic.lean"
  CODE=$?
  set -e
  printf 'OriginQuadratic_COMPILE_EXIT_CODE=%s\n' "$CODE"
  test "$CODE" -eq 0
  sha256sum "$RUN/OriginQuadratic.lean" "$RUN/OriginQuadratic.olean"
  sha256sum --check --status "$RUN/before_run.sha256"
  printf 'SNAPSHOT_HASHES_UNCHANGED=true\nEND_UTC=%s\n' "$(date -u +%FT%TZ)"
) > "$RUN/terminal.log" 2>&1
CODE=$?
set -e
cat "$RUN/terminal.log"
exit "$CODE"
