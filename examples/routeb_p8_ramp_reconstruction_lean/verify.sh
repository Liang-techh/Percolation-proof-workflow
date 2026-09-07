#!/usr/bin/env bash
set -euo pipefail

SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
ROOT=$(cd -- "$SIDE/../.." && pwd -P)
LAKE_ROOT=${ROUTEB_P8_RAMP_LAKE_ROOT:-$ROOT/examples/local_fkg}
LEAN_BIN=${ROUTEB_P8_RAMP_LEAN_BIN:-}
if test -z "$LEAN_BIN"; then
  for CANDIDATE in \
    /home/z5242/.elan/toolchains/leanprover--lean4---v4.32.0/bin/lean \
    /mnt/c/Users/z5242/.elan/bin/lean.exe; do
    if test -x "$CANDIDATE"; then LEAN_BIN="$CANDIDATE"; break; fi
  done
fi
if test -z "$LEAN_BIN" && command -v lean >/dev/null 2>&1; then LEAN_BIN=$(command -v lean); fi
test "$(tr -d '\r\n' < "$LAKE_ROOT/lean-toolchain")" = "leanprover/lean4:v4.32.0"
test -n "$LEAN_BIN"
mkdir -p "$SIDE/output"
RUN=$(mktemp -d "$SIDE/output/run-XXXXXXXX")
exec > >(tee "$RUN/verify.log") 2>&1
printf 'Output: %s\nUTC: %s\n' "$RUN" "$(date -u +%FT%TZ)"
"$LEAN_BIN" --version
export LEAN_PATH=''
for PACKAGE in "$LAKE_ROOT"/.lake/packages/*; do
  LIB="$PACKAGE/.lake/build/lib/lean"
  if test -d "$LIB"; then LEAN_PATH="${LEAN_PATH:+$LEAN_PATH:}$LIB"; fi
done
sha256sum "$SIDE/RampReconstruction.lean" "$SIDE/lean-toolchain" "$SIDE/verify.sh"
if grep -nE '(^|[^[:alnum:]_])(sorry|admit)([^[:alnum:]_]|$)|^[[:space:]]*axiom[[:space:]]|native_decide|implemented_by|^[[:space:]]*unsafe[[:space:]]' "$SIDE/RampReconstruction.lean"; then
  echo 'FAIL: forbidden proof escape token'; exit 1
fi
set +e
"$LEAN_BIN" -DwarningAsError=true --root="$SIDE" -o "$RUN/RampReconstruction.olean" \
  "$SIDE/RampReconstruction.lean" 2>&1 | tee "$RUN/compile.log"
CODE=${PIPESTATUS[0]}
set -e
printf 'RAMP_RECONSTRUCTION_COMPILE_EXIT_CODE=%s\n' "$CODE"
test "$CODE" -eq 0
for DECLARATION in constant_of_zero_derivative ramp_reconstruction terminal_transfer_one; do
  grep -q "'RouteBP8RampReconstruction.$DECLARATION' depends on axioms:" "$RUN/compile.log" || {
    echo "FAIL: missing axiom report for $DECLARATION"; exit 1;
  }
done
if grep -Eiq 'sorryAx|declaration uses.*axiom|(^|[^[:alnum:]_])admit([^[:alnum:]_]|$)|^[[:space:]]*axiom[[:space:]]' "$RUN/compile.log"; then
  echo 'FAIL: forbidden or custom axiom appeared in axiom audit'; exit 1
fi
sha256sum "$RUN/RampReconstruction.olean" "$RUN/compile.log"
echo 'FOCUSED_CHECK=PASS'
echo 'EXACT_RAMP_RECONSTRUCTION=PASS'
echo 'FLOWPIPE_COVERAGE=OPEN'
echo 'PHYSICAL_SOURCE_BINDING=OPEN'
echo 'REGISTRY_MUTATION=false'
