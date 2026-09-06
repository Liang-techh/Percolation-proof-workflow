#!/usr/bin/env bash
set -euo pipefail
SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
ROOT=$(cd -- "$SIDE/../.." && pwd -P)
CACHE=/home/z5242/sos_lean
LEAN=/home/z5242/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean
LINK="$ROOT/examples/routeb_isotropic_link_mass_lean/output/run-Tg6AVoHq"
MASS="$ROOT/examples/routeb_mass_functional_lean/output/run-pVaCVj2p"
ISO="$ROOT/examples/routeb_isotropic_inertia_lean/output/run-KWENke5I"
mkdir -p "$SIDE/output"
RUN=$(mktemp -d "$SIDE/output/run-XXXXXXXX")
printf 'ATTEMPT_DIRECTORY=%s\n' "$RUN"
set +e
(
  set -euo pipefail
  trap 'code=$?; printf "VERIFY_EXIT_CODE=%s\\n" "$code"' EXIT
  printf 'START_UTC=%s\n' "$(date -u +%FT%TZ)"
  cp "$SIDE/SixBodyIsotropicMass.lean" "$SIDE/README.md" "$SIDE/verify.sh" "$RUN/"
  test "$(git -C "$CACHE/.lake/packages/mathlib" rev-parse HEAD)" = 0df444a360eaa60ab8c11dca51a86af692955474
  test -f "$LINK/IsotropicLinkMass.olean"
  test -f "$MASS/MassFunctional.olean"
  test -f "$ISO/IsotropicInertia.olean"
  export LEAN_PATH="$RUN:$LINK:$MASS:$ISO"
  for PACKAGE in "$CACHE"/.lake/packages/*; do
    LIB="$PACKAGE/.lake/build/lib/lean"
    if test -d "$LIB"; then LEAN_PATH="$LEAN_PATH:$LIB"; fi
  done
  "$LEAN" --version
  printf 'LEAN_PATH=%s\n' "$LEAN_PATH"
  sha256sum "$SIDE/SixBodyIsotropicMass.lean" "$SIDE/README.md" "$SIDE/verify.sh" > "$RUN/input.sha256"
  printf 'SOURCE_SNAPSHOT_COMPLETE=true\n'
  set +e
  "$LEAN" -DwarningAsError=true --root="$RUN" \
    -o "$RUN/SixBodyIsotropicMass.olean" "$RUN/SixBodyIsotropicMass.lean"
  CODE=$?
  set -e
  printf 'SixBodyIsotropicMass_COMPILE_EXIT_CODE=%s\n' "$CODE"
  test "$CODE" -eq 0
  if grep -nE '(^|[^[:alnum:]_])(sorry|admit)([^[:alnum:]_]|$)|^[[:space:]]*axiom[[:space:]]' "$RUN/SixBodyIsotropicMass.lean"; then
    printf 'SOURCE_RESTRICTION_CHECK=FAILED\n'
    exit 1
  fi
  printf 'SOURCE_RESTRICTION_CHECK=PASSED\n'
  sha256sum "$RUN/SixBodyIsotropicMass.lean" "$RUN/SixBodyIsotropicMass.olean"
  printf 'JULIA_FLOAT64_BINDING=OPEN\nFULL_MASS_BINDING=OPEN\n'
  printf 'END_UTC=%s\n' "$(date -u +%FT%TZ)"
) > "$RUN/terminal.log" 2>&1
CODE=$?
set -e
cat "$RUN/terminal.log"
exit "$CODE"
