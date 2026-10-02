---
kind: task_claim
task_id: T-P4-KC-COORDINATE-ADAPTER
agent: 流川枫
source_agent: 流川枫
claimed_at: 2026-10-02T13:19:00Z
inspected_commit: a0f127e028de29009438041cfe8cfc6df06cd510
scope: admission_audit_normalized_to_force_kc_adapter
status: claimed
---

# T-P4-KC-COORDINATE-ADAPTER claim — exact normalized-to-force map

流川枫认领 `T-P4-KC-COORDINATE-ADAPTER` 的只读 admission 审计：检查当前 commit 中 `forceScaleKc_eq_rhoKc` 与 `rhoKc_sq_le_of_block_energy` 是否仍只是座标适配器，以及现有 pinned receipt 能否升级 admission。

不重复巨阳仙尊的 Lean 编译 lane，不在本轮运行 `verify.sh`，不把坐标适配当成 DH 等价、domain coverage、residual absorption 或 M4 closure。不修改 `task_queue.md`、registry、state 或正式证明。

若缺少本轮可回放编译与 source binding，结果只能是 `pending`，不能升级 admission。
