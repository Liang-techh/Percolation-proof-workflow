---
kind: companion_log
task_id: T-P5-176-PERSISTENT-RANK-STRATUM-COMMON-KERNEL-EXCLUSION
review_id: review-T-P5-176-persistent-rank-stratum-common-kernel-exclusion-kuangmanmozun-20260909T1830Z
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-09T18:31:00Z
review_commit: 688765cc6802a5dd1b821bf0590276ba16d7e3ab
status: pending
---

# T-P5-176 协作说明

- 当前完成：补上 T-P5-175 明确保留的 persistent high-corank 分支。证明对称仿射矩阵束 `A_s=A+sL` 若在某点 `A>=0`、`rank(A)=r`，且整个局部/多项式族始终 `rank<=r`，那么 `ker(A)` 必须同时落在 `ker(L)`；PSD 会把一般奇异 pencil 的 moving-kernel 行为冻结成 common kernel。
- P5 特化：对 `L_g=(g1^T+1g^T)/2`，只要当前 active support 上 `g` 不恒为零，则 `ker(L_g)` 中不存在任何非零非负向量。因此 physical positive-support zero contact 不可能位于 persistent rank stratum；在候选的实际 rank 上必有至少一个 next-size minor 是非零多项式。
- 对现有路线的直接影响：高余维 physical contact 不再需要“persistent Grassmann/common-kernel open branch”。corank-one 继续走 T-P5-173；corank>=2 只要是 physical contact，就必然落入 T-P5-175 的 isolated algebraic packet，候选参数仍至多二次代数。
- 失败边界：去掉 PSD 后存在 exact moving-kernel 反例 `[[0,0,-D],[0,0,1],[-D,1,0]]`；去掉非平凡 loading 后，常矩阵 `[[1,-1],[-1,1]]` 可有 persistent positive kernel `(1,1)`。因此这两个前提都不能静默删除。
- 给其他 Agent 的建议：后续 checker 在实际 support 上先判断 next-size minors 是否全恒零；若全恒零且 active PSD、`g_S!=0`，可直接返回 `PERSISTENT_PHYSICAL_CONTACT_IMPOSSIBLE`，不要再做 algebraic kernel continuation、pseudoinverse 或 Grassmann transport。只有 generic/debug 非物理矩阵束才保留 persistent branch。
- 仍未升级：actual `{g_i,K_ij,D}` source、same-key simplex/cell、coverage、Float64、Lean/kernel、封不觉独立验证、registry/admission、P5/P8/M4 parent closure 全部保持 open。
