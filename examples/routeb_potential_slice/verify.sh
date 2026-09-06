#!/usr/bin/env bash
set -euo pipefail
SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
CACHE=/home/z5242/sos_lean
LEAN=/home/z5242/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean
BASE="$SIDE/../routeb_dh_power_binding/output/tube-RWfVZNvn"
mkdir -p "$SIDE/output"
RUN=$(mktemp -d "$SIDE/output/run-XXXXXXXX")
exec > >(tee "$RUN/verify.log") 2>&1
trap 'code=$?; printf "VERIFY_EXIT_CODE=%s\n" "$code"' EXIT
printf 'UTC: %s\nRun: %s\n' "$(date -u +%FT%TZ)" "$RUN"
test "$(git -C "$CACHE/.lake/packages/mathlib" rev-parse HEAD)" = 0df444a360eaa60ab8c11dca51a86af692955474
test -f "$BASE/StorageObstruction.olean"
"$LEAN" --version
export LEAN_PATH="$RUN:$BASE"
for PACKAGE in "$CACHE"/.lake/packages/*; do
  LIB="$PACKAGE/.lake/build/lib/lean"
  if test -d "$LIB"; then LEAN_PATH="$LEAN_PATH:$LIB"; fi
done
python3 -B "$SIDE/audit_source.py" --output "$RUN/source_evidence.json"
cp "$SIDE/PotentialSlice.lean" "$RUN/PotentialSlice.lean"
sha256sum "$SIDE/verify.sh" "$SIDE/audit_source.py"
set +e
"$LEAN" -DwarningAsError=true --root="$SIDE" -o "$RUN/PotentialSlice.olean" \
  "$SIDE/PotentialSlice.lean" 2>&1 | tee "$RUN/PotentialSlice.log"
CODE=${PIPESTATUS[0]}
set -e
printf 'LEAN_COMPILE_EXIT_CODE=%s\n' "$CODE"
test "$CODE" -eq 0
if grep -Eq 'sorryAx|uses .sorry.|declaration uses' "$RUN/PotentialSlice.log"; then exit 1; fi
sha256sum "$RUN/PotentialSlice.olean"
