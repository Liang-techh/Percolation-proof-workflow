---
kind: companion_log
task_id: T-P5-142-ROBUST-INEXACT-MULTIPLIER-BRACKET
review_id: review-T-P5-142-robust-inexact-multiplier-bracket-guyuefangyuan-20260909T0931Z
source_agent: 古月方源
created_at: 2026-09-09T09:33:00Z
review_commit: 3e81bac2fe47fc97a041b32f311162d53ee5fdb7
status: pending
---

# T-P5-142 协作接力

- 当前完成：把 T-P5-141 的 inexact range-solve residual packet 从“只能给 conservative reset floor”推进成了对**真实 sharp floor**的双边夹逼。若 `A=b^T y+r^T y` 且 `sigma K-r r^T>=0`，则真实量满足 `A <= 4(E_tau-C-tau R) <= A+sigma`。
- 新的搜索规则：对 `tau_0<tau_1`，真实 floor 差满足 `D-sigma_0 <= 4(E_1-E_0) <= D+sigma_1`，其中 `D=4(tau_1-tau_0)R+A_1-A_0`。因此证明向右下降只需要右端 `sigma_1`，证明向右上升只需要左端 `sigma_0`。
- 最值得复用的结论：对 `tau_0<tau_1<tau_2`，如果 `A_0-A_1-sigma_1 > 4(tau_1-tau_0)R` 且 `A_1-A_2+sigma_1 < 4(tau_2-tau_1)R`，再结合 T-P5-140 已有 discrete convexity，就能把所有 global minimizer 限制在 `[tau_0,tau_2]`。数值上只需要把中间候选的 residual cap 做紧，外侧 cap 的大小不进入这两个 gate。
- 明确 obstruction：靠近 singular `K` 时，`sigma` 很小并不意味着 approximate `y` 在 `G` metric 下接近 exact solve。标量反例 `K=epsilon,G=1,y=0,b=r=epsilon,sigma=epsilon` 中 `sigma->0`，但 exact correction 恒为 `1`。所以后续 multiplier search 应优先消费本轮的 intrinsic floor/cross-secant gate，不要把 approximate `y^T G y` 直接当 T-P5-140 stationarity witness。
- 可选增强：若 interior candidate 真能提供 `lambda K-G>=0`，则可把 residual energy 运输到 `G` metric，再复用 T-P5-134 的 root-free quadratic sandwich 做 approximate stationarity bracket；但 `G>0` 且 `K` singular 时 full-space `lambda K-G>=0` 不可能成立。
- 给数学 Agent 的建议：下一步若 actual producer 已有多个 rational `tau` 的 approximate solve，优先形成同键 `A_i,sigma_i` packet 并跑三点 bracket；若 gate 卡住，只提高方向上真正需要的那一个 residual cap 精度，不要把所有点一起重算。
- 给 Lean Agent 的建议：先落纯标量叶 `inexactFloor_difference_interval`、`inexactFloor_descent/ascent`，再接 T-P5-140 的 discrete-convex theorem；矩阵层只需复用 T-P5-141 的 residual-energy interval，不需要引入 inverse API。
- 未闭合：actual same-key `G,H,b,C,R,tau,y,r,sigma`、source/coverage、solver/Float64 语义、controller/FD、P8、Lean/kernel、封不觉独立验证、admission/registry 全部仍是 pending。
- 关联：T-P5-139 / T-P5-140 / T-P5-141 / T-P5-142；正式 review commit `3e81bac2fe47fc97a041b32f311162d53ee5fdb7`。

共享 `collaboration_board.md` 当前通过连接器仍只能安全地整文件替换，读取又存在截断；为避免覆盖其他 Agent 的并行留言，本轮没有冒险重写该文件。以上中文内容可由梁智炜在收割时安全追加到留言板。
