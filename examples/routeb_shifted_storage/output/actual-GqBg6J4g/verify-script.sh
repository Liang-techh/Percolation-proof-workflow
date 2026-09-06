#!/usr/bin/env bash
set -euo pipefail
SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
CACHE=/home/z5242/sos_lean
LEAN=/home/z5242/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean
SHIFT="$SIDE/output/run-pKu0JIpS"
POTENTIAL="$SIDE/../routeb_potential_slice/output/run-SuGxG04V"
OBSTRUCTION="$SIDE/../routeb_dh_power_binding/output/tube-RWfVZNvn"
mkdir -p "$SIDE/output"
RUN=$(mktemp -d "$SIDE/output/actual-XXXXXXXX")
exec > >(tee "$RUN/verify.log") 2>&1
trap 'rc=$?; printf "VERIFY_EXIT_CODE=%s\n" "$rc"' EXIT
printf 'UTC: %s\nRun: %s\n' "$(date -u +%FT%TZ)" "$RUN"
test "$(git -C "$CACHE/.lake/packages/mathlib" rev-parse HEAD)" = 0df444a360eaa60ab8c11dca51a86af692955474
test "$(tr -d '\r\n' < "$CACHE/.lake/packages/mathlib/lean-toolchain")" = leanprover/lean4:v4.33.1
test -f "$SHIFT/ShiftedStorage.olean"
test -f "$POTENTIAL/PotentialSlice.olean"
test -f "$OBSTRUCTION/StorageObstruction.olean"
"$LEAN" --version
printf 'MATHLIB_COMMIT=%s\n' "$(git -C "$CACHE/.lake/packages/mathlib" rev-parse HEAD)"
sha256sum "$SIDE/ActualShift.lean" "$SIDE/verify_actual.sh" "$CACHE/lake-manifest.json"
sha256sum "$SHIFT/ShiftedStorage.lean" "$SHIFT/ShiftedStorage.olean" \
  "$POTENTIAL/PotentialSlice.lean" "$POTENTIAL/PotentialSlice.olean" \
  "$OBSTRUCTION/StorageObstruction.lean" "$OBSTRUCTION/StorageObstruction.olean"
cp "$SIDE/ActualShift.lean" "$RUN/ActualShift.lean"
cp "$SIDE/verify_actual.sh" "$RUN/verify-script.sh"
export LEAN_PATH="$RUN:$SHIFT:$POTENTIAL:$OBSTRUCTION"
for PACKAGE in "$CACHE"/.lake/packages/*; do
  LIB="$PACKAGE/.lake/build/lib/lean"
  if test -d "$LIB"; then LEAN_PATH="$LEAN_PATH:$LIB"; fi
done
printf 'LEAN_PATH=%s\n' "$LEAN_PATH"
"$LEAN" -DwarningAsError=true --root="$RUN" -o "$RUN/ActualShift.olean" "$RUN/ActualShift.lean" 2>&1 | tee "$RUN/compile.log"
printf 'LEAN_COMPILE_EXIT_CODE=0\n'
if grep -Eq 'sorryAx|uses .sorry.|declaration uses' "$RUN/compile.log"; then exit 1; fi
sha256sum "$RUN/ActualShift.olean"
