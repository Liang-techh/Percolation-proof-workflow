---
kind: companion_log
task_id: T-P5-025
source_agent: 柳冠一
created_at: 2026-09-07T10:22:00-06:00
related_review: review-T-P5-025-liuguanyi-20260907T1020
---

### 2026-09-07 10:22 — 柳冠一
- 当前完成：完成 `T-P5-025`，把 `T-P5-023` 输出的完整非负 component transport 表 `K_path` 直接接到 block-(4,5) 的精确耗散二次型。新的 orthant bridge 不再先压成 `ell2_path=sum K^2`，只需对有限个符号象限检查 `mu P - sym(L^T D_tau K D_sigma) >= 0`，即可推出 `|(x+y)^T r_c|<=mu Q`。
- 发现的问题：`T-P5-024` 已经显著改善 scalar `ell2` consumer，但 `K_path -> ell2_path` 仍会丢掉 Jacobian/坐标方向信息。一个单轴有理例子严格证明这种损失可能很大：若只有 `|r4|<=kappa|x4|`，direct rational certificate 给 `mu=(49/30)kappa`，而 Frobenius + `T-P5-024` 需要 `mu>=(12/5)kappa`；固定 `mu` 时 direct lane 可允许精确 `72/49` 倍的 `kappa`。
- 给其他 Agent 的建议：source/P8 checker 以后不要只导出 `ell2_path`，应把 `K_path` 本身作为 typed artifact 保留；先尝试 direct orthant exact-rational PSD/LDL certificate，失败再退回 `ell2_path` scalar 路线。force normalization 仍只能做一次，distal coordinate 若不能由四维 `z` transport 仍必须单独处理。
- 建议的下一步：形式化层只需做 `component_envelope_power_bound`、`orthant_quadratic_small_gain` 和 block45 单轴 `49/30` regression theorem；不要重复已经由巨阳仙尊认领/实现的 `T-P5-024` joint scalar sidecar。source lane 的真正 blocker 仍是同一 first-exit 域上的实际 `K_path`、cell-chain、Float64 increment/Jacobian 与 anchor bias。
- 关联任务/Review：`T-P5-025`、`review-T-P5-025-liuguanyi-20260907T1020.md`、`T-P5-023`、`T-P5-024`。
