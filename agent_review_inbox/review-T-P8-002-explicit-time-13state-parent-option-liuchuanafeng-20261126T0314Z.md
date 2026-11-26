---
kind: review_result
review_id: review-T-P8-002-explicit-time-13state-parent-option-liuchuanafeng-20261126T0314Z
source_agent: 流川枫
agent: 流川枫
task_id: T-P8-002
claim_id: claim-T-P8-002-liuchuanafeng-20261126T011700Z
created_at: 2026-11-26T03:14:00Z
inspected_commit: f03e44c55265b595e5d1c95170e862b483f1ac96
admission_label: architecture_only
status: completed
boundary: decision memo only; no source edits, no flowpipe claims, no registry/state/formal-proof changes
---

# Review result: T-P8-002 — explicit-time 13-state parent option

## Question / bottleneck inspected
Compare a candidate explicit-time 13-state parent option against the existing 14-state ramp parent at the statement / initial-domain / terminal level only. Deliver a decision memo and minimal theorem signature. No source edits.

## Evidence collected
- Task definition from `agent_review_inbox/task_queue.md` (status still `open` at inspected commit f03e44c).
- Existing claim files by 流川枫 for this task_id, including the unmatched claim at 20261126T011700Z.
- Concrete sidecar: `examples/routeb_p8_explicit_time_sidecar/README.md` and `RouteBP8ExplicitTimeSidecar.lean` (present at current main).
- 14-state ramp context referenced via imported `RouteBP8PicardStep` and prior interval-ramp leaves (Fin 14 with w and c slots).
- Prior reviews by this agent (e.g. 20261124T1727Z architecture_only) remain consistent; no intervening material closes the leaf into verified.

## Decision memo
The explicit-time 13-state sidecar is a clean interface reduction of the 14-state ramp parent:

- State vector reduced to Fin 13 → ℝ with order q₁…q₆, dq₁…dq₆, w; parameter c kept external.
- Initial domain: projection via `forgetTail13` from FullX0 (mechanical energy ≤ 9/400, w=0, c^{2} ≤ 3) yields `explicitInitial13`.
- Terminal statement: rewritten as `y wSlot13 = c` (slot 12), matching the 14-state terminal transfer through the external c.
- Minimal theorems already present: `explicitInitial13_of_fullX0`, `initialProjection13_from_fullX0`, `explicitTerminal13_transfer`, `explicitTerminal13_lift`, and the packaging `explicitTimeContract_assumptions`.

These changes are local, preserve the parent contract boundary, and do not alter the authoritative RouteBP8PicardStep target. No silent change to the target theorem is introduced.

## Minimal theorem signature (frozen)
```lean
theorem explicitInitial13_of_fullX0 (z : State14) (hz : FullX0 z) : initialProjection13 z
theorem explicitTerminal13_transfer (y : State13) (c : ℝ) : explicitTerminal13 y c ↔ y wSlot13 = c
```

## Admission
`architecture_only`. The interface and projection/terminal rewrite are explicit and source-independent. No flowpipe coverage, ODE existence, source binding, interval enclosure, or registry promotion is claimed or evidenced in this audit. Physical gates remain open. The leaf may stay pending for later source-authenticated children.

## Forbidden boundaries respected
No source edits, no registry/state/formal-proof mutation, no flowpipe claim, no target theorem change.
