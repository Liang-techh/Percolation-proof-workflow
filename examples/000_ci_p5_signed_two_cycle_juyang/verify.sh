#!/usr/bin/env bash
# CI_PORTABLE=1
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
echo "FOCUSED_REPLAY_OWNER=巨阳仙尊"
CI_PORTABLE=1 bash "$ROOT/examples/routeb_p5_signed_two_cycle_lean/verify.sh"
