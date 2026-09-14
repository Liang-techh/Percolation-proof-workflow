#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$ROOT/../.." && pwd)"
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

# The target imports repository-local BODY6 modules which in turn reach
# ActualStorage/ActualShift and other sidecar-owned sources. Compile that
# source import closure under this audit's pinned Lake environment instead of
# relying on stale committed receipts or developer-machine .olean files.
# Snapshot/output trees are evidence, not authoritative source.
BUILD_DIR="$(mktemp -d "$LAKE_ROOT/.aligned-pathcap-audit.XXXXXX")"
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

declare -A COMPILED_MODULES=()
declare -A VISITING_MODULES=()
# SignedGap consumes RouteBChristoffelPower.christoffelTwoChannelBound. The
# repository also contains an independent P5 top-level ChristoffelPower.lean,
# so bind this import closure to the exact source required by SignedGap and
# keep every other duplicate module name a hard error.
declare -A REPO_MODULE_SOURCE_OVERRIDES=(
  [ChristoffelPower]="$REPO_ROOT/examples/routeb_christoffel_power/ChristoffelPower.lean"
)

module_relpath() {
  printf '%s' "${1//./\/}"
}

find_repo_module_source() {
  local module="$1"
  local override="${REPO_MODULE_SOURCE_OVERRIDES[$module]:-}"
  if [[ -n "$override" ]]; then
    [[ -f "$override" ]] || {
      echo "repository module override missing for $module: $override" >&2
      return 2
    }
    printf '%s\n' "$override"
    return 0
  fi

  local rel
  rel="$(module_relpath "$module")"
  local -a matches=()
  mapfile -t matches < <(
    find "$REPO_ROOT/examples" \
      -path '*/output/*' -prune -o \
      -path '*/snapshots/*' -prune -o \
      -path '*/.lake/*' -prune -o \
      -type f -path "*/$rel.lean" -print | sort
  )

  if ((${#matches[@]} == 0)); then
    return 1
  fi
  if ((${#matches[@]} != 1)); then
    echo "ambiguous repository module source for $module:" >&2
    printf '  %s\n' "${matches[@]}" >&2
    return 2
  fi
  printf '%s\n' "${matches[0]}"
}

compile_repo_module() {
  local module="$1"
  [[ -n "${COMPILED_MODULES[$module]:-}" ]] && return 0
  if [[ -n "${VISITING_MODULES[$module]:-}" ]]; then
    echo "repository module import cycle at $module" >&2
    return 2
  fi

  local source rc=0
  source="$(find_repo_module_source "$module")" || rc=$?
  case "$rc" in
    0) ;;
    1)
      echo "EXTERNAL_IMPORT=$module"
      return 0
      ;;
    *) return "$rc" ;;
  esac

  VISITING_MODULES[$module]=1
  local dep
  while read -r dep; do
    [[ -z "$dep" ]] && continue
    compile_repo_module "$dep"
  done < <(awk '/^[[:space:]]*import[[:space:]]+/ { for (i = 2; i <= NF; ++i) print $i }' "$source")

  local rel staged olean
  rel="$(module_relpath "$module")"
  staged="$BUILD_DIR/$rel.lean"
  olean="$BUILD_DIR/$rel.olean"
  mkdir -p "$(dirname "$staged")"
  cp "$source" "$staged"
  echo "COMPILE_REPO_MODULE=$module source=${source#$REPO_ROOT/}"
  run_lean -DwarningAsError=true -o "$olean" "$staged"
  COMPILED_MODULES[$module]=1
  unset 'VISITING_MODULES[$module]'
}

compile_repo_module NEW_BODY6_SLICE_INITIALPATHCAPS20260907
compile_repo_module NEW_BODY6_SLICE_ACTUALSTORAGEALIGN20260907
echo "LOCAL_IMPORT_BOOTSTRAP=PASS"

AUDIT="$BUILD_DIR/AlignedPathcapConsumerAudit.lean"
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
echo "BODY6_ALIGNED_PATHCAP_CONSUMER_FOCUSED_CHECK=PASS"
echo "ALIGNED_PATHCAP_CONSUMER=true"
echo "UNPAID_SHIFT_COUNTEREXAMPLE=true"
echo "CONSUMER_PREMISES_INSTANCE_PROVED=false"
echo "WHOLE_PATH_INCLUSION_PROVED=false"
echo "PHYSICAL_DH_SOURCE_BINDING=OPEN"
echo "ODE_CONTINUATION_COVERAGE=OPEN"
echo "REGISTRY_MUTATION=false"
echo "SIDECAR_RESULT=PASS path=examples/routeb_body6_aligned_pathcap_consumer_audit/verify.sh"
