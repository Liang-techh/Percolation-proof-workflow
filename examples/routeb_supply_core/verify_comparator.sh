#!/usr/bin/env bash
# All outputs and frozen inputs stay in this sidecar. No tool builds/downloads.
# Usage: bash verify_comparator.sh [cached-exporter]
# ROUTEB_LEAN4EXPORT may select an existing compatible binary supplied later.
set -euo pipefail
SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
MODE=${1:-cached-exporter}
case "$MODE" in cached-exporter) ;; *) exit 2 ;; esac
CACHE=/home/z5242/sos_lean
TOOLS=/home/z5242/.cache/lean-ci-tools
PREFIX=/home/z5242/.elan/toolchains/leanprover--lean4---v4.33.1
export PATH="$PREFIX/bin:$PATH" LEAN_ABORT_ON_PANIC=1
mkdir -p "$SIDE/output"
RUN=$(mktemp -d "$SIDE/output/comparator-$MODE-XXXXXXXX")
exec > >(tee "$RUN/run.log") 2>&1
trap 'CODE=$?; printf "RUN_EXIT_CODE=%s\n" "$CODE"; exit "$CODE"' EXIT
printf 'UTC=%s\nRUN=%s\nMODE=%s\n' "$(date -u +%FT%TZ)" "$RUN" "$MODE"
command -v python3
"$PREFIX/bin/lean" --version
test "$(tr -d '\r\n' < "$SIDE/lean-toolchain")" = leanprover/lean4:v4.33.1
test "$(tr -d '\r\n' < "$CACHE/lean-toolchain")" = leanprover/lean4:v4.33.1
test "$(git -C "$CACHE/.lake/packages/mathlib" rev-parse HEAD)" = 0df444a360eaa60ab8c11dca51a86af692955474
test "$(git -C "$TOOLS/comparator" rev-parse HEAD)" = 575674928e239f5bc452aab72d1dd7b0f1326494
test "$(git -C "$TOOLS/nanoda" rev-parse HEAD)" = 68d5ca9db226849b41a6fff59d796ff19d0a8840
test "$(cat "$TOOLS/bin/landrun.commit")" = 811cfff51ceaf3d9843708aa6d22e9b84ccac8b4
export COMPARATOR_LANDRUN="$TOOLS/bin/landrun"
export COMPARATOR_NANODA="$TOOLS/nanoda/target/release/nanoda_bin"
export COMPARATOR_LEAN4EXPORT="${ROUTEB_LEAN4EXPORT:-$TOOLS/lean4export/.lake/build/bin/lean4export}"
COMPARATOR="$TOOLS/comparator/.lake/build/bin/comparator"
for BIN in "$COMPARATOR" "$COMPARATOR_LANDRUN" "$COMPARATOR_NANODA" "$COMPARATOR_LEAN4EXPORT"; do
  test -x "$BIN"
done
PROJECT="$RUN/project"
mkdir -p "$PROJECT/.lake/build/lib/lean" "$RUN/tmp"
export TMPDIR="$RUN/tmp"
FILES=(Challenge.lean Solution.lean DependencyAudit.lean RouteBSupplyCore.lean
       comparator.json lakefile.toml lean-toolchain verify_comparator.sh)
for FILE in "${FILES[@]}"; do cp -- "$SIDE/$FILE" "$PROJECT/$FILE"; done
(cd "$PROJECT" && sha256sum "${FILES[@]}") | tee "$RUN/inputs.sha256"
python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); d["name"]="routeBSupplyComparison"; print(json.dumps(d,indent=2))' \
  "$CACHE/lake-manifest.json" > "$PROJECT/lake-manifest.json"
ln -s "$CACHE/.lake/packages" "$PROJECT/.lake/packages"
sha256sum "$PROJECT/lake-manifest.json" "$CACHE/lake-manifest.json" | tee "$RUN/manifests.sha256"
while IFS=$'\t' read -r NAME REV; do
  ACTUAL=$(git -C "$CACHE/.lake/packages/$NAME" rev-parse HEAD)
  test "$ACTUAL" = "$REV"
  printf 'DEPENDENCY %s %s\n' "$NAME" "$ACTUAL"
done < <(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); [print(p["name"],p["rev"],sep="\t") for p in d["packages"] if p["type"]=="git"]' "$CACHE/lake-manifest.json")
if grep -nE '\b(sorry|admit|axiom|native_decide|implemented_by|unsafe)\b' \
    "$PROJECT/Challenge.lean" "$PROJECT/Solution.lean" "$PROJECT/RouteBSupplyCore.lean"; then
  printf 'Forbidden proof escape token\n'; exit 1
fi
python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); assert d["definition_names"]==[] and d["enable_nanoda"] is True; assert not (set(d["permitted_axioms"])-{"propext","Quot.sound","Classical.choice"})' "$PROJECT/comparator.json"
export LEAN_PATH="$PROJECT/.lake/build/lib/lean"
for PACKAGE in "$CACHE"/.lake/packages/*; do
  LIB="$PACKAGE/.lake/build/lib/lean"
  if test -d "$LIB"; then LEAN_PATH="$LEAN_PATH:$LIB"; fi
done
cd "$PROJECT"
for MODULE in RouteBSupplyCore Challenge Solution DependencyAudit; do
  printf 'CLEAN_COMPILE=%s\n' "$MODULE"
  "$PREFIX/bin/lean" -DwarningAsError=true --root="$PROJECT" \
    -o "$PROJECT/.lake/build/lib/lean/$MODULE.olean" "$MODULE.lean" \
    2>&1 | tee "$RUN/compile-$MODULE.log"
done
grep -qF 'ROUTEB_DEPENDENCY_AUDIT_OK' "$RUN/compile-DependencyAudit.log"
printf 'CLEAN_COMPILE_EXIT_CODE=0\n'
# Prepare normal Lake traces before the unmodified comparator enters landrun.
# On this WSL /mnt/c mount, landrun cannot remove direct-lean output files.
# Dependencies are the already populated cache; only local targets need building.
"$PREFIX/bin/lake" build Challenge Solution 2>&1 | tee "$RUN/lake-prebuild.log"
sha256sum "$COMPARATOR" "$COMPARATOR_LEAN4EXPORT" "$COMPARATOR_NANODA" \
  "$COMPARATOR_LANDRUN" "$PREFIX/bin/lean" | tee "$RUN/tools.sha256"
printf 'COMPARATOR_COMMAND=lake env %s comparator.json\n' "$COMPARATOR"
set +e
"$PREFIX/bin/lake" env "$COMPARATOR" comparator.json 2>&1 | tee "$RUN/comparator.log"
COMPARATOR_CODE=${PIPESTATUS[0]}
set -e
printf 'COMPARATOR_EXIT_CODE=%s\n' "$COMPARATOR_CODE"
(cd "$PROJECT" && sha256sum -c "$RUN/inputs.sha256") | tee "$RUN/input-stability.log"
sha256sum "$PROJECT"/.lake/build/lib/lean/{RouteBSupplyCore,Challenge,Solution,DependencyAudit}.olean \
  | tee "$RUN/compiled.sha256"
test "$COMPARATOR_CODE" -eq 0
grep -qxF 'Your solution is okay!' "$RUN/comparator.log"
grep -qxF 'nanoda kernel accepts the solution' "$RUN/comparator.log"
grep -qxF 'Lean default kernel accepts the solution' "$RUN/comparator.log"
printf 'COMPARATOR_ACCEPTED_NOT_REGISTERED\n'
