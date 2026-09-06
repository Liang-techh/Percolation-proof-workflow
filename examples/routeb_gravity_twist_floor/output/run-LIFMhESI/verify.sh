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
  cp "$SIDE/GravityTwistFloor.lean" "$SIDE/verify.sh" "$RUN/"
  for DOC in REPORT.md; do
    if test -f "$SIDE/$DOC"; then cp "$SIDE/$DOC" "$RUN/"; fi
  done
  mkdir "$RUN/inputs"
  cp "$ROOT/examples/routeb_J_strategy/REPORT.md" "$RUN/inputs/strategy_REPORT.md"
  cp "$ROOT/examples/routeb_J_strategy/SIGNED_WORK.md" "$RUN/inputs/SIGNED_WORK.md"
  cp "$ROOT/examples/routeb_signed_gap_source/output/run-20260905T203002Z-f4b7c48a/inputs/routeB_fourier_potential_rational.csv" "$RUN/inputs/routeB_fourier_potential_rational.csv"
  cp "$CACHE/lean-toolchain" "$CACHE/lake-manifest.json" "$RUN/inputs/"
  REV=$(git -C "$CACHE/.lake/packages/mathlib" rev-parse HEAD)
  printf 'MATHLIB_COMMIT=%s\n' "$REV"
  test "$REV" = 0df444a360eaa60ab8c11dca51a86af692955474
  "$LEAN" --version
  export LEAN_PATH="$RUN"
  for PACKAGE in "$CACHE"/.lake/packages/*; do
    LIB="$PACKAGE/.lake/build/lib/lean"
    if test -d "$LIB"; then LEAN_PATH="$LEAN_PATH:$LIB"; fi
  done
  printf 'LEAN_PATH=%s\n' "$LEAN_PATH"
  sha256sum "$LEAN" "$CACHE/.lake/packages/mathlib/Mathlib/Analysis/SpecialFunctions/Trigonometric/Bounds.lean" "$CACHE/.lake/packages/mathlib/.lake/build/lib/lean/Mathlib/Analysis/SpecialFunctions/Trigonometric/Bounds.olean" > "$RUN/cache.sha256"
  find "$RUN" -type f ! -name terminal.log ! -name before_run.sha256 -print0 |
    sort -z | xargs -0 sha256sum > "$RUN/before_run.sha256"
  printf 'PRE_RUN_SNAPSHOTS_COMPLETE\n'
  printf 'COMMAND=%s -DwarningAsError=true --root=%s -o %s/GravityTwistFloor.olean %s/GravityTwistFloor.lean\n' "$LEAN" "$RUN" "$RUN" "$RUN"
  set +e
  "$LEAN" -DwarningAsError=true --root="$RUN" -o "$RUN/GravityTwistFloor.olean" "$RUN/GravityTwistFloor.lean"
  CODE=$?
  set -e
  printf 'COMPILE_EXIT_CODE=%s\n' "$CODE"
  sha256sum --check --status "$RUN/before_run.sha256"
  printf 'SNAPSHOT_HASHES_UNCHANGED=true\n'
  test "$CODE" -eq 0
  sha256sum "$RUN/GravityTwistFloor.olean"
  printf 'END_UTC=%s\n' "$(date -u +%FT%TZ)"
) > "$RUN/terminal.log" 2>&1
CODE=$?
set -e
cat "$RUN/terminal.log"
exit "$CODE"
