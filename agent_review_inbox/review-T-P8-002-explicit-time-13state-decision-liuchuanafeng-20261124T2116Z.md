---
kind: review_result
review_id: review-T-P8-002-explicit-time-13state-decision-liuchuanafeng-20261124T2116Z
source_agent: 流川枫
agent: 流川枫
task_id: T-P8-002
created_at: 2026-11-24T21:16:00Z
inspected_commit: 61ee1eec5334faf754865f2a0e0b38b985852a96
admission_label: architecture_only
boundary: decision memo only; no source/registry/state/formal-proof edits; no flowpipe coverage claim
---

# Review result: T-P8-002 — explicit-time 13-state parent option

## Question / bottleneck

Compare a candidate explicit-time 13-state parent against the existing 14-state ramp parent (`RouteBP8PicardStep.RampRhsPremise`) at the statement and domain level. Deliver a decision memo and a minimal theorem signature. Do not edit source, do not claim flowpipe coverage, do not alter the target theorem.

## Evidence inspected

- `docs/routeb-p8-next-concrete-child.md` (2026-09-06): records the concrete obstruction that the audited Julia `full_rhs!` is 13-state (`du[13]=0`) while the Lean parent requires `F z wSlot = z cSlot` and `F z cSlot = 0` on a 14-state space. The zero-tail lift fails on the full `FullX0` family (counter-example with `c=1`).
- `docs/routeb-p8-flowpipe-binding-next.md`: confirms the same 13-vs-14 mismatch, lists the coordinate map, and states that the first actionable child is a coherent source binding (either true 14-state ramp or explicit-time 13-state).
- Existing claim `claim-T-P8-002-explicit-time-13state-parent-option-liuchuanafeng-20261124T1727Z.md` (same agent).
- No corresponding closing `review_result` observed prior to this file.
- No Lean/Julia execution performed in this review; admission remains non-verified.

## Decision memo

**Recommendation: pursue the explicit-time 13-state parent as an independent sibling option; do not silently rewrite the existing 14-state ramp parent.**

Rationale (statement/domain level only):

1. The deployed/audited source is 13-state with constant-`w` (`du[13]=0`). Instantiating the current `RampRhsPremise` requires a true `w'=c, c'=0` vector field that the source does not provide.
2. The natural zero-tail lift of the 13-state field into 14-state space falsifies `RampRhsPremise` on a non-empty open subset of `FullX0` (any state with `c 
eq 0`). Only the degenerate slice `c=0` survives.
3. Changing the existing parent in place would silently alter the target theorem and invalidate all downstream Picard/receipt adapters that already mention the 14-state ramp contract. The task forbids this.
4. An explicit-time formulation keeps the mechanical 12-state dynamics exactly as the source writes them, treats the ramp parameter `c` as an external constant, and recovers the linear ramp `w(t) = w0 + c*t` by a separate (trivial) ODE. This preserves the current parent as a possible future target if a true 14-state RHS is later supplied, while giving an immediately usable interface for the existing source.

The option remains architecture-only until a concrete source-to-G semantic binding, interval containment, and Picard existence proofs are supplied. It does not close P8, M4, or any registry entry.

## Minimal theorem signature (proposed, not yet formalized)

```text
theorem explicit_time_13state_ramp
  (G : ℝ → (Fin 13 → ℝ) → (Fin 13 → ℝ))
  (t0 t1 : ℝ) (c : ℝ)
  (sol : ℝ → Fin 13 → ℝ)
  (hsol : IsSolutionOfTimeDependent G sol)
  (hw : ∀ t, sol t (wSlot13) = sol t0 (wSlot13) + c * (t - t0))
  : ∀ t ∈ [t0, t1],
      sol t (wSlot13) = sol t0 (wSlot13) + c * (t - t0)
      ∧ mechanical_trajectory_matches_source sol t
```

(The signature is illustrative only; exact Lean encoding, domain hypotheses, and source-binding premises are left for a later leaf. No proof is claimed.)

## Admission

```text
admission_label          = architecture_only
source_binding           = OPEN
ramp_binding (14-state)  = OPEN / inconsistent with current source
explicit_time_option     = proposed, not formalized
flowpipe_coverage        = OPEN
registry                 = unchanged
formal_certificate_allowed = false
```

This review does not modify any authoritative checkpoint, StateStore, verified registry, or formal proof. It is an immutable inbox result only.
