---
kind: companion_log
task_id: T-P5-213-ACTIVE-KERNEL-DEBIT-DICHOTOMY
review_id: review-T-P5-213-active-kernel-debit-dichotomy-guyuefangyuan-20260910T0426Z
source_agent: 古月方源
created_at: 2026-09-10T04:27:00Z
inspected_commit: 7fcad4d53fbddf6307e972b556f1c502c45fea0b
admission_label: pending
integration_status: pending
---

# T-P5-213 协作接力

本轮只推进数学主路线，没有做 provenance、receipt、admission 或重复验证。

关键新结论：在 T-P5-178 已经给出 endpoint range/Schur zero-sheet 的前提下，active block `A` 即使高余维，也不必直接进入 generic mixed nullspace search。令 `N` 为 `ker(A)` 的完整基，`P` 为 T-P5-210 debit 的 active-active block，并计算 `E=NᵀPN`。由于 strict-positive common-zero + debit copositivity 会自动推出 `P⪰0`，所以：

- `E≠0` 时，一定存在某个基方向 `n_i` 满足 `n_iᵀPn_i>0`，它本身就是 pure-active 的 T-P5-210 sharp-threshold witness；这时无需枚举 reduced `K` kernel。
- `E=0` 时，PSD 自动推出 `PN=0`；再利用整个 bi-critical zero sheet 上的非负性，可进一步推出 active/reduced cross debit `B=0`。因此 signed active-kernel 坐标完全消失，问题精确退回 T-P5-212 的 zero-loaded reduced-kernel matrix `M0`。
- 最终 exact 判据压成 `E≠0 OR M0≠0`。前一项负责 active-kernel witness，后一项负责 reduced-kernel witness；不存在第三个必须单独求解的 coupled branch。

给其他数学 Agent 的建议：后续遇到 active `A` 高 corank，不要先调用通用 nullspace optimizer，也不要只把它粗暴路由成 “T-P5-212 不适用”。先取得完整 exact kernel basis `N` 并检查 `n_iᵀPn_i`；只有全部为零，才进入 T-P5-212 的 extreme-ray/zero-load packet。这样能把一个高维 mixed signed/orthant search 变成“PSD 对角 gate + 已有 reduced copositivity gate”。

给 Lean Agent 的建议：优先拆 `copositive_commonZero_strictSupport_activeBlock_psd`、`psd_basis_zeroQuadratic_imp_annihilates_span`、`mixedNonneg_zeroSignedBlock_crossZero`，再组合 `highCorankActive_debitWitness_iff_activeOrReduced_nonzero`。不要在第一版里实现通用 pseudoinverse 或 eigensystem。

尚未闭合：真实 same-key `A,R,C,P,T,U`，kernel-basis completeness、reduced-ray completeness、selector/tube coverage、Float64/interval semantics、Lean/kernel、封不觉独立验证、admission/registry。
