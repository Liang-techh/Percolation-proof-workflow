#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
TARGET="$ROOT/../routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907.lean"
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

#print axioms NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907.whole_path_has_initial_attempt
#print axioms NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907.project_whole_path_attempt
#print axioms NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907.project_initial_only_attempt
#print axioms NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907.projected_shift_cap_transfer_attempt
#print axioms NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907.already_shifted_cap_transfer_attempt
#print axioms NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907.initial_does_not_give_whole_path_attempt
#print axioms NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907.shift_accounting_counterexample_attempt
EOF

(
  cd "$LAKE_ROOT"
  lake env lean -DwarningAsError=true "$TMP"
) 2>&1 | tee "$OUT"

for theorem in \
  whole_path_has_initial_attempt \
  project_whole_path_attempt \
  project_initial_only_attempt \
  projected_shift_cap_transfer_attempt \
  already_shifted_cap_transfer_attempt \
  initial_does_not_give_whole_path_attempt \
  shift_accounting_counterexample_attempt; do
  grep -F "NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907.$theorem" "$OUT" >/dev/null || {
    echo "missing #print axioms report for $theorem" >&2
    exit 3
  }
done

if grep -F "sorryAx" "$OUT" >/dev/null; then
  echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2
  exit 4
fi

echo "AXIOM_AUDIT=PASS"
echo "BODY6_PATHDOMAIN_REPAIR_FOCUSED_CHECK=PASS"
echo "CAP_PLUS_SHIFT_ORDER_REPAIR=true"
echo "WHOLE_PATH_INCLUSION_PROVED=false"
echo "PHYSICAL_DH_SOURCE_BINDING=OPEN"
echo "REGISTRY_MUTATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_body6_pathdomain_projection_audit/verify.sh"
