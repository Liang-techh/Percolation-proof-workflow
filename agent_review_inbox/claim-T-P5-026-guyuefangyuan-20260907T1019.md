---
kind: task_claim
task_id: T-P5-026
source_agent: 古月方源
agent: 古月方源
claimed_at: 2026-09-07T10:19:00-06:00
status: claimed
continuation_of:
  - review-T-P5-025-liuguanyi-20260907T1020
  - review-T-P5-024-kuangmanmozun-20260907T0945
  - review-T-P5-020-guyuefangyuan-20260907T0743
---

# Claim — T-P5-026

I claim one bounded mathematical refinement of the direct `K_path` small-gain route: replace the globally-PSD sign-matrix checks of T-P5-025 by an exact feasible-cone reduction and a rational PSD-plus-entrywise-nonnegative (SPN) certificate on nonnegative cone coordinates.

Scope is source-independent mathematics only. I will prove the cone cover, count/remove impossible sign patterns, state the direct dissipation theorem, show that the SPN consumer strictly contains the previous PSD consumer, and give a Lean/checker-oriented theorem decomposition. I will not claim a concrete source `K_path`, Float64/Jacobian binding, P8 coverage, admission, provenance, or final P5/M4 closure.
