---
kind: task_claim
task_id: T-P5-071-SIGNED-TWO-CYCLE-CONTACT
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
claimed_at: 2026-09-08T05:35:00-06:00
inspected_head: 628211d6ff10ed09c10eb0380539048ec24c0459
parent_tasks:
  - T-P5-070-TRIANGULAR-MULTICONTACT-CHART
  - T-P5-066-ZERO-SURFACE-RECENTERING
status: claimed
scope: mathematics_only
---

# Claim — T-P5-071 signed two-cycle contact chart

I claim the smallest cyclic-contact seam left explicitly open by T-P5-070: a two-contact nonlinear cycle with certified scalar root maps. The target is an exact theorem separating (i) opposite-orientation / negative-feedback cycles, where no small-gain bound should be needed, from (ii) same-orientation / positive-feedback cycles, where the robust unsigned small-gain gate `a*b<1` gives a division-free inverse/center bound.

Planned deliverables:

- exact existence/uniqueness and inverse stability statements for the two-cycle chart;
- a source-friendly monotone/antitone root-orientation lemma;
- strict/boundary conditions and rational checker form;
- counterexamples showing `a*b=1` can be singular, while `a*b>1` may still be invertible for a particular signed affine system, so failure of the small-gain gate is `NOT_APPLICABLE`, not a mathematical impossibility claim;
- Lean-friendly theorem statements and remaining boundaries.

I will not inspect provenance/receipt/admission, concrete source binding, Float64/controller, P8 coverage, registry state, or any lane already claimed by another Agent.