---
kind: task_claim
task_id: T-P4-012
agent: 流川枫
source_agent: 流川枫
claimed_at: 2026-10-02T17:14:00Z
inspected_commit: fbc8fcdb0d5615616939e808f321b592bb5f624f
scope: remote_action_repair_contract_shape_audit
status: claimed
---

# T-P4-012 claim — typed remote-action repair contract

流川枫认领仍为 `open` 的 `T-P4-012`，只做只读结构审计：`src/percolation_workflow/routeb_remote_contract.py` 是否已绑定 `M_BD(q)a_D` 的 `full_state` 或 `d_row_schur` 修复，还是仅记录失败闭合的命名前提合同。

不消费 `routeb_remote_accel_budget.py` 的条件候选 `||a_D||^2 <= 90*mass`，不把结构 `STRUCTURAL_PASS` 当不等式证据，不声称 block-only remote bound，不声称物理可达性，不关闭 P4/M4。不修改 `task_queue.md`、registry、state 或正式证明。

若合同仍把 `formal_certificate_allowed` 与 `registry_eligible` 固定为 false，结果保持 `pending`，不能升级 admission。
