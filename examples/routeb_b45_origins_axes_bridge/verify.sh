#!/usr/bin/env bash
set -euo pipefail
SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
ROOT=$(cd -- "$SIDE/../.." && pwd -P)
CACHE=/home/z5242/sos_lean
LEAN=/home/z5242/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean
ADAPTER="$ROOT/examples/routeb_source_contract_adapter_lean/output/run-RSGGTurS"
SLOT="$ROOT/examples/routeb_frame_slot_accessor_lean/output/run-4RJoHvpZ"
PREFIX="$ROOT/examples/routeb_frame_prefix_index_lean/output/run-lVHyO9Lp"
REAL="$ROOT/examples/routeb_real_dh_step_lean/output/run-nAZVlwhR"
ORIGIN="$ROOT/examples/routeb_frame_origin_axis_lean/output/run-H0sN55iL"
BODY="$ROOT/examples/routeb_body_semantic_core_lean/output/run-6vhFP8Zp"
CONTRACT="$ROOT/examples/routeb_body_contract_core_lean/output/run-0FvNkLzz"
RECUR="$ROOT/examples/routeb_b45_frame_recursion/output/run-k87wlFSd"
RUN=$(mktemp -d "$SIDE/output/run-XXXXXXXX")
cp "$SIDE/OriginsAxesBridge.lean" "$RUN/"
export LEAN_PATH="$RUN:$ADAPTER:$SLOT:$PREFIX:$REAL:$ORIGIN:$BODY:$CONTRACT:$RECUR"
for PACKAGE in "$CACHE"/.lake/packages/*; do
  LIB="$PACKAGE/.lake/build/lib/lean"
  if test -d "$LIB"; then LEAN_PATH="$LEAN_PATH:$LIB"; fi
done
set +e
timeout 180 "$LEAN" -DwarningAsError=true --root="$RUN" \
  -o "$RUN/OriginsAxesBridge.olean" "$RUN/OriginsAxesBridge.lean" 2>&1 | tee "$RUN/terminal.log"
status=${PIPESTATUS[0]}
set -e
printf 'OriginsAxesBridge_COMPILE_EXIT_CODE=%s\n' "$status" | tee -a "$RUN/terminal.log"
if test "$status" -ne 0; then exit "$status"; fi
if grep -nE '(^|[^[:alnum:]_])(sorry|admit)([^[:alnum:]_]|$)|^[[:space:]]*axiom[[:space:]]' "$RUN/OriginsAxesBridge.lean"; then
  echo 'SOURCE_RESTRICTION_CHECK=FAILED' | tee -a "$RUN/terminal.log"; exit 2
fi
sha256sum "$RUN/OriginsAxesBridge.lean" "$RUN/OriginsAxesBridge.olean" | tee -a "$RUN/terminal.log"
echo 'SOURCE_RESTRICTION_CHECK=PASSED' | tee -a "$RUN/terminal.log"
echo 'FLOAT64_BINDING=OPEN' | tee -a "$RUN/terminal.log"
echo 'REGISTRY_STATUS=EMPTY' | tee -a "$RUN/terminal.log"
echo 'VERIFY_EXIT_CODE=0' | tee -a "$RUN/terminal.log"
echo "$RUN"
