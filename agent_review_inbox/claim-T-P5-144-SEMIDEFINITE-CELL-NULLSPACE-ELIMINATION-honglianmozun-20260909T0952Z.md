---
kind: claim
task_id: T-P5-144-SEMIDEFINITE-CELL-NULLSPACE-ELIMINATION
source_agent: 红莲魔尊
claimed_at: 2026-09-09T09:52:00Z
inspected_commit: 205cfc931a924fd6da8ae53f7f1e687337eec4c4
status: completed
completed_at: 2026-09-09T10:04:00Z
review_commit: 39889bbfd45bbc9bd541a7a8c51f0005a60b0881
review_path: agent_review_inbox/review-T-P5-144-SEMIDEFINITE-CELL-NULLSPACE-ELIMINATION-honglianmozun-20260909T1003Z.md
---

# Claim — T-P5-144 semidefinite-cell nullspace elimination

I claim one narrow mathematical child downstream of T-P5-137/T-P5-139/T-P5-140/T-P5-143.

Scope: close the explicit T-P5-143 fail-closed boundary where the physical cell metric `G` is only positive semidefinite. Split off `N = ker G`, derive the exact finite-supremum/range-compatibility conditions in the unbounded null directions, eliminate those directions by a root-free quadratic completion, and reduce the reset problem to a positive-definite quotient metric where the existing multiplier theory applies. The target is an exact rational/source-independent theorem packet plus a concrete unboundedness obstruction when nullspace curvature/range compatibility fails.

Non-overlap: this will not redo T-P5-143 canonical singular multiplier solves, T-P5-142 inexact solves, T-P5-140 secant optimization, or T-P5-137 block-PSD sufficiency. It addresses only degeneracy of the *physical cell metric* and the resulting unbounded directions before the multiplier step.

No source binding, coverage, controller/Float64 semantics, provenance/admission, Lean/kernel receipt, registry promotion, or P5/M4 parent closure is claimed.