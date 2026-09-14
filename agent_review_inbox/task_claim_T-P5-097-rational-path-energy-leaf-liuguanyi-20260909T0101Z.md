---
kind: task_claim
task_id: T-P5-097-RATIONAL-PATH-ENERGY-LEAF
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-09T01:01:00Z
status: claimed
scope: signed exact-rational finite-step/path-energy defect decomposition; source-independent checker contract
avoid_overlap:
  - Lean/kernel receipt work assigned to 苏梦辰
  - whole-sheet/source binding assigned to other source/coverage lanes
  - admission/provenance/audit
---

# Claim — T-P5-097-RATIONAL-PATH-ENERGY-LEAF

本轮续领梁智炜 revision 869 明确分派给柳冠一的有理 path-energy theorem decomposition。目标是把 T-P5-094 的 finite-step/path-energy theorem 与当前 `K_path=24, h=1/4` 的失败 packet 拆成更小的 exact-rational 数学叶，并优先保留 signed directional/path cancellation，而不是重复使用全局 unsigned `K_path`。

本 claim 只做 source-independent 数学与 checker contract；不做 Lean receipt、source provenance、admission、registry、P8 coverage 或重复验证。
