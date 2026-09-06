#!/usr/bin/env bash
set -euo pipefail
SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
ROOT=$(cd -- "$SIDE/../.." && pwd -P)
CACHE=/home/z5242/sos_lean
LEAN=/home/z5242/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean
ADAPTER="$ROOT/examples/routeb_source_contract_adapter_lean/output/run-RSGGTurS"
SLOT="$ROOT/examples/routeb_frame_slot_accessor_lean/output/run-4RJoHvpZ"
CONTRACT="$ROOT/examples/routeb_body_contract_core_lean/output/run-0FvNkLzz"
BODY="$ROOT/examples/routeb_body_semantic_core_lean/output/run-6vhFP8Zp"
PREFIX="$ROOT/examples/routeb_frame_prefix_index_lean/output/run-lVHyO9Lp"
FRAME="$ROOT/examples/routeb_frame_origin_axis_lean/output/run-H0sN55iL"
REAL="$ROOT/examples/routeb_real_dh_step_lean/output/run-nAZVlwhR"
RECUR="$ROOT/examples/routeb_b45_frame_recursion/output/run-k87wlFSd"
mkdir -p "$SIDE/output"
RUN=$(mktemp -d "$SIDE/output/run-XXXXXXXX")
printf 'ATTEMPT_DIRECTORY=%s\n' "$RUN"
set +e
(
  set -euo pipefail
  trap 'code=$?; printf "VERIFY_EXIT_CODE=%s\\n" "$code"' EXIT
  printf 'START_UTC=%s\n' "$(date -u +%FT%TZ)"
  cp "$SIDE/SingleBodyContractInstantiation.lean" "$SIDE/README.md" "$SIDE/verify.sh" "$RUN/"
  test "$(git -C "$CACHE/.lake/packages/mathlib" rev-parse HEAD)" = 0df444a360eaa60ab8c11dca51a86af692955474
  test -f "$ADAPTER/SourceContractAdapter.olean"
  test -f "$SLOT/FrameSlotAccessor.olean"
  test -f "$CONTRACT/BodyContractCore.olean"
  test -f "$BODY/BodySemanticCore.olean"
  test -f "$PREFIX/FramePrefixIndex.olean"
  test -f "$FRAME/FrameOriginAxis.olean"
  test -f "$REAL/RealDHStep.olean"
  test -f "$RECUR/FrameRecursion.olean"
  export LEAN_PATH="$RUN:$ADAPTER:$SLOT:$CONTRACT:$BODY:$PREFIX:$FRAME:$REAL:$RECUR"
  for PACKAGE in "$CACHE"/.lake/packages/*; do
    LIB="$PACKAGE/.lake/build/lib/lean"
    if test -d "$LIB"; then LEAN_PATH="$LEAN_PATH:$LIB"; fi
  done
  "$LEAN" --version
  printf 'LEAN_PATH=%s\n' "$LEAN_PATH"
  sha256sum "$SIDE/SingleBodyContractInstantiation.lean" "$SIDE/README.md" "$SIDE/verify.sh" > "$RUN/input.sha256"
  printf 'SOURCE_SNAPSHOT_COMPLETE=true\n'
  set +e
  "$LEAN" -DwarningAsError=true --root="$RUN" \
    -o "$RUN/SingleBodyContractInstantiation.olean" "$RUN/SingleBodyContractInstantiation.lean"
  CODE=$?
  set -e
  printf 'SingleBodyContractInstantiation_COMPILE_EXIT_CODE=%s\n' "$CODE"
  test "$CODE" -eq 0
  if grep -nE '(^|[^[:alnum:]_])(sorry|admit)([^[:alnum:]_]|$)|^[[:space:]]*axiom[[:space:]]' "$RUN/SingleBodyContractInstantiation.lean"; then
    printf 'SOURCE_RESTRICTION_CHECK=FAILED\n'
    exit 1
  fi
  printf 'SOURCE_RESTRICTION_CHECK=PASSED\n'
  sha256sum "$RUN/SingleBodyContractInstantiation.lean" "$RUN/SingleBodyContractInstantiation.olean"
  printf 'JULIA_FLOAT64_BINDING=OPEN\nFULL_MASS_BINDING=OPEN\n'
  printf 'END_UTC=%s\n' "$(date -u +%FT%TZ)"
) > "$RUN/terminal.log" 2>&1
CODE=$?
set -e
cat "$RUN/terminal.log"
exit "$CODE"
