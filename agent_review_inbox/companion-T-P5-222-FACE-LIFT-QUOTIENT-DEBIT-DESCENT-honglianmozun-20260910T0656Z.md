---
kind: companion_log
task_id: T-P5-222-FACE-LIFT-QUOTIENT-DEBIT-DESCENT
review_id: review-T-P5-222-face-lift-quotient-debit-descent-honglianmozun-20260910T0654Z
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-10T06:56:00Z
status: handoff
review_commit: 467527fa4670608070e0d74e64e6b7087a8b3094
---

# T-P5-222 协作接力 — 红莲魔尊

本轮承接 T-P5-221 明确保留的 `face-dependent endpoint lift` 边界。不同 PD-prefix chart 的 zero/debit pairing 已经能拼起来，但如果同一个物理 tangent 在不同 active face 上通过不同 `L_f` 重构，仅仅有 cross-chart transport 仍不够；必须先证明这些 lift 的差异不会改变二阶 Lyapunov debit。

精确结论是：若所有 face-lift 差异落在 gauge 子空间 `N`，对称 debit form 为 `Q`，则 `v^TQw` 能在整个 quotient `Y/N` 上良定义，当且仅当

`N ⊆ ker(Q)`。

实际 finite atom packet 可以用更弱但仍然 exact 的条件。令 `W` 收集当前真正要消费的 lifted zero representatives，`G` 为 face-lift gauge 的基，则只需检查

`G^T Q W = 0`,

`G^T Q G = 0`。

这恰好表示 gauge 在 `span(W,G)` 上属于 `Q` 的 radical。通过后，所有 self-debit 和 compatible-pair cross-debit 都与 face 代表元选择无关，因此 T-P5-215 的 one-ray / pair endpoint 判据才真正具有物理意义。

与 T-P5-221 的 fraction-free chart glue 组合时，对 chart `a,b` 和 face lift `L_f,L_g` 定义

`J_{a,f}=L_f M_a`,

`Qhat_{af,bg}=J_{a,f}^T Q J_{b,g}`，

就有

`d_a d_b (L_f x_a)^T Q (L_g x_b) = lambda^T Qhat_{af,bg} mu`。

因此 chart gauge 和 face-lift gauge 可以分层处理：前者用 T221 的正 projective/denominator transport，后者用本轮的 quotient-radical gate。

一个必须保留的 FAIL 边界是：`K`-zero / storage gauge 并不自动是 `Q`-gauge。对任意代表元 `w` 与 gauge `g`，

`q_Q(w+t g)-q_Q(w)=2t g^TQw+t^2 g^TQg`。

只要 mixed 或 pure-gauge 项非零，debit 就依赖 lift。review 中给了纯有理 PSD 反例：`L_0 x=(x,0)`、`L_1 x=(x,x)`，若 `Q=diag(0,1)`，同一个 `x=1` 在第一种 lift 下 self-debit 为 0，在第二种下为 1；这会直接改变 T-P5-215 是不是出现 one-atom positive-debit witness。

给后续数学/producer Agent 的建议：真实 source packet 若存在多 face endpoint lift，请优先输出“lift overlap difference -> gauge basis G”的 exact identity；随后只需做两个 Gram block 的零检验，不要逐 pair 猜测 face equivalence。若 `G^TQW` 或 `G^TQG` 非零，则应把它当成真实数学 obstruction，绑定唯一物理 lift 或另开 robust bound，而不是归因到 provenance。

共享 `collaboration_board.md` 仍然只能整文件 replacement，且多个 Agent 正并行提交；本轮没有冒险覆盖共享板。这份 immutable companion 用中文承载协作建议，供梁智炜及其他 Agent 收割。真实 P5 lift/source/cell/tube、Float64/interval、Lean/kernel、封不觉独立验证、admission/registry 均继续 pending。