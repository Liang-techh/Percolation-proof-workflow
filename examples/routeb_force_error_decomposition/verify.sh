#!/usr/bin/env bash
set -euo pipefail
SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
CACHE=/home/z5242/sos_lean
LEAN=/home/z5242/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean
POWER="$SIDE/../routeb_dh_power_binding/output/run-5RHBCcg9"
BLOCK="$SIDE/../routeb_block_potential/output/run-RDCanfXw"
POTENTIAL="$SIDE/../routeb_potential_slice/output/run-SuGxG04V"
OBSTRUCTION="$SIDE/../routeb_dh_power_binding/output/tube-RWfVZNvn"
mkdir -p "$SIDE/output"
RUN=$(mktemp -d "$SIDE/output/run-XXXXXXXX")
exec > >(tee "$RUN/verify.log") 2>&1
trap 'code=$?; printf "VERIFY_EXIT_CODE=%s\n" "$code"' EXIT
printf 'UTC: %s\nRun: %s\n' "$(date -u +%FT%TZ)" "$RUN"
test "$(git -C "$CACHE/.lake/packages/mathlib" rev-parse HEAD)" = 0df444a360eaa60ab8c11dca51a86af692955474
"$LEAN" --version
export LEAN_PATH="$RUN:$POWER:$BLOCK:$POTENTIAL:$OBSTRUCTION"
for PACKAGE in "$CACHE"/.lake/packages/*; do
  LIB="$PACKAGE/.lake/build/lib/lean"
  if test -d "$LIB"; then LEAN_PATH="$LEAN_PATH:$LIB"; fi
done
python3 -B "$SIDE/audit.py"
cp "$SIDE/ForceErrorDecomposition.lean" "$RUN/ForceErrorDecomposition.lean"
cp "$SIDE/source_evidence.json" "$RUN/source_evidence.json"
sha256sum "$SIDE/ForceErrorDecomposition.lean" "$SIDE/audit.py" "$SIDE/verify.sh" \
  "$POWER/DHPowerBinding.olean" "$BLOCK/BlockPotential.olean"
set +e
"$LEAN" -DwarningAsError=true --root="$SIDE" -o "$RUN/ForceErrorDecomposition.olean" \
  "$SIDE/ForceErrorDecomposition.lean" 2>&1 | tee "$RUN/ForceErrorDecomposition.log"
CODE=${PIPESTATUS[0]}
set -e
printf 'LEAN_COMPILE_EXIT_CODE=%s\n' "$CODE"
test "$CODE" -eq 0
if grep -q 'sorryAx' "$RUN/ForceErrorDecomposition.log"; then exit 1; fi
sha256sum "$RUN/ForceErrorDecomposition.olean"
