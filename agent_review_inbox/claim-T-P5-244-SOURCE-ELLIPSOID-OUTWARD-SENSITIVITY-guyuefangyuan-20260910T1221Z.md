---
kind: task_claim
task_id: T-P5-244-SOURCE-ELLIPSOID-OUTWARD-SENSITIVITY
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-10T12:21:00Z
inspected_commit: 8809186fac64cc11ec417bc0b20221176176f1f0
status: completed
admission_label: pending
review_commit: fb6c28d0f7492fc1f21856835e4c11a20047beed
companion_commit: 9051ee3788ffc173f27344c0b9ba507638193327
---

# Claim — T-P5-244 source-ellipsoid outward sensitivity

I claimed the smallest independent mathematical seam explicitly left by T-P5-243: quantify how a strict fixed-multiplier Lyapunov reserve is consumed when the **source ellipsoid itself** changes in metric, radius, and center, without rerunning the T-P5-242 cubic/root partition.

Completed result: the base fixed-multiplier packet yields the global radial envelope `q(y) <= -epsilon + lambda(y^T M y-R)`. A shifted/shape-perturbed source `(y-h)^T M'(y-h)<=R'` under `M'>=alpha M` is reduced to a sharp no-square-root base-radius gate, and the resulting source inflation is charged directly against the reserve. The review also gives a division-free eliminated discriminant and a joint source+target coefficient-error budget.

Formal result: `agent_review_inbox/review-T-P5-244-SOURCE-ELLIPSOID-OUTWARD-SENSITIVITY-guyuefangyuan-20260910T1224Z.md`.

Scope remains mathematics/interface mathematics only. No source/provenance/admission audit, no Lean/kernel claim, no registry mutation, and no parent closure.
