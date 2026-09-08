#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
TARGET="$ROOT/../routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_ALIGNEDPATHCAPCONSUMER20260908.lean"
EXPECTED_TOOLCHAIN="$(tr -d '\r\n' < "$ROOT/lean-toolchain")"

command -v lake >/dev/null 2>&1 || { echo "lake not found on PATH" >&2; exit 2; }
command -v lean >/dev/null 2>&1 || { echo "lean not found on PATH" >&2; exit 2; }
[[ -f "$TARGET" ]] || { echo "target missing: $TARGET" >&2; exit 2; }
[[ -d "$LAKE_ROOT" ]] || { echo "local_fkg Lake environment missing: $LAKE_ROOT" >&2; exit 2; }
[[ -f "$LAKE_ROOT/lake-manifest.json" ]] || { echo "pinned lake-manifest.json missing" >&2; exit 2; }

ACTUAL_TOOLCHAIN="$(tr -d '\r\n' < "$LAKE_ROOT/lean-toolchain")"
[[ "$ACTUAL_TOOLCHAIN" == "$EXPECTED_TOOLCHAIN" ]] || {
  echo "toolchain mismatch: audit=$EXPECTED_TOOLCHAIN local_fkg=$ACTUAL_TOOLCHAIN" >&2
  exit 2
}

if grep -nE '\b(sorry|admit)\b' "$TARGET"; then
  echo "PLACEHOLDER_SCAN=FAIL" >&2
  exit 4
fi
echo "PLACEHOLDER_SCAN=PASS"

TMP="$(mktemp --suffix=.lean)"
OUT="$(mktemp)"
trap 'rm -f "$TMP" "$OUT"' EXIT
cat "$TARGET" > "$TMP"
cat >> "$TMP" <<'EOF'

#print axioms RouteBAlignedPathcapConsumerProof.actualStorageEqualsBRplusB_at_aligned_pathcap
#print axioms RouteBAlignedPathcapConsumerProof.actualStorageDefect_nonneg_at_aligned_pathcap
EOF

(
  cd "$LAKE_ROOT"
  lake env lean -DwarningAsError=true "$TMP"
) 2>&1 | tee "$OUT"

for theorem in \
  actualStorageEqualsBRplusB_at_aligned_pathcap \
  actualStorageDefect_nonneg_at_aligned_pathcap; do
  grep -F "RouteBAlignedPathcapConsumerProof.$theorem" "$OUT" >/dev/null || {
    echo "missing #print axioms report for $theorem" >&2
    exit 3
  }
done

if grep -F "sorryAx" "$OUT" >/dev/null; then
  echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2
  exit 4
fi

echo "AXIOM_AUDIT=PASS"
echo "BODY6_ALIGNED_PATHCAP_CONSUMER_FOCUSED_CHECK=PASS"
echo "ALIGNED_PATHCAP_STORAGE_GATE=true"
echo "WHOLE_PATH_INCLUSION_PROVED=false"
echo "PHYSICAL_DH_SOURCE_BINDING=OPEN"
echo "ODE_CONTINUATION_COVERAGE=OPEN"
echo "REGISTRY_MUTATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_body6_aligned_pathcap_consumer_audit/verify.sh"
