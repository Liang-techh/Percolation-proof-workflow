#!/usr/bin/env bash
set -euo pipefail

SIDE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
ROOT=$(cd -- "$SIDE/../.." && pwd -P)
LEAN=${LEAN:-/home/z5242/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean}

mkdir -p "$SIDE/output"
RUN=$(mktemp -d "$SIDE/output/run-XXXXXXXX")
cp "$SIDE/RouteBP3SemanticBindingSidecar.lean" "$SIDE/README.md" "$SIDE/verify.sh" "$RUN/"

set +e
"$LEAN" --version > "$RUN/lean-version.log" 2>&1
LEAN_VERSION_EXIT=$?
set -e

if [ "$LEAN_VERSION_EXIT" -ne 0 ]; then
  {
    echo "VERIFY_STATUS=blocked"
    echo "BLOCKED_REASON=Lean toolchain unavailable or not executable"
    echo "LEAN_VERSION_EXIT_CODE=$LEAN_VERSION_EXIT"
    cat "$RUN/lean-version.log"
  } > "$RUN/verify.log"
  cat "$RUN/verify.log"
  exit 1
fi

set +e
"$LEAN" -DwarningAsError=true --root="$RUN" -o "$RUN/RouteBP3SemanticBindingSidecar.olean" "$RUN/RouteBP3SemanticBindingSidecar.lean" \
  > "$RUN/lean-compile.log" 2>&1
COMPILE_EXIT=$?
set -e

{
  echo "VERIFY_STATUS=$([ "$COMPILE_EXIT" -eq 0 ] && echo passed || echo blocked)"
  echo "LEAN_COMPILE_EXIT_CODE=$COMPILE_EXIT"
  if [ "$COMPILE_EXIT" -ne 0 ]; then
    echo "BLOCKED_REASON=Lean compile failed"
  fi
  cat "$RUN/lean-compile.log"
  if grep -nE '(^|[^[:alnum:]_])(sorry|admit)([^[:alnum:]_]|$)|^[[:space:]]*axiom[[:space:]]' "$RUN/RouteBP3SemanticBindingSidecar.lean"; then
    echo "RESTRICTION_CHECK=FAILED"
    exit 1
  fi
  echo "RESTRICTION_CHECK=PASSED"
} > "$RUN/verify.log"

cat "$RUN/verify.log"
exit "$COMPILE_EXIT"
