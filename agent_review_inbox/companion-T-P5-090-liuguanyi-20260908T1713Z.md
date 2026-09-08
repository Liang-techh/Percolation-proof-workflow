---
kind: companion_log
task_id: T-P5-090-MOVING-METRIC-CONTRACTION-CONGRUENCE
review_id: review-T-P5-090-moving-metric-contraction-congruence-liuguanyi-20260908T1710Z
source_agent: 柳冠一
created_at: 2026-09-08T17:13:00Z
integration_status: pending
---

# T-P5-090 中文协作接力

本轮补的是 T-P5-082/T-P5-088 之间仍缺的一层：**状态/时间依赖 metric 下的 differential contraction 如何穿过 moving nonlinear chart。** 这和 T-P5-087 的“用 moving metric 测量 Euler defect”以及 T-P5-088 的“状态 storage 导数”都不同，因此没有重复抢占。

物理系统写成 `xdot=-F`、`A=D_xF`，metric 为 `W(t,x)` 时，必须先形成完整 material derivative

`L_F W = W_t - D_xW[F]`

和完整 contraction tensor

`C_x = A^T W + W A - L_F W`。

若 moving chart 为 `x=T(t,z)`、`J=D_zT`，normalized field 满足 `JG=F(T)+T_t`，并记 `B=D_zG`、`M=J^T(W o T)J`，则本轮证明了精确恒等式

`B^T M + M B - (M_t-D_zM[G]) = J^T C_x J`。

因此物理侧只要有 `C_x >= 2 mu W`，normalized side 就自动有

`C_z >= 2 mu M`，

而且 **同一个 `mu` 原值保留**。前向证明只是把物理 quadratic-form inequality 代入 `xi=J eta`，不需要 `J^{-1}`、sqrt、广义特征值或矩阵求逆。

给 source/CSE lane 的关键建议：不要把 `B^TM`、`MB`、`-M_t`、`+DM[G]` 或展开后的 `J_t/DJ[G]/W_t/DW[...]` 分别绝对值化收费。它们之间有 exact connection cancellation；应先形成完整 signed contraction tensor，再 enclosure。

两个反例也已经写入正式 review。其一，`F=0,W(t)=1+t` 时真实 variational energy 增长，若漏掉 `W_t` 会错误判成不增。其二，`F=0,W=1,T(t,z)=(1+t)z` 时 normalized Jacobian 看起来产生正 contraction，但 pulled metric 的 `M_t` 精确把它抵消，最终 `C_z=0`；冻结 `M` 会凭空制造 contraction。

建议 Lean lane 后续先做纯代数叶 `contraction_rate_pullback`，再分别做 `moving_chart_variational_connection`、`pullback_metric_material_deriv` 和完整 tensor congruence。T-P5-088 的 state-storage theorem 与本 theorem 可共用 material-derivative 定义，但不要合成一个过载 theorem：一个作用于状态 storage，一个作用于 variational energy。

边界仍保持 open：真实 deployed `W/F/A/T/J/G/B` source binding、same-tube coverage、exact rational tensor lower certificate、metric coercivity、有限步/secant contraction、Float64/FD/controller、P8/ODE coverage、Lean/kernel、封不觉独立验证以及 admission/registry。本结果仍只是 pending mathematical/interface child。
