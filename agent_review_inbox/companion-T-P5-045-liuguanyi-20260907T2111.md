---
kind: companion_log
review_id: companion-T-P5-045-liuguanyi-20260907T2111
task_id: T-P5-045
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-07T21:11:00-06:00
related_review: review-T-P5-045-liuguanyi-20260907T2108
review_commit: da4bb4f34f20a884ac95b2a808d454159196c5fd
integration_status: pending
admission_label: pending
---

# T-P5-045 协作摘要

本轮已读取 `README.md`、`task_queue.md`、`collaboration_board.md` 与柳冠一上一轮之后的新提交；未发现梁智炜新的点名，因此没有转去做 audit/provenance/admission，也没有抢占苏梦辰、巨阳仙尊、古月方源、狂蛮魔尊、红莲魔尊正在推进的 P5-040/042/043/044 工作。

本轮补的是红莲魔尊 `T-P5-044` 明确留下的 source-to-math 缺口：状态相关 signed `2x2` residual block 只有区间信息时，怎样稳健地进入 correlated Lyapunov gate，同时不破坏 skew/cross cancellation。

关键接口应改为先形成三个 signed symmetric invariant：

```text
p = a4(r)+k44,
s = 1/6+k55,
sigma = k45+k54,
D4 = 4*p*s-sigma^2.
```

这样 `D4=4 Delta`，而 correlated bias 可直接写成

```text
B = s*b4^2-sigma*b4*b5+p*b5^2.
```

所以原 `T-P5-044` quarter gate 可完全无 `/2`、`/4` 地改写成

```text
800 B < (109-r) D4.
```

若同一 cell 上有 rational bounds `pL/pU,sL/sU,|sigma|<=Q`，定义

```text
Dmin = 4*pL*sL-Q^2.
```

只要 `pL>0,Dmin>0`，就自动得到整 cell 的 `p>0,s>0,D4>=Dmin>0`。若再有 `|b4|<=beta4, |b5|<=beta5`，则

```text
Ebox = sU*beta4^2 + Q*beta4*beta5 + pU*beta5^2
```

统一控制 `B<=Ebox`。因此只需检查

```text
800 Ebox < (109-rU) Dmin
```

即可推出整 cell 的 correlated quarter barrier。若覆盖整个 `r in [0,1]`，它进一步简化成非常干净的 exact-rational 条件

```text
200 Ebox < 27 Dmin.
```

对应 `Kc=1/12` 的 parameter/incremental tube 则简化为

```text
200 Eg < 9 Dmin.
```

本轮最重要的 source 提醒：`k45,k54` 绝不能先分别取绝对值再相加。应先在 signed interval 中形成 `sigma=k45+k54`，再给 `|sigma|<=Q`。对纯 skew 例子 `K=[[0,M],[-M,0]]`，真实 `sigma=0`，能量代价与 `M` 无关；若先 absolute，则会得到伪造的 `Q=2|M|`，甚至把真实始终正的 determinant lower bound 错判为负。这是信息丢失 obstruction，不只是常数保守。

建议 source/checker 下一步优先保留 `(u,x,parameter)` 坐标下的 signed `J_u`，输出 `k44/k55/(k45+k54)` 的同 cell rational enclosure；transverse/anchor 项再进入 `b`。若 source 能直接给 `-sigma*b4*b5<=chi`，还可用 correlated cross cap 进一步替代 `Q*beta4*beta5`。

建议 Lean 最小接口为：`scaled_correlated_invariants`、`scaled_symmetric_det_lower_of_interval`、`scaled_adjugate_bias_le_box`、`scaled_adjugate_bias_le_cross_cap`、`correlated_quarter_gate_of_interval_box`、`correlated_one_twelfth_parameter_gate_of_interval_box`。本轮未做 Lean compile、source/Float64、coverage、receipt、registry 或 admission；结果保持 `pending mathematical/interface child`。
