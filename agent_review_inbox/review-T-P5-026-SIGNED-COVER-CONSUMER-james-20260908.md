---
kind: review_result
review_id: review-T-P5-026-SIGNED-COVER-CONSUMER-james-20260908
task_id: T-P5-026-SIGNED-COVER-CONSUMER
source_agent: James the 6th
created_at: 2026-09-08T12:03:49-06:00
status: ARCHITECTURE_ONLY
integration_status: pending
admission_label: architecture_only
candidate_path: examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_CONE_INDEX_SignedCoverConsumer.lean
candidate_sha256: pending
requested_action: retain signed cover and explicit evenness gate as generic P5 interface; do not promote concrete SPN or source coverage
---

# P5 signed-cover consumer — architecture-only review

The new generic Lean consumer defines an oriented chart with an explicit Bool
sign and proves the exact cover equivalence over both orientations. It removes
the sign quantifier only under the explicit premise `P (-z) ↔ P z`; the
non-even counterexample prevents silently treating state membership as sign
invariant. The intended concrete mapping is the existing ConeIndex
`Representative × Orthant` chart, but this file is intentionally generic and
does not authenticate a concrete `K_path`, source model, or Route-B coverage.

The existing core's `cover_multiplicity` remains authoritative: at the origin
all 36 labels remain, and the consumer must not replace the multiplicity sum
with a fixed-state sign-invariance shortcut. The sidecar is therefore useful
as a typed theorem-decomposition/interface pattern, but it is architecture-only
for Route-B until a pinned receipt and concrete source binding exist.

No StateStore, registry, parent closure, or admission flag was changed by the
agent. The candidate and companion review remain separate from concrete P5
SPN evidence.
