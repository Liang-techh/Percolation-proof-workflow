#!/usr/bin/env bash
set -euo pipefail
SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
ROOT=$(cd -- "$SIDE/../.." && pwd -P)
CACHE=/home/z5242/sos_lean
LEAN=/home/z5242/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean
SLOT="$ROOT/examples/routeb_frame_slot_accessor_lean/output/run-4RJoHvpZ"
CONTRACT="$ROOT/examples/routeb_body_contract_core_lean/output/run-0FvNkLzz"
mkdir -p "$SIDE/output"
RUN=$(mktemp -d "$SIDE/output/run-XXXXXXXX")
printf 'ATTEMPT_DIRECTORY=%s\n' "$RUN"
set +e
(
  set -euo pipefail
  trap 'code=$?; printf "VERIFY_EXIT_CODE=%s\\n" "$code"' EXIT
  printf 'START_UTC=%s\n' "$(date -u +%FT%TZ)"
  cp "$SIDE/SourceContractAdapter.lean" "$SIDE/README.md" "$SIDE/verify.sh" "$RUN/"
  test "$(git -C "$CACHE/.lake/packages/mathlib" rev-parse HEAD)" = 0df444a360eaa60ab8c11dca51a86af692955474
  test -f "$SLOT/FrameSlotAccessor.olean"
  test -f "$CONTRACT/BodyContractCore.olean"
  export LEAN_PATH="$RUN:$SLOT:$CONTRACT"
  for PACKAGE in "$CACHE"/.lake/packages/*; do
    LIB="$PACKAGE/.lake/build/lib/lean"
    if test -d "$LIB"; then LEAN_PATH="$LEAN_PATH:$LIB"; fi
  done
  "$LEAN" --version
  printf 'LEAN_PATH=%s\n' "$LEAN_PATH"
  sha256sum "$SIDE/SourceContractAdapter.lean" "$SIDE/README.md" "$SIDE/verify.sh" > "$RUN/input.sha256"
  printf 'SOURCE_SNAPSHOT_COMPLETE=true\n'
  set +e
  "$LEAN" -DwarningAsError=true --root="$RUN" \
    -o "$RUN/SourceContractAdapter.olean" "$RUN/SourceContractAdapter.lean"
  CODE=$?
  set -e
  printf 'SourceContractAdapter_COMPILE_EXIT_CODE=%s\n' "$CODE"
  test "$CODE" -eq 0
  if grep -nE '(^|[^[:alnum:]_])(sorry|admit)([^[:alnum:]_]|$)|^[[:space:]]*axiom[[:space:]]' "$RUN/SourceContractAdapter.lean"; then
    printf 'SOURCE_RESTRICTION_CHECK=FAILED\n'
    exit 1
  fi
  printf 'SOURCE_RESTRICTION_CHECK=PASSED\n'
  sha256sum "$RUN/SourceContractAdapter.lean" "$RUN/SourceContractAdapter.olean"
  printf 'JULIA_FLOAT64_BINDING=OPEN\nFULL_MASS_BINDING=OPEN\n'
  printf 'END_UTC=%s\n' "$(date -u +%FT%TZ)"
) > "$RUN/terminal.log" 2>&1
CODE=$?
set -e
cat "$RUN/terminal.log"
exit "$CODE"
