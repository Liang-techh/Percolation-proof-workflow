import NEW_FIXED_LAMBDA_ADMISSIBILITY_STRICT_RESERVE_FINAL_BRIDGE20260907
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBFixedLambdaQuantitativeReserveLower

open RouteBFixedLambdaAdmissibility
open RouteBFixedLambdaNoDivisionRatio
open RouteBFixedLambdaFiniteReserveAggregation
open RouteBFixedLambdaTwoEtaUnion
open RouteBFixedLambdaUniformFeasibility
open RouteBFixedLambdaWeightedAbsorption
open RouteBFixedLambdaFinalStrictExport
open RouteBFixedLambdaStrictReserveFinalBridge

noncomputable section

/-!
This sidecar adds only a quantitative lower-bound layer.  The cell family
retains its fixed parameter, support disjointness, positive denominators, and
ratio fields.  The new reserve contract is a per-cell lower bound by a
nonnegative `delta`; one explicit positive delta witness makes the aggregate
lower bound strict.
-/

structure QuantitativeReserveLowerPremise
    (f : FiniteDisjointCellFamily) where
  params : FixedLambdaParameters ℚ
  reserve : Nat → ℚ
  delta : Nat → ℚ
  delta_nonnegative :
    ∀ i ∈ f.rows, 0 ≤ delta i
  reserve_lower_bound :
    ∀ i ∈ f.rows, delta i ≤ reserve i
  rows_nonempty : f.rows.Nonempty
  positive_delta_witness :
    ∃ i ∈ f.rows, 0 < delta i

theorem total_delta_positive
    {f : FiniteDisjointCellFamily}
    (h : QuantitativeReserveLowerPremise f) :
    0 < ∑ i in f.rows, h.delta i := by
  exact Finset.sum_pos' h.delta_nonnegative h.positive_delta_witness

theorem total_delta_le_total_reserve
    {f : FiniteDisjointCellFamily}
    (h : QuantitativeReserveLowerPremise f) :
    (∑ i in f.rows, h.delta i) ≤ totalReserve f h.reserve := by
  unfold totalReserve
  apply Finset.sum_le_sum
  intro i hi
  exact h.reserve_lower_bound i hi

structure StrictAggregateReserveLowerBound
    {f : FiniteDisjointCellFamily}
    (h : QuantitativeReserveLowerPremise f) where
  rows_nonempty : f.rows.Nonempty
  positive_lower_bound : 0 < ∑ i in f.rows, h.delta i
  reserve_lower_bound :
    (∑ i in f.rows, h.delta i) ≤ totalReserve f h.reserve

theorem build_strict_aggregate_reserve_lower_bound
    {f : FiniteDisjointCellFamily}
    (h : QuantitativeReserveLowerPremise f) :
    StrictAggregateReserveLowerBound h := by
  exact
    { rows_nonempty := h.rows_nonempty
      positive_lower_bound := total_delta_positive h
      reserve_lower_bound := total_delta_le_total_reserve h }

/-!
The following adapter exposes the quantitative lower bound to an already
existing final weighted consumer.  It does not reconstruct the final export;
it preserves that export's strict budget as a separate premise.
-/
theorem quantitative_lower_bound_to_final_budget
    {cells : FiniteDisjointCellFamily}
    (h : QuantitativeReserveLowerPremise cells)
    {f : Declared577SparseFold} {lambda : ℚ}
    (q : FixedLambdaParameters ℚ)
    (b : UniformMarginLowerBound f q.lambda)
    (p : ExplicitEtaSumPartition f)
    (reserve : Nat → ℚ)
    (coeff load : (EtaTag × Nat) → ℚ)
    (two : TwoRowMarginDenominatorPremise q)
    (adapter : ReserveToFinalBudgetAdapter cells
      (f := f) (lambda := lambda) reserve coeff load)
    (hshared_lambda : lambda = q.lambda)
    (final_export : FinalStrictConsumerExport q b p coeff load two) :
    0 < ∑ i in cells.rows, h.delta i ∧
      (∑ i in cells.rows, h.delta i) ≤
        weightedLoadTotal (f := f) coeff load ∧
      weightedLoadTotal (f := f) coeff load <
        weightedMarginTotal (f := f) (lambda := q.lambda) coeff := by
  have hdelta_pos := total_delta_positive h
  have hdelta_reserve := total_delta_le_total_reserve h
  have hload_eq := adapter.load_total_eq
  have hload_lower :
      (∑ i in cells.rows, h.delta i) ≤
        weightedLoadTotal (f := f) coeff load := by
    rw [hload_eq]
    exact hdelta_reserve
  exact ⟨hdelta_pos, hload_lower, final_export.union_load_lt_margin⟩

/- Admission boundary: the lower bound is quantitative finite arithmetic only;
   missing rows/nonnegative deltas/positive witness keep it open. -/

#print axioms total_delta_positive
#print axioms total_delta_le_total_reserve
#print axioms build_strict_aggregate_reserve_lower_bound
#print axioms quantitative_lower_bound_to_final_budget

end
end RouteBFixedLambdaQuantitativeReserveLower
