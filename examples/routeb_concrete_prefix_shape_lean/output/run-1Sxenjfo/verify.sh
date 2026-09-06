#!/usr/bin/env bash
set -euo pipefail
SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
ROOT=$(cd -- "$SIDE/../.." && pwd -P)
CACHE=/home/z5242/sos_lean
LEAN=/home/z5242/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean
PREFIX="$ROOT/examples/routeb_frame_prefix_index_lean/output/run-lVHyO9Lp"
STEP="$ROOT/examples/routeb_concrete_step_homogeneous_lean/output/run-ZBZY9WRv"
HOM="$ROOT/examples/routeb_homogeneous_prefix_projection_lean/output/run-7hl40Fdl"
HOM_BASE="$ROOT/examples/routeb_homogeneous_rotation_projection_lean/output/run-O33agpqU"
HOM_PREFIX="$ROOT/examples/routeb_rotation_prefix_orthogonality_lean/output/run-EZZSgIdS"
CLOSURE="$ROOT/examples/routeb_matrix_orthogonality_closure_lean/output/run-w9gDKPMw"
mkdir -p "$SIDE/output"
RUN=$(mktemp -d "$SIDE/output/run-XXXXXXXX")
printf 'ATTEMPT_DIRECTORY=%s\n' "$RUN"
set +e
(
  set -euo pipefail
  trap 'code=$?; printf "VERIFY_EXIT_CODE=%s\\n" "$code"' EXIT
  printf 'START_UTC=%s\n' "$(date -u +%FT%TZ)"
  cp "$SIDE/ConcretePrefixShape.lean" "$SIDE/README.md" "$SIDE/verify.sh" "$RUN/"
  test "$(git -C "$CACHE/.lake/packages/mathlib" rev-parse HEAD)" = 0df444a360eaa60ab8c11dca51a86af692955474
  test -f "$PREFIX/FramePrefixIndex.olean"
  test -f "$STEP/ConcreteStepHomogeneous.olean"
  test -f "$HOM/HomogeneousPrefixProjection.olean"
  test -f "$HOM_BASE/HomogeneousRotationProjection.olean"
  test -f "$HOM_PREFIX/RotationPrefixOrthogonality.olean"
  test -f "$CLOSURE/MatrixOrthogonalityClosure.olean"
  export LEAN_PATH="$RUN:$PREFIX:$STEP:$HOM:$HOM_BASE:$HOM_PREFIX:$CLOSURE"
  for PACKAGE in "$CACHE"/.lake/packages/*; do
    LIB="$PACKAGE/.lake/build/lib/lean"
    if test -d "$LIB"; then LEAN_PATH="$LEAN_PATH:$LIB"; fi
  done
  "$LEAN" --version
  printf 'LEAN_PATH=%s\n' "$LEAN_PATH"
  sha256sum "$SIDE/ConcretePrefixShape.lean" "$SIDE/README.md" "$SIDE/verify.sh" > "$RUN/input.sha256"
  printf 'SOURCE_SNAPSHOT_COMPLETE=true\n'
  set +e
  "$LEAN" -DwarningAsError=true --root="$RUN" \
    -o "$RUN/ConcretePrefixShape.olean" "$RUN/ConcretePrefixShape.lean"
  CODE=$?
  set -e
  printf 'ConcretePrefixShape_COMPILE_EXIT_CODE=%s\n' "$CODE"
  test "$CODE" -eq 0
  if grep -nE '(^|[^[:alnum:]_])(sorry|admit)([^[:alnum:]_]|$)|^[[:space:]]*axiom[[:space:]]' "$RUN/ConcretePrefixShape.lean"; then
    printf 'SOURCE_RESTRICTION_CHECK=FAILED\n'
    exit 1
  fi
  printf 'SOURCE_RESTRICTION_CHECK=PASSED\n'
  sha256sum "$RUN/ConcretePrefixShape.lean" "$RUN/ConcretePrefixShape.olean"
  printf 'JULIA_FLOAT64_BINDING=OPEN\nFULL_MASS_BINDING=OPEN\n'
  printf 'END_UTC=%s\n' "$(date -u +%FT%TZ)"
) > "$RUN/terminal.log" 2>&1
CODE=$?
set -e
cat "$RUN/terminal.log"
exit "$CODE"
