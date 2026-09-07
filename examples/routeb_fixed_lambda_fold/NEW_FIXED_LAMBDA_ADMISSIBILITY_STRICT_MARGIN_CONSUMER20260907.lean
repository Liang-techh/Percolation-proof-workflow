import NEW_FIXED_LAMBDA_ADMISSIBILITY_UNIFORM_MARGIN_BUDGET_REVISED20260907
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBFixedLambdaStrictMarginConsumer

open RouteBFixedLambdaAdmissibility
open RouteBFixedLambdaTwoEtaUnion
open RouteBFixedLambdaUniformFeasibility
open RouteBFixedLambdaUniformMarginBudget
open RouteBFixedLambdaUniformMarginBudgetRevised

noncomputable section

/-!
This sidecar is the strictness consumer for the revised explicit delta bridge.
It accepts only the typed upper-gap/cell-lower/ratio contract and derives
strict row feasibility and strict downstream load separation.
-/

def strictPointwiseLoadWithinDelta
    {f : Declared577SparseFold} {lambda : ℚ}
    (b : ExplicitUpperGapCellLowerContract f lambda)
    (load : (EtaTag × Nat) → ℚ) : Prop :=
  ∀ x ∈ unionRows f,
    0 ≤ load x ∧ load x < b.gap * b.cellLower

theorem gap_contract_gives_strict_upper
    {f : Declared577SparseFold} {lambda : ℚ}
    (b : ExplicitUpperGapCellLowerContract f lambda)
    (x : EtaTag × Nat) (hx : x ∈ unionRows f) :
    lambda < (unionRow f x).lambdaUpper := by
  have hgap : 0 < (unionRow f x).lambdaUpper - lambda :=
    lt_of_lt_of_le b.gap_pos (b.upper_gap x hx)
  exact sub_pos.mp hgap

theorem gap_contract_gives_strict_margin
    {f : Declared577SparseFold} {lambda : ℚ}
    (b : ExplicitUpperGapCellLowerContract f lambda)
    (x : EtaTag × Nat) (hx : x ∈ unionRows f) :
    0 < marginAt lambda (unionRow f x) := by
  exact lt_of_lt_of_le (explicit_delta_positive b)
    (explicit_delta_le_marginAt b x hx)

theorem gap_contract_gives_row_strict_feasibility
    {f : Declared577SparseFold} {lambda : ℚ}
    (b : ExplicitUpperGapCellLowerContract f lambda)
    (hlower : 1 < lambda) :
    ∀ x ∈ unionRows f,
      1 < lambda ∧
        lambda < (unionRow f x).lambdaUpper ∧
        0 < marginAt lambda (unionRow f x) := by
  intro x hx
  exact ⟨hlower, gap_contract_gives_strict_upper b x hx,
    gap_contract_gives_strict_margin b x hx⟩

/-!
The strict load version is intentionally separate from the non-strict budget
consumer: strict slack below delta remains strict slack below every row
margin.
-/
theorem strict_load_is_strictly_below_row_margin
    {f : Declared577SparseFold} {lambda : ℚ}
    (b : ExplicitUpperGapCellLowerContract f lambda)
    (load : (EtaTag × Nat) → ℚ)
    (hload : strictPointwiseLoadWithinDelta b load) :
    ∀ x ∈ unionRows f,
      0 ≤ load x ∧ load x < marginAt lambda (unionRow f x) := by
  intro x hx
  have hxload := hload x hx
  have hdelta_margin := explicit_delta_le_marginAt b x hx
  exact ⟨hxload.1, lt_of_lt_of_le hxload.2 hdelta_margin⟩

/- Admission boundary: strictness is derived over supplied finite typed rows;
   no source, coverage, digest, or registry evidence is introduced. -/

#print axioms gap_contract_gives_strict_upper
#print axioms gap_contract_gives_strict_margin
#print axioms gap_contract_gives_row_strict_feasibility
#print axioms strict_load_is_strictly_below_row_margin

end
end RouteBFixedLambdaStrictMarginConsumer
