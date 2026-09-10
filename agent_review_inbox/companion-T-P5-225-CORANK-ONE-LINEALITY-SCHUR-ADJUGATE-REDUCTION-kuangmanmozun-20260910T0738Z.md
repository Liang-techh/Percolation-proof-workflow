---
kind: companion_log
task_id: T-P5-225-CORANK-ONE-LINEALITY-SCHUR-ADJUGATE-REDUCTION
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-10T07:38:00Z
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
review_commit: 3ea6316491536353fd7908122a0926e494906e13
admission_label: pending
---

# 狂蛮魔尊协作留言 — T-P5-225

本轮接 T-P5-224 的 signed-lineality Schur 分支，专门处理 `A<=0` 且 `P=-A` 为 PSD corank-one 的常见情形，没有碰 provenance / receipt / admission。

核心压缩：令 `J=adj(P)`。在 `P>=0, rank(P)=ell-1` 下，`J` 是非零 rank-one PSD，且 `range(J)=ker(P)`。因此 T-P5-224 的 `range(B) subset range(P)` 条件精确等价于 `JB=0`。

- 若 `JB!=0`：这不是“checker 不适用”，而是可以直接构造真实数学 obstruction。任取非零 `(JB)_{ij}`，令 `z=J e_i`，则 `Pz=0` 且 `z^T B e_j!=0`；固定 `a=e_j` 后沿 `c=t z` 可使 debit 无界增大。
- 若 `JB=0`：选任意 `delta_i=J_ii>0` 的 anchor，删除该坐标后的 `P_II` 自动 PD。令 `H=adj(P_II)`，则可以构造无奇异逆的 scaled solve `P Ytilde=delta_i B`，并形成完全 fraction-free 的 reduced matrix

`Dhat_i = delta_i C0 + B_I^T H B_I`。

它满足 `Dhat_i=delta_i D`，其中 `D` 正是 T-P5-224 的 Schur reduced orthant block。因为 `delta_i>0`，所以 `D` 与 `Dhat_i` 在正交锥上的正负号完全一致；后续直接对 `-Dhat_i` 调现有 copositivity checker 即可。

若 checker 找到 `a0>=0` 且 `a0^T Dhat_i a0>0`，无需除法即可回构 endpoint witness：

`a*=delta_i a0`, `c*=Ytilde a0`,

并有 `q(c*,a*)=delta_i(a0^T Dhat_i a0)>0`。

不同合法 anchor 还满足 exact checksum

`delta_k Dhat_i = delta_i Dhat_k`，

因此可用于检查同一数学 packet 的两个独立 fraction-free 构造是否一致；但这不是 source provenance。

已给四类边界反例：省略 `JB=0` 会漏掉 kernel-cross 无界正 witness；删除 `J_ii=0` 的错误坐标会留下奇异 principal block；去掉 PSD 后 anchor determinant 可为负导致 sign 反转；corank>1 时 `adj(P)=0`，即使存在 kernel-cross obstruction 也会被单 adjugate gate 漏掉。

下一条建议数学 seam：higher-corank `P` 的 maximal-rank principal anchor / compound-minor 版本，把 `range(B)` 的 kernel-cross gate 与 fraction-free reduced `Dhat` 推广到 `adj(P)=0` 的情形，同时证明不同 maximal anchor 的正比例不变性。

当前仍未升级 actual same-key `A/B/C0`、source/selector/cell/tube、coverage、Float64/interval、最终 actual copositivity、Lean/kernel、封不觉独立验证、admission、registry 或 P5/P8/M4 parent closure。