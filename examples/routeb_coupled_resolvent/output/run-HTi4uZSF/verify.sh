#!/usr/bin/env bash
set -euo pipefail
SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
CACHE=/home/z5242/sos_lean
LEAN=/home/z5242/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean
mkdir -p "$SIDE/output"
RUN=$(mktemp -d "$SIDE/output/run-XXXXXXXX")
cp "$SIDE/CoupledResolvent.lean" "$RUN/CoupledResolvent.lean"
cp "$SIDE/verify.sh" "$RUN/verify.sh"
exec 3>&1
exec > >(tee "$RUN/verify.log" >&3) 2>&1
TEE_PID=$!
finish() {
  code=$?
  trap - EXIT
  printf 'VERIFY_EXIT_CODE=%s\n' "$code"
  exec 1>&3 2>&3
  wait "$TEE_PID" || true
  exit "$code"
}
trap finish EXIT
printf 'Run: %s\n' "$RUN"
test "$(git -C "$CACHE/.lake/packages/mathlib" rev-parse HEAD)" = 0df444a360eaa60ab8c11dca51a86af692955474
"$LEAN" --version
export LEAN_PATH="$RUN:$SIDE/../routeb_dh_power_binding/output/run-5RHBCcg9:$SIDE/../routeb_rotational_dual/output/run-JNEk4oY4:$SIDE/../routeb_local_energy_budget/output/run-37fVwazf"
for PACKAGE in "$CACHE"/.lake/packages/*; do
  LIB="$PACKAGE/.lake/build/lib/lean"
  if test -d "$LIB"; then LEAN_PATH="$LEAN_PATH:$LIB"; fi
done
sha256sum "$RUN/CoupledResolvent.lean" "$RUN/verify.sh"
set +e
"$LEAN" -DwarningAsError=true --root="$RUN" -o "$RUN/CoupledResolvent.olean" "$RUN/CoupledResolvent.lean"
CODE=$?
set -e
printf 'LEAN_COMPILE_EXIT_CODE=%s\n' "$CODE"
test "$CODE" -eq 0
sha256sum "$RUN/CoupledResolvent.olean"
