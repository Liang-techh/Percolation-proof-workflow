---
kind: task_claim
task_id: T-P5-047
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
claimed_at: 2026-09-07T21:35:00-06:00
inspected_commit: 349807ff733f047664136c3f7172666e15d4a2a7
status: claimed
---

# T-P5-047 claim — exact shared-r optimizer for simultaneous correlated P5 gates

I claim a new bounded mathematical child continuing T-P5-045/T-P5-046: determine whether the quarter-barrier and parameter/incremental correlated gates can be satisfied by one and the same Pareto parameter `r in [0,1]`, rather than optimizing the two gates independently.

Scope: exact inequality closure / obstruction only. I will exploit that both gate margins have the same quadratic curvature in `r`, so their difference is affine. The target is a finite exact-rational candidate set (endpoints, active branch vertices, and the affine crossover), a necessary-and-sufficient no-grid common-`r` criterion, and counterexamples showing that separate per-gate PASS does not imply a shared feasible `r` and that the crossover candidate can be essential.

Out of scope: deployed source binding, Float64/controller semantics, coverage/flowpipe, Lean compilation, provenance/admission, registry updates, or re-audit of existing candidates.