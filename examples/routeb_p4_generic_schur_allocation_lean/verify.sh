#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
LEAN_FILE="$ROOT/P4GenericSchurAllocation.lean"
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
  sq_nonnegative \
  sq_add \
  sq_sub_smul \
  combined_remainder_identity \
  combined_of_port_budget \
  relaxed_target_le_exact_total \
  exact_total_floor_of_relaxed_nonnegative \
  zero_radius_boundary_not_finite_witness; do
  grep -F "'RouteBP4GenericSchurAllocation.$theorem' depends on axioms:" "$OUT" >/dev/null || { echo "missing axiom report for $theorem" >&2; exit 3; }
done
if grep -F "sorryAx" "$OUT" >/dev/null; then echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2; exit 4; fi
echo "AXIOM_AUDIT=PASS"
echo "P4_GENERIC_SCHUR_ALLOCATION_FOCUSED_CHECK=PASS"
echo "FINITE_DIMENSION_GENERIC=true"
echo "EXACT_COMPLETED_SQUARE=true"
echo "NO_DOUBLE_CHARGE_COMPARISON=true"
echo "DENSE_METRIC_TRANSPORT=OPEN"
echo "DEPLOYED_SOURCE_BINDING=OPEN"
echo "P8_ODE_COVERAGE=OPEN"
echo "REGISTRY_MUTATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_p4_generic_schur_allocation_lean/verify.sh"
