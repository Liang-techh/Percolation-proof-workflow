import NEW_FIXED_LAMBDA_ADMISSIBILITY_FINITE_RESERVE_AGGREGATION20260907
import NEW_FIXED_LAMBDA_ADMISSIBILITY_FINAL_STRICT_EXPORT20260907
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBFixedLambdaStrictReserveFinalBridge

open RouteBFixedLambdaAdmissibility
open RouteBFixedLambdaNoDivisionRatio
open RouteBFixedLambdaFiniteReserveAggregation
open RouteBFixedLambdaTwoEtaUnion
open RouteBFixedLambdaUniformFeasibility
open RouteBFixedLambdaWeightedAbsorption
open RouteBFixedLambdaFinalStrictExport

noncomputable section

/-!
This sidecar supplies the strict finite-reserve parent seam.  The cell family
already carries pairwise-disjoint supports and positive denominators.  The new
premises are explicit nonnegativity, finite nonemptiness, and one strict
cross-multiplied reserve witness.
-/

structure StrictReserveFamilyPremise
    (f : FiniteDisjointCellFamily) where
  params : FixedLambdaParameters ℚ
  reserve : Nat → ℚ
  reserve_nonnegative :
    ∀ i ∈ f.rows, 0 ≤ reserve i
  reserve_cross_le :
    ∀ i ∈ f.rows,
      params.lambda * (f.cell i).cellGamma + reserve i ≤
        (f.cell i).externalGamma
  rows_nonempty : f.rows.Nonempty
  strict_reserve_witness :
    ∃ i ∈ f.rows,
      params.lambda * (f.cell i).cellGamma + reserve i <
        (f.cell i).externalGamma

theorem strict_total_reserve_lt_total_margin
    {f : FiniteDisjointCellFamily}
    (h : StrictReserveFamilyPremise f) :
    totalReserve f h.reserve < totalMargin f h.params.lambda := by
  unfold totalReserve totalMargin
  apply Finset.sum_lt_sum
  · intro i hi
    exact cross_multiplied_reserve_implies_margin_lower_bound
      (f.cell i) (h.reserve_cross_le i hi)
  · rcases h.strict_reserve_witness with ⟨i, hi, hstrict⟩
    exact ⟨i, hi,
      strict_cross_multiplied_reserve_implies_strict_margin_lower_bound
        (f.cell i) (h.reserve_nonnegative i hi) hstrict⟩

/-!
The adapter below is intentionally equality-based.  It is the minimal extra
premise needed to connect an independently indexed finite cell family to the
existing final weighted consumer; no index/row identity is inferred here.
-/

structure ReserveToFinalBudgetAdapter
    (cells : FiniteDisjointCellFamily)
    {f : Declared577SparseFold} {lambda : ℚ}
    (reserve : Nat → ℚ)
    (coeff load : (EtaTag × Nat) → ℚ) where
  load_total_eq :
    weightedLoadTotal coeff load = totalReserve cells reserve
  margin_total_eq :
    weightedMarginTotal (f := f) (lambda := lambda) coeff =
      totalMargin cells lambda

theorem strict_reserve_satisfies_final_weighted_budget
    {cells : FiniteDisjointCellFamily}
    (h : StrictReserveFamilyPremise cells)
    {f : Declared577SparseFold} {lambda : ℚ}
    (reserve : Nat → ℚ)
    (coeff load : (EtaTag × Nat) → ℚ)
    (adapter : ReserveToFinalBudgetAdapter cells
      (f := f) (lambda := lambda) reserve coeff load) :
    weightedLoadTotal (f := f) coeff load <
      weightedMarginTotal (f := f) (lambda := lambda) coeff := by
  rw [adapter.load_total_eq, adapter.margin_total_eq]
  simpa [h.params.lambda_eq_two] using
    (strict_total_reserve_lt_total_margin h)

/-!
If a caller also supplies the existing two-row premise, this budget inequality
is exactly the union-budget field required by `FinalStrictConsumerExport`.
The export itself remains conditional on those separately typed row premises.
-/
theorem final_budget_field_of_strict_reserve
    {cells : FiniteDisjointCellFamily}
    (h : StrictReserveFamilyPremise cells)
    {f : Declared577SparseFold} {lambda : ℚ}
    (q : FixedLambdaParameters ℚ)
    (b : UniformMarginLowerBound f q.lambda)
    (p : ExplicitEtaSumPartition f)
    (reserve : Nat → ℚ)
    (coeff load : (EtaTag × Nat) → ℚ)
    (two : TwoRowMarginDenominatorPremise q)
    (adapter : ReserveToFinalBudgetAdapter cells
      (f := f) (lambda := lambda) reserve coeff load)
    (hshared_lambda : lambda = q.lambda) :
    weightedLoadTotal (f := f) coeff load <
      weightedMarginTotal (f := f) (lambda := q.lambda) coeff := by
  have hbudget := strict_reserve_satisfies_final_weighted_budget
    h reserve coeff load adapter
  simpa [hshared_lambda] using hbudget

theorem build_final_strict_export_from_strict_reserve
    {cells : FiniteDisjointCellFamily}
    (h : StrictReserveFamilyPremise cells)
    {f : Declared577SparseFold} {lambda : ℚ}
    (q : FixedLambdaParameters ℚ)
    (b : UniformMarginLowerBound f q.lambda)
    (p : ExplicitEtaSumPartition f)
    (reserve : Nat → ℚ)
    (coeff load : (EtaTag × Nat) → ℚ)
    (two : TwoRowMarginDenominatorPremise q)
    (adapter : ReserveToFinalBudgetAdapter cells
      (f := f) (lambda := lambda) reserve coeff load)
    (hshared_lambda : lambda = q.lambda) :
    FinalStrictConsumerExport q b p coeff load two := by
  refine
    { union_load_lt_margin := final_budget_field_of_strict_reserve
        h q b p reserve coeff load two adapter hshared_lambda
      two_row_upper_strict := two.upper_strict
      two_row_positive_margin := two_row_positive_margin_of_upper two
      two_row_admissible := two_row_admissible_of_upper two }

/- Admission boundary: missing nonempty or strict-witness premises leave this
   certificate open; no source, coverage, digest, or registry closure follows. -/

#print axioms strict_total_reserve_lt_total_margin
#print axioms strict_reserve_satisfies_final_weighted_budget
#print axioms final_budget_field_of_strict_reserve
#print axioms build_final_strict_export_from_strict_reserve

end
end RouteBFixedLambdaStrictReserveFinalBridge
