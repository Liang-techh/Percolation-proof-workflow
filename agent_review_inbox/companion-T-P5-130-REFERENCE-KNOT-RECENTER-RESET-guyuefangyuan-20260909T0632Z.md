---
kind: companion_log
review_id: companion-T-P5-130-reference-knot-recenter-reset-guyuefangyuan-20260909T0632Z
task_id: T-P5-130-REFERENCE-KNOT-RECENTER-RESET
source_agent: 古月方源
created_at: 2026-09-09T06:32:00Z
related_review: review-T-P5-130-reference-knot-recenter-reset-guyuefangyuan-20260909T0630Z
review_commit: 7c48ca222df55971d46c3a1ec6b37cdd5aba27c9
claim_commit: 059a581140cf62946017798da46788b0ff5efa4c
status: pending
integration_status: pending
admission_label: pending
---

# 古月方源协作接力 — T-P5-130

本轮补的是 T-P5-127 连续 moving-recenter 之后真正的 reference/potential knot：物理状态可以连续，但 pre/post potential-gap storage 本身会换定义，因此必须做 reset theorem，不能继续把它当连续时间项。

得到的最小消费者如下：设 old-center gradient mismatch 的 dual budget 为 `B`，post potential 的强凸常数为 `mu`，pre storage coercivity 为 `m`，signed Hessian-jump 上界为 `ell`。选择 `alpha>0, eta>=0, El>=0, Ec>=0`，只需检查

- `B <= 4*mu*Ec`；
- `B <= 4*m*alpha*El`；
- `ell <= m*eta`；

即可推出

`W+ <= kappa W- + E`,

其中 `kappa=1+alpha+eta`、`E=El+Ec`。

这两个 `B` 收费不是重复 Young 造成的假损失。一维平移例 `F-=mu x^2, F+=mu(x-a)^2` 精确取到最小 additive reset

`E_min = mu a^2 (1+1/alpha)`，

恰好等于 `Ec_min+El_min`。所以真实 center jump 在 old center 处就有 `W-=0, W+>0`，不存在任何有限的纯 homogeneous reset。

它与 T-P5-108 的 dwell recovery 接起来后，若正超额的 flow certificate 是 `P A- <= QN A0`，则 affine reset 的固定 headroom gate 变成

`kappa*QN*H + P*((kappa-1)R0+E) <= P*H`。

对 `nu=9/20` 可取 `P=(20N+9h)^N, QN=(20N)^N`。`N=1` 时直接得到

`(20+9h)*((kappa-1)R0+E) <= (9h-20*(kappa-1))*H`。

因此 `kappa>1` 时必须先有足够 dwell 抵消 multiplicative tax；零 dwell 下除非 `kappa=1,E=0`，固定 headroom 不可能闭合。

给梁智炜/其他 Agent 的协作建议：下一条 source lane 不要再做 generic convexity，而应冻结一个同键 pre/post knot packet：`referenceKey, F-/F+, q-/q+, Q, mu, m, g/B, DeltaH/ell, physical segment coverage, R0/nu, actual dwell`。尤其要确认 T-P5-107 的 controller input jump 与这里的 potential/storage jump 是否是同一个 reference event；若是同一事件，应先写一个 exact combined reset identity，避免把两个描述重复加预算。

Lean 优先级：`center_relocation_cost`、`knot_linear_absorption`、`positive_excess_after_affine_reset`、`hybrid_headroom_step_affine`。这些先做纯标量/二次型代数，actual source 与 calculus specialization 后接。

共享 `collaboration_board.md` 当前连接器只提供整文件 replacement；文件很长且并行 Agent 持续写入，无法安全原子 append 而不承担覆盖历史留言的风险，因此本轮没有重写留言板。上述中文建议完整保存在本 companion，供梁智炜收割后安全追加/路由。
