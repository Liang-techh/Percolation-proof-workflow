---
kind: task_claim
task_id: T-P4-039
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-07T16:02:00-06:00
inspected_commit: ee85de08d92bdac4492a5722989c954b8d4ac0f9
scope: same-cell shared-theta/shared-lambda multirow sign-robust Young feasibility; construct exact-rational bridge behind T-P4-037/T-P4-038 without source/admission work
related_tasks:
  - T-P4-024
  - T-P4-027
  - T-P4-037
  - T-P4-038
status: claimed
---

# Claim — T-P4-039

柳冠一认领 `T-P4-039`：证明同一 source cell 中多行 combined-Schur/Young 预算共用一个 `theta` / `lambda` 时的实质数学接口。

边界：只推进 source-independent 的 common-parameter 数学；不重复 `T-P4-038` 单行 discriminant/Lean 验证，不做 provenance、receipt、registry/admission，也不声称 concrete P4 row/cell 已满足 premises。

目标：给出一个无平方根、exact-rational、可由有限多项式不等式检查的共同参数构造；同时明确 rowwise PASS 为什么不足、构造何时保守、以及下一步最小 Lean theorem。