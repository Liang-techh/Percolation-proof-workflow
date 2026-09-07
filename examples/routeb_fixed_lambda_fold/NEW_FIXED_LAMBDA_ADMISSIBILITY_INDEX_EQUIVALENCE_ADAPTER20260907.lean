import NEW_FIXED_LAMBDA_ADMISSIBILITY_FINAL_STRICT_EXPORT20260907
import NEW_FIXED_LAMBDA_ADMISSIBILITY_FINITE_RESERVE_AGGREGATION20260907
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBFixedLambdaIndexEquivalenceAdapter

open RouteBFixedLambdaAdmissibility
open RouteBFixedLambdaFiniteReserveAggregation
open RouteBFixedLambdaTwoEtaUnion
open RouteBFixedLambdaUniformFeasibility
open RouteBFixedLambdaWeightedAbsorption
open RouteBFixedLambdaFinalStrictExport

noncomputable section

/-!
This sidecar is an explicit transport adapter between an independently
indexed finite cell family and the existing tagged final union.  No equality
of totals is inferred from a row count: the row map, its finite image
properties, cell-value preservation, lambda equality, and both total
equalities are all fields of the adapter.
-/

structure FiniteCellToFinalIndexAdapter
    (cells : FiniteDisjointCellFamily)
    {f : Declared577SparseFold}
    (q : FixedLambdaParameters ℚ)
    (reserve : Nat → ℚ)
    (coeff load : (EtaTag × Nat) → ℚ) where
  cellLambda : ℚ
  rowMap : Nat → (EtaTag × Nat)
  row_map_mem :
    ∀ i ∈ cells.rows, rowMap i ∈ unionRows f
  row_map_injective :
    ∀ {i j : Nat}, i ∈ cells.rows → j ∈ cells.rows →
      rowMap i = rowMap j → i = j
  row_map_surjective :
    ∀ x ∈ unionRows f, ∃ i ∈ cells.rows, rowMap i = x
  lambda_eq : cellLambda = q.lambda
  cell_value_eq :
    ∀ i ∈ cells.rows,
      unionRow f (rowMap i) = cells.cell i
  load_total_eq :
    weightedLoadTotal (f := f) coeff load =
      totalReserve cells reserve
  margin_total_eq :
    weightedMarginTotal (f := f) (lambda := q.lambda) coeff =
      totalMargin cells cellLambda

theorem row_map_is_finite_bijection_on_selected_rows
    {cells : FiniteDisjointCellFamily}
    {f : Declared577SparseFold}
    (q : FixedLambdaParameters ℚ)
    (reserve : Nat → ℚ)
    (coeff load : (EtaTag × Nat) → ℚ)
    (a : FiniteCellToFinalIndexAdapter cells q reserve coeff load) :
    (∀ i ∈ cells.rows, a.rowMap i ∈ unionRows f) ∧
      (∀ x ∈ unionRows f, ∃ i ∈ cells.rows, a.rowMap i = x) := by
  exact ⟨a.row_map_mem, a.row_map_surjective⟩

theorem cell_aggregate_strict_budget_of_final_export
    {cells : FiniteDisjointCellFamily}
    {f : Declared577SparseFold}
    (q : FixedLambdaParameters ℚ)
    (b : UniformMarginLowerBound f q.lambda)
    (p : ExplicitEtaSumPartition f)
    (reserve : Nat → ℚ)
    (coeff load : (EtaTag × Nat) → ℚ)
    (two : TwoRowMarginDenominatorPremise q)
    (a : FiniteCellToFinalIndexAdapter cells q reserve coeff load)
    (final_export : FinalStrictConsumerExport q b p coeff load two) :
    totalReserve cells reserve < totalMargin cells a.cellLambda := by
  have hfinal :
      weightedLoadTotal (f := f) coeff load <
        weightedMarginTotal (f := f) (lambda := q.lambda) coeff :=
    final_export.union_load_lt_margin
  rw [a.load_total_eq, a.margin_total_eq] at hfinal
  exact hfinal

/-!
This projection makes the shared-lambda condition available to a later
consumer without constructing any source or coverage theorem.
-/
theorem transported_margin_uses_final_lambda
    {cells : FiniteDisjointCellFamily}
    {f : Declared577SparseFold}
    (q : FixedLambdaParameters ℚ)
    (reserve : Nat → ℚ)
    (coeff load : (EtaTag × Nat) → ℚ)
    (a : FiniteCellToFinalIndexAdapter cells q reserve coeff load) :
    a.cellLambda = q.lambda := by
  exact a.lambda_eq

/- Admission boundary: this adapter consumes explicit finite index/data and
   total-equality premises; it does not infer source or domain coverage. -/

#print axioms row_map_is_finite_bijection_on_selected_rows
#print axioms cell_aggregate_strict_budget_of_final_export
#print axioms transported_margin_uses_final_lambda

end
end RouteBFixedLambdaIndexEquivalenceAdapter
