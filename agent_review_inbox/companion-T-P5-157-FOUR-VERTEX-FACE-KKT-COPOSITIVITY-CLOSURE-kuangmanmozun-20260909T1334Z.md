---
kind: companion_log
task_id: T-P5-157
status: mathematical_progress
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_utc: 2026-09-09T13:34:00Z
---

# 狂蛮魔尊协作留言：T-P5-157 四顶点精确 copositivity closure

本轮没有抢 T-P5-155 的三顶点判据，也没有进入 T-P5-156 的 weighted-slack/refinement 路线，而是补了固定候选 `D` 下四顶点 simplex 的下一层精确缺口。

结论：若 `4×4` 对称有理矩阵 `M_D` 的四个 `3×3` principal face 都已经 copositive，则整个四顶点 simplex 仍然失败，当且仅当存在严格内部 KKT witness：`λ_i>0`、`sum λ=1`、`M_D λ=α 1`、`α<0`。因此 face 全过之后，剩余 obstruction 只是一个有理线性系统加严格符号条件，不再是新的非线性搜索。

为了让 checker 完全 exact，可引入 margin `t`，解有理 LP：最大化 `t`，约束 `M_D λ=α1`、`sum λ=1`、`λ_i>=t`、`-α>=t`。在四个 face 都 PASS 的前提下，`t_*>0` 等价于 full-simplex FAIL；精确 primal 给反例，精确 dual/Farkas 可给 `t_*<=0` 的 PASS 证书。

已给出必须保留的反例：`diag=5/2, offdiag=-1` 时四个三顶点 face 全部甚至 PSD，但四顶点 barycenter 有 `q=-1/8`，所以“所有 facets PASS”绝不能直接升级 full PASS。另一个 sharp endpoint 是 `diag=3, offdiag=-1`：barycenter 有 `α=0,q=0` 且整体 copositive，因此失败判据必须是严格 `α<0`，不能写成 `α<=0`。

若 `M` 可逆，有一个便宜 fast path：exact solve `My=1` 后，在 face 已通过时，full-simplex FAIL 当且仅当所有 `y_i<0`。但 singular/degenerate branch 必须回到 bordered exact system，不能用 pseudoinverse 或随意除 `1^Ty`。

当前只得到数学 child；actual `{g_i,K_ij,D}` source、same-key simplex 语义、Float64/runtime、Lean/kernel、封不觉独立验证、registry/admission 与 P5 parent closure 均未升级。
