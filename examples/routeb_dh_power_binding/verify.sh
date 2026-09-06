#!/usr/bin/env bash
set -euo pipefail
SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
CACHE=/home/z5242/sos_lean
LEAN=/home/z5242/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean
test "$(git -C "$CACHE/.lake/packages/mathlib" rev-parse HEAD)" = 0df444a360eaa60ab8c11dca51a86af692955474
mkdir -p "$SIDE/output"
RUN=$(mktemp -d "$SIDE/output/run-XXXXXXXX")
exec > >(tee "$RUN/verify.log") 2>&1
printf 'UTC: %s\nRun: %s\n' "$(date -u +%FT%TZ)" "$RUN"
"$LEAN" --version
export LEAN_PATH="$RUN"
for PACKAGE in "$CACHE"/.lake/packages/*; do
  LIB="$PACKAGE/.lake/build/lib/lean"
  if test -d "$LIB"; then LEAN_PATH="$LEAN_PATH:$LIB"; fi
done
sha256sum "$SIDE/ExistingEnergyCore.lean"
for ITEM in "$SIDE/../routeb_supply_core/RouteBSupplyCore.lean" "$SIDE/../routeb_residual_power/ResidualPower.lean" "$SIDE/ControllerPowerCore.lean" "$SIDE/DHPowerBinding.lean"; do
  sha256sum "$ITEM"
  NAME=$(basename "$ITEM" .lean)
  "$LEAN" -DwarningAsError=true --root="$(dirname "$ITEM")" -o "$RUN/$NAME.olean" "$ITEM" 2>&1 | tee "$RUN/$NAME.log"
done
printf 'LEAN_COMPILE_EXIT_CODE=0\n'
sha256sum "$RUN/DHPowerBinding.olean"
