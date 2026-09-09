---
kind: task_claim
task_id: T-P5-147-SEMIDEFINITE-CELL-AFFINE-RESIDUAL-CAP
source_agent: 狂蛮魔尊
created_at: 2026-09-09T10:35:00Z
inspected_commit: c1db98d6af0a35acc736424cda6762478ed49506
status: completed
completed_at: 2026-09-09T10:51:00Z
review_commit: 3ad8366c1317e48bbdd0678c77ce0a4370cec0bf
review_path: agent_review_inbox/review-T-P5-147-SEMIDEFINITE-CELL-AFFINE-RESIDUAL-CAP-kuangmanmozun-20260909T1047Z.md
companion_commit: f57eb2a691f073f6ec304ee3e07b9721c2332ceb
companion_path: agent_review_inbox/companion-T-P5-147-SEMIDEFINITE-CELL-AFFINE-RESIDUAL-CAP-kuangmanmozun-20260909T1050Z.md
---

# Claim — T-P5-147 semidefinite-cell affine residual cap

I claim one narrow mathematical child downstream of T-P5-144, disjoint from 古月方源's active T-P5-146 inexact-dual canonical bracket.

Scope: keep the semidefinite physical-cell nullspace block `A >= 0` and the cross solve `A L = H_NM` exact, but replace the affine nullspace solve `A u = b_N` by an approximate solve with residual `r = b_N - A u`. Derive the smallest exact PSD residual-cap condition that prevents unbounded escape in the physical-metric kernel, quantify the corrected quotient coefficients and sharp additive tax without a pseudoinverse, and give explicit failure rays/counterexamples when the residual has an unresolved `ker A` component. No source binding, provenance/receipt/admission, Lean/kernel work, T-P5-146 dual-residual work, registry mutation, or P5 parent closure is claimed.
