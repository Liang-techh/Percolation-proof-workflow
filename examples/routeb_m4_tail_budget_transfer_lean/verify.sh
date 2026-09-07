#!/usr/bin/env bash
set -euo pipefail
# CI_PORTABLE=1

ROOT="$(cd "$(dirname "$0")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"

if [[ -z "${LAKE:-}" ]]; then
  LAKE="$(command -v lake || true)"
fi

if [[ -z "$LAKE" ]]; then
  echo "BUILD_ENV_BLOCKED: cannot locate lake on PATH" >&2
  exit 2
fi

if [[ ! -f "$LAKE_ROOT/lakefile.toml" && ! -f "$LAKE_ROOT/lakefile.lean" ]]; then
  echo "BUILD_ENV_BLOCKED: local Lake root missing at $LAKE_ROOT" >&2
  exit 2
fi

EXPECTED_TOOLCHAIN="$(tr -d '\r\n' < "$ROOT/lean-toolchain")"
ACTUAL_TOOLCHAIN="$(tr -d '\r\n' < "$LAKE_ROOT/lean-toolchain")"
if [[ "$ACTUAL_TOOLCHAIN" != "$EXPECTED_TOOLCHAIN" ]]; then
  echo "BUILD_ENV_BLOCKED: toolchain mismatch" >&2
  echo "EXPECTED_TOOLCHAIN=$EXPECTED_TOOLCHAIN" >&2
  echo "ACTUAL_TOOLCHAIN=$ACTUAL_TOOLCHAIN" >&2
  exit 2
fi

echo "LEAN_TOOLCHAIN=$EXPECTED_TOOLCHAIN"
LOG="$(mktemp)"
trap 'rm -f "$LOG"' EXIT

(
  cd "$LAKE_ROOT"
  "$LAKE" env lean -DwarningAsError=true "$ROOT/M4TailBudgetTransfer.lean"
) 2>&1 | tee "$LOG"

for DECL in \
  tail_budget_transfer \
  old_gate_plus_rho16_exact \
  old_gate_plus_tail_of_rho_le_16 \
  tail_budget_from_slack; do
  grep -q "RouteBM4TailBudgetTransfer.$DECL" "$LOG" || {
    echo "FAIL: missing axiom report for $DECL" >&2
    exit 1
  }
done

if grep -Eiq 'sorryAx|declaration uses.*axiom|unknown module|error:' "$LOG"; then
  echo "AXIOM_AUDIT=FAIL"
  exit 1
fi

echo "AXIOM_AUDIT=PASS"
echo "M4_TAIL_BUDGET_TRANSFER_FOCUSED_CHECK=PASS"
echo "PHYSICAL_RHOBAR_BINDING=OPEN"
echo "P8_FLOWPIPE_COVERAGE=OPEN"
echo "REGISTRY_MUTATION=false"
