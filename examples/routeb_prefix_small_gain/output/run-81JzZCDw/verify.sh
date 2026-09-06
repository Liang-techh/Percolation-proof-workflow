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
  mkdir "$RUN/inputs"
  for NAME in PrefixSmallGain.lean verify.sh DERIVATION.md ATTEMPT_HISTORY.md; do
    cp "$SIDE/$NAME" "$RUN/$NAME"
  done
  INPUTS=(
    examples/routeb_coupled_gain_bridge/DERIVATION.md
    examples/routeb_coupled_gain_bridge/GainBridge.lean
    examples/routeb_coupled_gain_bridge/verify.sh
    artifacts/routeb_gain_checkpoint_20260905/REPORT.md
    examples/routeb_coupled_resolvent/DERIVATION.md
    examples/routeb_coupled_resolvent/CoupledResolvent.lean
    examples/routeb_coupled_resolvent/source_bounds.py
    examples/routeb_coupled_resolvent/output/bounds-20260905T193103Z-725e99c7/source_bounds.json
    examples/routeb_coupled_finite_gain/DERIVATION.md
    examples/routeb_coupled_finite_gain/output/run-20260905T194943Z-9ad8ada4/results.json
  )
  for REL in "${INPUTS[@]}"; do
    mkdir -p "$RUN/inputs/$(dirname "$REL")"
    cp "$ROOT/$REL" "$RUN/inputs/$REL"
    printf 'INPUT=%s\n' "$REL"
  done
  find "$RUN" -type f ! -name terminal.log ! -name before_run.sha256 -print0 |
    sort -z | xargs -0 sha256sum > "$RUN/before_run.sha256"
  printf 'PRE_RUN_SNAPSHOTS_COMPLETE\n'
  REV=$(git -C "$CACHE/.lake/packages/mathlib" rev-parse HEAD)
  printf 'MATHLIB_COMMIT=%s\n' "$REV"
  test "$REV" = 0df444a360eaa60ab8c11dca51a86af692955474
  "$LEAN" --version
  export LEAN_PATH="$RUN"
  for PACKAGE in "$CACHE"/.lake/packages/*; do
    LIB="$PACKAGE/.lake/build/lib/lean"
    if test -d "$LIB"; then LEAN_PATH="$LEAN_PATH:$LIB"; fi
  done
  printf 'COMMAND=lean -DwarningAsError=true --root=RUN -o RUN/PrefixSmallGain.olean RUN/PrefixSmallGain.lean\n'
  set +e
  "$LEAN" -DwarningAsError=true --root="$RUN" -o "$RUN/PrefixSmallGain.olean" "$RUN/PrefixSmallGain.lean"
  CODE=$?
  set -e
  printf 'LEAN_COMPILE_EXIT_CODE=%s\n' "$CODE"
  test "$CODE" -eq 0
  sha256sum "$RUN/PrefixSmallGain.olean"
  printf 'END_UTC=%s\n' "$(date -u +%FT%TZ)"
) > "$RUN/terminal.log" 2>&1
CODE=$?
set -e
cat "$RUN/terminal.log"
exit "$CODE"
