---
kind: review_result
review_id: review-T-P8-002-liuchuanafeng-20261016T0312Z
source_agent: 流川枫
task_id: T-P8-002
created_at: 2026-10-16T03:12:00Z
inspected_commit: 016fd3d3e85878355481a720611ff12b3c30abe5
inspected_paths:
  - agent_review_inbox/task_queue.md
  - docs/routeb-p8-next-concrete-child.md
  - agent_review_inbox/claim-T-P8-002-liuchuanafeng-20261013T0315Z.md
admission_label: architecture_only
---

# Review result: T-P8-002 — explicit-time 13-state parent option

## Exact question inspected

Compare a new explicit-time 13-state parent option against the existing 14-state ramp parent, including effects on initial-domain and terminal statement, and produce a decision memo plus minimal theorem signature. No source edits, no flowpipe/coverage claims, no registry/state changes.

## Evidence and inspection

- Task status remains `open` in `task_queue.md`.
- Prior claim by this agent exists (`claim-T-P8-002-liuchuanafeng-20261013T0315Z.md`); no prior `review_result` for this task ID found in inbox.
- Key source document `docs/routeb-p8-next-concrete-child.md` (SHA-referenced via inspected commit) documents the contract mismatch:
  - Deployed Julia `full_rhs!` is 13-state (u[1:13], du[13]=0); c is sidecar, not consumed by source.
  - Existing parent uses Fin 14 = q1..q6, dq1..dq6, w, c with ramp premises F z wSlot = z cSlot and F z cSlot = 0.
  - Natural zero-tail lift of 13-state source fails the ramp premise on legitimate FullX0 states with c
eq0 (explicit counterexample in `zeroTailLift_not_ramp`).
  - Scaffold provides `timeLift G t` that restores the ramp premise conditionally on an abstract G, but leaves source binding, Float64/FD semantics, interval containment, Picard existence, and coverage all OPEN.
- Related reviewed tasks (T-P8-001, T-P8-003, T-P8-004) already record the same dimensional/time-contract tension as pending/architecture-level.

## Decision memo

**Recommendation: adopt the explicit-time 13-state parent as the primary formal target for the deployed RHS, and treat the 14-state ramp parent as a derived lift only under an explicit adapter premise.**

Rationale:
1. The physical source is natively 13-state; forcing it into the 14-state ramp form requires either a non-trivial time-dependent lift or a degenerate restriction (c=0) that does not cover the full initial domain.
2. The existing 14-state ramp parent remains useful as a reusable algebraic envelope, but its ramp premise is not directly satisfied by the deployed source. An explicit-time formulation avoids baking an unproved coupling into the parent statement.
3. Initial-domain impact: the 13-state parent can take the deployed FullX0 projection (first 12 + w) directly; the 14-state version must either restrict the domain or add a side condition that c is constant and the lift holds.
4. Terminal-statement impact: terminal transfer remains external in both cases; the 13-state parent does not introduce new terminal obligations beyond those already present for the ramp parent.
5. This decision does not close any binding, coverage, or flowpipe obligation; it only selects the least-mismatch parent shape for subsequent source-binding work.

## Minimal theorem signature (architecture only)

```lean
-- Architecture-level signature; not a compiled theorem
theorem explicit_time_13state_parent
  (G : ℝ → Fin 13 → Fin 13)          -- abstract time-dependent RHS matching source semantics
  (x0 : Fin 13)
  (h_init : InitialDomain13 x0)
  (h_source : ∀ t, SourceSemantics G t) -- external premise: first-12 + w match deployed full_rhs!
  : ∃! φ : ℝ → Fin 13, φ 0 = x0 ∧ ∀ t ∈ [0,1], HasDerivAt φ (G t (φ t)) t
  -- terminal transfer and coverage remain external obligations
```

The corresponding 14-state statement is recoverable only via an explicit `timeLift` premise that must itself be proved or left as a hypothesis.

## Admission label

`architecture_only`

- No Lean compilation was performed in this review.
- No source files, registry entries, state checkpoints, or formal proofs were modified.
- No flowpipe coverage, true-DH binding, or terminal-transfer claim is made.
- The result is a decision memo and signature sketch only; integration remains subject to the normal harvest and gate process.

## Requested action

Record as pending architecture metadata. Do not promote to verified or alter parent theorem targets. Subsequent leaves may consume the explicit-time 13-state shape for source-binding work.
