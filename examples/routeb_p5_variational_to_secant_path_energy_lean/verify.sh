#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
LEAN_FILE="$ROOT/P5VariationalToSecantPathEnergy.lean"
EXPECTED_TOOLCHAIN="$(tr -d '\r\n' < "$ROOT/lean-toolchain")"
command -v lake >/dev/null 2>&1 || { echo "lake not found on PATH" >&2; exit 2; }
command -v lean >/dev/null 2>&1 || { echo "lean not found on PATH" >&2; exit 2; }
[[ -d "$LAKE_ROOT" ]] || { echo "local_fkg Lake environment not found at $LAKE_ROOT" >&2; exit 2; }
[[ -f "$LAKE_ROOT/lake-manifest.json" ]] || { echo "pinned lake-manifest.json missing at $LAKE_ROOT" >&2; exit 2; }
ACTUAL_TOOLCHAIN="$(tr -d '\r\n' < "$LAKE_ROOT/lean-toolchain")"
[[ "$ACTUAL_TOOLCHAIN" == "$EXPECTED_TOOLCHAIN" ]] || { echo "toolchain mismatch: sidecar=$EXPECTED_TOOLCHAIN local_fkg=$ACTUAL_TOOLCHAIN" >&2; exit 2; }
if grep -nE '\b(sorry|admit)\b' "$LEAN_FILE"; then echo "PLACEHOLDER_SCAN=FAIL" >&2; exit 4; fi
echo "PLACEHOLDER_SCAN=PASS"
OUT="$(mktemp)"; trap 'rm -f "$OUT"' EXIT
(cd "$LAKE_ROOT" && lake env lean -DwarningAsError=true "$LEAN_FILE") 2>&1 | tee "$OUT"
for theorem in \
  one_step_rational_decay_from_integral_packet \
  relative_rate_one_step_from_integral_packet \
  finite_sum_path_energy_contraction \
  quadratic_midpoint_jensen_of_psd_direction \
  two_sample_secant_packet \
  raw_normalized_chord_sq_expands \
  pullback_tangent_contracts \
  nonlinear_chart_unit_packet; do
  grep -F "'RouteBP5VariationalToSecantPathEnergy.$theorem' depends on axioms:" "$OUT" >/dev/null || { echo "missing axiom report for $theorem" >&2; exit 3; }
done
if grep -F "sorryAx" "$OUT" >/dev/null; then echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2; exit 4; fi
echo "AXIOM_AUDIT=PASS"
echo "P5_VARIATIONAL_TO_SECANT_PATH_ENERGY_FOCUSED_CHECK=PASS"
echo "RATIONAL_ONE_STEP_PACKET=true"
echo "FINITE_SUM_PATH_ENERGY=true"
echo "MIDPOINT_JENSEN_PACKET=true"
echo "NONLINEAR_CHART_COUNTEREXAMPLE=true"
echo "FULL_CALCULUS_FTC=OPEN"
echo "ARBITRARY_N_PARTITION=OPEN"
echo "PATH_INFIMUM_GEODESIC=OPEN"
echo "SAME_TUBE_SOURCE_COVERAGE=OPEN"
echo "FLOAT64_FD_CONTROLLER_SOLVE=OPEN"
echo "P8_ODE_COVERAGE=OPEN"
echo "REGISTRY_MUTATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_p5_variational_to_secant_path_energy_lean/verify.sh"
