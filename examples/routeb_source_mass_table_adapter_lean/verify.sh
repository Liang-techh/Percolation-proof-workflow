#!/usr/bin/env bash
set -euo pipefail

SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
ROOT=$(cd -- "$SIDE/../.." && pwd -P)
CACHE=/home/z5242/sos_lean
LEAN=/home/z5242/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean
SOURCE_CONTRACT="$ROOT/examples/routeb_source_contract_adapter_lean/output/run-RSGGTurS"
CONTRACT_MASS="$ROOT/examples/routeb_contract_mass_functional_adapter_lean/output/run-H1RwjdoF"
REGULARIZED="$ROOT/examples/routeb_regularized_six_body_mass_lean/output/run-2UEw1Rrk"
MASS_REG="$ROOT/examples/routeb_mass_regularizer_lean/output/run-8qHz1Tiv"
MASS="$ROOT/examples/routeb_mass_functional_lean/output/run-pVaCVj2p"
ISO="$ROOT/examples/routeb_isotropic_inertia_lean/output/run-KWENke5I"
BODY="$ROOT/examples/routeb_body_contract_core_lean/output/run-0FvNkLzz"
SEM="$ROOT/examples/routeb_body_semantic_core_lean/output/run-6vhFP8Zp"
SLOT="$ROOT/examples/routeb_frame_slot_accessor_lean/output/run-4RJoHvpZ"
PREFIX="$ROOT/examples/routeb_frame_prefix_index_lean/output/run-lVHyO9Lp"
FRAME="$ROOT/examples/routeb_frame_origin_axis_lean/output/run-H0sN55iL"
REAL="$ROOT/examples/routeb_real_dh_step_lean/output/run-nAZVlwhR"
RECUR="$ROOT/examples/routeb_b45_frame_recursion/output/run-k87wlFSd"

mkdir -p "$SIDE/output"
RUN=$(mktemp -d "$SIDE/output/run-XXXXXXXX")
printf 'ATTEMPT_DIRECTORY=%s\n' "$RUN"
for file in \
  "$SOURCE_CONTRACT/SourceContractAdapter.olean" \
  "$CONTRACT_MASS/ContractMassFunctionalAdapter.olean" \
  "$REGULARIZED/RegularizedSixBodyMass.olean" \
  "$MASS_REG/MassRegularizer.olean" \
  "$MASS/MassFunctional.olean" \
  "$ISO/IsotropicInertia.olean" \
  "$BODY/BodyContractCore.olean" \
  "$SEM/BodySemanticCore.olean" \
  "$SLOT/FrameSlotAccessor.olean" \
  "$PREFIX/FramePrefixIndex.olean" \
  "$FRAME/FrameOriginAxis.olean" \
  "$REAL/RealDHStep.olean" \
  "$RECUR/FrameRecursion.olean"; do
  test -f "$file"
done

cp "$SIDE/SourceMassTableAdapter.lean" "$SIDE/README.md" "$SIDE/verify.sh" "$RUN/"
export LEAN_PATH="$RUN:$SOURCE_CONTRACT:$CONTRACT_MASS:$REGULARIZED:$MASS_REG:$MASS:$ISO:$BODY:$SEM:$SLOT:$PREFIX:$FRAME:$REAL:$RECUR"
for PACKAGE in "$CACHE"/.lake/packages/*; do
  LIB="$PACKAGE/.lake/build/lib/lean"
  if test -d "$LIB"; then LEAN_PATH="$LEAN_PATH:$LIB"; fi
done

set +e
"$LEAN" -DwarningAsError=true --root="$RUN" \
  -o "$RUN/SourceMassTableAdapter.olean" \
  "$RUN/SourceMassTableAdapter.lean" 2>&1 | tee "$RUN/terminal.log"
status=${PIPESTATUS[0]}
set -e
printf 'SourceMassTableAdapter_COMPILE_EXIT_CODE=%s\n' "$status" | tee -a "$RUN/terminal.log"
if [ "$status" -ne 0 ]; then exit "$status"; fi
if grep -nE '(^|[^[:alnum:]_])(sorry|admit)([^[:alnum:]_]|$)|^[[:space:]]*axiom[[:space:]]' \
  "$RUN/SourceMassTableAdapter.lean"; then
  echo 'SOURCE_RESTRICTION_CHECK=FAILED' | tee -a "$RUN/terminal.log"
  exit 2
fi
sha256sum "$RUN/SourceMassTableAdapter.lean" "$RUN/SourceMassTableAdapter.olean" | tee -a "$RUN/terminal.log"
echo 'SOURCE_RESTRICTION_CHECK=PASSED' | tee -a "$RUN/terminal.log"
echo 'JULIA_FLOAT64_BINDING=OPEN' | tee -a "$RUN/terminal.log"
echo 'FOURIER_COMPARATOR=OPEN' | tee -a "$RUN/terminal.log"
echo 'VERIFY_EXIT_CODE=0' | tee -a "$RUN/terminal.log"
echo "$RUN"
