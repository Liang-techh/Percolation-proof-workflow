#!/usr/bin/env bash
set -euo pipefail
SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
CACHE=/home/z5242/sos_lean
LEAN=/home/z5242/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean
mkdir -p "$SIDE/output"
RUN=$(mktemp -d "$SIDE/output/run-XXXXXXXX")
exec > >(tee "$RUN/verify.log") 2>&1
trap 'code=$?; printf "VERIFY_EXIT_CODE=%s\n" "$code"' EXIT
printf 'Run: %s\n' "$RUN"
test "$(git -C "$CACHE/.lake/packages/mathlib" rev-parse HEAD)" = 0df444a360eaa60ab8c11dca51a86af692955474
"$LEAN" --version
export LEAN_PATH="$RUN"
for PACKAGE in "$CACHE"/.lake/packages/*; do
  LIB="$PACKAGE/.lake/build/lib/lean"
  if test -d "$LIB"; then LEAN_PATH="$LEAN_PATH:$LIB"; fi
done
cp "$SIDE/RotationalDual.lean" "$RUN/RotationalDual.lean"
sha256sum "$RUN/RotationalDual.lean" "$SIDE/verify.sh"
set +e
"$LEAN" -DwarningAsError=true --root="$RUN" -o "$RUN/RotationalDual.olean" "$RUN/RotationalDual.lean"
CODE=$?
set -e
printf 'LEAN_COMPILE_EXIT_CODE=%s\n' "$CODE"
test "$CODE" -eq 0
sha256sum "$RUN/RotationalDual.olean"
