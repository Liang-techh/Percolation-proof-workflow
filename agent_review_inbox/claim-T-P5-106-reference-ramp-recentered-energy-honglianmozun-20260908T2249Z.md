---
kind: task_claim
task_id: T-P5-106-REFERENCE-RAMP-RECENTERED-ENERGY
agent: 红莲魔尊
source_agent: 红莲魔尊
coordinator: 梁智炜
created_at: 2026-09-08T22:49:00Z
status: claimed
inspected_commit: c1bc01495c5589ce13b2b36950dd6c4307c44b95
upstream:
  - T-P5-104-REFERENCE-CROSS-ENERGY-COLLAR
  - T-P5-105-NONSYMMETRIC-REFERENCE-COLLAR
  - P5-103-ACTUAL-REFERENCE-CONTEXT-BINDING
---

# Claim — T-P5-106 reference ramp recentered energy

红莲魔尊认领一个不与 T-P5-105 重复的最小 energy child：对当前 nonsymmetric Route-B reference law `M q'' + D q' + B q = g w(t)`，寻找 exact algebraic input-following center `a`（只要求 `B a = g`），并比较“位置-only recenter”与同时平移速度的 recenter。目标是把持续输入振幅从 `Vdot` 中精确消掉，只让 ramp slope/curvature 进入 energy ledger；优先给出对连续 piecewise-affine ramp 无人工 reset 的 Lyapunov identity、division-free collar gate、absolute `pB` 回接，以及 coefficient mismatch / input jump 的精确 obstruction。

Non-overlap: 不重复柳冠一的 T-P5-105 skew-stiffness derivative/PSD packet；不做 P5-103 source 字段搜索或 Lean CI；不做狂蛮魔尊的 observation-kernel repair；不做 provenance/receipt/admission/re-audit；不声明 actual runtime/referenceKey/P8 coverage 已绑定。
