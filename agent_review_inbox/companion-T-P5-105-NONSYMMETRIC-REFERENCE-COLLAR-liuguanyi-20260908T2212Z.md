---
kind: companion_log
task_id: T-P5-105-NONSYMMETRIC-REFERENCE-COLLAR
source_agent: 柳冠一
created_at: 2026-09-08T22:12:00Z
review_commit: 805f5ac6d2cbbc9bda42a08cf6f01636fe64affc
integration_status: pending
admission_label: pending
---

# T-P5-105 协作补充

本轮补的是 T-P5-104 到真实 Route-B reference block 之间的一条数学断口：T-P5-104 的 generic collar 假设 stiffness 对称，但 T-P5-018 固定的实际 2×2 block 有 `B45=-1/100`、`B54=-1/200`，不能直接把 `B` 当成对称 `K`。正确做法是先写 `B=K-A`，保留 skew `A`，并把 `v^T A q` 放进完整 signed dissipation quadratic form；不能先逐项绝对值化，也不能静默删掉 `Aq`。

已经得到 exact-real bridge：对

`M v' + D v + (K-A)q = g w`

采用 hypocoercive storage

`V=1/2 v^T M v + 1/2 q^T K q + q^T M v + 1/2 q^T D q`

有精确恒等式

`V'=-Qd+w c^T x`，

其中 `x=(q,v)`、`c=(g,g)`，`Qd` 的 block matrix 为 `[[K,A/2],[A^T/2,D-M]]`。这让 nonsymmetric reference 可以继续消费 T-P5-104 的 squared-power absorption，而不改变真实 ODE。

对 T-P5-018 的 rational coefficient packet，本轮找到一组更紧且完全有理的候选常数：

- rate packet：`lambda=9/10`；
- input packet：`chi=3/20`；
- reference-storage 到 P5-098 block budget：`pB <= (67/2)V`。

对应三个 exact PSD matrix 均已用正 leading principal minors 检查。于是若 `w^2<=Wbar`，可取 `theta=1/2`、`beta=3Wbar/40`，得到

`V' <= -(9/20)V + (3/40)Wbar`，

reference collar 的简单 gate 是 `Wbar<=6R`。再若 actual remote budget 有 `pD<=PDbar`，P5-098 的 hybrid anchor 条件由

`2 PDbar + 67 R <= 2 rho`

直接推出。取最小非严格 collar `R=Wbar/6`，在当前 `rho=28/5` 下可压成纯整数 gate：

`60 PDbar + 335 Wbar <= 336`。

这条结果的价值在于：source lane 若选择 canonical RefSpec，不必把整条 `qbar/vbar` trajectory 当 primitive artifact；可改为交付同一 reference/context 的 coefficient semantics、初值绑定、`w^2` 上界和 actual remote `pD` 上界，再由唯一 nominal ODE 与本轮 collar theorem 推导 reference budget。

尚未闭合：真实 `referenceKey` 选择的是哪套 exact coefficient semantics、Julia/Float64 parse/assembly/solve、同一路径上的 `Wbar/PDbar`、reference/actual context identity、FD/reference halo、P8 flowpipe、Lean/kernel、封不觉独立验证与 admission/registry。以上结果继续保持 pending，不改变 P5/P8 parent 状态。
