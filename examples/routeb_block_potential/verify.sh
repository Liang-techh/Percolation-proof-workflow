#!/usr/bin/env bash
set -euo pipefail
SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
CACHE=/home/z5242/sos_lean
LEAN=/home/z5242/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean
BASE="$SIDE/../routeb_potential_slice/output/run-SuGxG04V"
OBSTRUCTION="$SIDE/../routeb_dh_power_binding/output/tube-RWfVZNvn"
mkdir -p "$SIDE/output"
RUN=$(mktemp -d "$SIDE/output/run-XXXXXXXX")
exec > >(tee "$RUN/verify.log") 2>&1
trap 'code=$?; printf "VERIFY_EXIT_CODE=%s\n" "$code"' EXIT
printf 'UTC: %s\nRun: %s\n' "$(date -u +%FT%TZ)" "$RUN"
test "$(git -C "$CACHE/.lake/packages/mathlib" rev-parse HEAD)" = 0df444a360eaa60ab8c11dca51a86af692955474
test -f "$BASE/PotentialSlice.olean"
test -f "$OBSTRUCTION/StorageObstruction.olean"
"$LEAN" --version
export LEAN_PATH="$RUN:$BASE:$OBSTRUCTION"
for PACKAGE in "$CACHE"/.lake/packages/*; do
  LIB="$PACKAGE/.lake/build/lib/lean"
  if test -d "$LIB"; then LEAN_PATH="$LEAN_PATH:$LIB"; fi
done
python3 -B "$SIDE/audit.py"
cp "$SIDE/BlockPotential.lean" "$RUN/BlockPotential.lean"
sha256sum "$SIDE/BlockPotential.lean" "$SIDE/audit.py" "$SIDE/audit_results.json" \
  "$BASE/PotentialSlice.olean" "$OBSTRUCTION/StorageObstruction.olean"
set +e
"$LEAN" -DwarningAsError=true --root="$SIDE" -o "$RUN/BlockPotential.olean" \
  "$SIDE/BlockPotential.lean" 2>&1 | tee "$RUN/BlockPotential.log"
CODE=${PIPESTATUS[0]}
set -e
printf 'LEAN_COMPILE_EXIT_CODE=%s\n' "$CODE"
test "$CODE" -eq 0
if grep -q 'sorryAx' "$RUN/BlockPotential.log"; then exit 1; fi
sha256sum "$RUN/BlockPotential.olean"
