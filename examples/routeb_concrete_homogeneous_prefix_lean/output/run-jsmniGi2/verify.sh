#!/usr/bin/env bash
set -euo pipefail
SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
ROOT=$(cd -- "$SIDE/../.." && pwd -P)
CACHE=/home/z5242/sos_lean
LEAN=/home/z5242/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean
SLOT="$ROOT/examples/routeb_frame_slot_accessor_lean/output/run-4RJoHvpZ"
SLOT_PREFIX="$ROOT/examples/routeb_frame_prefix_index_lean/output/run-lVHyO9Lp"
SLOT_FRAME="$ROOT/examples/routeb_frame_origin_axis_lean/output/run-H0sN55iL"
SLOT_REAL="$ROOT/examples/routeb_real_dh_step_lean/output/run-nAZVlwhR"
SLOT_RECUR="$ROOT/examples/routeb_b45_frame_recursion/output/run-k87wlFSd"
HOM="$ROOT/examples/routeb_homogeneous_prefix_projection_lean/output/run-7hl40Fdl"
HOM_PREFIX="$ROOT/examples/routeb_rotation_prefix_orthogonality_lean/output/run-EZZSgIdS"
HOM_CLOSURE="$ROOT/examples/routeb_matrix_orthogonality_closure_lean/output/run-w9gDKPMw"
mkdir -p "$SIDE/output"
RUN=$(mktemp -d "$SIDE/output/run-XXXXXXXX")
printf 'ATTEMPT_DIRECTORY=%s\n' "$RUN"
set +e
(
  set -euo pipefail
  trap 'code=$?; printf "VERIFY_EXIT_CODE=%s\\n" "$code"' EXIT
  printf 'START_UTC=%s\n' "$(date -u +%FT%TZ)"
  cp "$SIDE/ConcreteHomogeneousPrefix.lean" "$SIDE/README.md" "$SIDE/verify.sh" "$RUN/"
  test "$(git -C "$CACHE/.lake/packages/mathlib" rev-parse HEAD)" = 0df444a360eaa60ab8c11dca51a86af692955474
  test -f "$SLOT/FrameSlotAccessor.olean"
  test -f "$SLOT_PREFIX/FramePrefixIndex.olean"
  test -f "$SLOT_FRAME/FrameOriginAxis.olean"
  test -f "$SLOT_REAL/RealDHStep.olean"
  test -f "$SLOT_RECUR/FrameRecursion.olean"
  test -f "$HOM/HomogeneousPrefixProjection.olean"
  test -f "$HOM_PREFIX/RotationPrefixOrthogonality.olean"
  test -f "$HOM_CLOSURE/MatrixOrthogonalityClosure.olean"
  export LEAN_PATH="$RUN:$SLOT:$SLOT_PREFIX:$SLOT_FRAME:$SLOT_REAL:$SLOT_RECUR:$HOM:$HOM_PREFIX:$HOM_CLOSURE"
  for PACKAGE in "$CACHE"/.lake/packages/*; do
    LIB="$PACKAGE/.lake/build/lib/lean"
    if test -d "$LIB"; then LEAN_PATH="$LEAN_PATH:$LIB"; fi
  done
  "$LEAN" --version
  printf 'LEAN_PATH=%s\n' "$LEAN_PATH"
  sha256sum "$SIDE/ConcreteHomogeneousPrefix.lean" "$SIDE/README.md" "$SIDE/verify.sh" > "$RUN/input.sha256"
  printf 'SOURCE_SNAPSHOT_COMPLETE=true\n'
  set +e
  "$LEAN" -DwarningAsError=true --root="$RUN" \
    -o "$RUN/ConcreteHomogeneousPrefix.olean" "$RUN/ConcreteHomogeneousPrefix.lean"
  CODE=$?
  set -e
  printf 'ConcreteHomogeneousPrefix_COMPILE_EXIT_CODE=%s\n' "$CODE"
  test "$CODE" -eq 0
  if grep -nE '(^|[^[:alnum:]_])(sorry|admit)([^[:alnum:]_]|$)|^[[:space:]]*axiom[[:space:]]' "$RUN/ConcreteHomogeneousPrefix.lean"; then
    printf 'SOURCE_RESTRICTION_CHECK=FAILED\n'
    exit 1
  fi
  printf 'SOURCE_RESTRICTION_CHECK=PASSED\n'
  sha256sum "$RUN/ConcreteHomogeneousPrefix.lean" "$RUN/ConcreteHomogeneousPrefix.olean"
  printf 'JULIA_FLOAT64_BINDING=OPEN\nFULL_MASS_BINDING=OPEN\n'
  printf 'END_UTC=%s\n' "$(date -u +%FT%TZ)"
) > "$RUN/terminal.log" 2>&1
CODE=$?
set -e
cat "$RUN/terminal.log"
exit "$CODE"
