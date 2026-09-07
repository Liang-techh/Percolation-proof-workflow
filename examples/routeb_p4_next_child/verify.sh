#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-../local_fkg}"
if [[ -z "${LAKE:-}" ]]; then
  if command -v lake >/dev/null 2>&1; then
    LAKE="$(command -v lake)"
  else
    for candidate in \
      /mnt/c/Users/z5242/.elan/bin/lake.exe \
      /c/Users/z5242/.elan/bin/lake.exe \
      'C:/Users/z5242/.elan/bin/lake.exe'; do
      if [[ -f "$candidate" ]]; then
        LAKE="$candidate"
        break
      fi
    done
  fi
fi
if [[ -z "${LAKE:-}" ]]; then
  echo "BUILD_ENV_BLOCKED: cannot locate lake/lake.exe" >&2
  exit 2
fi
cd "$ROOT"

echo "LEAN_TOOLCHAIN=$(cat lean-toolchain)"
LOG="$(mktemp)"
trap 'rm -f "$LOG"' EXIT
if command -v wslpath >/dev/null 2>&1; then
  LEAN_FILE="$(wslpath -w "$ROOT/P4RationalSchurAbsorption.lean")"
else
  LEAN_FILE="$ROOT/P4RationalSchurAbsorption.lean"
fi
(cd "$LAKE_ROOT" && "$LAKE" env lean -DwarningAsError=true \
  "$LEAN_FILE") 2>&1 | tee "$LOG"
grep -q "exact_schur_margin" "$LOG"
grep -q "exact_schur_nonnegative" "$LOG"
grep -q "residual_absorption" "$LOG"
if grep -Eiq 'sorryAx|declaration uses.*axiom|unknown module|error:' "$LOG"; then
  echo "AXIOM_AUDIT=FAIL"
  exit 1
fi
echo "AXIOM_AUDIT=PASS"
echo "FOCUSED_CHECK=PASS"
