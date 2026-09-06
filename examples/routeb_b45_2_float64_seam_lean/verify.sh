#!/usr/bin/env bash
set -euo pipefail

SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
CACHE=${ROUTEB_LEAN_CACHE:-/home/z5242/sos_lean}
LEAN_BIN=${ROUTEB_LEAN_BIN:-/home/z5242/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean}
EXPECTED_MATHLIB=0df444a360eaa60ab8c11dca51a86af692955474

test "$(tr -d '\r\n' < "$SIDE/lean-toolchain")" = leanprover/lean4:v4.33.1
test -x "$LEAN_BIN"
test "$(git -C "$CACHE/.lake/packages/mathlib" rev-parse HEAD)" = "$EXPECTED_MATHLIB"

mkdir -p "$SIDE/output"
RUN=$(mktemp -d "$SIDE/output/run-XXXXXXXX")
exec > >(tee "$RUN/verify.log") 2>&1

printf 'Output: %s\nUTC: %s\n' "$RUN" "$(date -u +%FT%TZ)"
"$LEAN_BIN" --version
printf 'Mathlib commit: %s\n' "$EXPECTED_MATHLIB"

export LEAN_PATH=''
for PACKAGE in "$CACHE"/.lake/packages/*; do
  LIB="$PACKAGE/.lake/build/lib/lean"
  if test -d "$LIB"; then
    LEAN_PATH="${LEAN_PATH:+$LEAN_PATH:}$LIB"
  fi
done

printf 'Input SHA256:\n'
sha256sum "$SIDE/Float64Seam.lean" "$SIDE/lean-toolchain" "$SIDE/verify.sh"
if grep -nE '\b(sorry|admit|unsafe|native_decide|implemented_by)\b' "$SIDE/Float64Seam.lean"; then
  printf 'FAIL: forbidden proof escape token\n'
  exit 1
fi

printf 'Command: %s -DwarningAsError=true --root=%s -o %s %s\n' \
  "$LEAN_BIN" "$SIDE" "$RUN/Float64Seam.olean" "$SIDE/Float64Seam.lean"
"$LEAN_BIN" -DwarningAsError=true --root="$SIDE" -o "$RUN/Float64Seam.olean" \
  "$SIDE/Float64Seam.lean" 2>&1 | tee "$RUN/compile.log"

if grep -q 'sorryAx' "$RUN/compile.log"; then
  printf 'FAIL: sorryAx appeared in the axiom audit\n'
  exit 1
fi

AXIOM_LINES=$(grep -c 'depends on axioms:' "$RUN/compile.log" || true)
if test "$AXIOM_LINES" -ne 14; then
  printf 'FAIL: expected 14 axiom reports, got %s\n' "$AXIOM_LINES"
  exit 1
fi
if grep 'depends on axioms:' "$RUN/compile.log" | grep -vE '\[(propext, Classical.choice, Quot.sound|propext, Classical.choice, Quot.sound)\]'; then
  printf 'FAIL: unexpected axiom in report\n'
  exit 1
fi

sha256sum "$RUN/Float64Seam.olean" "$RUN/compile.log"
printf 'PASS: targeted seam compilation; 14 reports; no proof holes; no comparator/state/registry input.\n'
