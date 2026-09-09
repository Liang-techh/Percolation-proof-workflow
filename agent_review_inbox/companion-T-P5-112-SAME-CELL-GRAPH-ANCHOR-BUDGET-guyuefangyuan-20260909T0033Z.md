---
kind: companion_log
task_id: T-P5-112-SAME-CELL-GRAPH-ANCHOR-BUDGET
review_id: T-P5-112-SAME-CELL-GRAPH-ANCHOR-BUDGET-guyuefangyuan-20260909T0030Z
source_agent: 古月方源
status: handoff
---

## 中文协作接力

古月方源本轮把“真实 P5 anchor budget”继续向 actual source 压了一层：同 cell 隐式 acceleration graph 不需要显式 `M^{-1}`。若物理线段上有定量 squared lower-gain

`gamma * Q_A(v) <= Q_R(Mv)`

以及二阶隐式 jet RHS

`J2 = D2R[delta,delta] - D2M[delta_q,delta_q] alpha - 2 DM[delta_q] Dalpha[delta]`

的同段上界 `Q_R(J2)<=H2`，则 affine anchor predictor 的真实 remainder 满足严格的 division-free 结论

`4 gamma Q_A(r_anchor) <= H2`。

因此真实 anchor budget `D_anchor` 的最终 checker 只需要 `H2 <= 4 gamma D_anchor`；若有 `H2<=K2*Q_Z(delta)^2` 和 cell displacement cap `Q_Z(delta)<=S`，则只验 `K2*S^2 <= 4 gamma D_anchor`。

给 source/CSE lane 的最小建议：现有 exact extractor 已有 `M,DM,R,DR`，下一步不要先求 alpha/Y 数值或 inverse；优先补物理 pullback 下的 `D2M,D2R`（或直接 `J2` exact evaluator）、same-cell correlated `H2/K2`，以及定量 lower-gain。若继续沿已有 preconditioner `X,kappa`，只再补 `Q_A(Xy)<=chi Q_R(y)`，即可得到 `(1-kappa)^2 Q_A(v)<=chi Q_R(Mv)`，最终 anchor gate 为 `chi H2 <= 4(1-kappa)^2 D_anchor`。

两个必须避免的误接：只在 anchor 点证明 Hessian/second jet 不够（`alpha(x)=x^3` 在 0 点二阶导为0但到1的 affine remainder=1）；只证明 `M` nonsingular 也不够（标量 `M=eps, R=x^2/2` 时 second RHS 恒为1而 anchor remainder=`1/(2eps)` 可任意大）。所以 whole physical segment coverage 与 quantitative lower gain 都是不可删的 premise。

物理 segment 必须在 `(q,v,w)` 空间取，`c_i,s_i` 应由 `q_i` 重新 pullback；不能把独立 `(c,s)` 线性插值当成真实同 cell 路径。若下游使用不同/moving metric，还需先做 metric comparator，不能默认与本 theorem 的固定 `Q_A` 相同。
