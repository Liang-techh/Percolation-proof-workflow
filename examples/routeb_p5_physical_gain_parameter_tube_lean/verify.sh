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
  exit 2
fi
if [[ ! -f "$LAKE_ROOT/lake-manifest.json" ]]; then
  echo "BUILD_ENV_BLOCKED: pinned lake-manifest.json missing at $LAKE_ROOT" >&2
  exit 2
fi

echo "LEAN_TOOLCHAIN=$EXPECTED_TOOLCHAIN"
echo "LAKE_MANIFEST=$LAKE_ROOT/lake-manifest.json"
LOG="$(mktemp)"
trap 'rm -f "$LOG"' EXIT
(
  cd "$LAKE_ROOT"
  "$LAKE" env lean -DwarningAsError=true "$ROOT/P5PhysicalGainParameterTube.lean"
) 2>&1 | tee "$LOG"

for DECL in \
  moving_frame_a4_endpoint_bound \
  moving_frame_a5_endpoint_bound \
  moving_frame_time_abs_bound \
  four_term_square \
  four_term_component_budget \
  component_physical_gain_transport \
  parameterGain_nonneg \
  two_channel_cauchy \
  square_le_square_of_abs_le \
  product_slack_cross_bound \
  physical_gain_to_mu_nu_envelope \
  parameter_tube_gain_gate \
  slack_feasibility_necessity \
  exact_feasibility_factor; do
  grep -q "RouteBP5PhysicalGainParameterTube.$DECL" "$LOG" || {
    echo "FAIL: missing axiom report for $DECL" >&2
    exit 1
  }
done

if grep -Eiq 'sorryAx|declaration uses.*axiom|unknown module|error:' "$LOG"; then
  echo "AXIOM_AUDIT=FAIL"
  exit 1
fi

echo "AXIOM_AUDIT=PASS"
echo "P5_PHYSICAL_GAIN_PARAMETER_TUBE_FOCUSED_CHECK=PASS"
echo "SOURCE_PHYSICAL_GAIN_TABLE=OPEN"
echo "SOURCE_FLOAT64_INCREMENTAL_SEMANTICS=OPEN"
echo "P8_SAME_DOMAIN_COVERAGE=OPEN"
echo "ODE_FIRST_EXIT_CONTINUATION=OPEN"
echo "P5_P8_M4_FINAL_INTEGRATION=false"
echo "REGISTRY_MUTATION=false"
