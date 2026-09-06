#!/usr/bin/env bash
set -euo pipefail
SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
ROOT=$(cd -- "$SIDE/../.." && pwd -P)
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
  cp "$SIDE/PositiveSupplyGate.lean" "$SIDE/audit.py" "$SIDE/DERIVATION.md" "$SIDE/README.md" "$SIDE/verify.sh" "$RUN/"
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
  sha256sum "$LEAN" > "$RUN/compiler.sha256"
  find "$RUN" -type f ! -name terminal.log ! -name before_run.sha256 -print0 |
    sort -z | xargs -0 sha256sum > "$RUN/before_run.sha256"
  printf 'PROSPECTIVE_SNAPSHOT_COMPLETE\n'
  python3 -B "$RUN/audit.py" "$RUN"
  printf 'COMMAND=%s -DwarningAsError=true --root=%s -o %s/PositiveSupplyGate.olean %s/PositiveSupplyGate.lean\n' "$LEAN" "$RUN" "$RUN" "$RUN"
  set +e
  "$LEAN" -DwarningAsError=true --root="$RUN" -o "$RUN/PositiveSupplyGate.olean" "$RUN/PositiveSupplyGate.lean"
  CODE=$?
  set -e
  printf 'PositiveSupplyGate_COMPILE_EXIT_CODE=%s\n' "$CODE"
  test "$CODE" -eq 0
  sha256sum "$RUN/PositiveSupplyGate.lean" "$RUN/PositiveSupplyGate.olean"
  sha256sum --check --status "$RUN/before_run.sha256"
  printf 'SNAPSHOT_HASHES_UNCHANGED=true\nEND_UTC=%s\n' "$(date -u +%FT%TZ)"
) > "$RUN/terminal.log" 2>&1
CODE=$?
set -e
cat "$RUN/terminal.log"
exit "$CODE"
