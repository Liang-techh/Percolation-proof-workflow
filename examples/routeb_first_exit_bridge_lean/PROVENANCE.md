# Provenance and evidence boundary

Prepared on 2026-09-06 from read-only inspection of:

- `docs/routeb-block45-proof-sketch.md`, especially the P8 statement and the
  requirement to close domain containment and continuation by first exit;
- `docs/routeb-target-contract-extraction.md`, for `T=1`, the full 12-state
  radius-`0.15` initial set, ramp input, and the warning that skipped simulation
  failures/out-of-limit trajectories are not domain proof;
- `artifacts/task_EV_flowpipe_continuation_gap_20260907/gap.json`, for the
  explicit attainment, exit-contradiction, source-domain, ODE, and provenance
  gaps;
- `artifacts/routeb_agent_entry_flowpipe_next_20260906T092401Z/REPORT.md`, for
  the narrow P8 probe boundary: 35 reachsets, `T=0.001`, radius `0.001`,
  constant interval disturbance, and `coverage_complete=false`.

The Lean theorem is artifact-local logical infrastructure only. None of those
documents is imported as a Lean axiom, and no numerical statement from them is
promoted to a theorem. A future concrete adapter must instantiate every premise
of `p8_firstExit_domain_continuation_assembly` and separately bind the exact
Route-B vector field, domain, initial set, ramp input, and horizon.
