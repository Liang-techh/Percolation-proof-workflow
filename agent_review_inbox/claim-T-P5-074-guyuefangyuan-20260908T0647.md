---
kind: task_claim
task_id: T-P5-074-WEIGHTED-STRONG-MONOTONE-SCC
source_agent: 古月方源
agent: 古月方源
claimed_at: 2026-09-08T06:47:00-06:00
parent_tasks:
  - T-P5-070-TRIANGULAR-MULTICONTACT-CHART
  - T-P5-071-SIGNED-TWO-CYCLE-CONTACT
  - T-P5-072-SIGNED-SIMPLE-CYCLE-CONTACT
scope: mathematics_only_general_scc_weighted_strong_monotonicity
---

# T-P5-074 claim — weighted strong-monotone contact chart for general SCCs

古月方源认领 T-P5-072 明确留下的下一层数学缺口：当 contact SCC 含 chord、一个 root 同时依赖多个 contact，因而不再是 triangular/simple-cycle 时，寻找一个仍能利用 signed cross-coupling、且比 absolute small-gain 更强的可检查 sufficient theorem。

本轮只做 source-independent 数学：构造 weighted strong-monotonicity / signed symmetric-part certificate，给出 general SCC 的唯一性、定量 inverse bound、common-core existence 接口、exact-rational diagonal-dominance checker，以及 absolute small-gain 会假阴性的 negative-feedback/skew counterexample。不会做 source binding、Float64/FD/controller/solve、P8/ODE、Lean compile/kernel、receipt/provenance/admission/re-audit，也不会抢占 T-P5-073 的 Lean lane。
