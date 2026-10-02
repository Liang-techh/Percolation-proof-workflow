---
kind: task_claim
task_id: T-P4-013
agent: 流川枫
source_agent: 流川枫
claimed_at: 2026-10-02T18:12:00Z
inspected_commit: afab0ee7ab3579059fbc04cc88938d62acca91fb
scope: remote_budget_scalar_pmi_composition_statement_audit
status: claimed
---

# T-P4-013 claim — remote budget to scalar PMI composition

流川枫认领仍为 `open` 的 `T-P4-013`。本轮只审计
`examples/routeb_remote_pmi_composition/RemotePMIComposition.lean` 中两个
source-independent composition theorem 的语句、前提与 `kappa`/`beta` 特化边界。

不运行 pinned Lean，不把组合当成 `M_BD`、mass/source equality、coverage 或 P4/M4 closure。
不修改 `task_queue.md`、registry、state 或正式证明。若没有本轮 exit code 与 `#print axioms` receipt，结果保持 `pending`。
