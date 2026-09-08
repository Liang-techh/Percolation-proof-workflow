---
kind: task_claim
task_id: T-P5-066-ZERO-SURFACE-RECENTERING
agent: 柳冠一
source_agent: 柳冠一
claimed_at: 2026-09-08T04:03:00-06:00
inspected_commit: fb0ef3beff8e046cc44270288e5f5bd684003b79
parent_tasks:
  - T-P5-064-ANALYTIC-UNIT-PULLBACK
  - T-P5-065-RELATIVE-REMAINDER-ABSORPTION
scope: prove a minimal simple-zero displacement/recentering theorem for h=u*(x-r0)+e when the remainder is not divisible by the nominal factor, with exact assumptions separating root existence/location from exact recentered nonvanishing-unit factorization; record parameter/domain boundaries without auditing provenance/admission
non_overlap: do not redo T-P5-064 unit-pullback Lean repair, T-P5-065 same/higher-order remainder absorption, source provenance, receipt/admission, Float64, or P8 coverage
status: claimed
---

柳冠一认领一个最小但实质性的 source-to-math bridge：当 additive remainder 会移动 simple zero surface、因而无法直接消费 T-P5-064/065 时，证明 root displacement、唯一性与 recentered exact factorization 的充分条件，并明确何时只能得到位置包络而不能升级为 unit factorization。
