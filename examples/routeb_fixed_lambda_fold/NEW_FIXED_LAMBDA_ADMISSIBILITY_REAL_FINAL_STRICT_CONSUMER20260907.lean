import NEW_FIXED_LAMBDA_ADMISSIBILITY_COMPOSED_REINDEX_SLACK20260907
import NEW_FIXED_LAMBDA_ADMISSIBILITY_RAT_REAL_FINITE_SUM_CAST20260907
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBFixedLambdaRealFinalStrictConsumer

open RouteBFixedLambdaAdmissibility
open RouteBFixedLambdaFiniteReindexSumEquality
open RouteBFixedLambdaComposedReindexSlack
open RouteBFixedLambdaAggregateSlack
open RouteBFixedLambdaRatRealFiniteSumCast
open RouteBFixedLambdaWeightedAbsorption

noncomputable section

/-!
This sidecar is the real-valued final consumer for the already-composed
rational fixed-lambda budget.  It records the rational source/target totals,
their real cast chain, the casted sigma, and the casted margin-minus-load gap.
No finite reindex, finite-sum cast, or rational slack theorem is reproved.
-/

def rationalSourceTotal
    {h : QuantitativeReserveLowerPremise cells}
    {s : ExternalTotalMarginSlackPremise h}
    {f : Declared577SparseFold}
    (q : FixedLambdaParameters ℚ)
    (coeff load : (EtaTag × Nat) → ℚ)
    (a : ComposedReindexSlackAdapter h s q coeff load) : ℚ :=
  ∑ i in a.reindex.source, a.reindex.sourceWeight i

def rationalTargetTotal
    {h : QuantitativeReserveLowerPremise cells}
    {s : ExternalTotalMarginSlackPremise h}
    {f : Declared577SparseFold}
    (q : FixedLambdaParameters ℚ)
    (coeff load : (EtaTag × Nat) → ℚ)
    (a : ComposedReindexSlackAdapter h s q coeff load) : ℚ :=
  ∑ j in a.reindex.target, a.reindex.targetWeight j

def rationalMarginTotal
    {f : Declared577SparseFold}
    (q : FixedLambdaParameters ℚ)
    (coeff : (EtaTag × Nat) → ℚ) : ℚ :=
  weightedMarginTotal (f := f) (lambda := q.lambda) coeff

def rationalLoadTotal
    {f : Declared577SparseFold}
    (coeff load : (EtaTag × Nat) → ℚ) : ℚ :=
  weightedLoadTotal (f := f) coeff load

def realSigma
    {h : QuantitativeReserveLowerPremise cells}
    {s : ExternalTotalMarginSlackPremise h}
    (slack : AggregateSlackCertificate h s) : ℝ :=
  (slack.sigma : ℝ)

def realMarginTotal
    {f : Declared577SparseFold}
    (q : FixedLambdaParameters ℚ)
    (coeff : (EtaTag × Nat) → ℚ) : ℝ :=
  (rationalMarginTotal q coeff : ℝ)

def realLoadTotal
    {f : Declared577SparseFold}
    (coeff load : (EtaTag × Nat) → ℚ) : ℝ :=
  (rationalLoadTotal coeff load : ℝ)

structure RealFinalStrictConsumerAdapter
    {cells : FiniteDisjointCellFamily}
    (h : QuantitativeReserveLowerPremise cells)
    (s : ExternalTotalMarginSlackPremise h)
    {f : Declared577SparseFold}
    (q : FixedLambdaParameters ℚ)
    (coeff load : (EtaTag × Nat) → ℚ)
    (a : ComposedReindexSlackAdapter h s q coeff load)
    (slack : AggregateSlackCertificate h s) where
  source_total_eq_reserve :
    rationalSourceTotal q coeff load a = totalReserve cells h.reserve
  target_total_eq_load :
    rationalTargetTotal q coeff load a = rationalLoadTotal coeff load
  margin_total_eq_cell_margin :
    rationalMarginTotal q coeff = totalMargin cells h.params.lambda
  shared_lambda : h.params.lambda = q.lambda
  source_real_eq_cast :
    sourceRealSum a.reindex = (rationalSourceTotal q coeff load a : ℝ)
  target_real_eq_cast :
    targetRealSum a.reindex = (rationalTargetTotal q coeff load a : ℝ)
  source_target_real_eq :
    sourceRealSum a.reindex = targetRealSum a.reindex
  sigma_eq_cast :
    realSigma slack = (slack.sigma : ℝ)
  sigma_pos : 0 < realSigma slack
  sigma_le_cast_rational_gap :
    realSigma slack ≤
      ((rationalMarginTotal q coeff - rationalLoadTotal coeff load : ℚ) : ℝ)
  margin_load_gap_eq_cast :
    realMarginTotal q coeff - realLoadTotal coeff load =
      ((rationalMarginTotal q coeff - rationalLoadTotal coeff load : ℚ) : ℝ)
  sigma_le_real_gap :
    realSigma slack ≤ realMarginTotal q coeff - realLoadTotal coeff load

