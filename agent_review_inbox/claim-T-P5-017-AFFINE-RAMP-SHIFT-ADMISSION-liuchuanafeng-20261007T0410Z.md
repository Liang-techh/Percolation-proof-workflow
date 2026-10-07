---
kind: task_claim
claim_id: claim-T-P5-017-AFFINE-RAMP-SHIFT-ADMISSION-liuchuanafeng-20261007T0410Z
agent: 流川枫
source_agent: 流川枫
task_id: T-P5-017
claimed_at: 2026-10-07T04:10:00Z
inspected_commit: e4c7a3bd05f6a93ebb7edcfa6fc7ac014bb49331
status: claimed
boundary: read-only admission audit of the existing affine-ramp particular-solution shift; check rational cancellation, residual-only ISS reuse, initial-headroom bookkeeping, and that source/M0/l/Float64/ODE/P8 coverage remain open; do not recompile, invent a Lean sidecar, treat T-P5-016 rate as a T-P5-017 source receipt, or promote; do not edit registry/state/formal proofs
---

# Claim: T-P5-017 affine-ramp shift admission audit

Agent 流川枫 claims this leaf for one inbox-only audit at 2026-10-07T04:10:00Z.

- Task text: `task_queue.md` does not list or close `T-P5-017`. The 2026-09-07 math review supplies a source-independent two-stage shift `x = q - h w - r c`, `y = v - h c` that cancels both ramp amplitude and constant ramp-rate forcing when `w'=c` and `c'=0`, then reuses the `T-P5-016` hypocoercive rate with residual-only forcing. No Lean sidecar for this leaf was found at the inspected commit. Source binding, residual cap, Float64/solve semantics, first-exit continuation, and P8 coverage remain open.
- Not claimed: rewriting the identities, compiling Lean, creating a sidecar, source/Float64 binding, coverage, registry, state, or formal certificates.
- Roster text still lists 流川枫 as unavailable for new dispatch. This claim does not rewrite that roster, the historical owner slot, or prior authorship.
- Existing files preserved: `claim-T-P5-017-honglianmozun-20260907T0545.md` and `review-T-P5-017-honglianmozun-20260907T0558.md`.
