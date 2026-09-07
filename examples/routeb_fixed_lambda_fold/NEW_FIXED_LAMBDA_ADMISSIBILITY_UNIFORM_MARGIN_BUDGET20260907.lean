import NEW_FIXED_LAMBDA_ADMISSIBILITY_UNIFORM_FEASIBILITY20260907
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBFixedLambdaUniformMarginBudget

open RouteBFixedLambdaAdmissibility
open RouteBFixedLambdaTwoEtaUnion
open RouteBFixedLambdaUniformFeasibility

noncomputable section

/-!
This sidecar supplies a reusable uniform margin lower-bound object over the
finite tagged sparse union.  It deliberately uses an explicit lower-bound
premise rather than pretending that a receipt's displayed minimum has already
been computed or verified in Lean.
-/

structure UniformMarginLowerBound
    (f : Declared577SparseFold) (lambda : ℚ) where
  delta : ℚ
  delta_pos : 0 < delta
  lower_bound :
    ∀ x ∈ unionRows f, delta ≤ marginAt lambda (unionRow f x)

def pointwiseLoadWithinMarginBudget
    {f : Declared577SparseFold} {lambda : ℚ}
    (b : UniformMarginLowerBound f lambda)
    (load : (EtaTag × Nat) → ℚ) : Prop :=
  ∀ x ∈ unionRows f,
    0 ≤ load x ∧ load x ≤ b.delta

theorem uniform_margin_budget_consumes_pointwise_load
    {f : Declared577SparseFold} {lambda : ℚ}
    (b : UniformMarginLowerBound f lambda)
    (load : (EtaTag × Nat) → ℚ)
    (hload : pointwiseLoadWithinMarginBudget b load) :
    ∀ x ∈ unionRows f,
      0 ≤ load x ∧ load x ≤ marginAt lambda (unionRow f x) := by
  intro x hx
  have hxload := hload x hx
  exact ⟨hxload.1, le_trans hxload.2 (b.lower_bound x hx)⟩

/-!
The following contract is the typed source-facing shape for deriving a
uniform delta.  The external-gamma lower bound is retained explicitly as a
coefficient sanity bound; the margin estimate itself uses the positive cell
coefficient and the upper-gap bound.
-/
structure UniformUpperGapAndCoefficientBounds
    (f : Declared577SparseFold) (lambda : ℚ) where
  gap : ℚ
  cellLower : ℚ
  externalLower : ℚ
  gap_pos : 0 < gap
  cellLower_pos : 0 < cellLower
  externalLower_pos : 0 < externalLower
  upper_gap :
    ∀ x ∈ unionRows f,
      gap ≤ (unionRow f x).lambdaUpper - lambda
  cell_lower :
    ∀ x ∈ unionRows f,
      cellLower ≤ (unionRow f x).cellGamma
  external_lower :
    ∀ x ∈ unionRows f,
      externalLower ≤ (unionRow f x).externalGamma

def gapMarginDelta
    {f : Declared577SparseFold} {lambda : ℚ}
    (b : UniformUpperGapAndCoefficientBounds f lambda) : ℚ :=
  b.gap * b.cellLower

theorem gapMarginDelta_positive
    {f : Declared577SparseFold} {lambda : ℚ}
    (b : UniformUpperGapAndCoefficientBounds f lambda) :
    0 < gapMarginDelta b := by
  exact mul_pos b.gap_pos b.cellLower_pos

theorem external_gamma_positive_from_bound
    {f : Declared577SparseFold} {lambda : ℚ}
    (b : UniformUpperGapAndCoefficientBounds f lambda) :
    ∀ x ∈ unionRows f, 0 < (unionRow f x).externalGamma := by
  intro x hx
  exact lt_of_lt_of_le b.externalLower_pos (b.external_lower x hx)

/-!
For each supplied cell, the existing ratio field rewrites the candidate
margin as `(lambdaUpper - lambda) * cellGamma`.  The gap and coefficient
bounds then produce the uniform delta `gap * cellLower`.
-/
theorem margin_lower_bound_from_uniform_gap
    {f : Declared577SparseFold} {lambda : ℚ}
    (b : UniformUpperGapAndCoefficientBounds f lambda) :
    UniformMarginLowerBound f lambda := by
  refine
    { delta := gapMarginDelta b
      delta_pos := gapMarginDelta_positive b
      lower_bound := ?_ }
  intro x hx
  have hcell_ne : (unionRow f x).cellGamma ≠ 0 :=
    ne_of_gt (unionRow f x).cellGamma_pos
  have hfactor :
      marginAt lambda (unionRow f x) =
        ((unionRow f x).lambdaUpper - lambda) *
          (unionRow f x).cellGamma := by
    unfold marginAt
    rw [(unionRow f x).lambdaUpper_eq_ratio]
    field_simp [hcell_ne]
    ring
  have hupper_nonneg :
      0 ≤ (unionRow f x).lambdaUpper - lambda :=
    le_trans (le_of_lt b.gap_pos) (b.upper_gap x hx)
  have hproduct :
      b.gap * b.cellLower ≤
        ((unionRow f x).lambdaUpper - lambda) *
          (unionRow f x).cellGamma :=
    mul_le_mul (b.upper_gap x hx) (b.cell_lower x hx)
      (le_of_lt b.gap_pos) hupper_nonneg
  change b.gap * b.cellLower ≤ marginAt lambda (unionRow f x)
  rw [hfactor]
  exact hproduct

theorem uniform_margin_budget_from_gap_contract
    {f : Declared577SparseFold} {lambda : ℚ}
    (b : UniformUpperGapAndCoefficientBounds f lambda) :
    UniformMarginLowerBound f lambda :=
  margin_lower_bound_from_uniform_gap b

/- Admission boundary: delta and budget are finite typed premises/implications;
   no minimum receipt, source, coverage, or registry fact is inferred. -/

#print axioms uniform_margin_budget_consumes_pointwise_load
#print axioms gapMarginDelta_positive
#print axioms external_gamma_positive_from_bound
#print axioms margin_lower_bound_from_uniform_gap
#print axioms uniform_margin_budget_from_gap_contract

end
end RouteBFixedLambdaUniformMarginBudget
