---
kind: review_result
task_id: T-P4-032
source_agent: Liang-techh coordinator
created_at: 2026-09-07
integration_status: pending
---

基于独立 API review 应用最小候选修复：

1. 增加 `import Mathlib.Tactic.Linarith`；
2. `hB_left` 的 `simpa only` 增加 `Matrix.mul_assoc`，仅规范三矩阵乘积括号；
3. 保持显式 `h_inv_left : M_DD_inv * M_DD = 1`，不引入 `nonsing_inv` 或 solver。

当前候选文件的 SHA-256 为
`403C41C6F325E906A9D3555B6886D1371DFA2D84826ABCC7BF83C12E21293BFB`。
该修复尚未运行 Lean/Lake，因此状态为 `REPAIR_PATCHED__PENDING_LEAN_COMPILE`，
不可进入 registry，也不改变 `formal_certificate_allowed=false`。
