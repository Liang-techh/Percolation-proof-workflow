#!/usr/bin/env bash
set -euo pipefail
SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
BASE="$SIDE/output/run-5RHBCcg9"
test -f "$BASE/DHPowerBinding.olean"
export LEAN_PATH="$BASE:$SIDE/output/tube-RWfVZNvn"
CHRISTOFFEL="$SIDE/../routeb_christoffel_power/output/run-YC2fOLUR"
test -f "$CHRISTOFFEL/ChristoffelPower.olean"
export LEAN_PATH="$LEAN_PATH:$CHRISTOFFEL"
for PACKAGE in /home/z5242/sos_lean/.lake/packages/*; do
  LIB="$PACKAGE/.lake/build/lib/lean"
  if test -d "$LIB"; then LEAN_PATH="$LEAN_PATH:$LIB"; fi
done
RUN=$(mktemp -d "$SIDE/output/tube-XXXXXXXX")
exec > >(tee "$RUN/verify.log") 2>&1
printf 'Run: %s\nUTC: %s\n' "$RUN" "$(date -u +%FT%TZ)"
sha256sum "$BASE/DHPowerBinding.olean" "$CHRISTOFFEL/ChristoffelPower.olean"
if test "$#" -eq 0; then set -- FDForceBudget MechanicalAssembly EnergyTube; fi
for NAME in "$@"; do
  case "$NAME" in FDForceBudget|MechanicalAssembly|EnergyTube|StorageObstruction|ShiftBudgetObstruction) ;; *) exit 2 ;; esac
  if test "$NAME" = ShiftBudgetObstruction; then
    sha256sum "$SIDE/output/tube-RWfVZNvn/StorageObstruction.olean"
  fi
  sha256sum "$SIDE/$NAME.lean"
  cp "$SIDE/$NAME.lean" "$RUN/$NAME.lean"
  /home/z5242/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean \
    -DwarningAsError=true --root="$SIDE" -o "$RUN/$NAME.olean" "$SIDE/$NAME.lean" 2>&1 | tee "$RUN/$NAME.log"
  printf '%s_COMPILE_EXIT_CODE=0\n' "$NAME"
  sha256sum "$RUN/$NAME.olean"
done
printf 'LEAN_COMPILE_EXIT_CODE=0\n'
