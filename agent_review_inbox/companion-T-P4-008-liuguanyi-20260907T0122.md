---
kind: companion_log
task_id: T-P4-008
source_agent: 柳冠一
created_at: 2026-09-07T01:22:00-06:00
---

# T-P4-008 协作提示

- 当前完成：已把 PMI 的归一化坐标 `f_B`、generalized-force residual `l_F=I_B f_B-M0_BB a_B` 和完整 DH block dynamics 分开，并给出精确桥接。
- 关键修正：`(q5/20,q4/20)` 是 `f_B` 内部的 raw `kc` 项；在当前 `l_F` force 坐标里必须先乘 `I_B=diag(1/5,1/10)`，因此真正的 `kc` force 项是 `+(q5/100,q4/200)`。当前 `docs/routeb-p4-kc-force-contract.md` 把前者称为 generalized force，与 `routeb-c2-d-normalization-audit.md` 和 PMI 实际使用 `Ival*f` 的语义冲突，建议梁智炜收割时 fail-closed 地区分两个 typed quantity，不要二选一覆盖历史结果。
- 远端 obstruction：完整 identity 必含 `+M_BD(q)a_D`。即使 `y↔q_cross` 完成、`kc` 常数完全够用，只要没有同域 remote-action bound，局部变量 PMI 仍不能 source-bind 完整 `l_F`；在 `q_B=0` 时可令 `kc=0,y=0` 而 remote term 非零，直接击穿任何 RHS 随 `y` 消失的 universal envelope。
- 给其他 Agent 的建议：形式化 Agent 可独立实现 `kc_normalization_bridge` 与 `block_force_residual_decomposition` 两个极小代数 lemma；source/P8 lane 应另给 `M_BD a_D` 同域界或显式扩大状态接口。`T-P4-011` 的 raw-vector Schur 数学不必废弃，但在接 `l_F` 前必须插入 `I_B` normalization。
- 关联任务/Review：`T-P4-008`，`review-T-P4-008-liuguanyi-20260907T0120.md`，并影响 `T-P4-007`、`T-P4-011`。
