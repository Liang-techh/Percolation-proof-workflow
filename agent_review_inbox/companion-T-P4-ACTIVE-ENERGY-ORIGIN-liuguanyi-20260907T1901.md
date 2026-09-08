# 柳冠一协作摘要 — T-P4-ACTIVE-ENERGY-ORIGIN

本轮没有接手 provenance、receipt、admission 或重复审计，而是补了 active-energy origin 后面真正缺的数学桥：物理势能进入 `U(q)-U(0)` 归一化储能时，正确的 typed contract 应是“相对同一锚点的势能差相等”，而不是要求两个 raw potential 的绝对常数完全相同。

给后续 Agent 的关键结论：若两套势能在同一 source-covered 连通链上只相差常数，则它们产生的 normalized energy 完全一致；更一般地，若每段上两套势能差的路径导数误差不超过 `ε_r`，则 normalized storage 的误差不超过 `Σ ε_r`，可直接作为 `OneSidedComparison` 的 `delta`。这允许 source/Jacobian lane 用真实 cell-chain 证明 storage transfer，而不用伪造 raw potential equality。

请特别注意两个边界。第一，当前 `sourceG` 是 fixed-step central finite-difference 对象，不能未经定理直接当成 analytic derivative premise。第二，对 BODY6 的“原点属于 active domain”这一个点来说，全局 gauge-equivalence 仍然是过强前提；最小 obligation 只是实际 candidate 的 `V(0,0)≤1`，或把它在原点绑定到已经显式归一化的 `normalizedEnergy`。不要因为本轮补了全局 bridge，就把 one-point obstruction 重新升级成大规模 source audit。

正式推导、反例、最小 theorem statements 与剩余边界见：`agent_review_inbox/review-T-P4-ACTIVE-ENERGY-ORIGIN-liuguanyi-20260907T1900.md`。
