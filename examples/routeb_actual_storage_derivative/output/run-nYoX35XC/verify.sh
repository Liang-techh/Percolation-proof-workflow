#!/usr/bin/env bash
set -euo pipefail
SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
ROOT=$(cd -- "$SIDE/../.." && pwd -P)
CACHE=/home/z5242/sos_lean
LEAN=/home/z5242/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean
PARENT="$ROOT/examples/routeb_actual_energy_storage_lean"
UPSTREAM="$PARENT/output/run-ZWEIdfZ8"
mkdir -p "$SIDE/output"
RUN=$(mktemp -d "$SIDE/output/run-XXXXXXXX")
printf 'ATTEMPT_DIRECTORY=%s\n' "$RUN"
set +e
(
  set -euo pipefail
  trap 'code=$?; printf "VERIFY_EXIT_CODE=%s\n" "$code"' EXIT
  printf 'START_UTC=%s\n' "$(date -u +%FT%TZ)"
  cp "$SIDE/ActualStorageDerivative.lean" "$SIDE/verify.sh" "$SIDE/README.md" "$SIDE/ATTEMPT_HISTORY.md" "$RUN/"
  cp -a "$UPSTREAM" "$RUN/upstream"
  cp "$PARENT/FINAL_RECEIPT.md" "$RUN/upstream_receipt.md"
  grep -q '^ActualStorage_COMPILE_EXIT_CODE=0$' "$RUN/upstream/terminal.log"
  grep -q '^VERIFY_EXIT_CODE=0$' "$RUN/upstream/terminal.log"
  cmp "$PARENT/ActualStorage.lean" "$RUN/upstream/ActualStorage.lean"
  cmp "$PARENT/ReferenceMass.lean" "$RUN/upstream/ReferenceMass.lean"
  test "$(sha256sum "$RUN/upstream/ActualStorage.olean" | cut -d' ' -f1)" = 7b3f8836286e56b7b306faf5bca26338752a16b1c271a2b6eb51a524bd05ae97
  test "$(sha256sum "$RUN/upstream/cache/ReferenceMass.olean" | cut -d' ' -f1)" = 9e84474ff4d5aa440e9dcf1054e0f22b645fa6e645f42cd351e58e9057e70d43
  test "$(sha256sum "$RUN/upstream/cache/SignedGap.olean" | cut -d' ' -f1)" = 498aed10c67f6988066d16fa510bcfde461be3be0b6cb546ed326b4a56c4300e
  REV=$(git -C "$CACHE/.lake/packages/mathlib" rev-parse HEAD)
  printf 'MATHLIB_COMMIT=%s\n' "$REV"
  test "$REV" = 0df444a360eaa60ab8c11dca51a86af692955474
  "$LEAN" --version
  sha256sum "$LEAN" > "$RUN/compiler.sha256"
  export LEAN_PATH="$RUN:$RUN/upstream:$RUN/upstream/cache"
  for PACKAGE in "$CACHE"/.lake/packages/*; do
    LIB="$PACKAGE/.lake/build/lib/lean"
    if test -d "$LIB"; then LEAN_PATH="$LEAN_PATH:$LIB"; fi
  done
  printf 'LEAN_PATH=%s\n' "$LEAN_PATH"
  find "$RUN" -type f ! -path "$RUN/terminal.log" ! -path "$RUN/before_run.sha256" -print0 |
    sort -z | xargs -0 sha256sum > "$RUN/before_run.sha256"
  printf 'PRE_RUN_SNAPSHOTS_COMPLETE\n'
  printf 'COMMAND=%s -DwarningAsError=true --root=%s -o %s/ActualStorageDerivative.olean %s/ActualStorageDerivative.lean\n' "$LEAN" "$RUN" "$RUN" "$RUN"
  set +e
  "$LEAN" -DwarningAsError=true --root="$RUN" -o "$RUN/ActualStorageDerivative.olean" "$RUN/ActualStorageDerivative.lean"
  CODE=$?
  set -e
  printf 'ActualStorageDerivative_COMPILE_EXIT_CODE=%s\n' "$CODE"
  test "$CODE" -eq 0
  sha256sum --check --status "$RUN/before_run.sha256"
  printf 'SNAPSHOT_HASHES_UNCHANGED=true\n'
  sha256sum "$RUN/ActualStorageDerivative.lean" "$RUN/ActualStorageDerivative.olean"
  printf 'END_UTC=%s\n' "$(date -u +%FT%TZ)"
) > "$RUN/terminal.log" 2>&1
CODE=$?
set -e
cat "$RUN/terminal.log"
exit "$CODE"
