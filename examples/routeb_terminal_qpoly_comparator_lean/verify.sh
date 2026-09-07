#!/usr/bin/env bash
set -euo pipefail
SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
CACHE=/home/z5242/sos_lean
LEAN=/home/z5242/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean
MATHLIB_COMMIT=0df444a360eaa60ab8c11dca51a86af692955474
mkdir -p "$SIDE/output"
RUN=$(mktemp -d "$SIDE/output/run-XXXXXXXX")
trap 'code=$?; printf "VERIFY_EXIT_CODE=%s\\n" "$code"' EXIT
cp "$SIDE/F4DirectQpolyComparator.lean" "$SIDE/README.md" "$SIDE/REPORT.md" "$SIDE/lean-toolchain" "$RUN/"
test "$(git -C "$CACHE/.lake/packages/mathlib" rev-parse HEAD)" = "$MATHLIB_COMMIT"
export LEAN_PATH="$RUN"
for PACKAGE in "$CACHE"/.lake/packages/*; do
  LIB="$PACKAGE/.lake/build/lib/lean"
  if test -d "$LIB"; then LEAN_PATH="$LEAN_PATH:$LIB"; fi
done
"$LEAN" --version
printf 'MATHLIB_COMMIT=%s\n' "$MATHLIB_COMMIT"
printf 'LEAN_PATH=%s\n' "$LEAN_PATH"
sha256sum "$SIDE/F4DirectQpolyComparator.lean" "$SIDE/README.md" "$SIDE/REPORT.md" "$SIDE/lean-toolchain" > "$RUN/input.sha256"
set +e
"$LEAN" -DwarningAsError=true --root="$RUN" -o "$RUN/F4DirectQpolyComparator.olean" "$RUN/F4DirectQpolyComparator.lean" > "$RUN/compile.log" 2>&1
CODE=$?
set -e
cat "$RUN/compile.log"
printf 'F4DirectQpolyComparator_COMPILE_EXIT_CODE=%s\n' "$CODE"
test "$CODE" -eq 0
if grep -nE '(^|[^[:alnum:]_])(sorry|admit)([^[:alnum:]_]|$)|^[[:space:]]*(axiom|unsafe)[[:space:]]' "$RUN/F4DirectQpolyComparator.lean"; then
  printf 'SOURCE_RESTRICTION_CHECK=FAILED\n'
  exit 1
fi
printf 'SOURCE_RESTRICTION_CHECK=PASSED\n'
sha256sum "$RUN/F4DirectQpolyComparator.lean" "$RUN/F4DirectQpolyComparator.olean"
printf 'DEPLOYED_DH_D_GATE_PROOF=OPEN\nREGISTRY_PROMOTION=NOT_CLAIMED\n'
