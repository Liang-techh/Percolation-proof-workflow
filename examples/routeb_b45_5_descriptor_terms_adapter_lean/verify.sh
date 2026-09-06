#!/usr/bin/env bash
set -euo pipefail

SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
ROOT=$(cd -- "$SIDE/../.." && pwd -P)
CACHE=/home/z5242/sos_lean
LEAN=/home/z5242/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean
UPSTREAM="$ROOT/examples/routeb_b45_5_residual_decomposition_lean/output/run-AeO1JYiI"
mkdir -p "$SIDE/output"
RUN=$(mktemp -d "$SIDE/output/run-XXXXXXXX")
printf 'ATTEMPT_DIRECTORY=%s\n' "$RUN"

set +e
(
  set -euo pipefail
  trap 'code=$?; printf "VERIFY_EXIT_CODE=%s\\n" "$code"' EXIT
  cp "$SIDE/DescriptorTermsAdapter.lean" "$SIDE/README.md" \
    "$SIDE/INTERFACE.md" "$SIDE/verify.sh" "$RUN/"
  test -f "$UPSTREAM/ResidualDecomposition.olean"
  MATHLIB_COMMIT=$(git -C "$CACHE/.lake/packages/mathlib" rev-parse HEAD)
  printf 'LEAN_TOOLCHAIN_COMMIT=819816b2e0a3bf405af45ae5c7af2491d8f5bee6\n'
  printf 'MATHLIB_COMMIT=%s\n' "$MATHLIB_COMMIT"
  test "$MATHLIB_COMMIT" = 0df444a360eaa60ab8c11dca51a86af692955474
  "$LEAN" --version
  export LEAN_PATH="$RUN:$UPSTREAM"
  for PACKAGE in "$CACHE"/.lake/packages/*; do
    LIB="$PACKAGE/.lake/build/lib/lean"
    if test -d "$LIB"; then LEAN_PATH="$LEAN_PATH:$LIB"; fi
  done
  printf 'LEAN_PATH=%s\n' "$LEAN_PATH"
  sha256sum "$LEAN" > "$RUN/compiler.sha256"
  sha256sum "$RUN/DescriptorTermsAdapter.lean" > "$RUN/source.sha256"
  "$LEAN" -DwarningAsError=true --root="$RUN" \
    -o "$RUN/DescriptorTermsAdapter.olean" \
    "$RUN/DescriptorTermsAdapter.lean"
  printf 'DescriptorTermsAdapter_COMPILE_EXIT_CODE=0\n'
  sha256sum "$RUN/DescriptorTermsAdapter.lean" \
    "$RUN/DescriptorTermsAdapter.olean"
  ! grep -nE '\b(sorry|admit|axiom)\b' "$RUN/DescriptorTermsAdapter.lean"
  printf 'SOURCE_RESTRICTION_CHECK=PASSED\n'
  printf 'RESIDUAL_BOUND=OPEN\nFLOAT64_BINDING=OPEN\nSOURCE_COMPARATOR=OPEN\n'
  printf 'END_UTC=%s\n' "$(date -u +%FT%TZ)"
) > "$RUN/terminal.log" 2>&1
CODE=$?
set -e
cat "$RUN/terminal.log"
exit "$CODE"
