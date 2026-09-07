#!/usr/bin/env bash
# Offline focused verifier.  It never invokes elan installation or lake update.
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
test "$(git -C "$MATHLIB" rev-parse HEAD)" = "$EXPECTED_MATHLIB"
"$LEAN_BIN" --version
printf 'MATHLIB_COMMIT=%s\n' "$EXPECTED_MATHLIB"

if grep -nE '\b(sorry|admit|axiom|native_decide|implemented_by|unsafe)\b' \
    "$SIDE/JointPSigmaBudget.lean"; then
  printf 'FAIL: forbidden proof escape token\n'
  exit 1
fi

sha256sum "$SIDE/JointPSigmaBudget.lean" "$SIDE/lean-toolchain" \
  "$SIDE/lakefile.toml" "$SIDE/verify.sh" "$CACHE/lake-manifest.json"

# Bypass Lake entirely.  Only prebuilt cached libraries are placed on LEAN_PATH.
export LEAN_PATH=''
for PACKAGE in "$CACHE"/.lake/packages/*; do
  LIB="$PACKAGE/.lake/build/lib/lean"
  if test -d "$LIB"; then LEAN_PATH="${LEAN_PATH:+$LEAN_PATH:}$LIB"; fi
done

set +e
"$LEAN_BIN" -DwarningAsError=true --root="$SIDE" \
  -o "$RUN/JointPSigmaBudget.olean" "$SIDE/JointPSigmaBudget.lean" \
  2>&1 | tee "$RUN/compile.log"
COMPILE_RC=${PIPESTATUS[0]}
set -e
printf 'LEAN_COMPILE_EXIT_CODE=%s\n' "$COMPILE_RC"
test "$COMPILE_RC" -eq 0

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
   if (count != 10 || bad) exit 1
 }' "$RUN/compile.log"

sha256sum "$RUN/JointPSigmaBudget.olean"
printf 'PASS: 10 theorem axiom reports; zero proof holes; no custom axioms.\n'
