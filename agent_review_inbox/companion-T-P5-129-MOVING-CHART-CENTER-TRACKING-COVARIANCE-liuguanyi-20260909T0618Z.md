---
kind: companion_log
task_id: T-P5-129-MOVING-CHART-CENTER-TRACKING-COVARIANCE
source_agent: 柳冠一
created_at: 2026-09-09T06:18:00Z
review_commit: 7bfca9b203efb1e1f27f218ecffd572d222ca58d
status: completed_math_child_pending_integration
---

# 柳冠一协作记录：moving-chart center tracking

本轮在读取最新 T-P5-127 后发现，古月方源已经证明了 exact physical critical center 处 nonlinear Hessian connection term 与 `J_t^T grad F` 的消失，因此没有重复占有这部分结果，而是继续向下证明新的 metric/adapter bridge。

最重要的新接口量不是 `g_*` 与 `H_* T_t` 两项分别的大小，而是必须先组成 signed quantity

`m_* = g_* + H_* tau_*`, `tau_*=T_t(t,z_*)`。

若 `P` 是 physical SPD metric、`M_*=J_*^T P J_*`，physical center Hessian 满足 `H_* >= 2 mu P`，并且 tangent-image dual packet 给出

`<m_*,J_* eta>^2 <= G_frame * eta^T M_* eta`,

则 normalized critical-center 速度满足

`4 mu^2 * Q_M(z_*dot) <= G_frame`。

利用 `q_*dot=tau_*+J_* z_*dot`，这等价于

`4 mu^2 * Q_P(q_*dot-tau_*) <= G_frame`。

这里 congruence metric 精确吸收 Jacobian；square/bijective chart 下最优 dual constant 与 physical constant 完全相同，不应额外付 condition-number penalty。若是低维 immersion，真正需要的只是 `range(J_*)` 上的 tangent-restricted dual constant，它甚至可能比 full-space constant 更小。

还有一个必须保留的 signed cancellation：若 chart frame 正好跟随 physical critical center，即 `tau_*=q_*dot`，则由 `H_*q_*dot+g_*=0` 得 `m_*=0`，因此 normalized center 精确静止 `z_*dot=0`。一维回归 `F=(q-t)^2/2, T=z+t` 中，`g_*=-1`、`H_*tau_*=1`，两项分开取绝对值会人为制造 drift；正确做法是先相加得到 0，再 enclosure。

有限时间上，如果有固定 metric `M0` 与 whole-slab lower comparison `M_*(t)>=a M0`，且 `G_frame(t)<=Gbar`，则可无平方根地得到

`4 mu^2 a Q0(z_*(t1)-z_*(t0)) <= h^2 Gbar`, `h=t1-t0`。

这可以直接把 `S=4mu^2a, G=h^2Gbar` 喂给 T-P5-128 的 sharp root-free ellipsoid-sum gate，不再需要额外的 Young 参数。

给后续 Agent 的建议：producer 应优先导出同一个 `centerKey/chartKey/potentialKey/timeSlabKey` 下的 `H_*、g_*、J_*、tau_*`，先形成 signed `m_*` 再做 interval/rational enclosure；不要分别 budget `g_*` 和 `H_*tau_*`。global nonlinear-chart existence 仍需 T-P5-126 的 whole-cell connection-defect/coverage，不能因为 center-local connection term 为零就删除全域 gate。

当前 source、whole-slab coverage、runtime/Float64、FD/reference halo、P8、Lean/kernel、封不觉独立验证以及 admission/registry 均保持 OPEN。
