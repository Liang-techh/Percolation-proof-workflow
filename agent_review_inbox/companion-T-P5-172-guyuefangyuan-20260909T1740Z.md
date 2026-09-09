---
kind: companion_log
task_id: T-P5-172-LOW-DEGREE-SYMBOLIC-PIVOT-CORRIDOR
review_id: review-T-P5-172-low-degree-symbolic-pivot-corridor-guyuefangyuan-20260909T1737Z
source_agent: 古月方源
created_at: 2026-09-09T17:40:00Z
status: handoff_note
---

# T-P5-172 中文协作接力

- 当前完成：把 T-P5-170/T-P5-171 明确留下的 symbolic-`D` degree-growth 缺口压平。对 P5 的 `M_D=M_0+D L_g`、`L_g=(g1^T+1g^T)/2`，固定 pivot order 的每一个 pivot 对角正性和 pivot-row 非正 gate，都可以改读原矩阵的 principal / almost-principal minor，不必展开递归 scaled Schur matrix。
- 关键结构：`rank(L_g)<=2`，而且任意 row/column square submatrix 的 `D`-dependent columns 都落在二维 span 中，所以**所有 square minors，包括 almost-principal minors，对 D 的次数都至多 2**。这把整条 fixed-order symbolic corridor 精确变成有限个 quadratic sign gates。
- exact sign transport：若已消去集合为 `P` 且 `Delta_P=det M[P,P]>0`，则普通 Schur entry 满足 `Gamma_{P;i,j}=Delta_P*S_ij`，其中 `Gamma` 是 rows `P++[i]`、cols `P++[j]` 的 bordered minor。T-P5-170 的 recursive current matrix 只是该 Schur complement 的正数倍，因此 pivot sign 与 `Gamma` 的 sign 完全相同。
- checker 建议：不要把 recursively scaled entries 当 primary symbolic evidence；它们会携带前面 principal minors 的正 prefactor，虚增 polynomial degree。生产原始 `Delta/Gamma` 的 quadratic coefficient triples `(a,b,c)`，再在 rational `[L,U]` 上用 root-free gate：concave 看 endpoints；convex 若单调看对应 endpoint；vertex 在区间内时只查 `4ac-b²`。要查 `q<=0` 就对 `-q` 使用同一 gate。
- regression：对 review 中的 3x3 exact rational family，pivot order `1→2` 在 `[1/4,1/3]` 全程有效，terminal determinant 从 `-1721/64` 变到 `995/36`，存在唯一 sharp root约 `0.2910465`。naive scaled recursion 的 terminal scalar是 `(D+1)*det(M_D)`，已经变 cubic；但 `D+1>0`，所以真实 sign 仍只需 quadratic `det(M_D)`。这直接说明高次只是 denominator-clearing 的正 prefactor baggage。
- 给数学 Agent 的建议：若后续研究 symbolic floor search，请优先做“fixed pivot order + quadratic minor corridor”；只有 corridor gate 变号时才 branch order。pivot gate 失败不是 copositivity FAIL。T-P5-171 的 contact lift继续只在 fixed candidate处消费即可，不要把 strict complementarity混进这里。
- 给 Lean lane 的建议：最便宜的首叶是 `quadratic_nonneg_on_Icc_rootfree` / strict 版本，其次是 bordered-minor sign transport。generic rank-two polynomial-degree theorem如果 Matrix/Polynomial API 太重，可以先对实际低维固定 minors生成系数恒等式并用 `ring` 证明，再后置泛化。
- 边界提醒：`Delta_P=0` 必须回 T-P5-170 zero-pivot/T-P5-160 kernel branch；如果真实 floor pencil不是 rank<=2 的单参数 affine loading，本轮 degree-two 结论不能按字段名继承。`g_i>0` 不是 minor algebra需要的，但 sharp-floor monotonicity需要显式保留。
- 当前状态：`CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending`。actual source、coverage、Float64、Lean/kernel、封不觉独立验证、admission/registry均未声明闭合。
- 协作板说明：当前 GitHub connector 对 `collaboration_board.md` 只提供整文件 replacement，文件体量又很大；为避免并行覆盖历史留言，本轮没有危险地重写共享板，以上中文接力以 immutable companion 留存，待协调端有安全 append/harvest 时可转录。

关联正式 review：`agent_review_inbox/review-T-P5-172-LOW-DEGREE-SYMBOLIC-PIVOT-CORRIDOR-guyuefangyuan-20260909T1737Z.md`，commit `c4e82b5839bc037672c73635775399632e515406`。