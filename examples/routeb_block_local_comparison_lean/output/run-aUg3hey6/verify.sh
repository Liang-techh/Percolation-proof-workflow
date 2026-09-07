#!/usr/bin/env bash
set -euo pipefail

SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
ROOT=$(cd -- "$SIDE/../.." && pwd -P)
CACHE=/home/z5242/sos_lean
LEAN=/home/z5242/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean
DEPENDENCY="$ROOT/examples/routeb_local_energy_budget/output/run-37fVwazf"

mkdir -p "$SIDE/output"
RUN=$(mktemp -d "$SIDE/output/run-XXXXXXXX")
exec 3>&1
exec > "$RUN/verify.log" 2>&1
trap 'code=$?; printf "VERIFY_EXIT_CODE=%s\n" "$code"; cat "$RUN/verify.log" >&3' EXIT

printf 'UTC=%s\nRUN=%s\n' "$(date -u +%FT%TZ)" "$RUN"
test "$(git -C "$CACHE/.lake/packages/mathlib" rev-parse HEAD)" = 0df444a360eaa60ab8c11dca51a86af692955474
test "$(tr -d '\r\n' < "$CACHE/.lake/packages/mathlib/lean-toolchain")" = leanprover/lean4:v4.33.1
test -f "$DEPENDENCY/LocalEnergyBudget.olean"
test "$(sha256sum "$ROOT/examples/routeb_local_energy_budget/LocalEnergyBudget.lean" | awk '{print $1}')" = 6ed571661f816473120b69e1550627cf5f16ae0ef68df6ffd22dd77f00dac23f
test "$(sha256sum "$DEPENDENCY/LocalEnergyBudget.olean" | awk '{print $1}')" = 058fe6692deca45f4c66142cc63898c98b5d0bbe402dbedbf86885f85fdefe91

cp "$SIDE/BlockLocalComparison.lean" "$SIDE/README.md" "$SIDE/verify.sh" "$RUN/"
cp "$DEPENDENCY/LocalEnergyBudget.olean" "$RUN/"

"$LEAN" --version
printf 'MATHLIB_COMMIT=%s\n' "$(git -C "$CACHE/.lake/packages/mathlib" rev-parse HEAD)"
sha256sum "$RUN/BlockLocalComparison.lean" "$RUN/README.md" "$RUN/verify.sh" "$RUN/LocalEnergyBudget.olean"

export LEAN_PATH="$RUN"
for PACKAGE in "$CACHE"/.lake/packages/*; do
  LIB="$PACKAGE/.lake/build/lib/lean"
  if test -d "$LIB"; then LEAN_PATH="$LEAN_PATH:$LIB"; fi
done

set +e
"$LEAN" -DwarningAsError=true --root="$RUN" \
  -o "$RUN/BlockLocalComparison.olean" "$RUN/BlockLocalComparison.lean" 2>&1 | tee "$RUN/compile.log"
COMPILE_RC=${PIPESTATUS[0]}
set -e
printf 'LEAN_COMPILE_EXIT_CODE=%s\n' "$COMPILE_RC"
test "$COMPILE_RC" -eq 0

if grep -nE '(^|[^[:alnum:]_])(sorry|admit)([^[:alnum:]_]|$)|^[[:space:]]*axiom[[:space:]]' \
    "$RUN/BlockLocalComparison.lean"; then
  printf 'SOURCE_RESTRICTION_CHECK=FAILED\n'
  exit 1
fi
printf 'SOURCE_RESTRICTION_CHECK=PASSED\n'
sha256sum "$RUN/BlockLocalComparison.olean"
printf 'REAL_DYNAMICS_BINDING=OPEN\nRESIDUAL_BOUND=OPEN\nDOMAIN_COVERAGE=OPEN\n'
