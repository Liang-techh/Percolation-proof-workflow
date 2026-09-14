---
kind: companion_log
task_id: T-P5-138-RANKONE-SCHUR-RESET-DECOMPOSITION
review_id: review-T-P5-138-rankone-schur-reset-decomposition-guyuefangyuan-20260909T0824Z
source_agent: 古月方源
created_at: 2026-09-09T08:26:00Z
status: pending_handoff
---

# T-P5-138 中文协作接力

本轮补的是 T-P5-137 后面的一个纯数学叶，不是 source/audit/admission。对固定 `tau`，令

`K = H + tau G`, `e = E - C - tau R`。

T-P5-137 的增广 PSD 条件

`[[K,-b/2],[-b^T/2,e]] >= 0`

与下面三个条件严格等价：

`K>=0`, `e>=0`, `4eK-bb^T>=0`。

因此固定参数后的 trusted checker 可以完全不求 `K^-1`、不开平方根，也不必一定做 `(n+1)x(n+1)` 分解；若 source 已有 dual cap `B K-bb^T>=0`，只要再验 `B<=4e` 即可接回 reset theorem。

最重要的新 obstruction 是奇异边界：若存在 `v` 使 `Kv=0` 但 `b^Tv!=0`，则任意有限 `E` 都不可能让 rank-one gate 成立，因为

`v^T(4eK-bb^T)v=-(b^Tv)^2<0`。

这说明 multiplier 搜索如果卡在 singular `K` 上，不能只继续加大 reset floor；要么移动 `tau` 进入内部，要么证明 `b` 正好消掉 nullspace，要么改变 reset geometry。反过来，`K` 不必严格正定：`K=diag(0,1), b=(0,2), e=1` 就是精确可行的 singular 例子，所以后续 Lean/source 接口不要把 `K>=0` 错加强成 `K>0`。

还有一个实现层提醒：**联合搜索 `(tau,E)` 时仍应保留 T-P5-137 的增广 affine LMI。** rank-one 形式虽然等价，但 `4(E-C-tau R)(H+tau G)-bb^T` 对 `(tau,E)` 是非线性的。最合理的分工是：搜索层用增广 LMI；参数冻结后 checker/Lean 可用 rank-one decomposition；奇异点先跑 nullspace obstruction。

给后续 Agent 的建议：

- source/CSE lane：若能拿到真实 same-key `(G,H,b,C,R)`，优先同时保留 frozen `tau,E` 与 `K`，不要先把 full geometry 压回 `(A,B,R)`；若已有 dual-metric witness，直接输出 `B K-bb^T` 的 exact rational PSD 证据。
- Lean lane：先做四个小叶 `quadratic_block_nonneg_of_rankone_domination`、`rankone_domination_impossible_on_null`、`dual_cap_promotes_rankone_domination`、`ellipsoid_reset_of_rankone_domination`；最后再做矩阵版 iff。前四个基本只需要实数平方、序关系和 `nlinarith`。
- 搜索/设计 lane：不要因为本 review 出现 rank-one gate 就把现有 affine SDP/LMI 改成非线性搜索；两种表示职责不同。

当前仍缺真实 knot/source packet、same-cell coverage、完整 reset term accounting、Float64/controller/P8、Lean/kernel、封不觉独立验证和 admission/registry。正式 review commit 为 `2a86f55903249300cd2bde81f678f1e34f7493f1`。