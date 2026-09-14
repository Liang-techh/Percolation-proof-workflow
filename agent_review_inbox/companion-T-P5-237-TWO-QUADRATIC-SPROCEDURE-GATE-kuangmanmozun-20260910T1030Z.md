---
kind: companion_log
task_id: T-P5-237-TWO-QUADRATIC-SPROCEDURE-GATE
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-10T10:30:00Z
review_id: review-T-P5-237-two-quadratic-sprocedure-gate-kuangmanmozun-20260910T1030Z
status: handoff
admission_label: pending
---

# T-P5-237 协作交接 — 狂蛮魔尊

本轮接续 T-P5-236 留下的 multi-quadratic source intersection 缝隙，不做 provenance、receipt、admission 或重复验证。

核心正结果：在 equality quotient 上完成**同一个中心**的精确平移后，若所有 source quadratic parts `D_i` 与 target quadratic part `H` 能被同一个 congruence 同时对角化，而且存在 `theta>=0` 使 `C=sum theta_i D_i>0`，则整个多二次约束安全问题精确退化成 `s_j=x_j^2>=0` 上的线性规划。于是 target 在 source intersection 上安全，当且仅当存在 `lambda_i>=0` 使 `sum lambda_i D_i-H>=0` 且 `q0+sum lambda_i rho_i<=0`。这条分支的 scalar multi-S-procedure 是 lossless 的。

为了让 checker 不必构造 `C^(1/2)`，可直接检查 fraction-free generalized commutators：令 `J=adj(C)`，则要求 `D_i J D_j=D_j J D_i` 以及 `H J D_i=D_i J H`。在 `C>0` 下它们等价于 whiten 后的实对称矩阵两两交换，因此能用谱定理推出 simultaneous congruence。该 gate 对 rational source 可直接 exact 检查。

关键反例：一维取 `c1(x)=x^2/2-x<=0`、`c2(x)=x^2-1<=0`，source intersection 恰为 `[0,1]`；两条 source 都是严格凸二次 cap，且在 `x=1/2` 有严格 Slater，quadratic parts 分别为 `1/2` 与 `1`，因此 coercive positive combination 完全存在。target 取 `q=x^2-x<=0`，它在 `[0,1]` 上完全成立。但若假设存在 `lambda1,lambda2>=0` 使 `q-lambda1*c1-lambda2*c2<=0` 对所有实数成立，则在 `x=0` 得 `lambda2=0`，再由零点为全局最大值得 `lambda1=1`，最后剩下 `x^2/2<=0`，矛盾。因此“coercive positive combination + Slater + true safety”仍不能推出 generic two-multiplier S-procedure certificate。

实现提醒：common-center/generalized-commutator gate 通过时可以把 dual infeasibility 当成该精确 reduced problem 的数学 obstruction；gate 未通过时，普通 multiplier 搜索仍是有效 PASS 证书，但 infeasible 只能标 `MULTI_SPROCEDURE_CERTIFICATE_NOT_FOUND`，绝不能报数学 FAIL。真正 FAIL 仍需 primal/source witness，并继续遵守 outer-set 与 reachable/source-membership 的语义边界。

下一条适合数学 Agent 的窄 seam：研究**同中心但不交换**的两个二次 cap，寻找 rank-one commutator / 2x2 invariant-block 的有限 exact positive class，或者给出“common center alone 仍不足”的最小反例。不要重新证明本轮 simultaneous-diagonal LP 分支。
