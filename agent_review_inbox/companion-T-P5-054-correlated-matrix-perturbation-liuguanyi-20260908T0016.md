---
kind: companion_log
task_id: T-P5-054
review_id: review-T-P5-054-correlated-matrix-perturbation-liuguanyi-20260908T0013
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-08T00:16:00-06:00
integration_status: pending
admission_label: pending
---

# 柳冠一协作摘要 — T-P5-054

- 当前完成：补上 `T-P5-053` exact Bernstein packet 与实际近似 source 之间的一层数学 bridge。先形成 branch-free 对称矩阵包 `G=[[4κp-b4²,2κσ-b4b5],[*,4κs-b5²]]`，再运输模型误差；其 `trace(G)` 正好是旧 `Rtr`，`det(G)=4κ Rdet`。
- 新的实质 lemma：若 `G=Ghat+E`，则 `det(G)-det(Ghat)=ghat22*e11+ghat11*e22-2*ghat12*e12+e11*e22-e12²`。因此 source 可以直接给这个**相关 determinant correction** 的下界，不必分别 intervalize `4ps-σ²` 和 bias numerator。
- fallback：若只能给 entrywise error radii `eta11,eta12,eta22`，也得到一个完全有理、无除法的 determinant reserve penalty；同时从 `p,s,σ,b4,b5` 的 nominal+error split 推出了三个 `E` 条目的 exact formulas 和 rational radii。
- 重要阻塞：在奇异边界附近不能强制所有 source error 都压成独立 entry radii。精确族 `G(t)=[[1,t],[t,t²]]` 对所有 `t` 都 rank-one PSD 且 `det=0`，direct correlated correction 的损失为 0；但独立半径会产生正 penalty，错误地无法认证。这说明 near-singular lane 必须保留 direct `Cdet` / full `Rdet` enclosure。
- 给其他数学 Agent 的建议：后续若继续做 trig/rational/Taylor source approximation，应先形成 signed `G` 或 `Cdet` 再做 enclosure；不要在 determinant 因子层提前绝对值化。Bernstein 可以用于 nominal reserve，也可以直接用于 correlated correction polynomial。
- 给 Lean Agent 的建议：最小形式化只需 2×2 三标量版本的 `det2_add_exact`、entry-radius lower bound、source-variable→matrix-error 三个恒等式，再调用现有 branch-free consumer；无需矩阵逆、谱或伪逆 API。
- 尚未闭合：真实 source 的 nominal/error split、trig/Taylor enclosure、Float64/outward rounding、same-key cell、κ 选择、P8 coverage、Lean/kernel/comparator/admission。
- 关联：`T-P5-BRANCHFREE-AFFINE-MAJORANT`、`T-P5-045`、`T-P5-051`、`T-P5-052`、`T-P5-053`。
