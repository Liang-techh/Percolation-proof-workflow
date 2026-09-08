---
kind: task_claim
task_id: T-P5-049
review_id: review-T-P5-049-guyuefangyuan-20260907T2234
agent: 古月方源
source_agent: 古月方源
claimed_at: 2026-09-07T22:25:00-06:00
inspected_commit: 23bfff2bf59d479a3b8acfa0f87edaba0a6052f5
continuation_of:
  - review-T-P5-046-guyuefangyuan-20260907T2132
  - review-T-P5-047-kuangmanmozun-20260907T2148
  - review-T-P5-048-liuguanyi-20260907T2200
scope: derive_an_exact_varying-curvature_finite-family_shared-r_feasibility_criterion_without_curvature_homogenization_using_one-dimensional_Helly_and_square-root-free_pairwise_interval_overlap; include_exact_obstruction_and_regression_examples
non_overlap: do_not_touch_T-P5-048_Lean_formalization_rank-one_boundary_source_receipts_provenance_coverage_or_admission
status: claimed
---

# T-P5-049 claim — exact varying-curvature shared-`r` feasibility

I will attack the mathematical gap explicitly left open by `T-P5-048`: a genuine shared-`r` feasibility theorem for finitely many concave quadratic gates with cell-dependent curvatures `d_i>0`, without first replacing them by a common-curvature lower minorant.

The target is a root-free/rational checker criterion based on (i) exact positivity of each one-row gate on `[0,1]`, (ii) exact pairwise overlap of the open positivity intervals, and (iii) the one-dimensional finite Helly property.  This is disjoint from the concurrent T-P5-048 Lean/CI, singular rank-one Lyapunov, source/Float64, receipt, coverage, and admission lanes.
