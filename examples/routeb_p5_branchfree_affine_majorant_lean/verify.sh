#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
LEAN_FILE="$ROOT/P5BranchFreeAffineMajorant.lean"
EXPECTED_TOOLCHAIN="$(tr -d '\r\n' < "$ROOT/lean-toolchain")"

command -v lake >/dev/null 2>&1 || {
  echo "lake not found on PATH" >&2
  exit 2
}
command -v lean >/dev/null 2>&1 || {
  echo "lean not found on PATH" >&2
  exit 2
}

if [[ ! -d "$LAKE_ROOT" ]]; then
  echo "local_fkg Lake environment not found at $LAKE_ROOT" >&2
  exit 2
fi
if [[ ! -f "$LAKE_ROOT/lake-manifest.json" ]]; then
  echo "pinned lake-manifest.json missing at $LAKE_ROOT" >&2
  exit 2
fi

ACTUAL_TOOLCHAIN="$(tr -d '\r\n' < "$LAKE_ROOT/lean-toolchain")"
if [[ "$ACTUAL_TOOLCHAIN" != "$EXPECTED_TOOLCHAIN" ]]; then
  echo "toolchain mismatch: sidecar=$EXPECTED_TOOLCHAIN local_fkg=$ACTUAL_TOOLCHAIN" >&2
  exit 2
fi

OUT="$(mktemp)"
trap 'rm -f "$OUT"' EXIT

(
  cd "$LAKE_ROOT"
  lake env lean -DwarningAsError=true "$LEAN_FILE"
) 2>&1 | tee "$OUT"

for theorem in \
  sym2_scaled_qf_completion_identity \
  sym2_scaled_qf_nonneg_of_trace_det4 \
  majorant_trace_identity \
  majorant_det4_identity \
  affine_majorant_scaled_identity \
  affine_energy_le_of_two_invariant_gates \
  affine_energy_le_of_nonnegative_remainders \
  affine_energy_lt_of_two_invariant_gates \
  source_family_affine_energy_le \
  degenerate_family_joint_gates \
  degenerate_family_affine_bound; do
  grep -F "'RouteBP5BranchFreeAffineMajorant.$theorem' depends on axioms:" "$OUT" >/dev/null || {
    echo "missing axiom report for $theorem" >&2
    exit 3
  }
done

if grep -F "sorryAx" "$OUT" >/dev/null; then
  echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2
  exit 4
fi

echo "AXIOM_AUDIT=PASS"
echo "P5_BRANCHFREE_AFFINE_MAJORANT_FOCUSED_CHECK=PASS"
echo "BRANCH_FREE_TWO_GATE_FORWARD_CONSUMER=true"
echo "SIGNED_SIGMA_SAME_KEY_REQUIRED=true"
echo "JOINT_RTRACE_RDET_ENCLOSURE_REQUIRED=true"
echo "OPTIONAL_GLOBAL_IFF_CONVERSE=OPEN"
echo "SOURCE_FLOAT64_BINDING=OPEN"
echo "P8_ODE_COVERAGE=OPEN"
echo "P5_M4_FINAL_INTEGRATION=false"
echo "REGISTRY_MUTATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_p5_branchfree_affine_majorant_lean/verify.sh"
