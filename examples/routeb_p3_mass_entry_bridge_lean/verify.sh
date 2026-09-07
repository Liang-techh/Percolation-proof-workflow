#!/usr/bin/env bash
set -euo pipefail

SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
ROOT=$(cd -- "$SIDE/../.." && pwd -P)
LAKE_ROOT=${ROUTEB_P3_LAKE_ROOT:-$ROOT/examples/local_fkg}
if test -n "${ROUTEB_P3_LEAN_BIN:-}"; then
  LEAN_BIN="$ROUTEB_P3_LEAN_BIN"
else
  LEAN_BIN=''
  for CANDIDATE in \
    /home/z5242/.elan/toolchains/leanprover--lean4---v4.32.0/bin/lean \
    /mnt/c/Users/z5242/.elan/bin/lean.exe \
    /mnt/c/Users/z5242/.elan/toolchains/leanprover--lean4---v4.32.0/bin/lean.exe; do
    if test -x "$CANDIDATE"; then
      LEAN_BIN="$CANDIDATE"
      break
    fi
  done
  if test -z "$LEAN_BIN" && command -v lean >/dev/null 2>&1; then
    LEAN_BIN=$(command -v lean)
  fi
fi

test "$(tr -d '\r\n' < "$LAKE_ROOT/lean-toolchain")" = "leanprover/lean4:v4.32.0"
test -n "$LEAN_BIN"
test -x "$LEAN_BIN" || command -v "$LEAN_BIN" >/dev/null 2>&1
mkdir -p "$SIDE/output"
RUN=$(mktemp -d "$SIDE/output/run-XXXXXXXX")
exec > >(tee "$RUN/verify.log") 2>&1

printf 'Output: %s\nUTC: %s\n' "$RUN" "$(date -u +%FT%TZ)"
"$LEAN_BIN" --version
printf 'Pinned local_fkg toolchain: %s\n' "$(tr -d '\r\n' < "$LAKE_ROOT/lean-toolchain")"

export LEAN_PATH=''
for PACKAGE in "$LAKE_ROOT"/.lake/packages/*; do
  LIB="$PACKAGE/.lake/build/lib/lean"
  if test -d "$LIB"; then
    LEAN_PATH="${LEAN_PATH:+$LEAN_PATH:}$LIB"
  fi
done

sha256sum "$SIDE/MassEntryBridge.lean" "$SIDE/lean-toolchain" "$SIDE/verify.sh"
if grep -nE '(^|[^[:alnum:]_])(sorry|admit)([^[:alnum:]_]|$)|^[[:space:]]*axiom[[:space:]]|native_decide|implemented_by|^[[:space:]]*unsafe[[:space:]]' "$SIDE/MassEntryBridge.lean"; then
  printf 'FAIL: forbidden proof escape token\n'
  exit 1
fi

set +e
"$LEAN_BIN" -DwarningAsError=true --root="$SIDE" \
  -o "$RUN/MassEntryBridge.olean" "$SIDE/MassEntryBridge.lean" \
  2>&1 | tee "$RUN/compile.log"
CODE=${PIPESTATUS[0]}
set -e
printf 'MASS_ENTRY_BRIDGE_COMPILE_EXIT_CODE=%s\n' "$CODE"
test "$CODE" -eq 0
for DECLARATION in \
  interval_contains_translated \
  regularizer_is_explicit \
  mass_entry_float64_to_exact_interval \
  mass_entry_float64_membership; do
  grep -q "'RouteBP3MassEntryBridge.$DECLARATION' depends on axioms:" \
    "$RUN/compile.log" || {
      printf 'FAIL: missing axiom report for %s\n' "$DECLARATION"
      exit 1
    }
done
# Lean may wrap the axiom list across several lines. Audit forbidden escapes
# independently of line wrapping; standard classical axioms are allowed here.
if grep -Eiq 'sorryAx|declaration uses.*axiom|(^|[^[:alnum:]_])admit([^[:alnum:]_]|$)|^[[:space:]]*axiom[[:space:]]' "$RUN/compile.log"; then
  printf 'FAIL: forbidden or custom axiom appeared in axiom audit\n'
  exit 1
fi

sha256sum "$RUN/MassEntryBridge.olean" "$RUN/compile.log"
printf 'FOCUSED_CHECK=PASS\n'
printf 'CONDITIONAL_SOURCE_BRIDGE=OPEN\n'
printf 'REGISTRY_MUTATION=false\n'
