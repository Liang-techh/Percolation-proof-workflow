#!/usr/bin/env bash
# Offline compilation. Never invokes elan, lake update/build, or a downloader.
set -euo pipefail
SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
CACHE=${ROUTEB_LEAN_CACHE:-/home/z5242/sos_lean}
LEAN_BIN=${ROUTEB_LEAN_BIN:-/home/z5242/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean}
MATHLIB="$CACHE/.lake/packages/mathlib"
EXPECTED_MATHLIB=0df444a360eaa60ab8c11dca51a86af692955474
mkdir -p "$SIDE/output"
RUN=$(mktemp -d "$SIDE/output/run-XXXXXXXX")
exec > >(tee "$RUN/verify.log") 2>&1
printf 'Output: %s\nUTC: %s\n' "$RUN" "$(date -u +%FT%TZ)"
test "$(tr -d '\r\n' < "$SIDE/lean-toolchain")" = leanprover/lean4:v4.33.1
test "$(tr -d '\r\n' < "$MATHLIB/lean-toolchain")" = leanprover/lean4:v4.33.1
test -x "$LEAN_BIN"
"$LEAN_BIN" --version
test "$(git -C "$MATHLIB" rev-parse HEAD)" = "$EXPECTED_MATHLIB"
printf 'Mathlib commit: %s\n' "$EXPECTED_MATHLIB"
printf 'Existing dependency revisions (read-only cache):\n'
for PACKAGE in "$CACHE"/.lake/packages/*; do
  if test -d "$PACKAGE/.git"; then
    printf '%s ' "$(basename "$PACKAGE")"
    git -C "$PACKAGE" rev-parse HEAD
  fi
done
printf 'Input SHA256:\n'
sha256sum "$SIDE/RouteBSupplyCore.lean" "$SIDE/lean-toolchain" "$SIDE/verify.sh" \
  "$CACHE/lake-manifest.json"
if grep -nE '\b(sorry|admit|axiom|native_decide|implemented_by|unsafe)\b' \
    "$SIDE/RouteBSupplyCore.lean"; then
  printf 'FAIL: forbidden proof escape token\n'
  exit 1
fi
# Bypass Lake entirely so no imported projects or cached packages are rebuilt.
export LEAN_PATH=''
for PACKAGE in "$CACHE"/.lake/packages/*; do
  LIB="$PACKAGE/.lake/build/lib/lean"
  if test -d "$LIB"; then
    LEAN_PATH="${LEAN_PATH:+$LEAN_PATH:}$LIB"
  fi
done
printf 'Command: %s -DwarningAsError=true --root=%s -o %s %s\n' \
  "$LEAN_BIN" "$SIDE" "$RUN/RouteBSupplyCore.olean" "$SIDE/RouteBSupplyCore.lean"
"$LEAN_BIN" -DwarningAsError=true --root="$SIDE" -o "$RUN/RouteBSupplyCore.olean" \
  "$SIDE/RouteBSupplyCore.lean" 2>&1 | tee "$RUN/compile.log"
printf 'Lean exit code: 0\n'
# Check all 18 #print outputs; only Lean/Mathlib's standard foundations allowed.
awk '
 /depends on axioms:|does not depend on any axioms/ {
   count++
   if ($0 ~ /depends on axioms:/) {
     line=$0; sub(/^.*\[/, "", line); sub(/\].*$/, "", line)
     gsub(/,/, " ", line); n=split(line, names, /[[:space:]]+/)
     for (i=1; i<=n; i++)
       if (names[i] != "" && names[i] != "propext" &&
           names[i] != "Classical.choice" && names[i] != "Quot.sound") bad=1
   }
 }
 END {
   printf "Axiom audit: %d declarations; unexpected axioms: %d\n", count, bad+0
   if (count != 18 || bad) exit 1
 }' "$RUN/compile.log"
sha256sum "$RUN/RouteBSupplyCore.olean"
printf 'PASS: 18 theorem axiom reports; zero proof holes; no custom axioms.\n'
