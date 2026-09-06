#!/usr/bin/env bash
set -euo pipefail
SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
ROOT=$(cd -- "$SIDE/../.." && pwd -P)
CACHE=/home/z5242/sos_lean
LEAN=/home/z5242/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean
UPSTREAM="$ROOT/examples/routeb_signed_gap_lean/output/run-iH9FGdAL"
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
  cp -a "$UPSTREAM" "$RUN/upstream"
  for REL in artifacts/routeb_6dof/state.json examples/routeb_J_strategy/REPORT.md examples/routeb_affine_multiplier/DERIVATION.md examples/routeb_signed_gap_lean/FINAL_RECEIPT.md; do
    mkdir -p "$RUN/inputs/$(dirname "$REL")"
    cp "$ROOT/$REL" "$RUN/inputs/$REL"
  done
  REV=$(git -C "$CACHE/.lake/packages/mathlib" rev-parse HEAD)
  printf 'MATHLIB_COMMIT=%s\n' "$REV"
  test "$REV" = 0df444a360eaa60ab8c11dca51a86af692955474
  "$LEAN" --version
  test "$(sha256sum "$RUN/upstream/SignedGap.olean" | cut -d' ' -f1)" = 498aed10c67f6988066d16fa510bcfde461be3be0b6cb546ed326b4a56c4300e
  test "$(sha256sum "$RUN/upstream/ResidualMultiplier.olean" | cut -d' ' -f1)" = 72d43da8ba07fbda9f27521a27dfca950e2ff2e72b386d9df7126da72860d5b3
  export LEAN_PATH="$RUN:$RUN/upstream:$RUN/upstream/cache"
  for PACKAGE in "$CACHE"/.lake/packages/*; do
    LIB="$PACKAGE/.lake/build/lib/lean"
    if test -d "$LIB"; then LEAN_PATH="$LEAN_PATH:$LIB"; fi
  done
  printf 'LEAN_PATH=%s\n' "$LEAN_PATH"
  find "$RUN" -type f ! -path "$RUN/terminal.log" ! -path "$RUN/before_run.sha256" -print0 |
    sort -z | xargs -0 sha256sum > "$RUN/before_run.sha256"
  printf 'PRE_RUN_SNAPSHOTS_COMPLETE\n'
  printf 'COMMAND=%s -DwarningAsError=true --root=%s -o %s/UniversalMultiplier.olean %s/UniversalMultiplier.lean\n' "$LEAN" "$RUN" "$RUN" "$RUN"
  set +e
  "$LEAN" -DwarningAsError=true --root="$RUN" -o "$RUN/UniversalMultiplier.olean" "$RUN/UniversalMultiplier.lean"
  CODE=$?
  set -e
  printf 'UniversalMultiplier_COMPILE_EXIT_CODE=%s\n' "$CODE"
  test "$CODE" -eq 0
  sha256sum "$RUN/UniversalMultiplier.lean" "$RUN/UniversalMultiplier.olean"
  printf 'END_UTC=%s\n' "$(date -u +%FT%TZ)"
) > "$RUN/terminal.log" 2>&1
CODE=$?
set -e
cat "$RUN/terminal.log"
exit "$CODE"
