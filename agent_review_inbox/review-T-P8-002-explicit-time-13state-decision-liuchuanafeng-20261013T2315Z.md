---
kind: review_result
review_id: review-T-P8-002-explicit-time-13state-decision-20261013
source_agent: 流川枫
created_at: 2026-10-13T23:15:00Z
task_id: T-P8-002
inspected_commit: 2068ebe68fa1774525e2957a7f8199bf3683458e
inspected_paths:
  - agent_review_inbox/task_queue.md
  - docs/routeb-p8-next-concrete-child.md
  - docs/routeb-p8-flowpipe-binding-next.md
admission_label: architecture_only
---

# T-P8-002 Decision Memo: explicit-time 13-state parent option vs existing 14-state ramp parent

## Question inspected

Compare a new explicit-time 13-state parent with the existing 14-state ramp parent (including initial-domain and terminal statement changes). Deliver a decision memo and minimal theorem signature. No source edits, no flowpipe/coverage claim, no registry/state/formal-proof mutation.

## Evidence summary (read-only)

From `docs/routeb-p8-next-concrete-child.md` and `docs/routeb-p8-flowpipe-binding-next.md` (dated 2026-09-06, still current at inspected commit):

- Existing Lean parent `RouteBP8PicardStep` uses `Fin 14 = q1..q6, dq1..dq6, w, c` and requires `RampRhsPremise F`:
  ```
  ∀ z, F z wSlot = z cSlot ∧ F z cSlot = 0
  ```
  i.e., autonomous `w' = c`, `c' = 0`.

- Audited Julia true-DH `full_rhs!` is 13-state (`u[1:13]`, `du[13] = 0`). Receipt template marks `c` as sidecar not consumed by source. Natural zero-tail lift of the 13-state source into 14-state fails `RampRhsPremise` on non-degenerate `c ≠ 0` points that still satisfy `FullX0` (e.g., `c=1`, mechanical energy 0, `w=0`).

- An existing adapter scaffold `timeLift G t` (in `examples/routeb_p8_contract_adapter/`) lifts an abstract time-dependent 13-state `G : time → State13 → State13` to a 14-state field that *does* satisfy the ramp premise for each fixed `t`. This is compiled as conditional interface only; it does not bind the real Julia source body, Float64/FD/solve semantics, or any enclosure/coverage.

- Explicit alternative already noted in the docs: change the P8 contract to an explicit-time 13-state RHS `F13(t)`, prove `w(t) = c * t` (with `c` constant), and build a corresponding parent/flowpipe adapter. This avoids embedding a non-consumed `c` into the state vector.

## Decision

**Prefer the explicit-time 13-state parent option as the next architectural direction**, with the following precise boundaries:

1. **Keep the existing 14-state ramp parent untouched** (do not silently rewrite its theorem statement). Treat it as a reusable conditional interface for any future true 14-state source that actually implements `w'=c, c'=0`.

2. **Introduce a disjoint explicit-time 13-state parent** whose state is exactly the source dimension (`Fin 13 = q1..q6, dq1..dq6, w`) and whose RHS is allowed to be non-autonomous:
   ```
   F13 : ℝ → (Fin 13 → ℝ) → (Fin 13 → ℝ)
   ```
   with the ramp relation recovered by integration rather than by an extra state:
   ```
   w(t) = w(0) + c * t    (c constant, supplied as a parameter, not a state component)
   ```

3. **Initial-domain change**: the existing `FullX0` (12 mechanical coordinates + energy + `c^{2} ≤ 3`) remains, but `c` becomes a frozen parameter of the family rather than a dynamic coordinate. The initial box must still cover the mechanical ball plus the admissible `c` range; no new coverage is claimed here.

4. **Terminal statement change**: any terminal-transfer or first-exit theorem must be restated over the 13-state trajectory plus the explicit affine `w(t)`. The existing 14-state terminal skeleton cannot be reused without a fresh proof of the integration identity.

## Minimal theorem signature (architecture only, not a proof)

```lean
-- Minimal signature for the preferred explicit-time parent (not yet formalized)
theorem explicitTime13_ramp_identity
    (G : ℝ → (Fin 13 → ℝ) → (Fin 13 → ℝ))
    (c : ℝ)
    (sol : ℝ → Fin 13 → ℝ)
    (hsol : ∀ t, sol t = integral of G t (sol t) + initial)
    (hw0 : sol 0 wSlot = 0) :
    ∀ t ∈ [0,1], sol t wSlot = c * t := by
  sorry  -- architecture placeholder only; not admitted
```

Companion obligation (still open):
```lean
theorem source_binding_to_explicitTime13
    -- exact semantic equality between Julia full_rhs! (13-state, du[13]=0)
    -- and the first 12 components of G t, with w-component identically 0
    -- plus separate proof that the physical w evolves as c*t.
    : Prop := sorry
```

## Forbidden boundaries observed

- No source files edited.
- No state.json / registry / formal-proof mutation.
- No claim of flowpipe coverage, Picard image existence, interval containment, or true-DH reachability.
- The above signatures are decision artifacts only.

## Admission label

`architecture_only`

The comparison and recommended direction are recorded for coordinator harvest. Actual source binding, Lean formalization of the new parent, and any subsequent coverage proof remain open and must go through the normal verification and registry gates.
