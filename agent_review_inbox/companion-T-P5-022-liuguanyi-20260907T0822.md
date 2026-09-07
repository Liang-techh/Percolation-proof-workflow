---
kind: companion_log
task_id: T-P5-022
source_agent: 柳冠一
created_at: 2026-09-07T08:22:00-06:00
related_review: review-T-P5-022-liuguanyi-20260907T0820
---

# T-P5-022 协作交接

本轮把 `T-P5-020/T-P5-021` 的 `ell2/B2` 消费接口补成了真正带坐标语义的 source adapter。source/checker 不应只输出一个“Jacobian norm”，而应显式输出状态 transport `S`、force map `A`、Jacobian 绝对值界 `H` 与 nominal-anchor component box `c`；随后按有限和计算 `K=A_abs*H*S`、`ell2=sum K^2` 与 `B2=sum (A_abs*c)^2`。

最重要的跨层边界有两个。第一，若 actual/nominal 在 P8 中共享同一个 `w=c0*t,c=c0`，这些 source 坐标的差为零，对应 `S` 行可直接置零，因此即使 residual 对 ramp 坐标敏感，也不应给 centered gain 收费。第二，若 residual 依赖某个会独立于 block-(4,5) error 变化的 distal/full-state 坐标，则四维 `N=||(x4,x5,y4,y5)||^2` 无法吸收它；必须证明 transport、扩大 Lyapunov state，或把它改走 additive/transverse 路线。

force normalization 只能做一次：raw PMI residual 才取 `A=diag(1/5,1/10)`；若上游已经是 `DHPowerBinding.forceError`/generalized-force，则必须取 `A=I`。否则会把平方 budget 错缩到 `1/25` 或 `1/100`。

形式化 Agent 最小可拆 `transported_jacobian_centered_gain`、`force_map_anchor_box_to_B2` 与 diagonal rational corollary；source/P8 lane 则需给同域 `S/A/H/c` 的真实 binding。当前仅 `pending`，待封不觉独立验证 / 待梁智炜收割与最终整合。
