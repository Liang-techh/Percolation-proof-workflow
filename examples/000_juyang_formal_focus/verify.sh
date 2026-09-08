#!/usr/bin/env bash
# CI_PORTABLE=1
# Focused early lane: surface owned compile results before unrelated shared lanes.
# The 000 prefix is intentional because the shared workflow sorts verify paths.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

bash "$ROOT/../routeb_p5_initial_reference_bridge_lean/verify.sh"
bash "$ROOT/../routeb_p5_invariant_path_sheet_lean/verify.sh"
bash "$ROOT/../routeb_p5_target_domain_obstruction_lean/verify.sh"

echo "JUYANG_OWNED_FOCUSED_CHECK=PASS"
