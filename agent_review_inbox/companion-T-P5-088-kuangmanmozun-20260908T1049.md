---
kind: companion_log
task_id: T-P5-088-STATE-DEPENDENT-STORAGE-DERIVATIVE
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-08T10:49:00-06:00
review_result: review-T-P5-088-state-dependent-storage-kuangmanmozun-20260908T1046.md
status: pending mathematical child
---

# T-P5-088 中文协作摘要

本轮补的是 T-P5-087 明确留下的 moving-storage derivative 边界，而不是重复它的 moving-metric defect comparator。若 Lyapunov storage 本身写成 `V(t,y)=y^T W(t,y)y`，实际动力学为 `ydot=-G+e`，精确链式法则是

`Vdot = [-2<y,G>_W + y^T(W_t-D_yW[G])y] + [2<y,e>_W + y^T D_yW[e]y]`。

第二个方括号还能精确压成 `e dot grad_y V`。因此 state-dependent metric 下，residual/evaluator defect 不能只按旧的 `2<y,e>_W` 收费；`D_yW[e]` 是同一个 defect 的组成部分，应该先与普通 pairing 做 signed CSE，再 enclosure。

最小 closure：若 nominal 整体 `N_W <= -cV-D`，defect 整体 `E_W <= alpha V+beta`，则 `Vdot <= -(c-alpha)V-D+beta`。纯衰减要求 `alpha<c, beta=0`；first-exit level `Vstar` 只需 `beta < (c-alpha)Vstar`。若 nominal 拆开，则 `2<y,G>_W >= dV+D`、`y^T(W_t-DW[G])y <= gamma V+b0`、`E_W<=alpha V+beta` 给出 gate `gamma+alpha<d` 和 `b0+beta < (d-gamma-alpha)Vstar`，全程无需除法或平方根。

moving-storage 的 matrix charge 可直接检查 `gamma W-(W_t-DW[G]) >= 0`。source 端应先形成这个 signed matrix difference，再做 diagonal-dominance/interval 证书；不要分别对 `W_t` 与 `DW[G]` 取绝对值后再相加。

精确反例已经写入正式 review：一维 `W(y)=1-y`、`ydot=-y`、`0<=y<=3/4` 时 `W_t=0` 且 `W>=1/4`。冻结 metric 会预测 `Vdot_frozen=-2(1-y)y^2<0`，但真实 `Vdot=-2y^2+3y^3`，在 `y=3/4` 精确等于 `9/64>0`。所以遗漏 `D_yW[ydot]` 可以直接把“增长”错报成“衰减”，不是常数稍松的问题。

另一个二维反例：`W(y)=(1+y1)I`，在 `y=(0,1)`、`e=(1,0)` 时普通 pairing `2<y,e>_W=0`，但 `y^T DW[e] y=1`，所以真实 defect storage charge 是 1。任何只看普通 weighted pairing 的 checker 都是不完备的。

如果只有 whole defect charge `P=e dot grad V` 的平方界 `P^2<=H V`，则可用 division-free Young gate `H<=4 alpha beta` 推出 `P<=alpha V+beta`。当 `beta=0` 时该 gate 强制 `H=0`，明确说明 generic persistent additive defect 的 `O(sqrt(V))` 行为不能伪装成纯 relative rate；应送入现有 bias/first-exit lane。

建议下一步 source owner 提供：实际 `W,G,e`、`B_G=W_t-DW[G]` 的 signed CSE、`gamma W-B_G` 的 rational PSD/diagonal-dominance packet，以及 whole `E_W=e dot grad V` 的 one-sided 或 squared packet。Lean 侧最小叶可拆为 material derivative identity、nominal/defect split、full-gradient pairing identity、relative/additive decay、PSD-gap gate、square-packet absorption 与两个 regression。

边界保持不变：当前没有 claimed deployed source、Float64/controller/FD、P8 coverage、Lean/kernel、provenance、admission、registry 或 P5/M4 closure。