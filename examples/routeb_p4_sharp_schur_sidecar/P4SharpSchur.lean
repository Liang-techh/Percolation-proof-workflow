import Mathlib.Data.Real.Basic
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBP4SharpSchur

noncomputable section

/-!
# Sharp one-channel P4 Schur residual sidecar

This file formalizes the exact-real mathematics from
`review-T-P4-005-liuguanyi-20260906T2206.md`.

It deliberately contains no Julia/DH source binding, Float64 semantics,
receipt, domain-coverage, registry, or M4/P4 admission claim.
-/

theorem schur_residual_nonnegative_iff
    (p d r y : ℝ) (hp : 0 < p) :
    (∀ x : ℝ, 0 ≤ p * x ^ 2 + 2 * x * r + d * y ^ 2) ↔
      r ^ 2 ≤ p * d * y ^ 2 := by
  constructor
  · intro h
    have hp0 : p ≠ 0 := ne_of_gt hp
    have hmin := h (-r / p)
    have hscaled :
        0 ≤ p * (p * (-r / p) ^ 2 + 2 * (-r / p) * r + d * y ^ 2) :=
      mul_nonneg hp.le hmin
    have hid :
        p * (p * (-r / p) ^ 2 + 2 * (-r / p) * r + d * y ^ 2) =
          p * d * y ^ 2 - r ^ 2 := by
      field_simp [hp0]
      ring
    rw [hid] at hscaled
    linarith
  · intro hbudget x
    have hgap : 0 ≤ p * d * y ^ 2 - r ^ 2 := sub_nonneg.mpr hbudget
    have hsq : 0 ≤ (p * x + r) ^ 2 := sq_nonneg _
    have hmul :
        0 ≤ p * (p * x ^ 2 + 2 * x * r + d * y ^ 2) := by
      calc
        0 ≤ (p * x + r) ^ 2 + (p * d * y ^ 2 - r ^ 2) :=
          add_nonneg hsq hgap
        _ = p * (p * x ^ 2 + 2 * x * r + d * y ^ 2) := by
          ring
    exact (mul_nonneg_iff_of_pos_left hp).mp hmul

/- If the universal quadratic is required at `y = 0`, the residual must
   vanish. This is the formal zero-slice obstruction from the mathematical
   review. -/
theorem zero_y_forces_zero_residual
    (p d r : ℝ) (hp : 0 < p)
    (h : ∀ x : ℝ, 0 ≤ p * x ^ 2 + 2 * x * r) :
    r = 0 := by
  have hbudget : r ^ 2 ≤ p * d * (0 : ℝ) ^ 2 :=
    (schur_residual_nonnegative_iff p d r 0 hp).1 (by
      intro x
      simpa using h x)
  have hsq : r ^ 2 ≤ 0 := by
    simpa using hbudget
  nlinarith [sq_nonneg r]

/- Concrete block-4 coefficients from the existing exact-real P4 child. -/
def p4 : ℝ := 3 / 5

def d4 : ℝ := 116667666666667 / 1000000000000000

theorem p4_pos : 0 < p4 := by
  norm_num [p4]

/- `c = 1/4` fits strictly inside the sharp squared Schur budget. -/
theorem quarter_sq_lt_p4d4 :
    (1 / 4 : ℝ) ^ 2 < p4 * d4 := by
  norm_num [p4, d4]

theorem quarter_sq_le_p4d4 :
    (1 / 4 : ℝ) ^ 2 ≤ p4 * d4 := by
  exact (quarter_sq_lt_p4d4).le

/- A source-side squared envelope with coefficient `1/4` is enough to feed the
   same scalar P4 quadratic. No square root is introduced. -/
theorem quarter_residual_absorption
    (x y residual : ℝ)
    (hresidual : residual ^ 2 ≤ (1 / 4 : ℝ) ^ 2 * y ^ 2) :
    0 ≤ p4 * x ^ 2 + 2 * x * residual + d4 * y ^ 2 := by
  apply (schur_residual_nonnegative_iff p4 d4 residual y p4_pos).2
  calc
    residual ^ 2 ≤ (1 / 4 : ℝ) ^ 2 * y ^ 2 := hresidual
    _ ≤ (p4 * d4) * y ^ 2 := by
      exact mul_le_mul_of_nonneg_right quarter_sq_le_p4d4 (sq_nonneg y)

#print axioms schur_residual_nonnegative_iff
#print axioms zero_y_forces_zero_residual
#print axioms quarter_sq_lt_p4d4
#print axioms quarter_residual_absorption

end
end RouteBP4SharpSchur
