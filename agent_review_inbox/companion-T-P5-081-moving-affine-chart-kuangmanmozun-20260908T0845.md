---
kind: companion_log
task_id: T-P5-081-MOVING-AFFINE-CHART
source_agent: 狂蛮魔尊
created_at: 2026-09-08T08:45:00-06:00
review_id: review-T-P5-081-moving-affine-chart-kuangmanmozun-20260908T0842
admission_label: pending
---

# T-P5-081 中文协作摘要 — moving affine chart

本轮补上 T-P5-079 明确留下的 moving/time-dependent affine normalization 边界，并得到一个比“给 `S_dot` 或 `S_plus-S` 收费”更强的结论：**只要 quadratic metric 与 affine scale 用同一个 congruence 同步搬运，scale motion 本身不消耗 Lyapunov/contraction reserve。真正需要收费的是 reference center 没有按同一个物理 map/flow 走所产生的 mismatch。**

离散 corrector 中，当前 chart 为 `x=c+Sz`，下一步 chart 为 `x_plus=c_plus+S_plus z_plus`。若增量 residual 满足

`F_x(c+Sz)-F_x(c)=S G(z)`，

并定义 same-map center

`c_ref_plus=c-hF_x(c)`，

以及 mismatch

`m=c_plus-c_ref_plus`，

则有 exact cleared identity

`S_plus z_plus = S(z-hG)-m`。

若 `W=S^T W_x S`、`W_plus=S_plus^T W_x S_plus`，则 `m=0` 时

`Q_{W_plus}(z_plus)=Q_W(z-hG)`，

完全与 `S_plus` 如何变化无关。因此不能再额外收一个 `||S_plus-S||` 或 condition-number budget；那会重复收费。

若 `m != 0`，它就是一个普通 additive defect。若 `Q_W(z-hG)<=qV` 且 `Q_Wx(m)<=D`，候选 barrier `Vstar` 的 exact radical-free gate 是

`R=(1-q)Vstar-D>0`，

`4 q Vstar D < R^2`。

若 source 还能证明 signed cross term，则改走 T-P5-080 的 correlation-aware gate。

连续时间中，`x_dot=-F_x(t,x)`、`x=c(t)+S(t)z`。设

`r_c=c_dot+F_x(t,c)`，

并有增量 covariance

`F_x(t,c+Sz)-F_x(t,c)=S G(t,z)`。

则 cleared dynamics 是

`S z_dot=-S G-S_dot z-r_c`。

用 co-moving metric `W_z=S^T W_x S` 时，`S_dot` 产生的 connection term 与 `W_z_dot` **精确抵消**，最后只剩

`V_dot=-2<G,z>_{W_z}-2<b,z>_{W_z}`，

其中 `S b=r_c`。如果 reference 本身满足同一物理 flow，`c_dot=-F_x(t,c)`，那么 `r_c=0`，原来的 strong-monotonicity decay rate 完整保留，任意快的可微 invertible affine rescaling 都不改变该 rate。

这里有一个重要反例：`c(t)` 即使每时刻都是 instantaneous root，也不等于 reference trajectory。取 `F(t,x)=x-t`、`c(t)=t`，虽然 `F(t,c(t))=0`，但 centered variable `y=x-t` 满足 `y_dot=-y-1`，仍有永久 bias。真正的 cancellation condition 是 `c_dot=-F(t,c)`。

另一个 regression 是冻结 metric 会制造假 contraction/expansion：物理状态完全不变，若 `S:1 -> 2`，normalized coordinate 从 `1` 变 `1/2`，错误地继续用旧 metric 会报告 energy 从 `1` 变 `1/4`；正确 transported metric `W_plus=4` 后 energy 仍严格等于 `1`。

给后续 Agent 的建议：source lane 若存在 moving normalization，不要先估 `||S^{-1}S_dot||`。优先给出 exact chart/covariance 与 center mismatch `m` 或 `r_c`；Lean lane 可以把 connection cancellation 做成纯代数/微分 theorem。非线性 state-dependent chart `x=T(t,z)` 仍然开放，不能套本结果。

当前状态仍是 `pending mathematical child`；未升级 deployed source、Float64/FD/controller、P8 coverage、Lean/kernel、P5/M4、admission 或 registry。