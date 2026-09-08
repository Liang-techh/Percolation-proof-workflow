---
kind: companion_log
task_id: T-P5-074-WEIGHTED-STRONG-MONOTONE-SCC
review_id: review-T-P5-074-weighted-strong-monotone-scc-guyuefangyuan-20260908T0700
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-08T07:03:00-06:00
integration_status: pending
admission_label: pending
review_commit: 48c78207c758636227a8bb3f5be2e1f6c247e6c4
---

# T-P5-074 中文协作接力

本轮承接 T-P5-072 明确留下的“含 chord / 一个 root 依赖多个 contact 的一般 SCC”缺口，给出一条比 absolute small-gain 更强、但仍很适合 exact checker 的路线：对 `Phi=x-rho` 使用正对角权重 `W`，证明 weighted strong monotonicity

`<W(Phi(x)-Phi(x')),x-x'> >= kappa ||x-x'||_W^2`。

通过后，固定参数时直接有 division-free 平方逆界 `kappa^2 E <= Z`；带参数变化时，对任意有理 `lambda>0` 有

`lambda*kappa^2 E <= (1+lambda)(lambda Z + P D^2)`。

最重要的 source/checker 接口不是分别取 `|D_ij|`，而是先组合 signed symmetric pair

`w_i D_ij + w_j D_ji`

再取绝对值。若有 `D_ii>=d_i`、`|w_iD_ij+w_jD_ji|<=c_ij`，只需逐行检查

`2 w_i d_i - sum_{j!=i} c_ij >= 2 kappa w_i`

即可得到强单调性。全部 trusted arithmetic 只需要有理加乘与序比较，不需要 determinant、eigenvalue、matrix inverse、sqrt 或浮点优化。

这个 signed gate 确实扩大证书区域。review 中的三维 complete skew SCC

`S=[[0,2,-3],[-2,0,4],[3,-4,0]]`, `rho=Sx`

所有 pairwise absolute cycle products 都大于 1，且存在正的三环 product；但 `D Phi + D Phi^T=2I`，所以 `kappa=1` 精确通过，并得到 `||Delta x||^2 <= ||Delta xi||^2`。因此一般 SCC 不应只靠 simple-cycle parity 或 absolute gain product 决策。

若真实 roots 来自隐式方程 `h_i=0`，建议 source lane 直接证明清分母后的 pair inequality

`|w_i h_ij d_j + w_j h_ji d_i| <= c_ij d_i d_j`

其中 `d_i=partial_i h_i>0`。这样能在 polynomial/rational numerator 层保留负反馈 cancellation，避免先分别 bound 两个分式导致假阴性。

建议路由：先判 triangular；再判 simple cycle；两者都不适用时跑 T-P5-074 signed symmetric-part gate；若仍失败，只标 `NOT_CERTIFIED/NOT_APPLICABLE`，再考虑 P-matrix、interval Newton/Krawczyk 或 source-specific decomposition。review 还给了同号 `3/2` two-cycle：强单调 gate 失败但矩阵仍可逆，证明“不通过 T-P5-074”绝不能升级成 noninvertible。

Lean 最小层建议先只形式化 weighted secant consumer、平方逆界和 signed diagonal-dominance quadratic lower bound；Brouwer common-core existence、Jacobian-to-secant calculus bridge放后面，避免把第一版 sidecar 做大。

边界不变：真实 SCC/source derivative、Float64/FD/controller/solve、P8/ODE、Lean/kernel/comparator、封不觉验证、provenance/admission 与 P5/P8/M4 closure 都仍 open。

当前 GitHub 连接器对 `collaboration_board.md` 仍只有整文件 replacement；无法在不读取并重写整份约 2600 行历史的情况下安全原子追加，且并行 Agent 正在提交。因此本条中文建议先按 companion 协议持久化，供梁智炜收割时安全追加到留言板末尾。
