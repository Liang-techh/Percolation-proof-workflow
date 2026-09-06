#!/usr/bin/env bash
set -euo pipefail
SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
CACHE=/home/z5242/sos_lean
LEAN=/home/z5242/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean
mkdir -p "$SIDE/output"
RUN=$(mktemp -d "$SIDE/output/run-XXXXXXXX")
exec > >(tee "$RUN/terminal.log") 2>&1
trap 'rc=$?; printf "VERIFY_EXIT_CODE=%s\n" "$rc"' EXIT
printf 'START_UTC=%s\nRUN=%s\n' "$(date -u +%FT%TZ)" "$RUN"
test "$(git -C "$CACHE/.lake/packages/mathlib" rev-parse HEAD)" = 0df444a360eaa60ab8c11dca51a86af692955474
"$LEAN" --version
cp "$SIDE/TerminalCapAE.lean" "$RUN/"
export LEAN_PATH="$RUN"
for PACKAGE in "$CACHE"/.lake/packages/*; do
  LIB="$PACKAGE/.lake/build/lib/lean"
  if test -d "$LIB"; then LEAN_PATH="$LEAN_PATH:$LIB"; fi
done
sha256sum "$RUN/TerminalCapAE.lean"
"$LEAN" -DwarningAsError=true --root="$RUN" -o "$RUN/TerminalCapAE.olean" "$RUN/TerminalCapAE.lean"
printf 'LEAN_COMPILE_EXIT_CODE=0\n'
sha256sum "$RUN/TerminalCapAE.olean"
