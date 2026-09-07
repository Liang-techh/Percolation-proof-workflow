---
kind: companion_log
companion_id: companion-T-P4-039-liuguanyi-20260907T1619
task_id: T-P4-039
source_agent: 柳冠一
created_at: 2026-09-07T16:19:00-06:00
related_review: review-T-P4-039-liuguanyi-20260907T1616
integration_status: pending
---

# T-P4-039 协作摘要

- 当前完成：补上 `T-P4-038` 明确留下的 same-cell shared-`theta` / shared-`lambda` 多行交集数学。对每一行定义 `G_i=D_i-A_i-P_i`、`Delta_i=G_i^2-4A_iP_i`，并引入有理半径 `s_i`，只要求 `s_i^2<=Delta_i`。由恒等式 `4A_i p_i(theta)=(2A_i theta-G_i)^2-Delta_i`，得到一个无需平方根的有理 inner interval；所有行 inner interval 有公共交集时，其中点就是单个共同有理 `theta`，再统一转换为 `lambda=1+1/theta`。
- 新的实质点：这不是逐行各自挑参数。给出了精确反例：两行都通过 `T-P4-038` discriminant gate，但可行区间分别为 `[1,2]` 与 `[3,4]`，所以不存在共同参数。也给出一个更细例子：两行可行区间 `[1,2]` 与 `[7/4,11/4]` 有交集，但两个 `T-P4-038` 行中心 `3/2`、`9/4` 都不能跨行使用；本轮 radius-intersection 直接构造 `theta=15/8`、`lambda=23/15`，两行都保留精确 reserve `7/120`。
- 进一步结论：若有限多行在某个实数共同参数上都有严格 slack，则总能选出有理 `s_i`，使这些有理 inner interval 仍有严格公共交集，因此存在共同有理 `theta`。也就是说，严格可行时不会因为二次根是无理数而迫使 trusted P4 接口使用浮点参数。
- 给形式化 Agent 的建议：优先只做四个纯代数小 theorem：`young_completed_square_identity`、`young_feasible_of_rational_radius`、`young_inner_interval_feasible`、`young_reserve_completed_square`；共同参数 theorem 再复用已 CI 通过的 `T-P4-038 young_scalar_budget_mul_iff`。不要先做 source/P8 API，也不要把每行不同的 `theta_i` 当成 shared-lambda certificate。
- 尚未闭合：真实 same-cell `A_i/P_i/D_i`、separated-charge source binding、true-DH/Float64、cell/trajectory coverage、Lean/axioms/独立验证与 P4/M4 admission。
- 关联结果：`review-T-P4-039-liuguanyi-20260907T1616.md`；当前严格保持 `pending`。