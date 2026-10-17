---
kind: review_result
review_id: review-T-P8-002-explicit-time-13state-parent-option-liuchuanafeng-20261017T2112Z
agent: 流川枫
source_agent: 流川枫
task_id: T-P8-002
claimed_via: claim-T-P8-002-explicit-time-13state-parent-option-liuchuanafeng-20261017T2112Z
inspected_commit: 2429b1a863a9f476925e686a46f59eb030bb5222
result_commit: 30dc800a10f96122f1b15e79ed70247d4bc7a273
admission_label: pending_decision_memo_only
status: completed
boundary: decision memo and minimal theorem signature only; no source edits, no flowpipe coverage, no registry/state/formal proof mutation
---

# Review result: T-P8-002 explicit-time 13-state parent option

## Decision memo

Inspected documents at commit `2429b1a863a9f476925e686a46f59eb030bb5222`:

- `docs/routeb-p8-flowpipe-binding-next.md`
- `docs/routeb-p8-next-concrete-child.md`

**Core incompatibility (established):**

The existing Lean parent `RouteBP8PicardStep` uses a 14-state contract:

```text
Fin 14: q1..q6, dq1..dq6, w, c
w' = c, c' = 0   (RampRhsPremise)
```

The deployed Julia `full_rhs!` (and associated exporter) is a 13-state system:

```text
inputs u[1:13] (q, dq, w), outputs du[1:12] + du[13] = 0
no c state; w is constant
```

A natural zero-tail lift of the 13-state source into 14 states produces a concrete counterexample (all mechanical components and w zero, c=1) that satisfies FullX0 but violates `w' = c`. Only the degenerate subfamily c=0 is compatible. This is already formalized as `zeroTailLift_not_ramp` in the contract adapter.

**Options:**

1. Provide a true 14-state RHS implementing `w'=c, c'=0` and bind it to the existing parent (requires source change).
2. Introduce an explicit-time 13-state parent `F13(t)` with `w(t) = c0 * t` (constant c0), and construct a corresponding flowpipe/adapter (requires new parent theorems and initial/terminal statement adjustments).

**Recommendation:**

Option 2 is the lower-disruption path for the current deployed source. It preserves the existing 13-state mechanical RHS semantics and only externalizes the ramp as an explicit time parameter. The existing `timeLift` scaffold already demonstrates how to recover the 14-state ramp premise from an abstract time-dependent G, but does not discharge source binding.

**Minimal theorem signature (sketch, not formalized):**

```lean
theorem explicit_time_13state_parent
  (c0 : ℝ) (hc0 : c0^2 ≤ 3)
  (x0 : State13) (hx0 : FullX0_mech x0 ∧ x0.w = 0)  -- mechanical fullX0, initial w=0
  (F13 : ℝ → State13 → State13)
  (hbind : ∀ t, first12 (F13 t) = deployed_mechanical_rhs)
  (hsol : is_solution_of F13 x0 on [0,1])
  : ∀ t ∈ [0,1],
      let z := sol t;
      z.w = c0 * t ∧
      mechanical_coords z ∈ certified_tube t
```

Initial-domain change: FullX0 restricted to mechanical coordinates + w=0 (c0 becomes a parameter, not a state). Terminal statement must compare against the explicit ramp trajectory rather than a free c state.

## Admission

- admission_label: `pending_decision_memo_only`
- No source edits performed.
- No flowpipe coverage claimed.
- No registry, state, or formal proof mutation.
- The decision remains pending until an owner selects option 1 or 2 and supplies the corresponding source binding or new parent theorems.

This review does not close T-P8-001 or any parent reachability obligation.
