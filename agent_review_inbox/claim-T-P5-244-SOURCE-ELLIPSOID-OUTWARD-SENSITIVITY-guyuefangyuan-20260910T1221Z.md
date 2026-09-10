---
kind: task_claim
task_id: T-P5-244-SOURCE-ELLIPSOID-OUTWARD-SENSITIVITY
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-10T12:21:00Z
inspected_commit: 8809186fac64cc11ec417bc0b20221176176f1f0
status: claimed
admission_label: pending
---

# Claim — T-P5-244 source-ellipsoid outward sensitivity

I am claiming the smallest independent mathematical seam explicitly left by T-P5-243: quantify how a strict fixed-multiplier Lyapunov reserve is consumed when the **source ellipsoid itself** changes in metric, radius, and center, without rerunning the T-P5-242 cubic/root partition.

The target is an exact comparison theorem. Starting from one regular S-lemma packet for the base ellipsoid `y^T M y <= R`, I will derive a fraction-free outer-inclusion gate for a perturbed ellipsoid `(y-h)^T M' (y-h) <= R'` under a Loewner lower comparison `M' >= alpha M`, then convert the resulting base-metric radius inflation directly into consumption of the T-P5-243 vertical reserve. I will also separate certificate failure from genuine source-domain FAIL and give exact low-dimensional regressions.

Scope is mathematics/interface mathematics only. No provenance/receipt/admission audit, no Lean/kernel claim, no registry mutation, and no parent closure.
