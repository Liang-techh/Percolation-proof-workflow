---
kind: task_claim
task_id: T-P5-073-AFFINE-OFFSET-RELATIVE-DECAY
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
claimed_at: 2026-09-08T06:40:00-06:00
inspected_head: 7d847e354c8705769de36e0a24e652d2093376f4
parent_tasks:
  - P5-COMPONENTWISE-RELATIVE-DECAY
status: claimed
scope: mathematics_only
---

# Claim — T-P5-073 affine-offset relative-decay / zero-slice obstruction

I claim the smallest mathematical seam in the current P5 `componentwise_relative_decay` obligation: determine exactly when an additive force/FD offset can or cannot be absorbed into a componentwise relative-decay certificate.

The target is not source audit. I will prove a source-agnostic closure theorem separating:

- zero-containing cells, where pure `|R_i(v)| <= kappa_i |v_i|` forces exact vanishing on the whole transverse slice `v_i=0`;
- gap cells `|v_i| >= delta_i`, where a certified additive envelope `beta_i + kappa_i |v_i|` can be absorbed by an exact division-free gap condition;
- zero-containing cells where pure relative decay is impossible but a bias-aware invariant box still closes under an exact affine budget;
- sharp boundary cases and counterexamples showing why center vanishing alone is insufficient and why zero-slice vanishing alone does not imply a relative slope bound.

Planned deliverables: exact scalar/vector box statements, sharpness examples, Lean-friendly theorem statements, and a clear `PASS / BIAS-ROUTE / NOT_APPLICABLE` decision rule. I will not inspect provenance/receipt/admission, concrete source binding, Float64/controller, P8 coverage, registry state, or lanes already claimed by another Agent.