#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LEAN_FILE="$ROOT/AnthropicFLTQuotientTransport.lean"
EXPECTED_UPSTREAM_TOOLCHAIN="$(tr -d '\r\n' < "$ROOT/lean-toolchain")"
EXPECTED_COMPILE_TOOLCHAIN="leanprover/lean4:v4.33.0"
EXPECTED_FLT_SHA="aa2d8b34692b16c70f699536de0d8e75b9a3e9ef"
EXPECTED_MATHLIB_SHA="db584cd6d46c92f209a44c0f1c829460d327499d"
SOURCE_ROOT="${SOURCE_ROOT:-}"
LAKE_ROOT="${LAKE_ROOT:-}"

if [[ -z "${LAKE:-}" ]]; then
  if command -v lake >/dev/null 2>&1; then
    LAKE="$(command -v lake)"
  else
    echo "BUILD_ENV_BLOCKED: lake not found on PATH" >&2
    exit 2
  fi
fi

[[ -n "$SOURCE_ROOT" ]] || {
  echo "BUILD_ENV_BLOCKED: SOURCE_ROOT must point to Anthropic FLT $EXPECTED_FLT_SHA" >&2
  exit 2
}
[[ -d "$SOURCE_ROOT" ]] || { echo "BUILD_ENV_BLOCKED: SOURCE_ROOT not found: $SOURCE_ROOT" >&2; exit 2; }
[[ -f "$SOURCE_ROOT/lean-toolchain" ]] || { echo "BUILD_ENV_BLOCKED: source lean-toolchain missing at $SOURCE_ROOT" >&2; exit 2; }
[[ -f "$SOURCE_ROOT/lake-manifest.json" ]] || { echo "BUILD_ENV_BLOCKED: source lake-manifest.json missing at $SOURCE_ROOT" >&2; exit 2; }

ACTUAL_UPSTREAM_TOOLCHAIN="$(tr -d '\r\n' < "$SOURCE_ROOT/lean-toolchain")"
[[ "$ACTUAL_UPSTREAM_TOOLCHAIN" == "$EXPECTED_UPSTREAM_TOOLCHAIN" ]] || {
  echo "BUILD_ENV_BLOCKED: upstream toolchain mismatch: expected=$EXPECTED_UPSTREAM_TOOLCHAIN actual=$ACTUAL_UPSTREAM_TOOLCHAIN" >&2
  exit 2
}
if git -C "$SOURCE_ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  ACTUAL_FLT_SHA="$(git -C "$SOURCE_ROOT" rev-parse HEAD)"
  [[ "$ACTUAL_FLT_SHA" == "$EXPECTED_FLT_SHA" ]] || {
    echo "BUILD_ENV_BLOCKED: Anthropic FLT mismatch: expected=$EXPECTED_FLT_SHA actual=$ACTUAL_FLT_SHA" >&2
    exit 2
  }
fi
if ! grep -F "\"rev\": \"$EXPECTED_MATHLIB_SHA\"" "$SOURCE_ROOT/lake-manifest.json" >/dev/null; then
  echo "BUILD_ENV_BLOCKED: pinned Mathlib $EXPECTED_MATHLIB_SHA not present in FLT lake-manifest.json" >&2
  exit 2
fi

[[ -n "$LAKE_ROOT" ]] || {
  echo "BUILD_ENV_BLOCKED: LAKE_ROOT must point to standalone Mathlib $EXPECTED_MATHLIB_SHA ($EXPECTED_COMPILE_TOOLCHAIN)" >&2
  exit 2
}
[[ -d "$LAKE_ROOT" ]] || { echo "BUILD_ENV_BLOCKED: LAKE_ROOT not found: $LAKE_ROOT" >&2; exit 2; }
[[ -f "$LAKE_ROOT/lean-toolchain" ]] || { echo "BUILD_ENV_BLOCKED: compile lean-toolchain missing at $LAKE_ROOT" >&2; exit 2; }

ACTUAL_COMPILE_TOOLCHAIN="$(tr -d '\r\n' < "$LAKE_ROOT/lean-toolchain")"
[[ "$ACTUAL_COMPILE_TOOLCHAIN" == "$EXPECTED_COMPILE_TOOLCHAIN" ]] || {
  echo "BUILD_ENV_BLOCKED: compatibility toolchain mismatch: expected=$EXPECTED_COMPILE_TOOLCHAIN actual=$ACTUAL_COMPILE_TOOLCHAIN" >&2
  exit 2
}
if git -C "$LAKE_ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  ACTUAL_MATHLIB_SHA="$(git -C "$LAKE_ROOT" rev-parse HEAD)"
  [[ "$ACTUAL_MATHLIB_SHA" == "$EXPECTED_MATHLIB_SHA" ]] || {
    echo "BUILD_ENV_BLOCKED: Mathlib mismatch: expected=$EXPECTED_MATHLIB_SHA actual=$ACTUAL_MATHLIB_SHA" >&2
    exit 2
  }
fi

if grep -nE '\b(sorry|admit)\b' "$LEAN_FILE"; then
  echo "PLACEHOLDER_SCAN=FAIL" >&2
  exit 4
fi
echo "PLACEHOLDER_SCAN=PASS"

LOG="$(mktemp)"
trap 'rm -f "$LOG"' EXIT
(
  cd "$LAKE_ROOT"
  "$LAKE" env lean -DwarningAsError=true "$LEAN_FILE"
) 2>&1 | tee "$LOG"

for theorem in \
  quotientContinuousLinearEquiv \
  quotientPiContinuousLinearEquiv \
  quotient_transport_mk; do
  if ! grep -F "'AnthropicFLTQuotientTransport.$theorem' depends on axioms:" "$LOG" >/dev/null \
      && ! grep -F "'AnthropicFLTQuotientTransport.$theorem' does not depend on any axioms" "$LOG" >/dev/null; then
    echo "missing axiom report for $theorem" >&2
    exit 3
  fi
done

if grep -F "sorryAx" "$LOG" >/dev/null; then
  echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2
  exit 4
fi

echo "AXIOM_AUDIT=PASS"
echo "FLT_QUOTIENT_TRANSPORT_FOCUSED_CHECK=PASS"
echo "UPSTREAM_TOOLCHAIN=$EXPECTED_UPSTREAM_TOOLCHAIN"
echo "PORTABLE_COMPILE_TOOLCHAIN=$EXPECTED_COMPILE_TOOLCHAIN"
echo "PINNED_FLT_SHA=$EXPECTED_FLT_SHA"
echo "PINNED_MATHLIB_SHA=$EXPECTED_MATHLIB_SHA"
echo "PORTABLE_EVIDENCE=mathlib-4.33.0-compatibility-not-exact-flt-4.33.1-replay"
echo "REGISTRY_MUTATION=false"
echo "SIDECAR_RESULT=PASS path=examples/anthropic_flt_quotient_transport_sidecar/verify.sh"
