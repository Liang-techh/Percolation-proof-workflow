#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
LEAN_FILE="$ROOT/P4JointDefectMetric.lean"
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
  weighted_square_identity \
  scalar_weighted_square_le \
  weighted_defect_pushforward_add \
  weighted_defect_pushforward_sub \
  weighted_defect_relative_additive \
  quadratic_domination_pullback \
  singular_metric_kernel_obstruction \
  joint_metric_sign_flip \
  correction_sign_flip \
  block_diagonal_metric_sign_invariant; do
  grep -F "'RouteBP4JointDefectMetric.$theorem' depends on axioms:" "$OUT" >/dev/null || {
    echo "missing axiom report for $theorem" >&2
    exit 3
  }
done

if grep -F "sorryAx" "$OUT" >/dev/null; then
  echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2
  exit 4
fi

echo "AXIOM_AUDIT=PASS"
echo "P4_JOINT_DEFECT_METRIC_FOCUSED_CHECK=PASS"
echo "SOURCE_DEFECT_PAIR_BINDING=OPEN"
echo "SOURCE_TRANSFER_T_BINDING=OPEN"
echo "CONCRETE_JOINT_METRIC_OR_INTERVAL_CERTIFICATE=OPEN"
echo "P4_P8_M4_COVERAGE=OPEN"
echo "REGISTRY_MUTATION=false"
echo "FINAL_INTEGRATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_p4_joint_defect_metric_lean/verify.sh"
