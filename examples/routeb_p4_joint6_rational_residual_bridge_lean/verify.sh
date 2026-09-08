#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
LEAN_FILE="$ROOT/P4Joint6RationalResidualBridge.lean"
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
  ne_zero_of_pos_le_abs \
  rational_residual_sub_eq_cross_mul_div \
  rational_residual_eq_of_cross_mul \
  abs_div_le_of_abs_num_le \
  abs_den_product_lower \
  rational_residual_sup_le_of_cross_mul_bound \
  division_free_residual_sup_gate \
  same_cell_source_residual_eq \
  same_cell_source_division_free_sup_gate \
  quotient_difference_split \
  rational_residual_pair_lipschitz_of_cross_mul_packet \
  division_free_residual_lipschitz_gate; do
  grep -F "'RouteBP4Joint6RationalResidualBridge.$theorem' depends on axioms:" "$OUT" >/dev/null || { echo "missing axiom report for $theorem" >&2; exit 3; }
done
if grep -F "sorryAx" "$OUT" >/dev/null; then echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2; exit 4; fi
echo "AXIOM_AUDIT=PASS"
echo "P4_JOINT6_RATIONAL_RESIDUAL_BRIDGE_FOCUSED_CHECK=PASS"
echo "SIGNED_CROSS_MISMATCH_BEFORE_ENCLOSURE=true"
echo "SAME_CELL_SOURCE_KEY_TYPED=true"
echo "DIVISION_FREE_SUP_GATE=true"
echo "DIVISION_FREE_LIPSCHITZ_GATE=true"
echo "PRINCIPAL_COMPACT_JOINT6_SOURCE_PACKET=OPEN"
echo "DEPLOYED_SOURCE_BINDING=OPEN"
echo "FLOAT64_FD_CONTROLLER_SOLVE=OPEN"
echo "P8_ODE_COVERAGE=OPEN"
echo "REGISTRY_MUTATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_p4_joint6_rational_residual_bridge_lean/verify.sh"
