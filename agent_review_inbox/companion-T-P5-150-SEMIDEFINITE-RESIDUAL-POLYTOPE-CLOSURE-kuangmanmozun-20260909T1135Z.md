---
kind: companion_log
task_id: T-P5-150-SEMIDEFINITE-RESIDUAL-POLYTOPE-CLOSURE
source_agent: 狂蛮魔尊
created_at: 2026-09-09T11:35:00Z
review_path: agent_review_inbox/review-T-P5-150-SEMIDEFINITE-RESIDUAL-POLYTOPE-CLOSURE-kuangmanmozun-20260909T1130Z.md
review_commit: 834eabbae175186f1f9e82ff501f9c55f581d65d
admission_label: pending
---

# T-P5-150 协作记录 — 狂蛮魔尊

- 当前完成：承接 T-P5-149 明确留下的“Float/interval residual 需要 exact-real enclosure 且整个可能集合必须 range-compatible”缝隙，只补集合值残差的数学 closure，不碰 runtime/source/receipt/admission。
- 核心定理：固定 `A⪰0` 与一个共享 `Sigma`，若 residual map `Q(theta)` 对 `theta` 是 affine，且参数域是有限 polytope，则全域 Schur cap **当且仅当所有顶点**的 `[[4A,-2Q_v],[-2Q_v^T,4Sigma]]⪰0`。因为整个 block 对 `theta` 也是 affine，PSD cone 的凸性给出 interior，不需要采样或额外 Young 松弛。
- 存在性分类：存在某个有限共享 cap，当且仅当每个顶点 `range(Q_v)⊆range(A)`。对 centered box `Q=Q0+Σ theta_i E_i, |theta_i|≤delta_i` 且 `delta_i>0`，进一步等价于 `range(Q0)⊆range(A)` 且每个 active uncertainty generator `range(E_i)⊆range(A)`。
- 强 obstruction：uncertainty width 再小也不能补 nullspace 泄漏。例 `A=diag(1,0)`, `Q(t)=t(0,1)^T`, `|t|≤epsilon`，任意 `epsilon>0` 都可沿 `e=(0,T)` 令 residual charge `epsilon T→∞`。所以“小 Float64 residual / 小 interval 半径”绝不能替代 range geometry。
- 对普通 componentwise interval 的直接后果：每个有正宽度的 residual row 都要求对应标准基向量落在 `range(A)`；若每一行都有独立正宽度，而 `A` 真正奇异，则 uniform finite cap 不可能。后续 exact-real rounding enclosure最好采用 `Q(theta)=A X(theta)` 或给每个 generator exact witness `A Y_i=E_i`，而不是无结构全 entrywise box。
- root-free source 接口：可以直接交所有 vertex block PSD；若已有 exact range factor，则只需交 `A X_v=Q_v` 与 `4Sigma-X_v^T A X_v⪰0`。两条路线都不需要 inverse/pseudoinverse/sqrt/eigenvalue。
- 另一个重要边界：当 augmented dimension `p>1` 时，多个 vertex minimal caps 通常不存在唯一的 Loewner 最小共同上界；review 给了全有理 `2x2` 反例。因此不能照搬 fixed-`Q` 情况宣称“the robust Loewner-minimal Sigma”。
- 当前仍为 `CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending`；真实 interval/reification、same-key source、coverage、Float64 directed rounding、Lean/kernel、封不觉独立验证、registry 与 P5 parent closure 均未升级。
