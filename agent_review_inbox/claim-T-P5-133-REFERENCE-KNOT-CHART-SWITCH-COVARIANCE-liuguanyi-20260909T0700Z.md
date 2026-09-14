---
kind: task_claim
task_id: T-P5-133-REFERENCE-KNOT-CHART-SWITCH-COVARIANCE
source_agent: 柳冠一
created_at: 2026-09-09T07:00:00Z
inspected_commit: a521dbad9a0c1dac213ed61e745dff9c2c54cc4f
status: completed
integration_status: pending
result_path: agent_review_inbox/review-T-P5-133-REFERENCE-KNOT-CHART-SWITCH-COVARIANCE-liuguanyi-20260909T0710Z.md
result_commit: 4eec908f938ea1e30e5f381d254c62b5e1b45ae1
---

# 柳冠一 claim — T-P5-133 reference-knot chart-switch covariance

认领一个不与现有 T-P5-130/131/132 reset 标量优化重叠的最小跨层数学命题：处理 reference knot 同时发生坐标 chart 切换时，physical reset packet 如何无损运输到 normalized coordinates。

目标：

- 证明 pre/post chart 不同但 physical state 连续时，正确 gluing 条件是 `T_+(z_+)=T_-(z_-)=q`，不能默认 `z_+=z_-`；
- 对可逆 affine chart 证明 T-P5-130/131/132 的 `m,B,mu,ell,R,kappa,E` packet 在 congruence metric/covector pullback 下精确协变，不产生 Jacobian condition-number penalty；
- 对 nonlinear chart 给出 exact secant-Jacobian identity，说明 reset 的 physical displacement/linear mismatch 必须用 averaged Jacobian（或直接保留 physical packet），不能静默用 anchor tangent `J_*`；
- 给出 tangent-substitution 的精确 remainder/反例，并明确若坚持 normalized-only packet，需要额外 whole-segment chart bound；
- 输出最小 theorem statement、typed source contract 与 Lean 拆分建议，保持 source/runtime/coverage/P8/admission 全部外置。

不处理 provenance、receipt、admission、registry，也不重复 T-P5-131/132 的 sharp scalar reset envelope。

完成：数学结果已写入 `review-T-P5-133-REFERENCE-KNOT-CHART-SWITCH-COVARIANCE-liuguanyi-20260909T0710Z.md`；保持 `CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending`。