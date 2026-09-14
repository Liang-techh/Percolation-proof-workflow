---
kind: companion_log
review_id: review-T-P5-127-moving-recenter-envelope-tracking-guyuefangyuan-20260909T0530Z
task_id: T-P5-127-MOVING-RECENTER-ENVELOPE-TRACKING
source_agent: 古月方源
created_at: 2026-09-09T05:34:00Z
inspected_commit: 8771585ea270185eaecabbcbef960b0fb2579a87
integration_status: pending
---

# T-P5-127 中文协作接力

- 当前完成：承接 T-P5-125/T-P5-126 的 time-dependent recenter 缺口，得到两时间 critical-center drift、瞬时 center-speed、same-cell drift、exact potential-gap envelope identity，以及 temporal-gradient/temporal-Hessian 的 mixed small-gain closure。
- 最重要的新结构：对 `W(t,q)=F(t,q)-F(t,q_*(t))`，因为 `grad F(t,q_*)=0`，链式法则里没有额外独立的 `q_*dot` debit；真正留下的是 `partial_t F(t,q)-partial_t F(t,q_*)`。不要在 moving coordinates 和 potential-gap derivative 两边重复收费。
- center tracking 可完全不写 Hessian inverse：两时间形式直接有 `4 mu^2 Q(q_*(t1)-q_*(t0)) <= G01`；瞬时形式有 `4 mu^2 Q(q_*dot)<=G_*`。
- temporal power 的推荐拆分：`partial_tF(q)-partial_tF(q_*) = <partial_t gradF(q_*),x> + temporal-Hessian weighted integral`。前者是一阶 center-translation 项，后者是二阶 curvature 项。
- sharp gate：center-linear 项若只给 dual quadratic bound `G0`，则必须消费 mixed budget `G0 <= 4 mu alpha beta`；`beta=0` 在非零 moving center 情况一般不可能。例子 `F(t,q)=mu(q-vt)^2` 精确取等，说明 additive floor 不是 Young 松界。
- 二阶 temporal-Hessian 项若保留 signed upper `2 ell Q(x)`，则只需 `ell<=mu eta` 就可纯 relative 吸收；建议 source 先形成 signed scalar power 再 intervalize，不要先逐项取绝对值。
- nonlinear moving chart 在 exact physical critical center 处还有额外 cancellation：pulled-Hessian 的 connection term 因 `gradF=0` 消失，`J_t^T gradF` 也消失，最终仍回到物理 `H q_*dot + partial_t gradF=0`。但这要求 chart criticality 真能升级为 physical criticality，`ker(J^T)=0` 边界不能丢。
- 给其他 Agent 的建议：下一步不要再做 generic strong-convexity。优先找 actual same-key `partial_t gradF`、signed `partial_t HessF`、reference schedule/time strip 与 same-cell coverage；若真实 reference 是 piecewise constant/affine，则应分段证明这些项为零或有界，并把 knot jump 交给已有 hybrid jump/dwell lane。
- 关联：`T-P5-124`、`T-P5-125`、`T-P5-126`、`T-P5-127`；正式 review commit `8771585ea270185eaecabbcbef960b0fb2579a87`。

说明：共享 `collaboration_board.md` 当前可用写接口仍是整文件 replacement；在无法安全取得完整尾部并原子 append 的情况下，本轮不覆盖共享留言板，以上中文建议先以 companion 形式保留，供梁智炜收割时安全追加。