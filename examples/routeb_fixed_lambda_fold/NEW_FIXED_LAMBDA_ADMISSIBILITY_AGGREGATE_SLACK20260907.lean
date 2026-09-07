import NEW_FIXED_LAMBDA_ADMISSIBILITY_QUANTITATIVE_RESERVE_LOWER20260907
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBFixedLambdaAggregateSlack

open RouteBFixedLambdaAdmissibility
open RouteBFixedLambdaNoDivisionRatio
open RouteBFixedLambdaFiniteReserveAggregation
open RouteBFixedLambdaTwoEtaUnion
open RouteBFixedLambdaUniformFeasibility
open RouteBFixedLambdaWeightedAbsorption
open RouteBFixedLambdaFinalStrictExport
open RouteBFixedLambdaStrictReserveFinalBridge
open RouteBFixedLambdaQuantitativeReserveLower

noncomputable section

/-!
A lower bound on reserves alone cannot yield a positive margin-minus-reserve
slack.  This sidecar therefore makes the missing external aggregate premise
explicit: the total reserve plus the proposed sigma is bounded by an external
total margin, and the typed total margin equals that external quantity.
-/

structure ExternalTotalMarginSlackPremise
    (h : QuantitativeReserveLowerPremise cells) where
  externalTotalMargin : ℚ
  total_margin_eq_external :
    totalMargin cells h.params.lambda = externalTotalMargin
  reserve_plus_delta_le_external :
    totalReserve cells h.reserve +
        (∑ i in cells.rows, h.delta i) ≤ externalTotalMargin

def aggregateSigma
    (h : QuantitativeReserveLowerPremise cells) : ℚ :=
  ∑ i in cells.rows, h.delta i

structure AggregateSlackCertificate
    (h : QuantitativeReserveLowerPremise cells)
    (s : ExternalTotalMarginSlackPremise h) where
  sigma : ℚ
  sigma_eq_delta_sum : sigma = aggregateSigma h
  sigma_pos : 0 < sigma
  slack_lower_bound :
    sigma ≤ totalMargin cells h.params.lambda - totalReserve cells h.reserve

theorem build_aggregate_slack_certificate
    {cells : FiniteDisjointCellFamily}
    (h : QuantitativeReserveLowerPremise cells)
    (s : ExternalTotalMarginSlackPremise h) :
    AggregateSlackCertificate h s := by
  have hquant := build_strict_aggregate_reserve_lower_bound h
  refine
    { sigma := aggregateSigma h
      sigma_eq_delta_sum := rfl
      sigma_pos := hquant.positive_lower_bound
      slack_lower_bound := ?_ }
  unfold aggregateSigma
  rw [s.total_margin_eq_external]
  linarith [s.reserve_plus_delta_le_external]

/-!
The final adapter below consumes the existing final strict export rather than
re-proving it.  Its only additional mathematical premise is the explicit
total-equality adapter plus equality of the cell-family and final lambdas.
-/
theorem aggregate_slack_to_final_strict_consumer
    {cells : FiniteDisjointCellFamily}
    (h : QuantitativeReserveLowerPremise cells)
    (s : ExternalTotalMarginSlackPremise h)
    {f : Declared577SparseFold}
    (q : FixedLambdaParameters ℚ)
    (b : UniformMarginLowerBound f q.lambda)
    (p : ExplicitEtaSumPartition f)
    (coeff load : (EtaTag × Nat) → ℚ)
    (two : TwoRowMarginDenominatorPremise q)
    (adapter : ReserveToFinalBudgetAdapter cells
      (f := f) (lambda := h.params.lambda) h.reserve coeff load)
    (hshared_lambda : h.params.lambda = q.lambda)
    (final_export : FinalStrictConsumerExport q b p coeff load two) :
    0 < aggregateSigma h ∧
      aggregateSigma h ≤
        weightedMarginTotal (f := f) (lambda := q.lambda) coeff -
          weightedLoadTotal (f := f) coeff load ∧
      weightedLoadTotal (f := f) coeff load <
        weightedMarginTotal (f := f) (lambda := q.lambda) coeff := by
  have hcert := build_aggregate_slack_certificate h s
  have hmargin_eq :
      weightedMarginTotal (f := f) (lambda := q.lambda) coeff =
        totalMargin cells h.params.lambda := by
    simpa [hshared_lambda] using adapter.margin_total_eq
  have hload_eq :
      weightedLoadTotal (f := f) coeff load = totalReserve cells h.reserve :=
    adapter.load_total_eq
  have hslack :
      aggregateSigma h ≤
        weightedMarginTotal (f := f) (lambda := q.lambda) coeff -
          weightedLoadTotal (f := f) coeff load := by
    calc
      aggregateSigma h ≤
          totalMargin cells h.params.lambda - totalReserve cells h.reserve := by
            exact hcert.slack_lower_bound
      _ = weightedMarginTotal (f := f) (lambda := q.lambda) coeff -
          weightedLoadTotal (f := f) coeff load := by
            rw [hmargin_eq, hload_eq]
            rfl
  exact ⟨hcert.sigma_pos, hslack, final_export.union_load_lt_margin⟩

/- Admission boundary: sigma is conditional on an explicit external aggregate
   margin premise; no source, coverage, digest, or registry fact is inferred. -/

#print axioms build_aggregate_slack_certificate
#print axioms aggregate_slack_to_final_strict_consumer

end
end RouteBFixedLambdaAggregateSlack
