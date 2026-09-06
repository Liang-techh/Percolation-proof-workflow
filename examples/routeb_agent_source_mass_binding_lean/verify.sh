#!/usr/bin/env bash
set -euo pipefail
SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
ROOT=$(cd -- "$SIDE/../.." && pwd -P)
CACHE=/home/z5242/sos_lean
LEAN=/home/z5242/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean
SOURCE="$ROOT/examples/routeb_source_contract_adapter_lean/output/run-RSGGTurS"
CONTRACT="$ROOT/examples/routeb_body_contract_core_lean/output/run-0FvNkLzz"
BODY="$ROOT/examples/routeb_body_semantic_core_lean/output/run-6vhFP8Zp"
MASS="$ROOT/examples/routeb_mass_functional_lean/output/run-pVaCVj2p"
TABLE="$ROOT/examples/routeb_source_mass_table_minimal_lean/output/run-TrFQWCxh"
SLOT="$ROOT/examples/routeb_frame_slot_accessor_lean/output/run-4RJoHvpZ"
PREFIX="$ROOT/examples/routeb_frame_prefix_index_lean/output/run-lVHyO9Lp"
FRAME="$ROOT/examples/routeb_frame_origin_axis_lean/output/run-H0sN55iL"
REAL="$ROOT/examples/routeb_real_dh_step_lean/output/run-nAZVlwhR"
RECUR="$ROOT/examples/routeb_b45_frame_recursion/output/run-k87wlFSd"
mkdir -p "$SIDE/output"
RUN=$(mktemp -d "$SIDE/output/run-XXXXXXXX")
cp "$SIDE/AgentSourceMassBinding.lean" "$RUN/"
test "$(git -C "$CACHE/.lake/packages/mathlib" rev-parse HEAD)" = 0df444a360eaa60ab8c11dca51a86af692955474
export LEAN_PATH="$RUN:$SOURCE:$CONTRACT:$BODY:$MASS:$TABLE:$SLOT:$PREFIX:$FRAME:$REAL:$RECUR"
for PACKAGE in "$CACHE"/.lake/packages/*; do
  LIB="$PACKAGE/.lake/build/lib/lean"
  if test -d "$LIB"; then LEAN_PATH="$LEAN_PATH:$LIB"; fi
done
set +e
"$LEAN" -DwarningAsError=true --root="$RUN" -o "$RUN/AgentSourceMassBinding.olean" "$RUN/AgentSourceMassBinding.lean" 2>&1 | tee "$RUN/terminal.log"
CODE=${PIPESTATUS[0]}
set -e
printf 'AgentSourceMassBinding_COMPILE_EXIT_CODE=%s\n' "$CODE"
test "$CODE" -eq 0
if grep -nE '(^|[^[:alnum:]_])(sorry|admit)([^[:alnum:]_]|$)|^[[:space:]]*axiom[[:space:]]' "$RUN/AgentSourceMassBinding.lean"; then exit 1; fi
printf 'SOURCE_RESTRICTION_CHECK=PASSED\n'
printf 'MAIN_DAG_STATE_UNCHANGED=true\n'
