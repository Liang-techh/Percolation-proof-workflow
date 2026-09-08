---
kind: claim
task_id: T-P5-080-CORRELATION-AWARE-MIXED-DEFECT
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-08T08:08:00-06:00
status: claimed
scope: mathematics_only
parents:
  - T-P5-075-DAMPED-CORRECTOR-ENERGY
  - T-P5-078-MIXED-RELATIVE-ADDITIVE-CORRECTOR
---

# Claim — T-P5-080

I claim the smallest disjoint mathematical child explicitly left open by T-P5-078's correlation boundary: a **signed/correlation-aware contraction and barrier gate** for evaluator defects when source analysis can certify inner-product information instead of only independent norm envelopes.

The intended packet keeps the same weighted quadratic form `Q` and consumes, for the relative defect,

`Q(a) <= q V`, `Q(e_rel) <= K V`, and a signed lower bound `<a,e_rel>_W >= gamma V`.

I will derive the exact correlation-aware factor `q - 2 h gamma + h^2 K`, show how it strictly improves the independent-envelope factor when `gamma > -sqrt(qK)`, and give exact rational counterexamples showing that favorable sampled angles are useless unless a source theorem supplies the signed lower bound.

I will also give a source-friendly additive extension where the post-relative vector `b` satisfies a signed cross budget `<b,e_abs>_W >= -(j V + c)`, producing a purely affine energy recurrence and a radical-free invariant-level gate. This is deliberately separate from T-P5-079 similarity normalization and from all Lean/provenance/admission work.

No deployed SCC/source binding, Float64/FD/controller semantics, P8 coverage, Lean/kernel receipt, admission, registry mutation, or parent closure is claimed.