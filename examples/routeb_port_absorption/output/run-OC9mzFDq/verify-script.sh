#!/usr/bin/env bash
set -euo pipefail
SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
CACHE=/home/z5242/sos_lean
LEAN=/home/z5242/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean
mkdir -p "$SIDE/output"
RUN=$(mktemp -d "$SIDE/output/run-XXXXXXXX")
exec > >(tee "$RUN/verify.log") 2>&1
trap 'rc=$?; printf "VERIFY_EXIT_CODE=%s\n" "$rc"' EXIT
printf 'UTC: %s\nRun: %s\n' "$(date -u +%FT%TZ)" "$RUN"
test "$(git -C "$CACHE/.lake/packages/mathlib" rev-parse HEAD)" = 0df444a360eaa60ab8c11dca51a86af692955474
test "$(tr -d '\r\n' < "$CACHE/.lake/packages/mathlib/lean-toolchain")" = leanprover/lean4:v4.33.1
"$LEAN" --version
printf 'MATHLIB_COMMIT=%s\n' "$(git -C "$CACHE/.lake/packages/mathlib" rev-parse HEAD)"
sha256sum "$SIDE/PortAbsorption.lean" "$SIDE/verify.sh" "$CACHE/lake-manifest.json"
cp "$SIDE/PortAbsorption.lean" "$RUN/PortAbsorption.lean"
cp "$SIDE/verify.sh" "$RUN/verify-script.sh"
export LEAN_PATH="$RUN"
for PACKAGE in "$CACHE"/.lake/packages/*; do
  LIB="$PACKAGE/.lake/build/lib/lean"
  if test -d "$LIB"; then LEAN_PATH="$LEAN_PATH:$LIB"; fi
done
set +e
"$LEAN" -DwarningAsError=true --root="$RUN" -o "$RUN/PortAbsorption.olean" "$RUN/PortAbsorption.lean" 2>&1 | tee "$RUN/compile.log"
COMPILE_RC=${PIPESTATUS[0]}
set -e
printf 'LEAN_COMPILE_EXIT_CODE=%s\n' "$COMPILE_RC"
test "$COMPILE_RC" -eq 0 || exit "$COMPILE_RC"
sha256sum "$RUN/PortAbsorption.olean"
