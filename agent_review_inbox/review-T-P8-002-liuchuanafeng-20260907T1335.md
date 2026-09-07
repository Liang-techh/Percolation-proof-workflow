---
kind: review_result
review_id: T-P8-002-LIUCHUANAFENG-20260907T1335
task_id: T-P8-002
source_agent: 流川枫
created_at: 2026-09-07T13:35:00-06:00
integration_status: pending
admission_label: architecture_only
---

# T-P8-002 Decision memo: explicit-time 13-state parent option

## Exact question

Compare a new explicit-time 13-state parent with the existing 14-state ramp parent (including initial-domain and terminal statement changes). Deliver a decision memo and minimal theorem signature only. No source edits. Do not claim flowpipe coverage.

## Inspected commit / paths

- Commit: `fe954e09ba082c742a5299b2373e813b8653c513`
- `docs/routeb-p8-flowpipe-binding-next.md`
- `docs/routeb-p8-next-concrete-child.md`
- `agent_review_inbox/task_queue.md` (T-P8-002 entry)
- Existing analysis of `RouteBP8PicardStep`, `P8RhsReceipt`, `P8ContractAdapter`, and declared Julia source contract (13-state `full_rhs!` with `du[13]=0`)

## Evidence summary (from existing audits)

1. **14-state ramp parent contract** (`RouteBP8PicardStep`):
   - State: `Fin 14 = q1..q6, dq1..dq6, w, c`
   - `RampRhsPremise F` requires for all `z`:
     - `F z wSlot = z cSlot`
     - `F z cSlot = 0`
   - This encodes continuous ramp dynamics `w' = c`, `c' = 0`.

2. **Deployed source is 13-state**:
   - Julia `full_rhs!` consumes `u[1:13]` and writes `du[13] = 0` (constant `w`).
   - No `c` state; ReachabilityAnalysis problem is `dim:13`.
   - Natural zero-tail lift of the 13-state source to 14-state **contradicts** `RampRhsPremise` on the full `FullX0` family (counterexample: `c=1`, all else 0 yields `F wSlot = 0 ≠ 1`). Only the degenerate `c=0` subfamily survives.

3. **Existing adapter scaffold** (`P8ContractAdapter`):
   - `zeroTailLift_not_ramp` records the negative fact (compiled).
   - `timeLift G t` shows how an abstract time-dependent 13-state field can be lifted to satisfy the 14-state ramp premise **conditionally**; it does **not** bind the real Julia RHS, Float64/FD/solve semantics, interval containment, or coverage.

4. **Receipt / coverage status remains open**:
   - Dynamic endpoints in the receipt template are still pending/null for the mechanical coordinates.
   - No true-DH flowpipe or registry promotion is justified by the current conditional interface.

## Decision

**Recommend option 2: introduce an explicit-time 13-state parent** rather than forcing a 14-state ramp source that the deployed RHS does not provide.

### Rationale

- Preserves fidelity to the audited true-DH source (`du[13]=0`, no `c` state).
- Avoids inventing a continuous ramp ODE that is not present in the deployed probe.
- Moves the mismatch from an unsatisfiable premise into an explicit, auditable parent redesign (time appears in the statement, `w(t) = c₀ · t` or equivalent explicit formula).
- Keeps the existing 14-state ramp parent available for any future genuine 14-state ramp source; does not silently rewrite it.

### Rejected alternative (force 14-state ramp source)

- Would require rewriting or extending the Julia RHS and all provenance hashes.
- Risks silent semantic drift between “deployed constant-w probe” and “proof-only ramp ODE”.
- Out of scope for this task (no source edits).

## Minimal theorem signature (proposed)

```lean
/-- Explicit-time 13-state parent (decision-level signature only).
    State13 := Fin 13  -- q1..q6, dq1..dq6, w
    No continuous `c` state; ramp parameter `c₀` is a constant parameter
    of the initial-domain / theorem statement. --/
theorem routeB_p8_explicit_time_13_parent
    (c₀ : ℝ) (hc : c₀^2 ≤ 3)
    (F13 : ℝ → State13 → State13)  -- time-dependent RHS
    (hF_w : ∀ t z, (F13 t z).w = 0)  -- constant-w source fact
    (hbind : ExactSourceBinding F13 …)  -- placeholder for true-DH / FD / solve binding
    (hbox : OutwardIntervalEnclosure …)
    : ∀ x0 ∈ FullX0_13 (c₀), ∀ t ∈ Icc 0 1,
        trajectory F13 x0 t ∈ certified_tube (c₀) t := by
  sorry  -- signature only; not a proof
```

Notes on the signature:

- Initial domain carries the constant ramp slope `c₀` with `c₀² ≤ 3` (same numeric bound as the old `c` coordinate).
- Terminal / tube statements must be rewritten to be parameterized by `c₀` and explicit time; they cannot assume a free evolving `c(t)` state.
- `hbind` is intentionally left as an open obligation; this review does **not** discharge source binding, interval containment, Picard existence, or coverage.

## Admission label

`architecture_only`

- No Lean compile of a new parent was performed in this review.
- No source, state.json, registry, or formal_certificate_allowed change is authorized.
- The decision memo and signature are planning/architecture evidence only.

## Proposed integration

1. Record this review as the authoritative decision for `T-P8-002`.
2. Keep the existing 14-state ramp parent and `P8ContractAdapter` unchanged for historical/conditional use.
3. Next concrete work (out of scope here): design the exact `FullX0_13` and tube statements, then bind the first-12 components of the deployed `full_rhs!` (S1 in the existing child chain).
4. Do not promote any flowpipe or registry entry from this memo.

## Unresolved / next blockers

1. Exact source-to-`F13` semantic binding for the first 12 components (DH, FD, regularizer, solve).
2. Outward interval containment and Picard/local flowpipe existence for the 13-state field.
3. Partition continuation and `[0,1]` coverage under the explicit-time formulation.
4. Terminal-transfer comparison still depends on residual/energy budgets downstream of any flowpipe result.

## Response / handoff

流川枫 claimed the open task `T-P8-002`, inspected the existing P8 contract documentation and adapter analysis, and produced the decision memo above. Recommendation: adopt an explicit-time 13-state parent that matches the deployed constant-w source; retain the 14-state ramp parent only for future genuine ramp sources. No proof or coverage claim is made.
