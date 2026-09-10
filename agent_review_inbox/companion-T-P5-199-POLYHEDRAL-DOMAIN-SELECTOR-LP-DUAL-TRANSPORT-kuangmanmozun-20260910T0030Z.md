---
kind: companion_log
task_id: T-P5-199-POLYHEDRAL-DOMAIN-SELECTOR-LP-DUAL-TRANSPORT
source_agent: 狂蛮魔尊
created_at: 2026-09-10T00:30:00Z
integration_status: pending
review_path: agent_review_inbox/review-T-P5-199-POLYHEDRAL-DOMAIN-SELECTOR-LP-DUAL-TRANSPORT-kuangmanmozun-20260910T0030Z.md
review_commit: 04872637e1d211b2e91bb7be8bce2894ba043624
admission_label: pending
---

# T-P5-199 协作说明 — 狂蛮魔尊

本轮已读取 `README.md`、`task_queue.md`、`collaboration_board.md` 和最新消息。梁智炜没有新的直接点名；古月方源已在本轮之前认领 `T-P5-198-QUADRATIC-DOMAIN-RADIAL-CAP-COPOSITIVE-REDUCTION`，因此本任务严格避开二次型/椭球域路线，只处理 T-P5-197 明确留下的**多面体状态域到 selector 系数上界**问题。

本轮新增的关键结论如下。

1. 若 `e=Vy`、`y>=0`，实际域为 `Ae<=d`，则要证明 `w^T y<=R`，不需要也不应该构造 `V^{-1}`。只需给出 exact dual multiplier `lambda>=0`，验证 `(AV)^T lambda>=w` 与 `d^T lambda<=R`。这三组都是有限维有理线性不等式。

2. 对 T-P5-197 来说，可以进一步直接对 amplitude majorant `beta` 做 dual support bound：若 `(AV)^T lambda_beta>=beta` 且 `d^T lambda_beta<=B`，则直接得到 `beta^T y<=B`，最终 defect matrix 使用 `(h0+B)Q+sym(beta c^T)`。这通常比先找 `w,R,kappa` 再取 `B=kappa R` 更紧，也减少一个人为 gauge 层。

3. 找到一个必须保留的 representation-gauge obstruction：即使物理状态 polytope 是有界的，只要存在 `r>=0`、`Vr=0` 且 `w^T r>0`，selector 系数上界仍然不存在。最小反例是 `V=[1,-1]`、状态域 `[-1,1]`、`w=(1,1)`；`y=(t,t)` 永远映到同一个状态 `0`，但 `w^Ty=2t` 无界。因此“状态域有界”绝不能直接替代“selector 系数有界”。

4. 若状态 polytope 本身有界且 pullback 非空，则 selector feasible set 的所有 recession direction 恰好就是 `ker(V)∩R_+^p`。所以在这种常见情形下，radial cap 存在与否可以先做一个纯 selector gauge 检查，再决定是否生成 LP dual certificate。

给其他数学 Agent 的建议：T-P5-198 完成前不要重复二次域 radial-cap 推导；它完成后若继续推进，最值得研究的是“多面体约束 + 二次域约束”的混合 support certificate，目标应该是组合 T-P5-198 与 T-P5-199，而不是重新做其中任一分支。

当前没有升级 actual `A,d,V,beta` source binding、domain nonempty/coverage、Float64/interval、final copositivity、Lean/kernel、封不觉独立验证、admission、registry 或 P5/P8/M4 parent closure。正式数学内容与 theorem statements 见对应 review_result。
