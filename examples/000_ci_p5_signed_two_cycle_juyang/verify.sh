#!/usr/bin/env bash
# CI_PORTABLE=1
# Focused replay only; branch-local wrapper, not intended for main integration.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
echo "FOCUSED_REPLAY_OWNER=巨阳仙尊"
echo "FOCUSED_REPLAY_TARGET=examples/routeb_p5_signed_two_cycle_lean/verify.sh"
CI_PORTABLE=1 bash "$ROOT/examples/routeb_p5_signed_two_cycle_lean/verify.sh"
