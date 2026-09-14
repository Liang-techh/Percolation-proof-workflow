---
kind: companion_log
review_id: companion-GH-MATH-P4-SCHUR-ACTUAL-SOURCE-NEXT-guyuefangyuan-20260908T2232Z
task_id: GH-MATH-P4-SCHUR-ACTUAL-SOURCE-NEXT
source_agent: 古月方源
created_at: 2026-09-08T22:32:00Z
parent_review: review-GH-MATH-P4-SCHUR-ACTUAL-SOURCE-NEXT-guyuefangyuan-20260908T2230Z
integration_status: pending
admission_label: pending
registry_mutation: false
---

# 给梁智炜及 source lane 的中文接力

本轮已把 `GH-MATH-P4-SCHUR-ACTUAL-SOURCE-NEXT` 收窄成一个比“缺 actual capture”更具体的结构性阻塞：当前 signed-affine Schur helper 消费的是 `C=(4,5,6)` 的三维 defect `d` 与 3×3 `H=M0_CC^-1`，而目前最接近 actual/source 的 preconditioned + weighted packet 只恢复 `B=(4,5)` 的二维 principal defect，并且原 payload 仍只输出 rows 4/5。两者不能按字段名拼接。

关键数学结论：对任意三维 SPD metric `H`，只要观测映射秩小于 3，就不存在仅由这些观测推出的有限统一 `D=d^T H d` 上界。证明取非零 `v` 属于观测核，令 `d=t v`；观测恒为零，但 `D=t^2 v^T H v` 可任意大。因此：

- 两条 signed projection `u=<ell,d>_H`、`s=<ell+r0,d>_H` 绝不能反推出 `D`；
- rows4/5 或二维 weighted recovery 也绝不能自动成为 block456 三维 `D` producer；
- 若继续 block456 路线，source lane 必须补第三个独立 defect 方向，或直接交完整六维 `y=Xz_A` 与 3×6 `A` 的同源 box；
- 若改走 B=(4,5) 二维路线，则必须明确换 statement，并提供匹配的 2×2 metric/source chart，不能借用现有 3×3 `HQ`。

建议下一次 source 产物只做一个不可拆换的单 packet：冻结同一个 `source_key/configuration_key/domain_key`，同时交 `z_A`、`X`、`y=Xz_A`、所有 A-active 的 y enclosure、`J_d/b`、`A X=J_d`、C=(4,5,6) 顺序/单位、`M0_CC/H` 双边 inverse、`ell/r0`，以及独立生成的 `u/s/D` 三个输出。`D` 可以在 actual rational `A,b,H,y-box` 到位后用现有 exact vertex theorem 计算，但禁止由 `u,s` 重建。

另外，当前 source-rows review 已确认 preconditioned rows4/5 builder 存在 20 个非零 q/dq controller coefficient omission，所以旧 payload row 也不能直接改名为 `y_A` 分量。应先修复 source 表达式/重生成 packet，再做同键 join；synthetic Fraction self-test 只保留为数学 helper 测试，不是 runtime/source 证据。

共享 `collaboration_board.md` 当前 GitHub 写接口仍是整文件 replacement，而文件很大；本轮没有冒险覆盖其他 Agent 的并发留言。请梁智炜从本 companion 安全 harvest 上述中文接力。
