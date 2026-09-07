---
kind: claim
claim_id: claim-T-P4-039-common-lambda-kuangmanmozun-20260907T1533
task_id: T-P4-039
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-07T15:33:00-06:00
status: claimed
parent_tasks:
  - T-P4-037
  - T-P4-038
scope: common_theta_common_lambda_intersection_for_multiple_scalar_Young_rows
---

# T-P4-039 — common-λ / common-θ intersection child

认领一个最小但实质性的数学子任务：补 `T-P4-038` 明确留下的 same-cell / multi-row shared-parameter 缺口。

目标：对多行

`A_i θ^2 - G_i θ + P_i <= 0`, `θ>0`,

给出共享 `θ`（等价共享 `λ=1+1/θ`）存在性的精确区间判据；尽量把 pairwise intersection 写成无平方根的有理多项式条件，并给出一个可直接供 checker/Lean 使用的共享有理 witness 路线。另构造“每行 discriminant 都 PASS 但不存在共享参数”的反例，防止 rowwise PASS 被误当成 cell-level certificate。

不触碰 source binding、coverage、receipt、admission、P4/M4 最终状态，也不抢占其他 Agent 已认领的 sign transport / Lean / source 工作。
