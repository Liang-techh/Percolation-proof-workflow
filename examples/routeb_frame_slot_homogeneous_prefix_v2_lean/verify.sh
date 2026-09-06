#!/usr/bin/env bash
set -euo pipefail

SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
ROOT=$(cd -- "$SIDE/../.." && pwd -P)
CACHE=/home/z5242/sos_lean
LEAN=/home/z5242/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean
CONCRETE="$ROOT/examples/routeb_concrete_step_homogeneous_lean/output/run-ZBZY9WRv"
HOMOG="$ROOT/examples/routeb_homogeneous_prefix_projection_lean/output/run-7hl40Fdl"
HROT="$ROOT/examples/routeb_homogeneous_rotation_projection_lean/output/run-O33agpqU"
RPO="$ROOT/examples/routeb_rotation_prefix_orthogonality_lean/output/run-EZZSgIdS"
CLOSURE="$ROOT/examples/routeb_matrix_orthogonality_closure_lean/output/run-w9gDKPMw"
SLOT="$ROOT/examples/routeb_frame_slot_accessor_lean/output/run-4RJoHvpZ"
PREFIX="$ROOT/examples/routeb_frame_prefix_index_lean/output/run-lVHyO9Lp"
REAL="$ROOT/examples/routeb_real_dh_step_lean/output/run-nAZVlwhR"
ORIGIN="$ROOT/examples/routeb_frame_origin_axis_lean/output/run-H0sN55iL"
RECUR="$ROOT/examples/routeb_b45_frame_recursion/output/run-k87wlFSd"

mkdir -p "$SIDE/output"
RUN=$(mktemp -d "$SIDE/output/run-XXXXXXXX")
printf 'ATTEMPT_DIRECTORY=%s\n' "$RUN"
for f in \
  "$CONCRETE/ConcreteStepHomogeneous.olean" \
  "$HOMOG/HomogeneousPrefixProjection.olean" \
  "$HROT/HomogeneousRotationProjection.olean" \
  "$RPO/RotationPrefixOrthogonality.olean" \
  "$CLOSURE/MatrixOrthogonalityClosure.olean" \
  "$SLOT/FrameSlotAccessor.olean" \
  "$PREFIX/FramePrefixIndex.olean" \
  "$REAL/RealDHStep.olean" \
  "$ORIGIN/FrameOriginAxis.olean" \
  "$RECUR/FrameRecursion.olean"; do test -f "$f"; done

cp "$SIDE/FrameSlotHomogeneousPrefixV2.lean" "$SIDE/README.md" "$SIDE/verify.sh" "$RUN/"
export LEAN_PATH="$RUN:$CONCRETE:$HOMOG:$HROT:$RPO:$CLOSURE:$SLOT:$PREFIX:$REAL:$ORIGIN:$RECUR"
for PACKAGE in "$CACHE"/.lake/packages/*; do
  LIB="$PACKAGE/.lake/build/lib/lean"
  if test -d "$LIB"; then LEAN_PATH="$LEAN_PATH:$LIB"; fi
done

set +e
"$LEAN" -DwarningAsError=true --root="$RUN" \
  -o "$RUN/FrameSlotHomogeneousPrefixV2.olean" \
  "$RUN/FrameSlotHomogeneousPrefixV2.lean" 2>&1 | tee "$RUN/terminal.log"
status=${PIPESTATUS[0]}
set -e
printf 'FrameSlotHomogeneousPrefixV2_COMPILE_EXIT_CODE=%s\n' "$status" | tee -a "$RUN/terminal.log"
if [ "$status" -ne 0 ]; then exit "$status"; fi

if grep -nE '(^|[^[:alnum:]_])(sorry|admit)([^[:alnum:]_]|$)|^[[:space:]]*axiom[[:space:]]' \
  "$RUN/FrameSlotHomogeneousPrefixV2.lean"; then
  echo 'SOURCE_RESTRICTION_CHECK=FAILED' | tee -a "$RUN/terminal.log"
  exit 2
fi
sha256sum "$RUN/FrameSlotHomogeneousPrefixV2.lean" "$RUN/FrameSlotHomogeneousPrefixV2.olean" | tee -a "$RUN/terminal.log"
echo 'SOURCE_RESTRICTION_CHECK=PASSED' | tee -a "$RUN/terminal.log"
echo 'COMPARATOR_STATUS=OPEN' | tee -a "$RUN/terminal.log"
echo 'REGISTRY_STATUS=EMPTY' | tee -a "$RUN/terminal.log"
echo 'VERIFY_EXIT_CODE=0' | tee -a "$RUN/terminal.log"
echo "$RUN"
