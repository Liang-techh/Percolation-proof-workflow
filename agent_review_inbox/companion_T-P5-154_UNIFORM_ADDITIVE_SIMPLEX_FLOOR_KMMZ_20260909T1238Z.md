---
kind: companion_log
review_id: review-T-P5-154-uniform-additive-simplex-floor-kuangmanmozun-20260909T1233Z
task_id: T-P5-154-UNIFORM-ADDITIVE-SIMPLEX-FLOOR
source_agent: 狂蛮魔尊
created_at: 2026-09-09T12:38:00Z
related_review_path: agent_review_inbox/review-T-P5-154-UNIFORM-ADDITIVE-SIMPLEX-FLOOR-kuangmanmozun-20260909T1233Z.md
related_review_commit: c9b94c1f931c76c20a0f22e428425a4d659b57bb
status: pending
---

# T-P5-154 协作摘要 — 正 additive floor 不是 pairwise 问题

本轮接住 T-P5-153 的明确剩余缝隙：零 additive floor 在 homothetic cell 下可以由所有 pair 的 `K_ij>=0` 精确判定，但一旦允许统一正预算 `D>0`，不能再默认“把各条边都修好”就等于把整个 simplex 修好。

对候选 `D`，定义对称矩阵 `M_D`：对角项 `M_D[i,i]=D g_i`，非对角项满足

`2 M_D[i,j]=K_ij+D(g_i+g_j)`。

则对任意 simplex 权重 `lambda` 有精确恒等式

`lambda^T M_D lambda = Delta_lambda + D g_lambda`。

因此完整 simplex 上的统一 additive-floor 条件，精确地等价于 `M_D` 在非负正交锥上的 copositivity。PSD 是一个很干净的 exact-rational 充分通道，但 PSD 失败不能当成真实失败；真正的 target 仍是 copositive，而不是全空间 PSD。

最重要的反例是三顶点全有理系统：`g_i=1`、所有 `K_ij=-4`、候选 `D=1`。任意一条边上都有

`1-4t(1-t)=(2t-1)^2>=0`，

所以所有二顶点 restriction 全部精确通过；但在 barycenter `(1/3,1/3,1/3)` 上，`Delta+Dg=-1/3<0`。也就是说，任何 checker 若把“所有 edge repair PASS”升级成“full simplex PASS”，都会制造假 closure。

进一步对 `N` 个顶点、统一 `g_i=g>0`、统一负 pair coupling `K_ij=-kappa`，完整最坏点正好是均匀 barycenter，sharp floor 为

`D_* = kappa (N-1)/(2 g N)`。

单条边只要求 `D_edge=kappa/(4g)`，所以 full-simplex 与 edge floor 的比值为 `2(N-1)/N`；`N=3,g=1,kappa=4` 时分别是 `4/3` 与 `1`。这个差距证明 positive floor 存在真正的 multiway tax，不是 proof technique 的松弛。

建议后续 source/checker 采用三态 fail-closed 流程：先构造同一 key 的 exact rational `M_D`；若能给出 PSD/LDL witness，则直接认证该 `D`；若找到非负有理向量 `x` 使 `x^T M_D x<0`，则这是决定性的不足预算反例；若二者都没有，只能标记 `NOT_CERTIFIED`，不能退回 pairwise edge 逻辑假闭合。对于有特殊对称结构的真实 cell family，应先写专门的 exact theorem，再考虑 generic copositivity。

当前仍严格保持数学 child / pending：没有证明 deployed `{g_i,r_i,tau_i}`、homothetic source identity、同一 barycentric weights、domain/coverage、Float64、Lean/kernel、独立验证、admission 或 registry。