---
kind: review_result
review_id: review-T-P8-002-explicit-time-13state-parent-option-liuchuanafeng-20261124T1727Z
source_agent: 流川枫
created_at: 2026-11-24T17:27:00Z
inspected_commit: a02939a848f54c8cecd211c6c8c89226e22c05e4
task_id: T-P8-002
admission_label: architecture_only
---

# Review: T-P8-002 — explicit-time 13-state parent option

## Question / bottleneck

Compare a new explicit-time 13-state parent with the existing 14-state ramp parent, including initial-domain and terminal statement changes. Produce a decision memo and minimal theorem signature. No source edits.

## Evidence inspected

- `task_queue.md` entry for T-P8-002 (status open).
- `examples/routeb_p8_explicit_time_sidecar/README.md` and `RouteBP8ExplicitTimeSidecar.lean` (commit a02939a848f54c8cecd211c6c8c89226e22c05e4).
- `examples/routeb_p8_interval_ramp_lean/README.md` (14-state ramp context, Fin 14 with slots for w and c).
- Prior claims by this agent exist but no closing review_result observed in the listed inbox snapshot.

## Decision memo

The explicit-time 13-state sidecar is a clean interface reduction of the 14-state ramp parent:

- State vector reduced to Fin 13 	o ℝ with order q₁…q₆, dq₁…dq₆, w; parameter c kept external.
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
