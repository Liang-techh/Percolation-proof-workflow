import NEW_FIXED_LAMBDA_ADMISSIBILITY_UNIFORM_FEASIBILITY20260907
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBFixedLambdaNoDivisionRatio

open RouteBFixedLambdaAdmissibility
open RouteBFixedLambdaUniformFeasibility

noncomputable section

/-!
This sidecar is the no-division scalar seam for a future source adapter.  It
uses the typed positive denominator only to convert the ratio inequality once;
all subsequent margin and reserve transfers are expressed by multiplication
and subtraction, with no hidden division.
-/

theorem strict_upper_iff_cross_multiplied
    {lambda : ℚ} (c : CellMarginData ℚ) :
    lambda < c.lambdaUpper ↔
      lambda * c.cellGamma < c.externalGamma := by
  rw [c.lambdaUpper_eq_ratio]
  exact lt_div_iff₀ c.cellGamma_pos

theorem positive_margin_iff_cross_multiplied
    {lambda : ℚ} (c : CellMarginData ℚ) :
    0 < marginAt lambda c ↔
      lambda * c.cellGamma < c.externalGamma := by
  unfold marginAt
  exact sub_pos

theorem strict_upper_iff_positive_margin_no_division
    {lambda : ℚ} (c : CellMarginData ℚ) :
    lambda < c.lambdaUpper ↔ 0 < marginAt lambda c := by
  rw [strict_upper_iff_cross_multiplied c,
    positive_margin_iff_cross_multiplied c]

/-!
The reserve form is the source-facing budget contract.  A nonnegative reserve
`delta` is placed directly in the cross-multiplied inequality, so the proof
does not need to divide by `cellGamma` or reconstruct a displayed minimum.
-/
theorem cross_multiplied_reserve_implies_margin_lower_bound
    {lambda delta : ℚ} (c : CellMarginData ℚ)
    (hreserve : lambda * c.cellGamma + delta ≤ c.externalGamma) :
    delta ≤ marginAt lambda c := by
  unfold marginAt
  linarith

theorem strict_cross_multiplied_reserve_implies_strict_margin_lower_bound
    {lambda delta : ℚ} (c : CellMarginData ℚ)
    (hdelta : 0 ≤ delta)
    (hreserve : lambda * c.cellGamma + delta < c.externalGamma) :
    delta < marginAt lambda c := by
  unfold marginAt
  linarith

theorem cross_multiplied_reserve_implies_strict_positive_margin
    {lambda delta : ℚ} (c : CellMarginData ℚ)
    (hdelta : 0 < delta)
    (hreserve : lambda * c.cellGamma + delta ≤ c.externalGamma) :
    0 < marginAt lambda c := by
  exact lt_of_lt_of_le hdelta
    (cross_multiplied_reserve_implies_margin_lower_bound c hreserve)

/-!
This record is intentionally small: it carries only a fixed scalar, a typed
cell, and a cross-multiplied reserve premise.  It is suitable for a later
finite fold without importing a ratio or digest binding into that fold.
-/
structure NoDivisionCellReserve where
  lambda : ℚ
  delta : ℚ
  cell : CellMarginData ℚ
  delta_pos : 0 < delta
  reserve :
    lambda * cell.cellGamma + delta ≤ cell.externalGamma

theorem NoDivisionCellReserve.margin_positive
    (r : NoDivisionCellReserve) :
    0 < marginAt r.lambda r.cell := by
  exact cross_multiplied_reserve_implies_strict_positive_margin
    r.cell r.delta_pos r.reserve

/- Admission boundary: these are scalar no-division implications over supplied
   typed fields, not source, coverage, receipt, or registry evidence. -/

#print axioms strict_upper_iff_cross_multiplied
#print axioms positive_margin_iff_cross_multiplied
#print axioms strict_upper_iff_positive_margin_no_division
#print axioms cross_multiplied_reserve_implies_margin_lower_bound
#print axioms strict_cross_multiplied_reserve_implies_strict_margin_lower_bound
#print axioms cross_multiplied_reserve_implies_strict_positive_margin
#print axioms NoDivisionCellReserve.margin_positive

end
end RouteBFixedLambdaNoDivisionRatio
