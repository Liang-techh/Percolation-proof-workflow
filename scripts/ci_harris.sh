#!/usr/bin/env bash
# Run on Linux with elan, Python >= 3.11, git, Go, Cargo and jq available.
# Invoke with bash; no executable-bit assumption is needed on Windows checkouts.
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
# The checked-in upstream directory is a read-only research reference and may
# intentionally contain local audit edits.  CI defaults to it for provenance,
# but accepts an explicit clean clone/worktree for an uncompromised fixture.
UPSTREAM="${FORMAL_MATH_ROOT:-$ROOT/upstream/formal-math}"
PERCOLATION="$UPSTREAM/percolation"
MINIMAL="$ROOT/examples/minimal_lean"
HARRIS="$ROOT/examples/harris_replay"
LOCAL_FKG="$ROOT/examples/local_fkg"
FORMAL_MATH_COMMIT=795efb86f191735c5481675763537cfb4ff37e55
PERCOLATION_TOOLCHAIN=leanprover/lean4:v4.32.0
CI_LOG_DIR="${RUNNER_TEMP:-${TMPDIR:-/tmp}}/workflow-ci-logs"

die() { printf 'error: %s\n' "$*" >&2; exit 1; }
[[ "$(uname -s)" == Linux ]] || die 'the upstream landrun verifier requires Linux'
for tool in elan lake lean python3 git go cargo jq; do
  command -v "$tool" >/dev/null 2>&1 || die "$tool is required"
done
[[ -d "$UPSTREAM/.git" || -f "$UPSTREAM/.git" ]] \
  || die 'check out anthropics/formal-math at the pinned commit into upstream/formal-math first'
[[ "$(git -C "$UPSTREAM" rev-parse HEAD)" == "$FORMAL_MATH_COMMIT" ]] \
  || die "formal-math must be at $FORMAL_MATH_COMMIT"
git -C "$UPSTREAM" diff --quiet HEAD -- percolation .github/scripts/comparator-check.sh \
  || die 'tracked upstream fixture or comparator files were modified'
[[ -f "$PERCOLATION/Challenge.lean" ]] || die 'missing unittest statement fixture'
[[ -f "$UPSTREAM/.github/scripts/comparator-check.sh" ]] || die 'missing upstream verifier'

# Read the actual minimal fixture version (currently 4.33.1); do not force it
# onto the older percolation toolchain or rewrite any fixture source files.
minimal_toolchain="$(tr -d '[:space:]' < "$MINIMAL/lean-toolchain")"
[[ -n "$minimal_toolchain" ]] || die 'empty minimal fixture toolchain'
for project in "$PERCOLATION" "$HARRIS" "$LOCAL_FKG"; do
  [[ "$(tr -d '[:space:]' < "$project/lean-toolchain")" == "$PERCOLATION_TOOLCHAIN" ]] \
    || die "$project must use $PERCOLATION_TOOLCHAIN"
done
# Let each project (including comparator's own project) select its toolchain.
unset ELAN_TOOLCHAIN
elan toolchain install "$minimal_toolchain"
elan toolchain install "$PERCOLATION_TOOLCHAIN"
mkdir -p "$CI_LOG_DIR"
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"

cd "$ROOT"
python3 -m unittest discover -s tests -v 2>&1 | tee "$CI_LOG_DIR/unittest.log"

# Exercise durable recovery boundaries in the same pinned CI environment.
# These fixtures intentionally make no proof claim; they verify that stale
# evidence, worker death, host-agent expiry, and coordinator interruption are
# never promoted as successful theorems.
python3 scripts/test_stale_artifact_invalidation.py 2>&1 \
  | tee "$CI_LOG_DIR/stale-artifact-invalidation.log"
python3 scripts/test_host_recovery.py --output "$CI_LOG_DIR/host-recovery.json" 2>&1 \
  | tee "$CI_LOG_DIR/host-recovery.log"
python3 scripts/test_compile_process_recovery.py 2>&1 \
  | tee "$CI_LOG_DIR/compile-process-recovery.log"
python3 scripts/test_coordinator_crash_recovery.py 2>&1 \
  | tee "$CI_LOG_DIR/coordinator-crash-recovery.log"
python3 scripts/test_prove2me_transport.py 2>&1 \
  | tee "$CI_LOG_DIR/prove2me-transport.log"

# Populate the pinned mathlib path required by Harris's existing lakefile and
# manifest. Do not run lake update: keep the checked-in dependency revisions.
cd "$PERCOLATION"
if [[ "${SKIP_PERCOLATION_CACHE_GET:-0}" == 1 ]]; then
  printf 'skipped percolation cache getter; using the existing pinned mathlib cache\n' \
    | tee "$CI_LOG_DIR/percolation-cache.log"
else
  lake exe cache get 2>&1 | tee "$CI_LOG_DIR/percolation-cache.log"
fi
[[ -f "$PERCOLATION/.lake/packages/mathlib/lakefile.lean" ]] \
  || die 'percolation did not populate the Harris mathlib path dependency'

cd "$HARRIS"
# Fetch Harris's inherited manifest dependencies and their compiled cache too.
if [[ "${SKIP_INHERITED_CACHE_GET:-0}" == 1 ]]; then
  printf 'skipped inherited cache getter; using the existing pinned mathlib cache\n' \
    | tee "$CI_LOG_DIR/harris-cache.log"
else
  lake exe cache get 2>&1 | tee "$CI_LOG_DIR/harris-cache.log"
fi
# Baseline is deliberately failing and must never be a build target.
lake build Challenge Solution HarrisReplay 2>&1 | tee "$CI_LOG_DIR/harris-build.log"

export COMPARATOR_COMMIT=575674928e239f5bc452aab72d1dd7b0f1326494
export NANODA_COMMIT=68d5ca9db226849b41a6fff59d796ff19d0a8840
export LANDRUN_COMMIT=811cfff51ceaf3d9843708aa6d22e9b84ccac8b4
# Resolve lean4export from this project's release, as required by upstream.
unset LEAN4EXPORT_COMMIT
export LOG_DIR="$CI_LOG_DIR/comparator"
# Upstream forces enable_nanoda=true and requires exit zero plus the exact
# acceptance line for every configuration; no local comparator substitute.
bash "$UPSTREAM/.github/scripts/comparator-check.sh" 2>&1 | tee "$CI_LOG_DIR/comparator-check.log"

# Run the fresh local-FKG target through the same upstream comparator surface. The
# stateful agent/registry run is recorded separately; CI checks the reproducible
# final source bundle and never treats Challenge placeholders as proofs.
cd "$LOCAL_FKG"
lake build LocalFKGChallenge LocalFKGDefinitions LocalFKGObligations LocalFKGReduction \
  LocalFKGFinite LocalFKGMarginal LocalFKGSolutionAgent 2>&1 | tee "$CI_LOG_DIR/local-fkg-build.log"
export LOG_DIR="$CI_LOG_DIR/local-fkg-comparator"
bash "$UPSTREAM/.github/scripts/comparator-check.sh" 2>&1 | tee "$CI_LOG_DIR/local-fkg-comparator-check.log"
