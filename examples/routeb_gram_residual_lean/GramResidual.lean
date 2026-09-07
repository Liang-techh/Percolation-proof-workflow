import Mathlib.Data.Real.Basic
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBGramResidual

/-!
Reusable kernel seam for the finite coefficient residual used by the Route-B
tail Gram candidate.  The concrete CSV expansion remains an external exact
receipt; this file proves the generic real-analysis step that converts
pointwise bounded monomials into an `l1` residual bound and then absorbs that
bound into a positive algebraic decomposition.
-/

theorem weighted_residual_l1_bound
    {ι : Type*} [Fintype ι]
    (coeff atom : ι → ℝ)
    (h_atom : ∀ i, |atom i| ≤ 1) :
    |∑ i, coeff i * atom i| ≤ ∑ i, |coeff i| := by
  calc
    |∑ i, coeff i * atom i| ≤ ∑ i, |coeff i * atom i| := by
      simpa using
        (Finset.abs_sum_le_sum_abs
          (fun i => coeff i * atom i) Finset.univ)
    _ = ∑ i, |coeff i| * |atom i| := by
      apply Finset.sum_congr rfl
      intro i hi
      simp [abs_mul]
    _ ≤ ∑ i, |coeff i| := by
      apply Finset.sum_le_sum
      intro i hi
      simpa using
        (mul_le_mul_of_nonneg_left (h_atom i) (abs_nonneg (coeff i)))

theorem decomposition_nonnegative_of_abs_residual
    (value positive residual lower l1 : ℝ)
    (hdecomp : value = lower + positive + residual)
    (hpositive : 0 ≤ positive)
    (hresidual : |residual| ≤ l1)
    (hmargin : l1 ≤ lower) :
    0 ≤ value := by
  have hlow : -l1 ≤ residual := (abs_le.mp hresidual).1
  linarith

#print axioms weighted_residual_l1_bound
#print axioms decomposition_nonnegative_of_abs_residual

end RouteBGramResidual
