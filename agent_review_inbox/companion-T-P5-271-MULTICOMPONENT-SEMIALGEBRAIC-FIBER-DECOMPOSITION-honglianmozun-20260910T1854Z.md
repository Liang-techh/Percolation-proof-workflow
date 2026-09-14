---
kind: companion_log
task_id: T-P5-271-MULTICOMPONENT-SEMIALGEBRAIC-FIBER-DECOMPOSITION
review_id: review-T-P5-271-multicomponent-semialgebraic-fiber-decomposition-honglianmozun-20260910T1850Z
source_agent: 红莲魔尊
created_at: 2026-09-10T18:54:00Z
inspected_commit: dca236762bf7fa0687e0d6fbcaf030d895561a92
review_commit: 28be4ab630470caae390cfef4b534a0c96091076
admission_label: pending
---

# 红莲魔尊 — T-P5-271 数学交接

本轮承接 T-P5-270 明确保留的多分量 semialgebraic fiber seam，未做 provenance、receipt、admission、Lean 编译或重复 audit。

主要数学推进：

1. 对 `F_q={s∈[L,U]:P(q,s)≥0}`，普通 squarefree part 不能保存 inequality source；必须保留 squarefree factorization 中的**重数奇偶性**。奇重根穿越时符号翻转，偶重根不翻转。
2. 在避开 degree-drop、factor discriminant、factor 间 resultant、clipping boundary contact 与 `A2=0` 的每个 regular q-cell 上，所有真实根可按固定顺序表示为连续/解析的 algebraic root branches，source fiber 的组合拓扑保持不变。
3. fiber 组件不仅包括移动闭区间，还可能包括两侧都 `P<0` 的**偶重孤立 root singleton**；这类 singleton 不能作为“measure-zero”丢弃。
4. 对每个 interval component，`A2>0` 时复用 LEFT/RIGHT/INTERIOR exact clamp；`A2≤0` 时 slack 为 concave/affine，安全性恰等价于两个 endpoint reserve 都非负；singleton 只检查该代数根上的 reserve。
5. discriminant/resultant/degree-drop q 值必须作为 zero-dimensional point cells 独立检查。反例 `P(q,s)=-(q²+s²)≥0` 只有 `(0,0)` 一个可行点，所有邻近 open q-cell 都为空；忽略 point cell 会产生 false PASS。
6. disconnected fiber 不能用 convex hull 粗化：`P=(s²-1)(4-s²)≥0` 给 `[-2,-1]∪[1,2]`，而 `A=2-s²,K=1` 在真实 fiber 上安全、在 hull 的 `s=0` 处失败，因此 hull relaxation 会制造 false FAIL。

新的结构指纹是：

`one polynomial source inequality`
`→ parity-aware squarefree factors`
`→ finite q projection atlas`
`→ ordered algebraic roots`
`→ sign strips + singleton components`
`→ component-wise Lyapunov clamp`
`→ singular point-cell checks`
`→ finite exact reserve dispatcher`。

尚未闭合：actual P5 source polynomial/Boolean formula、same-key `q/s/A_i/K` binding、实际 clipping interval、cell/trajectory/FD coverage、Float64/interval、Lean/kernel、封不觉独立验证、admission/registry。

下一条不重复 seam：多个 polynomial inequalities/equalities 的一维 fiber arrangement。需要把所有 boundary polynomials 的 roots 放进统一排序，用 pairwise resultants 处理 active-boundary switch，再按 Boolean sign formula 构造真实 components，而不是退回二维黑箱优化。