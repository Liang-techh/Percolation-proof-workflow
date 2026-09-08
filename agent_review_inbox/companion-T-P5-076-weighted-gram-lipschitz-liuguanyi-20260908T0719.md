---
kind: companion_log
companion_id: companion-T-P5-076-weighted-gram-lipschitz-liuguanyi-20260908T0719
task_id: T-P5-076-WEIGHTED-GRAM-LIPSCHITZ
source_agent: 柳冠一
created_at: 2026-09-08T07:19:00-06:00
parent_review: review-T-P5-076-weighted-gram-lipschitz-liuguanyi-20260908T0716
admission_label: pending
---

# 柳冠一协作补充 — T-P5-076

本轮补上了 T-P5-075 明确缺少的“同一 weighted norm 的 squared-Lipschitz 常数从哪里来”这一数学接口。

最重要的协作提醒有三点：

1. **source 不要先对 `J_ij` 逐项取绝对值。** squared-Lipschitz 真正消费的是 `H=J^T W J`，其中交叉项 `H_jk=sum_i w_i J_ij J_ik` 可能在不同输出行之间发生精确符号抵消。应该先形成这个 signed Gram sum，再对整个 `H_jk` 做 enclosure。`[[1,1],[1,-1]]` 的例子中，真实 `H_12=0`、`Lambda=2`；absolute-first fallback 会把需要的 `Lambda` 放大到 4。

2. **implicit-root lane 可以完全无除法。** 令 `d_i=∂_i h_i>0`，`A_ii=d_i`、`A_ij=∂_j h_i`，则 `A_ij=d_i J_ij`。选择公共正 clearing scale `Delta` 与 `eta_i` 满足 `Delta=eta_i d_i^2` 后，直接形成 `P_jk=sum_i w_i eta_i A_ij A_ik=Delta H_jk`。后续 checker 只需验证 `P_jj`、`|P_jk|` 与 `Lambda w_j Delta` 的 exact-rational 不等式，不需要真的算 `1/d_i`。

3. **T-P5-074 与本轮可以共用一个 source Jacobian packet。** 前者从 `S=WJ+J^T W` 得到 `mu`，本轮从 `H=J^T W J` 得到 `Lambda`；两者一旦在同一 cell、同一 `W`、同一 `J` 上成立，T-P5-075 所需的 `mu^2<=Lambda` 事实上自动由 weighted Cauchy 推出，不必再向 deployed source 索取第三份物理证据。

建议 Lean agent 第一批只形式化纯代数叶：`weighted_gram_row_upper`、`weighted_jacobian_pointwise_sq_le`、`cleared_implicit_weighted_gram_identity`。segment integration 的 secant theorem 可以后置，以免把有限和式代数与分析 API 混在一起。

仍未闭合：真实 deployed SCC 的 `J=D Phi` 绑定、same-cell Gram enclosure、convex segment validity、corrector implementation/evaluator defect、Float64/FD/controller/solve、P8/ODE coverage、Lean/kernel、封不觉独立验证、comparator/admission/registry。当前只能作为 `pending mathematical/interface child` 消费。
