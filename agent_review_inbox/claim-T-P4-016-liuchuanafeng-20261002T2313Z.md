---
kind: task_claim
claim_id: claim-T-P4-016-liuchuanafeng-20261002T2313Z
agent: 流川枫
source_agent: 流川枫
task_id: T-P4-016
created_at: 2026-10-02T23:13:00Z
inspected_commit: 3bc8aaa5829b53526d50d050accbfdabb600427c
status: claimed
admission_label: pending
---

# Claim T-P4-016

流川枫认领 `T-P4-016`（exact nominal-distal tail PMI positivity）的独立审计叶。

边界：只核对仓库内 `src/percolation_workflow/routeb_nominal_distal_contract.py` 的 tail/Gram 接口，是否已经用完整非对角 `M0_BB` 证明无平方根 3x3 PMI，还是仅停在冻结 metadata、可选标量 Schur 恒等式和 candidate Gram LDL。不运行仓库外 CSV，不改 registry / state / 正式证明，不把浮点 PSD、采样正性或两个独立分量增益当成 3x3 PMI。

既有 `review-T-P4-016-kuangmanmozun-20260907T0344.md` 审的是执行余项聚合 Schur 预算，不是本任务的 nominal-distal tail PMI 合同；本 claim 不覆盖该文件。
