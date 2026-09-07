import NEW_FIXED_LAMBDA_ADMISSIBILITY20260907
import Mathlib.Data.Finset.Basic
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBFixedLambdaCoefficientBridge

open RouteBFixedLambdaAdmissibility

noncomputable section

/-!
This sidecar consumes the typed declarations from
`NEW_FIXED_LAMBDA_ADMISSIBILITY20260907.lean`; it does not repeat the
parameter or two-row structures.  Its purpose is the coefficient-level
bridge needed by a later finite fold:

  candidateMargin = externalGamma - lambda * cellGamma
  lambdaUpper = externalGamma / cellGamma

with a positive cell coefficient.  All source, CSV, interval, and coverage
facts remain premises of a future adapter.
-/

theorem coefficient_identity
    {α : Type*} [LinearOrderedField α]
    (p : FixedLambdaParameters α) (c : CellMarginData α) :
    c.externalGamma = p.lambda * c.cellGamma + c.candidateMargin := by
  rw [c.candidateMargin_eq, p.lambda_eq_two]
  ring

theorem strict_upper_iff_positive_margin
    {α : Type*} [LinearOrderedField α]
    (p : FixedLambdaParameters α) (c : CellMarginData α) :
    p.lambda < c.lambdaUpper ↔ 0 < c.candidateMargin := by
  rw [c.lambdaUpper_eq_ratio, c.candidateMargin_eq, p.lambda_eq_two]
  constructor
  · intro hupper
    have hcross : 2 * c.cellGamma < c.externalGamma :=
      (lt_div_iff₀ c.cellGamma_pos).mp hupper
    exact sub_pos.mpr hcross
  · intro hmargin
    apply (lt_div_iff₀ c.cellGamma_pos).mpr
    exact sub_pos.mp hmargin

/-!
The next theorem is the reusable finite-fold form.  It bridges only the
row-level upper-bound and margin conjuncts; it does not assert that `rows`
is complete or that its labels cover a physical domain.
-/
theorem finset_strict_upper_iff_positive_margin
    {α : Type*} [LinearOrderedField α]
    (p : FixedLambdaParameters α)
    (rows : Finset Nat)
    (row : Nat → CellMarginData α) :
    (∀ i ∈ rows, p.lambda < (row i).lambdaUpper) ↔
      (∀ i ∈ rows, 0 < (row i).candidateMargin) := by
  constructor
  · intro hupper i hi
    exact (strict_upper_iff_positive_margin p (row i)).mp (hupper i hi)
  · intro hmargin i hi
    exact (strict_upper_iff_positive_margin p (row i)).mpr (hmargin i hi)

theorem two_row_strict_upper_iff_positive_margin
    {α : Type*} [LinearOrderedField α]
    (w : TwoRowFixedLambdaWitness α) :
    (∀ i, w.params.lambda < (w.rows i).lambdaUpper) ↔
      (∀ i, 0 < (w.rows i).candidateMargin) := by
  constructor
  · intro hupper i
    exact (strict_upper_iff_positive_margin w.params (w.rows i)).mp
      (hupper i)
  · intro hmargin i
    exact (strict_upper_iff_positive_margin w.params (w.rows i)).mpr
      (hmargin i)

/-!
For a fixed `lambda=2`, the bridge supplies the exact margin consumer used by
the admissibility interface.  `theta=1` is already carried by the imported
parameter record; this theorem does not introduce a second parameter slot.
-/
theorem fixed_two_strict_upper_consumes_margin
    {α : Type*} [LinearOrderedField α]
    (p : FixedLambdaParameters α) (c : CellMarginData α)
    (hupper : 2 < c.lambdaUpper) :
    0 < c.candidateMargin := by
  have hfixed : p.lambda < c.lambdaUpper := by
    rw [p.lambda_eq_two]
    exact hupper
  exact (strict_upper_iff_positive_margin p c).mp hfixed

/- Admission boundary: these are algebraic bridges over supplied typed fields;
   they are not source bindings or coverage theorems. -/

#print axioms coefficient_identity
#print axioms strict_upper_iff_positive_margin
#print axioms finset_strict_upper_iff_positive_margin
#print axioms two_row_strict_upper_iff_positive_margin
#print axioms fixed_two_strict_upper_consumes_margin

end
end RouteBFixedLambdaCoefficientBridge
