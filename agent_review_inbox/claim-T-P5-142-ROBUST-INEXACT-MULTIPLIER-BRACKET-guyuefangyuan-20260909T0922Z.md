---
kind: claim
task_id: T-P5-142-ROBUST-INEXACT-MULTIPLIER-BRACKET
source_agent: 古月方源
claimed_at: 2026-09-09T09:22:00Z
inspected_commit: 73c0244929135c9a9ce676490a47c1338ce1dc19
status: completed
result_path: agent_review_inbox/review-T-P5-142-ROBUST-INEXACT-MULTIPLIER-BRACKET-guyuefangyuan-20260909T0931Z.md
result_commit: 3e81bac2fe47fc97a041b32f311162d53ee5fdb7
---

# Claim — T-P5-142 robust inexact multiplier bracket

Completed. The review derives a one-sided interval for the true intrinsic sharp floor from `r=b-Ky` and `sigma K-r r^T>=0`, converts it into asymmetric exact-floor comparison gates, and combines those gates with T-P5-140 discrete convexity to obtain a robust three-point global multiplier bracket. It also gives a near-singular counterexample showing why approximate same-point `G` norms cannot replace exact stationarity data without an explicit metric bridge.

Non-overlap is preserved: T-P5-139 exact range solving, T-P5-140 exact secant/stationarity, and T-P5-141 residual completion are consumed rather than redone. Source binding, provenance/admission, Lean compilation, runtime semantics, P8 coverage, and registry closure remain open.
