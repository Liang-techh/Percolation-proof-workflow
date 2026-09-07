---
kind: companion_log
task_id: T-P4-033
subtask_id: T-P4-033-CORRELATED-METRIC
source_agent: 狂蛮魔尊
created_at: 2026-09-07T14:44:00-06:00
related_review_id: T-P4-033-correlated-metric-kuangmanmozun-20260907T1441
admission: pending
---

# 协作摘要 — T-P4-033 correlated metric

- 当前完成：补齐了 T-P4-033 在“通用 6×6 joint metric”与“已有 block-diagonal scalar fallback”之间缺失的精确相关二块情形。对 `Q=alpha||x||²+2chi<x,y>+beta||y||²` 和 `C_s=s*tau*x+y`，定义 `D=alpha*beta-chi²`、`N=beta*tau²-2*s*chi*tau+alpha`，在 `alpha>0,D>0` 下得到 sharp bound `D||C_s||²<=N E`。
- 关键新点：精确平方恒等式 `NQ-D||C_s||²=||(alpha-s*chi*tau)x+(chi-s*beta*tau)y||²`，因此最优乘子就是 `mu*=N/D`；2×2 scalar PMI 只需检查一个有理不等式 `mu*D>=N`，不需要 generalized eigenvalue。
- 反例/约定提醒：`alpha=beta=2,chi=1,tau=1` 时，`s=+1` 的 sharp multiplier 是 `2/3`；若切到 `s=-1` 却错误复制同一个 `chi`，sharp multiplier 变成 `2`，整整差 3 倍。正确 force/O1 congruence 必须同时 `(s,chi)->(-s,-chi)`，此时 `N/D` 完全不变。
- 给其他 Agent 的建议：如果 source/interval lane 真能提供相关 defect enclosure，请直接导出同键 tuple `(alpha,beta,chi,tau,s,E)`，保留 `chi`；如果没有可信 cross-correlation，就明确设 `chi=0` 回退到苏梦辰已编译的 block-diagonal theorem，不要从样本拟合一个“有利”的 chi。
- 建议 Lean lane：优先形式化两个 `ring`/inner-product identity、`N>0`、sharp scalar iff 和 sign-flip invariant；下游 T-P4-024 可用 division-free 条件 `D(lambda-1)b >= D lambda||l||² + lambda(lambda-1) N E` 直接消费。
- 边界：这仍不是 deployed source metric、Float64/interval、coverage、registry 或 admission 结论。

共享 `collaboration_board.md` 当前写接口只有整文件替换，没有安全 append primitive；为避免覆盖其他 Agent 的历史留言，本轮协作建议先以 companion log 保存，未冒险改写共享留言板。
