---
kind: task_claim
task_id: T-P5-110-APPROXIMATE-REFERENCE-RECENTERING
source_agent: 红莲魔尊
created_at: 2026-09-08T23:50:00Z
status: claimed
integration_status: pending
---

# 红莲魔尊 claim — T-P5-110 approximate reference recentering

本轮未发现梁智炜对红莲魔尊的新点名任务。T-P5-107/108/109 已分别由柳冠一、古月方源、狂蛮魔尊推进 ramp-corner、hybrid dwell 与 sharp jump/reset，因此本 claim 不重复这些方向。

我认领一个与 T-P5-106 obstruction 直接衔接、但互不抢占的最小数学 child：当 deployed/source semantics 下不能证明 exact `B a = g` 时，研究 position recentering `z=q-a w, s=v` 的 **amplitude-mismatch / slope-sensitivity tradeoff**。目标是：

1. 推导 exact recentered energy identity，保留 `delta(a)=g-Ba` 的 signed amplitude term与 `a` 引入的 slope term；
2. 在给定 dissipation quadratic form `Q` 下构造 source-independent、square-only 的 joint forcing budget；
3. 给出选择 `a` 的 convex quadratic normal equation / exact rational gate，使 `a` 不必被强制为 exact static equilibrium shift；
4. 记录何时 exact recenter `Ba=g` 反而不是总 collar cost 的最优选择，以及缺少 input amplitude/slope packet 时的精确 obstruction。

边界：只做数学/能量设计，不做 T-P5-109 jump-reset sharpness、Lean compile、source/provenance/admission/registry；actual referenceKey 绑定保持显式 open。
