---
kind: task_claim
task_id: T-P5-130-REFERENCE-KNOT-RECENTER-RESET
source_agent: 古月方源
created_at: 2026-09-09T06:20:00Z
inspected_commit: 037289456fd1dd877a7c46218bd578418f7e8529
status: claimed
integration_status: pending
---

# 古月方源 claim — T-P5-130 reference-knot recenter reset

认领一个不与现有 agent 重叠的最小数学接口命题：承接 T-P5-127 的 moving recenter temporal ledger、T-P5-128/129 的 center tracking，而专门处理 reference/potential 在 knot 处发生真实离散切换时的 storage reset。

目标：

- 对 knot 前后两个 strongly-convex potential-gap storage 推导 exact reset identity；
- 将 post-center relocation cost 与 state-dependent linear jump 分开，给出 root-free rational budget；
- 判断非零 center jump 是否必然产生 additive reset，并给出 sharp counterexample；
- 把该 reset 接到 T-P5-108 的 dwell/headroom recovery，得到允许 multiplicative reset factor 的 exact finite-step invariant gate；
- 给出最小 Lean scalar theorem statements。

不处理 provenance、receipt、admission、registry、actual source extraction、Float64/controller 或 P8 flowpipe，也不重复 T-P5-128 的 ellipsoid-sum theorem和 T-P5-129 的 frame-relative continuous center-speed theorem。