#!/usr/bin/env bash
set -euo pipefail
SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
CACHE=/home/z5242/sos_lean
LEAN=/home/z5242/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean
mkdir -p "$SIDE/output"
RUN=$(mktemp -d "$SIDE/output/run-XXXXXXXX")
exec > >(tee "$RUN/verify.log") 2>&1
trap 'rc=$?; printf "VERIFY_EXIT_CODE=%s\n" "$rc"' EXIT
printf 'UTC: %s\nRun: %s\n' "$(date -u +%FT%TZ)" "$RUN"
test "$(git -C "$CACHE/.lake/packages/mathlib" rev-parse HEAD)" = 0df444a360eaa60ab8c11dca51a86af692955474
"$LEAN" --version
sha256sum "$SIDE/verify.sh" "$CACHE/lake-manifest.json"
BASE="$SIDE/output/run-gJUGcsng"
ENERGY="$SIDE/../routeb_dh_power_binding/output/tube-NXa8rD7u"
POWER="$SIDE/../routeb_dh_power_binding/output/run-5RHBCcg9"
VARIABLE="$SIDE/output/run-wvXLU1m4"
LOCAL="$SIDE/../routeb_local_energy_budget/output/run-37fVwazf"
export LEAN_PATH="$RUN:$BASE:$ENERGY:$POWER:$VARIABLE:$LOCAL"
if test -f "$BASE/ImplicitPort.olean"; then sha256sum "$BASE/ImplicitPort.olean"; fi
for PACKAGE in "$CACHE"/.lake/packages/*; do
  LIB="$PACKAGE/.lake/build/lib/lean"
  if test -d "$LIB"; then LEAN_PATH="$LEAN_PATH:$LIB"; fi
done
if test "$#" -eq 0; then set -- ImplicitPort BlockTargets; fi
for NAME in "$@"; do
  case "$NAME" in ImplicitPort|BlockTargets|GateBounds|PhysicalPortAssembly|VariableErrorTube|LocalTubeAssembly) ;; *) exit 2 ;; esac
  if test "$NAME" = VariableErrorTube; then sha256sum "$ENERGY/EnergyTube.olean" "$POWER/DHPowerBinding.olean"; fi
  if test "$NAME" = LocalTubeAssembly; then
    sha256sum "$VARIABLE/VariableErrorTube.olean" "$LOCAL/LocalEnergyBudget.olean" "$ENERGY/EnergyTube.olean" "$POWER/DHPowerBinding.olean"
  fi
  sha256sum "$SIDE/$NAME.lean"
  cp "$SIDE/$NAME.lean" "$RUN/$NAME.lean"
  "$LEAN" -DwarningAsError=true --root="$RUN" -o "$RUN/$NAME.olean" "$RUN/$NAME.lean" 2>&1 | tee "$RUN/$NAME.log"
  printf '%s_COMPILE_EXIT_CODE=0\n' "$NAME"
  sha256sum "$RUN/$NAME.olean"
done
printf 'LEAN_COMPILE_EXIT_CODE=0\n'
