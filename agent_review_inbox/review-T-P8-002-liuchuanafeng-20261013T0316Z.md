---
kind: review_result
review_id: review-T-P8-002-liuchuanafeng-20261013T0316
task_id: T-P8-002
parent_task_id: T-P8-001
source_agent: 流川枫
created_at: 2026-10-13T03:16:00Z
inspected_commit: 891bb692316b10afb5774c8d4854e06fbed21830
integration_status: pending
admission_label: architecture_only
proposed_integration_target: documentation
requested_action: record_decision_memo_for_coordinator
---

# T-P8-002 — Decision memo: explicit-time 13-state parent vs 14-state ramp parent

## Inspected artifacts

- Existing 14-state ramp parent sidecar: `examples/routeb_p8_ramp_reconstruction_sidecar/P8RampReconstruction.lean` (and README), which defines `State14 := Fin 14 → ℝ` with `wSlot=12`, `cSlot=13`, and proves ramp reconstruction under global differentiability (`c'=0`, `w'=c`, `w(1)=c0`).
- Explicit-time 13-state sidecar already present: `examples/routeb_p8_explicit_time_sidecar/RouteBP8ExplicitTimeSidecar.lean` and README.
  - Defines `State13 := Fin 13 → ℝ` (coordinates `q1..q6, dq1..dq6, w`).
  - Keeps `c` as an external parameter.
  - Provides `forgetTail13`, `initialProjection13` from `FullX0` (energy + w=0 + c^{2}≤3), and `terminalTransfer13` that rewrites to `y wSlot13 = c`.
  - Minimal theorems are identity/packaging only; no flowpipe or source binding.
- Related: `examples/routeb_p8_picard_step_lean` (imported parent) and other P8 adapters.

## Comparison

| Aspect | 14-state ramp parent | Explicit-time 13-state option |
|---|---|---|
| State dimension | 14 (includes c as state slot) | 13 (c external) |
| Coordinate order | q, dq, w, c | q, dq, w |
| Initial domain | FullX0: mechanical energy ≤ 9/400, w=0, c^{2}≤3 | Projected via forgetTail13 + external c |
| Terminal statement | w(1) = c0 (from ramp) | y_w = c (direct equality, no time integration of c) |
| Differentiability | Global HasDerivAt (stronger than needed) | Interface only; no derivative claims here |
| Deployed source match | Extra c slot not in deployed 13-state vector | Matches deployed 13-state (c parameter) |
| Existing Lean | Compiled candidate in ramp sidecar | Minimal packaging theorems already written |

## Decision

Prefer the explicit-time 13-state parent as the target interface for future source-authenticated P8 work.

Reasons:
1. Matches the deployed Julia/DH source coordinate order (13 states + external c).
2. Avoids carrying an unnecessary dynamic slot for a constant parameter.
3. Terminal predicate simplifies to a direct equality `w = c` rather than a reconstructed ramp value, reducing calculus obligations.
4. The projection from the existing 14-state FullX0 is already formalized and trivial.
5. Does not invalidate the existing ramp sidecar (which remains a valid abstract calculus child); it can be consumed as a lemma if needed.

Minimal theorem signature recommended for the 13-state parent (architecture only):

```text
theorem explicitTimeParent13
  (F13 : TimeVectorField13) (c : ℝ)
  (hFamily : sourceFamily13 F13 c)
  (hInit : ∀ z, FullX0 z → initialProjection13 z)
  (hTerm : ∀ y, terminalTransfer13 y c → terminalTransfer13 y c)
  : sourceFamily13 F13 c ∧ …  -- packaging of assumptions only
```

(Exact statement already present as `explicitTimeContract_assumptions` in the sidecar.)

## Boundary / forbidden compliance

- No source edits performed.
- No claim of flowpipe existence, coverage, interval containment, or ODE solution.
- No registry, state, or admission promotion. This is a pure decision/architecture memo.
- Existing ramp theorems remain untouched.

## Remaining obligations

Any later promotion still requires:
- Source binding of F13 to the deployed RHS,
- Interval-local regularity,
- Flowpipe / coverage receipts,
- Independent verification gates.

Admission remains `architecture_only`.
