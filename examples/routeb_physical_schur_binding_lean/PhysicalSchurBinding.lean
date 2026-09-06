import Mathlib.Data.Real.Basic
import Mathlib.Tactic

set_option autoImplicit false

/-!
Minimal conditional adapter from an explicit physical residual enclosure to a
scalar Schur/Young PMI.  The source-to-residual identification and the
enclosure itself are inputs; this file proves only the exact-real algebra that
consumes them.
-/

namespace RouteBPhysicalSchurBinding

/-- A physical residual action together with its explicit squared enclosure.
The state and the residual action remain abstract so that source semantics are
not manufactured by this algebraic adapter. -/
structure ExplicitResidualEnclosure (State : Type*) where
  residual : State → ℝ → ℝ
  beta : ℝ
  sq_le : ∀ state y, (residual state y) ^ 2 ≤ beta ^ 2 * y ^ 2

/-- Quadratic form of the scalar 2-by-2 Schur/PMI channel. -/
def pmiQuadratic (p d x residual y : ℝ) : ℝ :=
  p * x ^ 2 + 2 * x * residual + d * y ^ 2

/-- Young's inequality specialized to a residual known only through the
explicit squared enclosure `residual² ≤ beta² y²`. -/
theorem residual_young_lower_bound
    (epsilon beta x residual y : ℝ)
    (hepsilon : 0 < epsilon)
    (henclosure : residual ^ 2 ≤ beta ^ 2 * y ^ 2) :
    -(epsilon * x ^ 2 + beta ^ 2 / epsilon * y ^ 2) ≤
      2 * x * residual := by
  have hgap : 0 ≤ beta ^ 2 * y ^ 2 - residual ^ 2 := sub_nonneg.mpr henclosure
  have hsquare : 0 ≤ (epsilon * x + residual) ^ 2 := sq_nonneg _
  have hscaled :
      0 ≤ epsilon *
        (epsilon * x ^ 2 + 2 * x * residual + beta ^ 2 / epsilon * y ^ 2) := by
    calc
      0 ≤ (epsilon * x + residual) ^ 2 +
          (beta ^ 2 * y ^ 2 - residual ^ 2) := add_nonneg hsquare hgap
      _ = epsilon *
          (epsilon * x ^ 2 + 2 * x * residual + beta ^ 2 / epsilon * y ^ 2) := by
            field_simp [ne_of_gt hepsilon]
            ring
  have hcore :
      0 ≤ epsilon * x ^ 2 + 2 * x * residual + beta ^ 2 / epsilon * y ^ 2 :=
    (mul_nonneg_iff_of_pos_left hepsilon).mp hscaled
  linarith

/-- The residual enclosure, a positive Young parameter, and the two diagonal
budgets imply nonnegativity of the associated Schur/PMI quadratic form. -/
theorem pmi_nonnegative_of_residual_enclosure
    (p d epsilon beta x residual y : ℝ)
    (hepsilon : 0 < epsilon)
    (henclosure : residual ^ 2 ≤ beta ^ 2 * y ^ 2)
    (hprefix : epsilon ≤ p)
    (hschur : beta ^ 2 / epsilon ≤ d) :
    0 ≤ pmiQuadratic p d x residual y := by
  have hyoung := residual_young_lower_bound epsilon beta x residual y
    hepsilon henclosure
  have hx : 0 ≤ (p - epsilon) * x ^ 2 :=
    mul_nonneg (sub_nonneg.mpr hprefix) (sq_nonneg x)
  have hy : 0 ≤ (d - beta ^ 2 / epsilon) * y ^ 2 :=
    mul_nonneg (sub_nonneg.mpr hschur) (sq_nonneg y)
  unfold pmiQuadratic
  linarith

/-- Adapter theorem: instantiate the residual by a hash/source-bound physical
residual action, then consume its explicit enclosure in the Schur/Young PMI.
The theorem does not prove that any deployed DH residual satisfies `E.sq_le`. -/
theorem bound_physical_residual_to_pmi
    {State : Type*} (E : ExplicitResidualEnclosure State)
    (state : State) (p d epsilon x y : ℝ)
    (hepsilon : 0 < epsilon)
    (hprefix : epsilon ≤ p)
    (hschur : E.beta ^ 2 / epsilon ≤ d) :
    0 ≤ pmiQuadratic p d x (E.residual state y) y := by
  exact pmi_nonnegative_of_residual_enclosure
    p d epsilon E.beta x (E.residual state y) y
    hepsilon (E.sq_le state y) hprefix hschur

#print axioms residual_young_lower_bound
#print axioms pmi_nonnegative_of_residual_enclosure
#print axioms bound_physical_residual_to_pmi

end RouteBPhysicalSchurBinding
