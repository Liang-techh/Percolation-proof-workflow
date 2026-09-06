import Mathlib.Tactic
import Mathlib.Analysis.Real.Sqrt

set_option autoImplicit false

namespace RouteBCoupledGainBridge

/- Scalar admission only. The finite-horizon convolution estimate remains
   an explicit premise; this file does not formalize Young or the matrix flow. -/
theorem rational_envelope_admission
    {R N H J n h j budget : ℝ}
    (hbridge : R ≤ (Real.sqrt N + H * Real.sqrt J) ^ 2)
    (hn : 0 ≤ n) (hH : 0 ≤ H) (hj : 0 ≤ j)
    (hN : N ≤ n ^ 2) (hHupper : H ≤ h) (hJ : J ≤ j ^ 2)
    (hgate : (n + h * j) ^ 2 ≤ budget) : R ≤ budget := by
  have hh : 0 ≤ h := hH.trans hHupper
  have hsN : Real.sqrt N ≤ n := Real.sqrt_le_iff.mpr ⟨hn, hN⟩
  have hsJ : Real.sqrt J ≤ j := Real.sqrt_le_iff.mpr ⟨hj, hJ⟩
  have hprod : H * Real.sqrt J ≤ h * j :=
    (mul_le_mul_of_nonneg_right hHupper (Real.sqrt_nonneg J)).trans
      (mul_le_mul_of_nonneg_left hsJ hh)
  have hsum : Real.sqrt N + H * Real.sqrt J ≤ n + h * j := add_le_add hsN hprod
  have hl : 0 ≤ Real.sqrt N + H * Real.sqrt J := by positivity
  have hr : 0 ≤ n + h * j := by positivity
  have hsquare : (Real.sqrt N + H * Real.sqrt J) ^ 2 ≤ (n + h * j) ^ 2 := by
    have hp := mul_nonneg (sub_nonneg.mpr hsum) (add_nonneg hr hl)
    nlinarith
  exact hbridge.trans (hsquare.trans hgate)

theorem residual_point_one_admission
    {R N H J n h j : ℝ}
    (hbridge : R ≤ (Real.sqrt N + H * Real.sqrt J) ^ 2)
    (hn : 0 ≤ n) (hH : 0 ≤ H) (hj : 0 ≤ j)
    (hN : N ≤ n ^ 2) (hHupper : H ≤ h) (hJ : J ≤ j ^ 2)
    (hgate : (n + h * j) ^ 2 ≤ (1 / 10 : ℝ)) : R ≤ (1 / 10 : ℝ) := by
  exact rational_envelope_admission hbridge hn hH hj hN hHupper hJ hgate

/- This is a genuine closure condition, not permission to assume a residual
   budget that itself depends on the desired conclusion. -/
theorem feedback_amplitude_bound
    {rho n h a b : ℝ}
    (hfeedback : rho ≤ n + h * (a + b * rho))
    (hloop : h * b < 1) : rho ≤ (n + h * a) / (1 - h * b) := by
  apply (le_div_iff₀ (by linarith : 0 < 1 - h * b)).mpr
  nlinarith

/- Parameter-specific direct channel squared singular values. -/
def direct4Squared : ℝ :=
  (5 / 8 : ℝ) * (350003 / 3000000 : ℝ) ^ 2 * (165 / 7 : ℝ)
def direct5Squared : ℝ :=
  (10 / 13 : ℝ) * (200739 / 4000000 : ℝ) ^ 2 * 45

theorem direct_channel_scalar_bounds :
    0 ≤ direct5Squared ∧ direct5Squared ≤ direct4Squared ∧
    (447 / 1000 : ℝ) ^ 2 ≤ direct4Squared ∧
    direct4Squared ≤ (56 / 125 : ℝ) ^ 2 := by
  norm_num [direct4Squared, direct5Squared]

#eval ((5 / 8 : ℚ) * (350003 / 3000000 : ℚ) ^ 2 * (165 / 7 : ℚ))
#eval ((10 / 13 : ℚ) * (200739 / 4000000 : ℚ) ^ 2 * 45)
#print axioms rational_envelope_admission
#print axioms residual_point_one_admission
#print axioms feedback_amplitude_bound
#print axioms direct_channel_scalar_bounds

end RouteBCoupledGainBridge
