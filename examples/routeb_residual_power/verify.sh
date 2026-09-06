#!/usr/bin/env bash
set -euo pipefail
SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
CORE="$SIDE/../routeb_supply_core"
CACHE=/home/z5242/sos_lean
LEAN=/home/z5242/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean
test "$(git -C "$CACHE/.lake/packages/mathlib" rev-parse HEAD)" = 0df444a360eaa60ab8c11dca51a86af692955474
test "$(tr -d '\r\n' < "$CACHE/.lake/packages/mathlib/lean-toolchain")" = leanprover/lean4:v4.33.1
mkdir -p "$SIDE/output"
RUN=$(mktemp -d "$SIDE/output/run-XXXXXXXX")
exec > >(tee "$RUN/verify.log") 2>&1
printf 'UTC: %s\nRun: %s\n' "$(date -u +%FT%TZ)" "$RUN"
"$LEAN" --version
sha256sum "$CORE/RouteBSupplyCore.lean" "$SIDE/ResidualPower.lean" "$SIDE/verify.sh" "$CACHE/lake-manifest.json"
export LEAN_PATH="$RUN"
for PACKAGE in "$CACHE"/.lake/packages/*; do
  LIB="$PACKAGE/.lake/build/lib/lean"
  if test -d "$LIB"; then LEAN_PATH="$LEAN_PATH:$LIB"; fi
done
"$LEAN" -DwarningAsError=true --root="$CORE" -o "$RUN/RouteBSupplyCore.olean" "$CORE/RouteBSupplyCore.lean"
"$LEAN" -DwarningAsError=true --root="$SIDE" -o "$RUN/ResidualPower.olean" "$SIDE/ResidualPower.lean" 2>&1 | tee "$RUN/residual-compile.log"
printf 'LEAN_COMPILE_EXIT_CODE=0\n'
sha256sum "$RUN/ResidualPower.olean"
