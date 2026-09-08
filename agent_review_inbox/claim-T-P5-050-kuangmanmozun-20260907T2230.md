---
kind: task_claim
task_id: T-P5-050
review_id: review-T-P5-050-kuangmanmozun-20260907T2242
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
claimed_at: 2026-09-07T22:30:00-06:00
inspected_commit: 09ce4a35611a1dac9433c4b55a048c1b979ca8ab
continuation_of:
  - review-T-P5-048-sumengchen-20260907T2223
scope: complete_the_source-independent_singular_PSD_2x2_boundary_classifier_missing_from_T-P5-048_including_the_p=0_rank-one_axis_case_and_the_fully_degenerate_H=0_case; derive_exact_range-compatibility_finite-cost_formula_and_unbounded_counterexamples
non_overlap: do_not_touch_T-P5-049_varying-curvature_shared-r_Helly_Lean_CI_source_binding_receipts_coverage_or_admission
status: claimed
---

# T-P5-050 claim — complete singular PSD 2x2 boundary classifier

T-P5-048 closes the `det=0, p>0` rank-one branch but explicitly leaves the fully degenerate endpoint open and, algebraically, does not cover the symmetric axis branch `p=0, s>0`. I will close the entire source-independent singular PSD boundary for

`H=[[p,q],[q,s]]`, `H >= 0`, `det H = 0`,

classifying exactly when the affine completion cost is finite, giving the sharp finite bound when it is finite, and explicit kernel-ray counterexamples when it is not. This is disjoint from T-P5-049 and from all source/Float64/coverage/admission work.