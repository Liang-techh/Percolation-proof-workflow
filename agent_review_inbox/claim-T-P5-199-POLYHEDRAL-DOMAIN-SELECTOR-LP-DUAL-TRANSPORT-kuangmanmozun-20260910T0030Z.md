---
kind: task_claim
task_id: T-P5-199-POLYHEDRAL-DOMAIN-SELECTOR-LP-DUAL-TRANSPORT
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
claimed_at: '2026-09-10T00:30:00Z'
lease_expires_at: '2026-09-10T01:30:00Z'
completed_at: '2026-09-10T00:30:00Z'
unique_valid_claim: true
replacement_for: none
derived_from: '[T-P5-197-WEIGHTED-RADIAL-CUBIC-ABSORPTION]'
status: completed
result_path: agent_review_inbox/review-T-P5-199-POLYHEDRAL-DOMAIN-SELECTOR-LP-DUAL-TRANSPORT-kuangmanmozun-20260910T0030Z.md
result_commit: 04872637e1d211b2e91bb7be8bce2894ba043624
companion_path: agent_review_inbox/companion-T-P5-199-POLYHEDRAL-DOMAIN-SELECTOR-LP-DUAL-TRANSPORT-kuangmanmozun-20260910T0030Z.md
companion_commit: 93a8dc0e4e0fdce422c0ffdf1169e55478857470
---
# Review Claim — polyhedral state-domain to selector radial-cap transport

## Scope
Close the polyhedral half of the domain-transport seam left explicitly open by T-P5-197. For a selector representation `e=V y`, `y>=0`, and an actual polyhedral state-domain description `A e<=d`, derive a root-free exact LP/Farkas certificate for `w^T y<=R` that never introduces an inverse of possibly non-injective `V`.

Prove the one-line dual certificate, characterize the recession/non-injective obstruction, and give a counterexample showing that a bounded state polytope does not by itself bound selector coefficients. Provide a finite rational checker-facing theorem statement suitable for feeding the T-P5-197 radial-cap premise.

## Non-overlap
Do not redo T-P5-197 cubic absorption, T-P5-198 quadratic/ellipsoidal cap reduction, source provenance/admission, actual-domain extraction, Float64 enclosure, Lean/kernel verification, or independent audit. Do not claim any concrete physical polytope exists unless separately supplied by the source/domain lane.
