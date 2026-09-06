#!/usr/bin/env bash
set -euo pipefail
SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
ROOT=$(cd -- "$SIDE/../.." && pwd -P)
CACHE=/home/z5242/sos_lean
LEAN=/home/z5242/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean
mkdir -p "$SIDE/output"
RUN=$(mktemp -d "$SIDE/output/run-XXXXXXXX")
printf 'ATTEMPT_DIRECTORY=%s\n' "$RUN"
set +e
(
  set -euo pipefail
  trap 'code=$?; printf "VERIFY_EXIT_CODE=%s\n" "$code"' EXIT
  printf 'START_UTC=%s\n' "$(date -u +%FT%TZ)"
  cp "$SIDE"/*.lean "$SIDE/verify.sh" "$RUN/"
  for DOC in README.md ATTEMPT_HISTORY.md; do
    if test -f "$SIDE/$DOC"; then cp "$SIDE/$DOC" "$RUN/"; fi
  done
  INPUTS=(
    artifacts/routeb_6dof/state.json
    artifacts/routeb_prefix_checkpoint_20260905/REPORT.md
    examples/routeb_J_strategy/SIGNED_WORK.md
    examples/routeb_dh_power_binding/DHPowerBinding.lean
    examples/routeb_dh_power_binding/ControllerPowerCore.lean
    examples/routeb_dh_power_binding/MechanicalAssembly.lean
    examples/routeb_rotational_dual/RotationalDual.lean
    examples/routeb_coupled_resolvent/CoupledResolvent.lean
    examples/routeb_christoffel_power/ChristoffelPower.lean
    examples/routeb_local_energy_budget/LocalEnergyBudget.lean
    examples/routeb_prefix_small_gain/PrefixSmallGain.lean
  )
  for REL in "${INPUTS[@]}"; do
    mkdir -p "$RUN/inputs/$(dirname "$REL")"
    cp "$ROOT/$REL" "$RUN/inputs/$REL"
  done
  REV=$(git -C "$CACHE/.lake/packages/mathlib" rev-parse HEAD)
  printf 'MATHLIB_COMMIT=%s\n' "$REV"
  test "$REV" = 0df444a360eaa60ab8c11dca51a86af692955474
  "$LEAN" --version
  export LEAN_PATH="$RUN"
  CACHED=(
    routeb_dh_power_binding/output/run-5RHBCcg9
    routeb_rotational_dual/output/run-JNEk4oY4
    routeb_local_energy_budget/output/run-37fVwazf
    routeb_coupled_resolvent/output/run-HTi4uZSF
    routeb_christoffel_power/output/run-YC2fOLUR
    routeb_prefix_small_gain/output/run-90JWgVCt
  )
  mkdir "$RUN/cache"
  for REL in "${CACHED[@]}"; do
    cp "$ROOT/examples/$REL"/*.olean "$RUN/cache/"
  done
  export LEAN_PATH="$LEAN_PATH:$RUN/cache"
  for PACKAGE in "$CACHE"/.lake/packages/*; do
    LIB="$PACKAGE/.lake/build/lib/lean"
    if test -d "$LIB"; then LEAN_PATH="$LEAN_PATH:$LIB"; fi
  done
  printf 'LEAN_PATH=%s\n' "$LEAN_PATH"
  find "$RUN" -type f ! -name terminal.log ! -name before_run.sha256 -print0 |
    sort -z | xargs -0 sha256sum > "$RUN/before_run.sha256"
  printf 'PRE_RUN_SNAPSHOTS_COMPLETE\n'
  if test "$#" -eq 0; then set -- SignedGap; fi
  for NAME in "$@"; do
    case "$NAME" in SignedGap|ResidualMultiplier|IntegratedBudget) ;; *) exit 2 ;; esac
    printf 'COMMAND=%s -DwarningAsError=true --root=%s -o %s/%s.olean %s/%s.lean\n' "$LEAN" "$RUN" "$RUN" "$NAME" "$RUN" "$NAME"
    set +e
    "$LEAN" -DwarningAsError=true --root="$RUN" -o "$RUN/$NAME.olean" "$RUN/$NAME.lean"
    CODE=$?
    set -e
    printf '%s_COMPILE_EXIT_CODE=%s\n' "$NAME" "$CODE"
    test "$CODE" -eq 0
    sha256sum "$RUN/$NAME.olean"
  done
  printf 'END_UTC=%s\n' "$(date -u +%FT%TZ)"
) > "$RUN/terminal.log" 2>&1
CODE=$?
set -e
cat "$RUN/terminal.log"
exit "$CODE"
