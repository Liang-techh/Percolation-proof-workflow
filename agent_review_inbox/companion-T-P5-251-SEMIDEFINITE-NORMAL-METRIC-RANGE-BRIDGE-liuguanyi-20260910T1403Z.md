---
kind: companion_log
review_id: companion-T-P5-251-semidefinite-normal-metric-range-bridge-liuguanyi-20260910T1403Z
task_id: T-P5-251-SEMIDEFINITE-NORMAL-METRIC-RANGE-BRIDGE
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-10T14:03:00Z
inspected_commit: 835f80db550c24f0b9058645406d08077a7cebd5
parent_review: review-T-P5-251-semidefinite-normal-metric-range-bridge-liuguanyi-20260910T1403Z
parent_review_commit: ef68d2faa4e23bdad40c700937eccfa6e9b78306
status: pending
admission_label: pending
---

# T-P5-251 协作交接 — 柳冠一

- 当前完成：把 T-P5-250 的 `W>0` 厚管接口推广到 `W>=0` 的 partial-tube。证明 one-constraint S-lemma 本身不需要 `W>0`；真正新增的是 equality-multiplier reserve reuse 的 `range(Y) subset range(W)` 硬门。
- 新的数学接口：若 `WZ=Y`，则 generalized Schur charge 是解无关的 `Y^T Z=Z^T WZ`。对 rational 数据，可用 maximal principal anchor `R=W_II`、`delta=det R`、`H=adj R` 把 range gate 写成 `delta Y_J=W_JI H Y_I`，把 block PSD 写成 `tau delta A-Y_I^T H Y_I>=0`，全程无需 pseudoinverse、平方根或浮点 eigenspace。
- 重要修正：当 `W` 奇异时，`eta=0` 只推出 `WCξ=0`，一般不等于 `Cξ=0`。所以 zero-radius dispatcher 不能直接复用“exact image `Cξ=0`”；应把 `WC` 当作 partial-equality matrix，除非 source 另证 `WCξ=0 -> Cξ=0`。
- 失败语义：range gate 失败只说明“当前 equality-multiplier 的 normal-metric reserve reuse 不可用”，不能直接判真实目标 FAIL；direct one-tube S-lemma 仍可能靠 slack 自身曲率通过。正式 review 已给出一个 exact safe counterexample 锁死这一点。
- 给其他数学 Agent 的建议：下一步不要再造 generalized-Schur 变体，优先找 actual P5 normal residual `C` 和 metric `W` 的同源 packet，证明其奇异性是否结构性，并检查真实 `Y` 是否落在 `range(W)`；若不落，改走 direct tube S-lemma 或寻找 source curvature，不要误报失败。
- 给 Lean Agent 的建议：最值得先形式化的叶子是 `(1)` PSD block 的 kernel-cross annihilation；`(2)` `WZ=Y` 下的 exact congruence factorization；`(3)` maximal-anchor 的两条 fraction-free identity；`(4)` `e^TWe=0 <-> We=0`。这些 theorem 都是 source-independent，且可保持 Real/rational 分层。
- 保留边界：actual source binding、tube/trajectory/FD-halo coverage、Float64/interval rank semantics、Lean/kernel receipt、封不觉独立验证、admission/registry 全部仍 OPEN。

关联 review：`agent_review_inbox/review-T-P5-251-SEMIDEFINITE-NORMAL-METRIC-RANGE-BRIDGE-liuguanyi-20260910T1403Z.md`。