theorem build_real_final_strict_consumer_adapter
    {cells : FiniteDisjointCellFamily}
    (h : QuantitativeReserveLowerPremise cells)
    (s : ExternalTotalMarginSlackPremise h)
    {f : Declared577SparseFold}
    (q : FixedLambdaParameters ℚ)
    (coeff load : (EtaTag × Nat) → ℚ)
    (a : ComposedReindexSlackAdapter h s q coeff load)
    (slack : AggregateSlackCertificate h s) :
    RealFinalStrictConsumerAdapter h s q coeff load a slack := by
  have hbudget :=
    composed_reindex_and_slack_give_final_strict_budget
      h s q coeff load a slack
  have hsource_total_eq_reserve :
      rationalSourceTotal q coeff load a = totalReserve cells h.reserve := by
    exact a.source_reserve_eq
  have htarget_total_eq_load :
      rationalTargetTotal q coeff load a = rationalLoadTotal coeff load := by
    exact a.target_load_eq
  have hmargin_total_eq_cell_margin :
      rationalMarginTotal q coeff = totalMargin cells h.params.lambda := by
    exact a.final_margin_eq
  have hsource_real_eq_cast :
      sourceRealSum a.reindex = (rationalSourceTotal q coeff load a : ℝ) := by
    exact source_real_sum_eq_cast_source_rat_sum a.reindex
  have htarget_real_eq_cast :
      targetRealSum a.reindex = (rationalTargetTotal q coeff load a : ℝ) := by
    exact target_real_sum_eq_cast_target_rat_sum a.reindex
  have hsource_target_real_eq :
      sourceRealSum a.reindex = targetRealSum a.reindex := by
    exact finite_reindex_weight_sum_eq_after_rat_real_cast a.reindex
  have hsigma_pos : 0 < realSigma slack := by
    unfold realSigma
    exact_mod_cast hbudget.1
  have hrat_gap_le :
      slack.sigma ≤ rationalMarginTotal q coeff - rationalLoadTotal coeff load := by
    simpa [rationalMarginTotal, rationalLoadTotal] using hbudget.2.1
  have hsigma_le_cast_rational_gap :
      realSigma slack ≤
        ((rationalMarginTotal q coeff - rationalLoadTotal coeff load : ℚ) : ℝ) := by
    unfold realSigma
    exact_mod_cast hrat_gap_le
  have hmargin_load_gap_eq_cast :
      realMarginTotal q coeff - realLoadTotal coeff load =
        ((rationalMarginTotal q coeff - rationalLoadTotal coeff load : ℚ) : ℝ) := by
    unfold realMarginTotal realLoadTotal
    norm_num
  have hsigma_le_real_gap :
      realSigma slack ≤ realMarginTotal q coeff - realLoadTotal coeff load := by
    calc
      realSigma slack ≤
          ((rationalMarginTotal q coeff - rationalLoadTotal coeff load : ℚ) : ℝ) :=
        hsigma_le_cast_rational_gap
      _ = realMarginTotal q coeff - realLoadTotal coeff load :=
        hmargin_load_gap_eq_cast.symm
  exact
    { source_total_eq_reserve := hsource_total_eq_reserve
      target_total_eq_load := htarget_total_eq_load
      margin_total_eq_cell_margin := hmargin_total_eq_cell_margin
      shared_lambda := a.shared_lambda
      source_real_eq_cast := hsource_real_eq_cast
      target_real_eq_cast := htarget_real_eq_cast
      source_target_real_eq := hsource_target_real_eq
      sigma_eq_cast := rfl
      sigma_pos := hsigma_pos
      sigma_le_cast_rational_gap := hsigma_le_cast_rational_gap
      margin_load_gap_eq_cast := hmargin_load_gap_eq_cast
      sigma_le_real_gap := hsigma_le_real_gap }

theorem real_load_lt_real_margin_of_casted_sigma
    {cells : FiniteDisjointCellFamily}
    {h : QuantitativeReserveLowerPremise cells}
    {s : ExternalTotalMarginSlackPremise h}
    {f : Declared577SparseFold}
    {q : FixedLambdaParameters ℚ}
    {coeff load : (EtaTag × Nat) → ℚ}
    {a : ComposedReindexSlackAdapter h s q coeff load}
    {slack : AggregateSlackCertificate h s}
    (adapter : RealFinalStrictConsumerAdapter h s q coeff load a slack) :
    realLoadTotal coeff load < realMarginTotal q coeff := by
  exact sub_pos.mp
    (lt_of_lt_of_le adapter.sigma_pos adapter.sigma_le_real_gap)

theorem real_final_strict_consumer_output
    {cells : FiniteDisjointCellFamily}
    {h : QuantitativeReserveLowerPremise cells}
    {s : ExternalTotalMarginSlackPremise h}
    {f : Declared577SparseFold}
    {q : FixedLambdaParameters ℚ}
    {coeff load : (EtaTag × Nat) → ℚ}
    {a : ComposedReindexSlackAdapter h s q coeff load}
    {slack : AggregateSlackCertificate h s}
    (adapter : RealFinalStrictConsumerAdapter h s q coeff load a slack) :
    0 < realSigma slack ∧
      realSigma slack ≤ realMarginTotal q coeff - realLoadTotal coeff load ∧
      realLoadTotal coeff load < realMarginTotal q coeff := by
  exact ⟨adapter.sigma_pos, adapter.sigma_le_real_gap,
    real_load_lt_real_margin_of_casted_sigma adapter⟩

/- Admission boundary: all rational source/target, sigma positivity, shared
   lambda, and cast-gap premises remain explicit.  This is not a source,
   coverage, comparator, Lean-verification, or registry theorem. -/

#print axioms build_real_final_strict_consumer_adapter
#print axioms real_load_lt_real_margin_of_casted_sigma
#print axioms real_final_strict_consumer_output

end
end RouteBFixedLambdaRealFinalStrictConsumer
