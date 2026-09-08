#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAKE_ROOT="${LAKE_ROOT:-$ROOT/../local_fkg}"
SRC_ROOT="$ROOT/../routeb_b45_source_comparator_lean"
TARGET="$SRC_ROOT/NEW_BODY6_SLICE_ALIGNEDPATHCAPCONSUMER20260908.lean"
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

# Lean 4.32 rejects -o compilation when the input source is outside the Lake
# package root.  Stage the BODY6 local-import chain inside the pinned local_fkg
# root, compile it into an isolated cache, and remove the staging directory on
# exit.  No repository source file or Lake manifest is modified.
BUILD_DIR="$(mktemp -d "$LAKE_ROOT/.aligned-consumer-audit.XXXXXX")"
OUT="$(mktemp)"
trap 'rm -rf "$BUILD_DIR"; rm -f "$OUT"' EXIT

run_lean() {
  (
    cd "$LAKE_ROOT"
    lake env bash -c '
      build_dir="$1"
      shift
      export LEAN_PATH="$build_dir${LEAN_PATH:+:$LEAN_PATH}"
      exec lean "$@"
    ' _ "$BUILD_DIR" "$@"
  )
}

compile_local_module() {
  local module="$1"
  local source="$SRC_ROOT/$module.lean"
  local staged="$BUILD_DIR/$module.lean"
  [[ -f "$source" ]] || { echo "local import missing: $source" >&2; exit 2; }
  cp "$source" "$staged"
  run_lean -DwarningAsError=true -o="$BUILD_DIR/$module.olean" "$staged"
}

compile_local_module NEW_BODY6_SLICE_ACTUALSTORAGEALIGN20260907
compile_local_module NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907
compile_local_module NEW_BODY6_SLICE_INITIALPATHCAPS20260907
echo "LOCAL_IMPORT_BOOTSTRAP=PASS"

AUDIT="$BUILD_DIR/AlignedConsumerAudit.lean"
cat "$TARGET" > "$AUDIT"
cat >> "$AUDIT" <<'EOF'

#print axioms NEW_BODY6_SLICE_ALIGNEDPATHCAPCONSUMER20260908.consume_aligned_path_cap_attempt
#print axioms NEW_BODY6_SLICE_ALIGNEDPATHCAPCONSUMER20260908.source_full_cap_does_not_pay_shift_attempt
EOF

run_lean -DwarningAsError=true "$AUDIT" 2>&1 | tee "$OUT"

for theorem in \
  consume_aligned_path_cap_attempt \
  source_full_cap_does_not_pay_shift_attempt; do
  grep -F "NEW_BODY6_SLICE_ALIGNEDPATHCAPCONSUMER20260908.$theorem" "$OUT" >/dev/null || {
    echo "missing #print axioms report for $theorem" >&2
    exit 3
  }
done

if grep -F "sorryAx" "$OUT" >/dev/null; then
  echo "AXIOM_AUDIT=FAIL sorryAx detected" >&2
  exit 4
fi

echo "AXIOM_AUDIT=PASS"
echo "BODY6_ALIGNED_CONSUMER_FOCUSED_CHECK=PASS"
echo "SHIFT_CHARGED_ONCE=true"
echo "CONSUMER_PREMISES_INSTANCE_PROVED=false"
echo "PHYSICAL_SOURCE_PATH_ODE_BINDING=OPEN"
echo "DOMAIN_COVERAGE_FIRST_EXIT=OPEN"
echo "REGISTRY_MUTATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_body6_aligned_consumer_audit/verify.sh"
