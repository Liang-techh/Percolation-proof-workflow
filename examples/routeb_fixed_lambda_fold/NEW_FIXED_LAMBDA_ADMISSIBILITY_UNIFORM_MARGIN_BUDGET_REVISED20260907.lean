import NEW_FIXED_LAMBDA_ADMISSIBILITY_UNIFORM_MARGIN_BUDGET20260907
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBFixedLambdaUniformMarginBudgetRevised

open RouteBFixedLambdaAdmissibility
open RouteBFixedLambdaTwoEtaUnion
open RouteBFixedLambdaUniformFeasibility
open RouteBFixedLambdaUniformMarginBudget

noncomputable section

/-!
Revision seam: downstream consumers receive only explicit upper-gap,
cell-lower, positivity, and ratio premises.  The ratio is repeated as an
adapter premise so that this bridge does not silently consume a field from a
different metric or ledger.
-/

structure ExplicitUpperGapCellLowerContract
    (f : Declared577SparseFold) (lambda : ℚ) where
  gap : ℚ
  cellLower : ℚ
  gap_pos : 0 < gap
  cellLower_pos : 0 < cellLower
  upper_gap :
    ∀ x ∈ unionRows f,
      gap ≤ (unionRow f x).lambdaUpper - lambda
  cell_lower :
    ∀ x ∈ unionRows f,
      cellLower ≤ (unionRow f x).cellGamma
  ratio :
    ∀ x ∈ unionRows f,
      (unionRow f x).lambdaUpper =
        (unionRow f x).externalGamma /
          (unionRow f x).cellGamma

theorem marginAt_eq_upper_gap_mul_cell
    {lambda : ℚ} (c : CellMarginData ℚ)
    (hratio : c.lambdaUpper = c.externalGamma / c.cellGamma) :
    marginAt lambda c = (c.lambdaUpper - lambda) * c.cellGamma := by
  have hcell_ne : c.cellGamma ≠ 0 := ne_of_gt c.cellGamma_pos
  unfold marginAt
  rw [hratio]
  field_simp [hcell_ne]
  ring

theorem explicit_delta_positive
    {f : Declared577SparseFold} {lambda : ℚ}
    (b : ExplicitUpperGapCellLowerContract f lambda) :
    0 < b.gap * b.cellLower := by
  exact mul_pos b.gap_pos b.cellLower_pos

/-!
This is the row-level lower-bound bridge.  Every ingredient appears in the
statement or in the cell's typed positive-denominator field; no receipt
minimum or hidden source fact is consulted.
-/
theorem explicit_delta_le_marginAt
    {f : Declared577SparseFold} {lambda : ℚ}
    (b : ExplicitUpperGapCellLowerContract f lambda)
    (x : EtaTag × Nat) (hx : x ∈ unionRows f) :
    b.gap * b.cellLower ≤ marginAt lambda (unionRow f x) := by
  have hcell_pos : 0 < (unionRow f x).cellGamma :=
    (unionRow f x).cellGamma_pos
  have hupper_nonneg :
      0 ≤ (unionRow f x).lambdaUpper - lambda :=
    le_trans (le_of_lt b.gap_pos) (b.upper_gap x hx)
  have hproduct :
      b.gap * b.cellLower ≤
        ((unionRow f x).lambdaUpper - lambda) *
          (unionRow f x).cellGamma :=
    mul_le_mul (b.upper_gap x hx) (b.cell_lower x hx)
      (le_of_lt b.gap_pos) hupper_nonneg
  have hfactor :
      marginAt lambda (unionRow f x) =
        ((unionRow f x).lambdaUpper - lambda) *
          (unionRow f x).cellGamma :=
    marginAt_eq_upper_gap_mul_cell (lambda := lambda) (unionRow f x) (b.ratio x hx)
  rw [hfactor]
  exact hproduct

theorem revised_uniform_margin_lower_bound
    {f : Declared577SparseFold} {lambda : ℚ}
    (b : ExplicitUpperGapCellLowerContract f lambda) :
    UniformMarginLowerBound f lambda := by
  refine
    { delta := b.gap * b.cellLower
      delta_pos := explicit_delta_positive b
      lower_bound := ?_ }
  intro x hx
  exact explicit_delta_le_marginAt b x hx

theorem revised_budget_consumes_load
    {f : Declared577SparseFold} {lambda : ℚ}
    (b : ExplicitUpperGapCellLowerContract f lambda)
    (load : (EtaTag × Nat) → ℚ)
    (hload : ∀ x ∈ unionRows f,
      0 ≤ load x ∧ load x ≤ b.gap * b.cellLower) :
    ∀ x ∈ unionRows f,
      0 ≤ load x ∧ load x ≤ marginAt lambda (unionRow f x) := by
  have hbound := revised_uniform_margin_lower_bound b
  exact uniform_margin_budget_consumes_pointwise_load
    hbound load (by exact hload)

/- Admission boundary: this revised bridge is algebra over explicit typed
   premises only.  It is not receipt/source/coverage/registry evidence. -/

#print axioms marginAt_eq_upper_gap_mul_cell
#print axioms explicit_delta_positive
#print axioms explicit_delta_le_marginAt
#print axioms revised_uniform_margin_lower_bound
#print axioms revised_budget_consumes_load

end
end RouteBFixedLambdaUniformMarginBudgetRevised
