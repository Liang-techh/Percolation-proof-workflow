#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
LEAN_FILE="$ROOT/P5BaseStorageCollar.lean"
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
  energy_ledger_rate_compression \
  two_channel_allocation_composes \
  base_storage_collar_of_energy_ledger \
  lifted_base_storage_q2_identity \
  lift_weighted_square_completion \
  lifted_base_storage_robust_collar \
  lifted_base_storage_inner_boundary \
  affine_storage_normalization_transport \
  affine_storage_gate_covariant \
  affine_storage_gap_covariant \
  nonlinear_identity_lift_defect_regression; do
  grep -F "'RouteBP5BaseStorageCollar.$theorem' depends on axioms:" "$OUT" >/dev/null || { echo "missing axiom report for $theorem" >&2; exit 3; }
done
if grep -F "sorryAx" "$OUT" >/dev/null; then echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2; exit 4; fi
echo "AXIOM_AUDIT=PASS"
echo "P5_BASE_STORAGE_COLLAR_FOCUSED_CHECK=PASS"
echo "BASE_VARIATIONAL_SEMANTICS_SEPARATED=true"
echo "LIFT_DEFECT_RETAINED=true"
echo "AFFINE_SHIFT_BUDGET_TRANSPORTED=true"
echo "DEPLOYED_SOURCE_BINDING=OPEN"
echo "P8_ODE_COVERAGE=OPEN"
echo "REGISTRY_MUTATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_p5_base_storage_collar_lean/verify.sh"
