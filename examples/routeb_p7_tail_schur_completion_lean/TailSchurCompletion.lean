import Mathlib.Data.Real.Basic
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBP7TailSchurCompletion

/-!
Source-independent exact-real children for the P7 tail.  The first theorem
exposes the 2x2 Schur completion identity; the second gives the robust
quadratic upper bound needed to consume interval bounds on the cross vector.
No theorem here identifies these symbols with the deployed DH polynomial.
-/

theorem schur_completion_identity
    (a b d u1 u2 x y s : ℝ)
    (ha : a ≠ 0)
    (hdet : a * d - b ^ 2 ≠ 0) :
    a * x ^ 2 + 2 * b * x * y + d * y ^ 2 +
        2 * s * (u1 * x + u2 * y) =
      (a * x + b * y + s * u1) ^ 2 / a +
        (a * d - b ^ 2) / a *
          (y + s * (a * u2 - b * u1) / (a * d - b ^ 2)) ^ 2 -
        s ^ 2 * (d * u1 ^ 2 - 2 * b * u1 * u2 + a * u2 ^ 2) /
          (a * d - b ^ 2) := by
  field_simp [ha, hdet]
  ring

theorem robust_inverse_quadratic_bound_2x2
    (a b d u1 u2 U1 U2 B : ℝ)
    (ha : 0 ≤ a)
    (hd : 0 ≤ d)
    (hB : |b| ≤ B)
    (hU1 : 0 ≤ U1)
    (hU2 : 0 ≤ U2)
    (hu1 : |u1| ≤ U1)
    (hu2 : |u2| ≤ U2) :
    a * u1 ^ 2 + 2 * b * u1 * u2 + d * u2 ^ 2 ≤
      a * U1 ^ 2 + 2 * B * U1 * U2 + d * U2 ^ 2 := by
  have hu1_lo : -U1 ≤ u1 := (abs_le.mp hu1).1
  have hu1_hi : u1 ≤ U1 := (abs_le.mp hu1).2
  have hu2_lo : -U2 ≤ u2 := (abs_le.mp hu2).1
  have hu2_hi : u2 ≤ U2 := (abs_le.mp hu2).2
  have hu1_sq : u1 ^ 2 ≤ U1 ^ 2 := by
    nlinarith [sq_nonneg (U1 - u1), sq_nonneg (U1 + u1)]
  have hu2_sq : u2 ^ 2 ≤ U2 ^ 2 := by
    nlinarith [sq_nonneg (U2 - u2), sq_nonneg (U2 + u2)]
  have hcross_abs : |b * u1 * u2| ≤ B * U1 * U2 := by
    calc
      |b * u1 * u2| = |b| * |u1| * |u2| := by simp [abs_mul]
      _ ≤ B * U1 * U2 := by
        gcongr
  have hcross : b * u1 * u2 ≤ B * U1 * U2 := by
    exact (le_abs_self (b * u1 * u2)).trans hcross_abs
  have ha_sq := mul_le_mul_of_nonneg_left hu1_sq ha
  have hd_sq := mul_le_mul_of_nonneg_left hu2_sq hd
  nlinarith [ha_sq, hd_sq, mul_le_mul_of_nonneg_left hcross (by norm_num : (0 : ℝ) ≤ 2)]

theorem schur_tail_absorption
    (a b d u1 u2 x y s tau eta : ℝ)
    (ha : 0 < a)
    (hdet : 0 < a * d - b ^ 2)
    (hbound : (d * u1 ^ 2 - 2 * b * u1 * u2 + a * u2 ^ 2) /
        (a * d - b ^ 2) ≤ eta)
    (heta : eta ≤ tau) :
    0 ≤ a * x ^ 2 + 2 * b * x * y + d * y ^ 2 +
      2 * s * (u1 * x + u2 * y) + tau * s ^ 2 := by
  have hidentity := schur_completion_identity a b d u1 u2 x y s
    (ne_of_gt ha) (ne_of_gt hdet)
  have hfirst : 0 ≤ (a * x + b * y + s * u1) ^ 2 / a := by
    positivity
  have hsecond : 0 ≤ (a * d - b ^ 2) / a *
      (y + s * (a * u2 - b * u1) / (a * d - b ^ 2)) ^ 2 := by
    positivity
  have hlast : 0 ≤ (tau -
      (d * u1 ^ 2 - 2 * b * u1 * u2 + a * u2 ^ 2) /
        (a * d - b ^ 2)) * s ^ 2 := by
    have hcoef : 0 ≤ tau -
        (d * u1 ^ 2 - 2 * b * u1 * u2 + a * u2 ^ 2) /
          (a * d - b ^ 2) := by linarith
    positivity
  rw [hidentity]
  nlinarith

theorem schur_tail_absorption_at_p7
    (a b d u1 u2 x y s eta : ℝ)
    (ha : 0 < a)
    (hdet : 0 < a * d - b ^ 2)
    (hbound : (d * u1 ^ 2 - 2 * b * u1 * u2 + a * u2 ^ 2) /
        (a * d - b ^ 2) ≤ eta)
    (heta : eta ≤ (1 / 160000 : ℝ)) :
    0 ≤ a * x ^ 2 + 2 * b * x * y + d * y ^ 2 +
      2 * s * (u1 * x + u2 * y) + (1 / 160000 : ℝ) * s ^ 2 := by
  exact schur_tail_absorption a b d u1 u2 x y s
    (1 / 160000 : ℝ) eta ha hdet hbound heta

#print axioms schur_completion_identity
#print axioms robust_inverse_quadratic_bound_2x2
#print axioms schur_tail_absorption
#print axioms schur_tail_absorption_at_p7

end RouteBP7TailSchurCompletion
