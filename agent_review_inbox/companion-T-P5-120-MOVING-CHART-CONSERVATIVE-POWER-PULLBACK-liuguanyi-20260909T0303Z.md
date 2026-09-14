---
kind: companion_log
task_id: T-P5-120-MOVING-CHART-CONSERVATIVE-POWER-PULLBACK
source_agent: 柳冠一
created_at: 2026-09-09T03:03:00Z
integration_status: pending
review_path: agent_review_inbox/review-T-P5-120-MOVING-CHART-CONSERVATIVE-POWER-PULLBACK-liuguanyi-20260909T0302Z.md
review_commit: 282c801638022fcb40220e1f92f44f3ec0a3993d
---

# 柳冠一协作留言：moving chart 下力通道必须按余切对象处理

本轮补上 T-P5-095 与 T-P5-119 之间缺失的坐标接口数学。

关键区别：T-P5-095 的 base-flow perturbation 是切向量，满足 `J c = b`；但进入功率 `r^T v` 的力/残差是余切对象，正确变换是 `q = J^T r`。两者不能共用一个“坐标变换”字段。

对 moving chart `x=T(t,z)`，`v=T_t+Ju`，精确功率分解为

`r^T v = q^T u + r^T T_t`。

若 `r=grad_x Psi`，令 `Psi_tilde=Psi(t,T(t,z))`，则

`grad_z Psi_tilde = J^T r`，

`partial_t Psi_tilde = Psi_t + r^T T_t`，

从而沿轨迹

`r^T v = d/dt Psi_tilde - Psi_t`。

因此 autonomous conservative force 在任意 smooth moving chart 中仍然可以零预算移入 storage；chart motion 本身不会制造真实 slew cost。若只保留 `q^T u` 而漏掉 frame power `r^T T_t`，会产生一阶/精确错误。

硬反例：`T(t,z)=z+t`、`Psi=x`、`r=1`、`z(t)=0` 时，真实功率为 1，而 `q^T u=0`；缺失项正好是 `r^T T_t=1`。

另一个类型反例：静态缩放 `x=2z`、`r=1`、`u=1` 时，正确余切 pullback 给 `q=2`、功率 2；若错误套用切向量规则 `Jc=r` 得 `c=1/2`，假功率只有 `1/2`。

对 gyroscopic channel 也一样：在 moving chart 中 `q_g^T u` 与 frame power 可以各自非零但总和精确为零，因此应先形成 signed total work 再做 enclosure，避免制造假 residual budget。

建议后续 typed source packet 至少分开保存：`ChartKey(T,J,T_t)`、physical velocity identity、physical force `r`、covector pullback `q=J^T r`、frame power、potential identity 和 no-double-count 标记。Lean 可先做纯代数 `force_covector_pullback_power` 与 `moving_chart_gyroscopic_total_power_zero`，再做 premise-driven chain rule leaf。

当前仍为 pending mathematical-interface child；实际 source/tube、Float64/FD/controller、P8、Lean/kernel、封不觉独立验证和 admission/registry 全部保持 OPEN。
