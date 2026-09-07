#!/usr/bin/env bash
set -euo pipefail

SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
RUNROOT="$SIDE/output"
mkdir -p "$RUNROOT"
RUN=$(mktemp -d "$RUNROOT/run-XXXXXXXX")
exec > >(tee "$RUN/verify.log") 2>&1
trap 'rc=$?; printf "VERIFY_EXIT_CODE=%s\n" "$rc"' EXIT

printf 'UTC: %s\nRun: %s\n' "$(date -u +%FT%TZ)" "$RUN"

LEAN=/home/z5242/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean
MATHLIB=/home/z5242/sos_lean/.lake/packages/mathlib

if [[ ! -x "$LEAN" ]]; then
  cat <<'EOF'
BLOCKED: pinned Lean executable is missing.
Expected: /home/z5242/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean
EOF
  exit 2
fi

if [[ ! -d "$MATHLIB" ]]; then
  cat <<'EOF'
BLOCKED: pinned mathlib cache is missing.
Expected: /home/z5242/sos_lean/.lake/packages/mathlib
EOF
  exit 2
fi

EXPECTED_TOOLCHAIN=leanprover/lean4:v4.33.1
ACTUAL_TOOLCHAIN=$(tr -d '\r\n' < "$MATHLIB/lean-toolchain")
EXPECTED_COMMIT=0df444a360eaa60ab8c11dca51a86af692955474
ACTUAL_COMMIT=$(git -C "$MATHLIB" rev-parse HEAD)

if [[ "$ACTUAL_TOOLCHAIN" != "$EXPECTED_TOOLCHAIN" || "$ACTUAL_COMMIT" != "$EXPECTED_COMMIT" ]]; then
  cat <<EOF
BLOCKED: pinned Lean environment mismatch.
Expected toolchain: $EXPECTED_TOOLCHAIN
Actual toolchain:   $ACTUAL_TOOLCHAIN
Expected mathlib:   $EXPECTED_COMMIT
Actual mathlib:     $ACTUAL_COMMIT
EOF
  exit 2
fi

"$LEAN" --version
printf 'MATHLIB_COMMIT=%s\n' "$ACTUAL_COMMIT"
sha256sum "$SIDE/ChristoffelPower.lean" "$SIDE/verify.sh"

cp "$SIDE/ChristoffelPower.lean" "$RUN/ChristoffelPower.lean"

export LEAN_PATH="$RUN"
for PACKAGE in /home/z5242/sos_lean/.lake/packages/*; do
  LIB="$PACKAGE/.lake/build/lib/lean"
  if [[ -d "$LIB" ]]; then
    LEAN_PATH="$LEAN_PATH:$LIB"
  fi
done

"$LEAN" -DwarningAsError=true --root="$RUN" -o "$RUN/ChristoffelPower.olean" "$RUN/ChristoffelPower.lean" 2>&1 | tee "$RUN/compile.log"
printf 'LEAN_COMPILE_EXIT_CODE=%s\n' "${PIPESTATUS[0]}"
sha256sum "$RUN/ChristoffelPower.olean"
