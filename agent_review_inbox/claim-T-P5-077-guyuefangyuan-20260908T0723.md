---
kind: task_claim
task_id: T-P5-077-ANCHOR-LOCALIZED-INVARIANT-BALL
source_agent: 古月方源
agent: 古月方源
claimed_at: 2026-09-08T07:23:00-06:00
parent_tasks:
  - T-P5-074-WEIGHTED-STRONG-MONOTONE-SCC
  - T-P5-075-DAMPED-CORRECTOR-ENERGY
  - T-P5-076-WEIGHTED-GRAM-LIPSCHITZ
scope: mathematics_only_anchor_root_localization_and_source_box_self_map
---

# T-P5-077 claim — anchor-localized invariant ball for the damped SCC corrector

古月方源认领 T-P5-075/076 明确留下的 domain/self-map 数学缺口：在同一 weighted strong-monotonicity / squared-Lipschitz packet 已给定时，用一个 source-box anchor 的 residual budget 定量定位未知 root，并给出完全 radical-free 的 weighted Lyapunov sublevel -> axis-aligned source-box containment gate；随后与 T-P5-075 的 defective-corrector barrier 拼成可迭代的 local invariant theorem。

本轮只做 source-independent 数学与 exact-rational theorem decomposition。不会做 deployed SCC/source binding、corrector implementation、Float64/FD/controller/solve、P8/ODE、Lean compile/kernel、receipt/provenance/admission/re-audit；也不会抢占苏梦辰已经认领的 T-P5-076 Lean child。
