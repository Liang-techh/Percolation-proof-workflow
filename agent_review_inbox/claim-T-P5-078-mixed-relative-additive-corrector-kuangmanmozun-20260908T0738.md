---
kind: claim
task_id: T-P5-078-MIXED-RELATIVE-ADDITIVE-CORRECTOR
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-08T07:38:00-06:00
status: claimed
scope: mathematics_only
parents:
  - T-P5-073-AFFINE-OFFSET-RELATIVE-DECAY
  - T-P5-075-DAMPED-CORRECTOR-ENERGY
  - T-P5-077-ANCHOR-LOCALIZED-INVARIANT-BALL
---

# Claim — T-P5-078

I claim the smallest disjoint closure child left between the P5 relative-error and defective-corrector lanes: **a sharp envelope-level gate for a corrector whose evaluator defect contains both a state-relative component and a persistent additive component**.

The intended packet is

`Q(a) <= q Q(d)`,

`Q(e_rel) <= K Q(d)`,

`Q(e_abs) <= E`,

with actual update `d_plus = a - h e_rel - h e_abs` in one common weighted quadratic norm `Q`.

I will derive:

1. an exact radical-free necessary/sufficient envelope gate for the relative part to preserve strict contraction;
2. a modular rational auxiliary-factor gate that composes the relative part with the sharp additive first-exit barrier from T-P5-075;
3. counterexamples showing that separately spending a full relative allowance and a full additive allowance is unsound;
4. the `E=0` zero-floor branch versus the `E>0` persistent-floor obstruction;
5. Lean-friendly scalar theorem statements using only multiplication, squares and order.

This does not claim a deployed SCC, source binding, evaluator implementation, Float64/FD/controller semantics, coverage, Lean/kernel verification, admission, registry mutation, or parent closure. I will not modify or audit T-P5-077's existing Lean sidecar.