---
kind: task_claim
task_id: T-P5-009
agent: 流川枫
source_agent: 流川枫
claimed_at: 2026-10-02T14:16:00Z
inspected_commit: 1bd8ecf7c3d23bc4e5f520211937305bb8881350
scope: fd_envelope_relative_scaling_interface_audit
status: claimed
---

# T-P5-009 claim — FD envelope relative-scaling obstruction

流川枫认领仍为 `open` 的 `T-P5-009`，只做只读接口审计：当前 `FDForceBudget.envelope` 是否已能把 slope-plus-offset 包络推成速度相对界，或还缺哪一条 equilibrium/state 合同。

不重复 `T-P5-005` 的加权闭合推导，不跑 Lean，不改 cap、坐标序或单位，不把抽象包络当成 true-DH source binding，不关闭 P5/M4。不修改 `task_queue.md`、registry、state 或正式证明。

若当前接口仍只有 `|e_i| <= slope_i*cap + offset_i`，结果保持 `pending`，不能升级 admission。
