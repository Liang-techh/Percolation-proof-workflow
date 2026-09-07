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
  LEAN_FILE="$(wslpath -w "$ROOT/P4SharpSchur.lean")"
else
  LEAN_FILE="$ROOT/P4SharpSchur.lean"
fi

(cd "$LAKE_ROOT" && "$LAKE" env lean -DwarningAsError=true "$LEAN_FILE") 2>&1 | tee "$LOG"

grep -q "schur_residual_nonnegative_iff" "$LOG"
grep -q "zero_y_forces_zero_residual" "$LOG"
grep -q "quarter_sq_lt_p4d4" "$LOG"
grep -q "quarter_residual_absorption" "$LOG"

if grep -Eiq 'sorryAx|declaration uses.*axiom|unknown module|error:' "$LOG"; then
  echo "AXIOM_AUDIT=FAIL"
  exit 1
fi

echo "AXIOM_AUDIT=PASS"
echo "P4_SHARP_SCHUR_FOCUSED_CHECK=PASS"
