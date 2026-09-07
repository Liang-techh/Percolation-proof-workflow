#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
LEAN_FILE="$ROOT/P4RobustPhaseCells.lean"
EXPECTED_TOOLCHAIN="$(tr -d '\r\n' < "$ROOT/lean-toolchain")"
EXPECTED_MATHLIB_REV="81a5d257c8e410db227a6665ed08f64fea08e997"

command -v lake >/dev/null 2>&1 || { echo "lake not found on PATH" >&2; exit 2; }
command -v lean >/dev/null 2>&1 || { echo "lean not found on PATH" >&2; exit 2; }

if [[ ! -d "$LAKE_ROOT" ]]; then
  echo "pinned Lake environment not found at $LAKE_ROOT" >&2
  exit 2
fi

ACTUAL_TOOLCHAIN="$(tr -d '\r\n' < "$LAKE_ROOT/lean-toolchain")"
if [[ "$ACTUAL_TOOLCHAIN" != "$EXPECTED_TOOLCHAIN" ]]; then
  echo "toolchain mismatch: sidecar=$EXPECTED_TOOLCHAIN local_fkg=$ACTUAL_TOOLCHAIN" >&2
  exit 2
fi

if ! grep -F "\"rev\": \"$EXPECTED_MATHLIB_REV\"" "$LAKE_ROOT/lake-manifest.json" >/dev/null; then
  echo "mathlib manifest pin mismatch" >&2
  exit 2
fi

OUT="$(mktemp)"
trap 'rm -f "$OUT"' EXIT
(
  cd "$LAKE_ROOT"
  lake env lean -DwarningAsError=true "$LEAN_FILE"
) 2>&1 | tee "$OUT"

for theorem in \
  base_trig_cell_of_abs_le \
  formed_angle_error_to_reduced_radius \
  phase_neg_quarter_cell \
  phase_zero_cell \
  phase_pos_quarter_cell \
  quarter_phase_cell \
  theta_cos_lower_constant \
  theta_all6_exact_cells_from_qbox \
  alpha_all6_exact_cells \
  robust_phase_cell_of_formed_angle_error \
  robust_theta_cell_of_formed_angle_error \
  robust_alpha_cell_of_formed_angle_error; do
  grep -F "'RouteBP4RobustPhaseCells.$theorem' depends on axioms:" "$OUT" >/dev/null || {
    echo "missing axiom report for $theorem" >&2
    exit 3
  }
done

if grep -F "sorryAx" "$OUT" >/dev/null; then
  echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2
  exit 4
fi

echo "AXIOM_AUDIT=PASS"
echo "P4_ROBUST_PHASE_CELLS_FOCUSED_CHECK=PASS"
echo "ANGLE_FORMATION_FLOAT64_BINDING=OPEN"
echo "LIBM_OUTPUT_INCLUSION=OPEN"
echo "D1_D2_D3_PROPAGATION=OPEN"
echo "P8_COVERAGE=OPEN"
echo "REGISTRY_MUTATION=false"
echo "FINAL_INTEGRATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_p4_robust_phase_cells_lean/verify.sh"
