---
kind: review_result
review_id: review-T-P8-002-explicit-time-13state-parent-option-liuchuanafeng-20261128T0215Z
source_agent: 流川枫
created_at: 2026-11-28T02:16:00Z
inspected_commit: 7e0299e129be647dcd18e970709f726fe2ab42c2
inspected_paths:
  - docs/routeb-p8-flowpipe-binding-next.md
  - docs/routeb-p8-next-concrete-child.md
  - examples/routeb_p8_picard_step_lean/RouteBP8PicardStep.lean
  - examples/routeb_p8_contract_adapter/P8ContractAdapter.lean
task_id: T-P8-002
admission_label: architecture_only
proposed_integration: documentation-only decision memo; no DAG/registry/state change
---

# Review result: T-P8-002 — explicit-time 13-state parent option

## Question / bottleneck inspected
Compare a new explicit-time 13-state parent with the existing 14-state ramp parent (`RouteBP8PicardStep`), including initial-domain and terminal statement changes. Produce a decision memo and minimal theorem signature. No source edits.

## Evidence
- Current main commit `7e0299e129be647dcd18e970709f726fe2ab42c2`.
- `docs/routeb-p8-flowpipe-binding-next.md` (SHA of content inspected via get_file): documents that the deployed Julia `full_rhs!` is 13-state with `du[13]=0` (constant-`w`), while the Lean parent requires `Fin 14` and `RampRhsPremise` (`F z wSlot = z cSlot`, `F z cSlot = 0`). Natural lift of the 13-state source contradicts the ramp premise on nonzero-`c` states in `FullX0` (e.g., `c=1`). Source hashes and coordinate map confirm the mismatch. Status remains OPEN for source_binding / ramp_binding.
- `docs/routeb-p8-next-concrete-child.md`: records the negative fact `zeroTailLift_not_ramp` (CLOSED) and the conditional `timeLift_rampPremise` (COMPILED / conditional_interface_only). Explicitly states that the adapter does not discharge S1 (exact source-to-G first-12 semantic binding). Admission: source_binding=OPEN, ramp_binding=OPEN for deployed 13-state source, formal_certificate_allowed=false, registry unchanged.
- Existing Lean artifacts (`RouteBP8PicardStep.lean`, `P8ContractAdapter.lean`) confirm the 14-state ramp contract and the negative lift fact. No new source or theorem was constructed in this review.

## Decision memo
**Decision: do not silently replace the existing 14-state ramp parent; keep it as the current formal target and treat the explicit-time 13-state option as a separate, still-open alternative parent that requires its own contract.**

Reasons:
1. The deployed true-DH RHS is 13-state with constant-`w` (`du[13]=0`). Instantiating the existing `RampRhsPremise` on a natural lift is impossible for the full `FullX0` family (`c^{2}≤3`).
2. Changing the parent in-place would alter the target theorem statement (initial-domain, terminal transfer, and ramp dynamics), which is forbidden.
3. The existing `timeLift` scaffold shows how an abstract time-dependent 13-state field can be lifted to satisfy the ramp premise, but it does not bind the real Julia source body, Float64/FD/solve semantics, or any coverage. It remains conditional_interface_only.
4. Therefore the explicit-time 13-state parent is a valid design alternative, but it is not yet a drop-in replacement. It requires:
   - a new parent signature that makes time explicit,
   - a precise statement of initial domain and terminal condition compatible with `w(t)=c*t`,
   - and an independent source-binding obligation (S1) that is currently OPEN.

**Minimal theorem signature (architecture_only, not formalized here):**

```text
theorem explicit_time_13state_parent
  (G : ℝ → State13 → State13)          -- time-dependent first-12 field
  (hG : ∀ t, Continuous (G t) ∧ …)      -- regularity assumptions
  (x0 : State13)
  (c0 : ℝ)
  (h0 : FullX0_13 x0 c0)              -- initial energy + c^{2}≤3
  (sol : ∀ t ∈ [0,1], IsSolution (timeLift G) sol t)
  : ∀ t ∈ [0,1],
      sol t ∈ certified_tube t ∧
      sol t wSlot = c0 * t ∧
      sol t cSlot = c0
```

(The signature is illustrative only; exact Lean formulation, source binding of `G` to the deployed `full_rhs!`, interval enclosure, and coverage remain open.)

## Admission label and boundary
- **admission_label: `architecture_only`**
- No source files, state, registry, or formal proofs were edited.
- No claim of flowpipe coverage, source equality, or parent closure.
- The result does not promote any theorem to verified and does not close T-P8-002; the task remains open pending a concrete source-bound parent or an explicit user decision to change the target statement.

## Proposed next action
Coordinator may record this decision memo as documentation-only. Next high-value leaf remains the source-side first-12 semantic binding (S1) for either the existing ramp path or a newly declared explicit-time parent. Do not treat this review as proof progress.
