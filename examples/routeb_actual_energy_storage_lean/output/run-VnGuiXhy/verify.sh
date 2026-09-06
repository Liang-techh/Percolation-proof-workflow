#!/usr/bin/env bash
set -euo pipefail
SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
ROOT=$(cd -- "$SIDE/../.." && pwd -P)
CACHE=/home/z5242/sos_lean
LEAN=/home/z5242/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean
SIGNED="$ROOT/examples/routeb_signed_gap_lean/output/run-iH9FGdAL"
GRAVITY="$ROOT/examples/routeb_gravity_twist_floor/output/run-LIFMhESI"
REFERENCE="$ROOT/examples/routeb_coupled_linear_reference/output/run-20260905T192654Z-3dbe159f"
mkdir -p "$SIDE/output"
RUN=$(mktemp -d "$SIDE/output/run-XXXXXXXX")
printf 'ATTEMPT_DIRECTORY=%s\n' "$RUN"
set +e
(
  set -euo pipefail
  trap 'code=$?; printf "VERIFY_EXIT_CODE=%s\n" "$code"' EXIT
  printf 'START_UTC=%s\n' "$(date -u +%FT%TZ)"
  cp "$SIDE"/*.lean "$SIDE/verify.sh" "$RUN/"
  for DOC in README.md audit.py ATTEMPT_HISTORY.md; do
    if test -f "$SIDE/$DOC"; then cp "$SIDE/$DOC" "$RUN/"; fi
  done
  mkdir -p "$RUN/cache" "$RUN/inputs/signed" "$RUN/inputs/gravity" "$RUN/inputs/reference"
  cp "$SIGNED/cache"/*.olean "$SIGNED/SignedGap.olean" "$GRAVITY/GravityTwistFloor.olean" "$RUN/cache/"
  cp "$SIGNED/SignedGap.lean" "$SIGNED/terminal.log" "$SIGNED/before_run.sha256" "$RUN/inputs/signed/"
  cp -r "$SIGNED/inputs" "$RUN/inputs/signed/dependency_sources"
  cp "$GRAVITY/GravityTwistFloor.lean" "$GRAVITY/terminal.log" "$GRAVITY/before_run.sha256" "$RUN/inputs/gravity/"
  cp "$GRAVITY/inputs/routeB_fourier_potential_rational.csv" "$RUN/inputs/gravity/"
  cp "$REFERENCE/reference.json" "$REFERENCE/audit.py" "$REFERENCE/terminal.log" "$RUN/inputs/reference/"
  cp "$REFERENCE/inputs/routeB_fourier_mass_full_rational.csv" "$RUN/inputs/reference/"
  cp "$CACHE/lean-toolchain" "$CACHE/lake-manifest.json" "$RUN/inputs/"
  REV=$(git -C "$CACHE/.lake/packages/mathlib" rev-parse HEAD)
  printf 'MATHLIB_COMMIT=%s\n' "$REV"
  test "$REV" = 0df444a360eaa60ab8c11dca51a86af692955474
  "$LEAN" --version
  export LEAN_PATH="$RUN:$RUN/cache"
  for PACKAGE in "$CACHE"/.lake/packages/*; do
    LIB="$PACKAGE/.lake/build/lib/lean"
    if test -d "$LIB"; then LEAN_PATH="$LEAN_PATH:$LIB"; fi
  done
  printf 'LEAN_PATH=%s\n' "$LEAN_PATH"
  sha256sum "$LEAN" > "$RUN/compiler.sha256"
  find "$RUN" -type f ! -name terminal.log ! -name before_run.sha256 -print0 |
    sort -z | xargs -0 sha256sum > "$RUN/before_run.sha256"
  printf 'PRE_RUN_SNAPSHOTS_COMPLETE\n'
  if test -f "$RUN/audit.py"; then python3 -B "$RUN/audit.py" "$RUN"; fi
  if test "$#" -eq 0; then set -- ReferenceMass ActualStorage; fi
  for NAME in "$@"; do
    case "$NAME" in ReferenceMass|ActualStorage|StorageDerivative) ;; *) exit 2 ;; esac
    printf 'COMMAND=%s -DwarningAsError=true --root=%s -o %s/%s.olean %s/%s.lean\n' "$LEAN" "$RUN" "$RUN" "$NAME" "$RUN" "$NAME"
    set +e
    "$LEAN" -DwarningAsError=true --root="$RUN" -o "$RUN/$NAME.olean" "$RUN/$NAME.lean"
    CODE=$?
    set -e
    printf '%s_COMPILE_EXIT_CODE=%s\n' "$NAME" "$CODE"
    test "$CODE" -eq 0
    sha256sum "$RUN/$NAME.olean"
  done
  sha256sum --check --status "$RUN/before_run.sha256"
  printf 'SNAPSHOT_HASHES_UNCHANGED=true\nEND_UTC=%s\n' "$(date -u +%FT%TZ)"
) > "$RUN/terminal.log" 2>&1
CODE=$?
set -e
cat "$RUN/terminal.log"
exit "$CODE"
