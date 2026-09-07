import NEW_FIXED_LAMBDA_ADMISSIBILITY_FINITE_REINDEX_SUM_EQUALITY20260907
import NEW_FIXED_LAMBDA_ADMISSIBILITY_AGGREGATE_SLACK20260907
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBFixedLambdaComposedReindexSlack

open RouteBFixedLambdaAdmissibility
open RouteBFixedLambdaFiniteReindexSumEquality
open RouteBFixedLambdaFiniteReserveAggregation
open RouteBFixedLambdaTwoEtaUnion
open RouteBFixedLambdaUniformFeasibility
open RouteBFixedLambdaWeightedAbsorption
open RouteBFixedLambdaFinalStrictExport
open RouteBFixedLambdaAggregateSlack
open RouteBFixedLambdaQuantitativeReserveLower

noncomputable section

/-!
This sidecar composes two already separate facts: finite reindex equality and
an aggregate positive-slack certificate.  Every bridge between the source
cell sum, target weighted-load sum, and final weighted-margin sum is explicit.
-/

structure ComposedReindexSlackAdapter
    {cells : FiniteDisjointCellFamily}
    (h : QuantitativeReserveLowerPremise cells)
    (s : ExternalTotalMarginSlackPremise h)
    {f : Declared577SparseFold}
    (q : FixedLambdaParameters ℚ)
    (coeff load : (EtaTag × Nat) → ℚ) where
  reindex : FiniteReindexWeightAdapter
  source_reserve_eq :
    sourceSum reindex.source reindex.sourceWeight =
      totalReserve cells h.reserve
  target_load_eq :
    targetSum reindex.target reindex.targetWeight =
      weightedLoadTotal (f := f) coeff load
  final_margin_eq :
    weightedMarginTotal (f := f) (lambda := q.lambda) coeff =
      totalMargin cells h.params.lambda
  shared_lambda : h.params.lambda = q.lambda

/-!
The previous theorem's explicit slack premise is carried directly here.  A
small existential-style output records the final strict inequality without
re-proving the reserve or reindex lemmas.
-/
theorem composed_reindex_and_slack_give_final_strict_budget
    {cells : FiniteDisjointCellFamily}
    (h : QuantitativeReserveLowerPremise cells)
    (s : ExternalTotalMarginSlackPremise h)
    {f : Declared577SparseFold}
    (q : FixedLambdaParameters ℚ)
    (coeff load : (EtaTag × Nat) → ℚ)
    (a : ComposedReindexSlackAdapter h s q coeff load)
    (slack : AggregateSlackCertificate h s) :
    0 < slack.sigma ∧
      slack.sigma ≤
        weightedMarginTotal (f := f) (lambda := q.lambda) coeff -
          weightedLoadTotal (f := f) coeff load ∧
      weightedLoadTotal (f := f) coeff load <
        weightedMarginTotal (f := f) (lambda := q.lambda) coeff := by
  have hload_eq :
      totalReserve cells h.reserve =
        weightedLoadTotal (f := f) coeff load := by
    calc
      totalReserve cells h.reserve =
          sourceSum a.reindex.source a.reindex.sourceWeight :=
        a.source_reserve_eq.symm
      _ = targetSum a.reindex.target a.reindex.targetWeight :=
        finite_reindex_weight_sum_eq a.reindex
      _ = weightedLoadTotal (f := f) coeff load := a.target_load_eq
  have hmargin_eq :
      weightedMarginTotal (f := f) (lambda := q.lambda) coeff =
        totalMargin cells h.params.lambda := by
    exact a.final_margin_eq
  have hslack :
      slack.sigma ≤
        weightedMarginTotal (f := f) (lambda := q.lambda) coeff -
          weightedLoadTotal (f := f) coeff load := by
    calc
      slack.sigma ≤
          totalMargin cells h.params.lambda - totalReserve cells h.reserve :=
        slack.slack_lower_bound
      _ = weightedMarginTotal (f := f) (lambda := q.lambda) coeff -
          weightedLoadTotal (f := f) coeff load := by
        rw [hmargin_eq, hload_eq]
  have hpositive_gap :
      0 < weightedMarginTotal (f := f) (lambda := q.lambda) coeff -
        weightedLoadTotal (f := f) coeff load :=
    lt_of_lt_of_le slack.sigma_pos hslack
  exact ⟨slack.sigma_pos, hslack, sub_pos.mp hpositive_gap⟩

/- Admission boundary: all reindex, total-equality, shared-lambda, and
   positive-slack premises remain explicit; no coverage/source claim follows. -/

#print axioms composed_reindex_and_slack_give_final_strict_budget

end
end RouteBFixedLambdaComposedReindexSlack
