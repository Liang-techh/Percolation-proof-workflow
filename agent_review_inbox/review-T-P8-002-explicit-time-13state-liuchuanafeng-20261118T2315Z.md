---
kind: review_result
review_id: review-T-P8-002-explicit-time-13state-liuchuanafeng-20261118T2315Z
task_id: T-P8-002
agent: 流川枫
source_agent: 流川枫
created_at: 2026-11-18T23:15:00Z
inspected_commit: f8c9cc9762274e9d811c557ce385862937a90587
status: DECISION_MEMO_PENDING
integration_status: pending
admission_label: architecture_only
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
flowpipe_coverage_claimed: false
---

# Decision memo: T-P8-002 explicit-time 13-state parent option vs 14-state ramp

## Inspected question
Compare a candidate explicit-time 13-state parent with the existing 14-state ramp parent (as referenced in related T-P8-003/T-P8-004 and ramp reconstruction sidecars), focusing on initial-domain, terminal statement, and minimal theorem signature differences. No source edits performed.

## Evidence boundary
- Task queue entry for T-P8-002 is open, no prior claim/review by this agent.
- Related completed leaves: T-P8-003 (freeze state contract, reviewed_pending) and T-P8-004 (explicit-time contract sidecar, reviewed_pending) already exist and bound a 13-state explicit-time interface with external parameter `c`, initial projection, and terminal-transfer assumptions.
- Existing ramp reconstruction appears under `examples/routeb_p8_ramp_reconstruction_sidecar/` (referenced in later T-P8-007/009). No new executable comparison, Lean compile, or source-hash re-verification was run in this inbox-only pass.
- Current main HEAD: f8c9cc9762274e9d811c557ce385862937a90587.

## Minimal theorem signature observation (architecture only)
The 14-state ramp parent encodes time as an explicit state component with ramp dynamics. A pure 13-state explicit-time parent would externalize time/`c` and require a separate terminal-transfer premise to recover the same end-point statement on [0,1]. Initial-domain projection and terminal statement must be restated; they are not identical without an additional interface lemma.

This is consistent with the already-integrated T-P8-004 sidecar boundary. No concrete counter-example or formal equivalence was derived here.

## Decision / recommendation
Keep the existing 14-state ramp parent as the current target until an explicit typed interface lemma equating the two formulations (including domain and terminal) is supplied and independently checked. Do not silently replace the target theorem.

The option remains open for a future focused sidecar, but this review does not promote it.

## Admission
- admission_label: architecture_only
- No source binding, no flowpipe coverage, no registry promotion, no formal certificate.
- Integration should treat this as documentation/DAG metadata only; status of T-P8-002 remains open/pending until stronger evidence arrives.

No files outside this review were modified.
