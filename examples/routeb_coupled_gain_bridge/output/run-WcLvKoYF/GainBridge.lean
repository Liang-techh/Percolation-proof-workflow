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
noncomputable def direct4Squared : ℝ :=
  (5 / 8 : ℝ) * (350003 / 3000000 : ℝ) ^ 2 * (165 / 7 : ℝ)
noncomputable def direct5Squared : ℝ :=
  (10 / 13 : ℝ) * (200739 / 4000000 : ℝ) ^ 2 * 45

theorem direct_channel_scalar_bounds :
    0 ≤ direct5Squared ∧ direct5Squared ≤ direct4Squared ∧
    (447 / 1000 : ℝ) ^ 2 ≤ direct4Squared ∧
    direct4Squared ≤ (56 / 125 : ℝ) ^ 2 := by
  norm_num [direct4Squared, direct5Squared]

theorem supplied_gain_arithmetic :
    (9289 / 500000 : ℝ) ≤ (137 / 1000 : ℝ) ^ 2 ∧
    (137 / 1000 : ℝ) + (422703 / 500000 : ℝ) * (1 / 5 : ℝ) =
      (765203 / 2500000 : ℝ) ∧
    (765203 / 2500000 : ℝ) ^ 2 < (1 / 10 : ℝ) := by
  norm_num

/- The supplied gain constants and J cap are explicit premises. In particular,
   this theorem does not establish the nonlinear J bound. -/
theorem actual_reference_cost_under_J_cap
    {R N H J : ℝ}
    (hbridge : R ≤ (Real.sqrt N + H * Real.sqrt J) ^ 2)
    (hN : N ≤ (9289 / 500000 : ℝ))
    (hH0 : 0 ≤ H) (hH : H ≤ (422703 / 500000 : ℝ))
    (hJ : J ≤ (1 / 25 : ℝ)) : R < (1 / 10 : ℝ) := by
  have hNsq : N ≤ (137 / 1000 : ℝ) ^ 2 := hN.trans (by norm_num)
  have hJsq : J ≤ (1 / 5 : ℝ) ^ 2 := hJ.trans (by norm_num)
  have hR : R ≤ (765203 / 2500000 : ℝ) ^ 2 :=
    rational_envelope_admission (n := (137 / 1000 : ℝ))
      (h := (422703 / 500000 : ℝ)) (j := (1 / 5 : ℝ)) hbridge
      (by norm_num) hH0 (by norm_num) hNsq hH hJsq (by norm_num)
  exact hR.trans_lt (by norm_num)

/- Final refined N,H receipt. The initial gate above is intentionally retained
   as historical, valid conditional arithmetic. -/
theorem final_gain_arithmetic :
    (2877 / 200000 : ℝ) ≤ (3 / 25 : ℝ) ^ 2 ∧
    (1 / 20 : ℝ) ≤ (9 / 40 : ℝ) ^ 2 ∧
    (3 / 25 : ℝ) + (403089 / 500000 : ℝ) * (9 / 40 : ℝ) =
      (6027801 / 20000000 : ℝ) ∧
    (6027801 / 20000000 : ℝ) ^ 2 < (1 / 10 : ℝ) := by
  norm_num

theorem final_reference_cost_under_J_cap
    {R N H J : ℝ}
    (hbridge : R ≤ (Real.sqrt N + H * Real.sqrt J) ^ 2)
    (hN : N ≤ (2877 / 200000 : ℝ))
    (hH0 : 0 ≤ H) (hH : H ≤ (403089 / 500000 : ℝ))
    (hJ : J ≤ (1 / 20 : ℝ)) : R < (1 / 10 : ℝ) := by
  have hNsq : N ≤ (3 / 25 : ℝ) ^ 2 := hN.trans (by norm_num)
  have hJsq : J ≤ (9 / 40 : ℝ) ^ 2 := hJ.trans (by norm_num)
  have hR : R ≤ (6027801 / 20000000 : ℝ) ^ 2 :=
    rational_envelope_admission (n := (3 / 25 : ℝ))
      (h := (403089 / 500000 : ℝ)) (j := (9 / 40 : ℝ)) hbridge
      (by norm_num) hH0 (by norm_num) hNsq hH hJsq (by norm_num)
  exact hR.trans_lt (by norm_num)

/- PRIMARY route: original state outputs, not the optional R<=.1 intermediate.
   KP,KT are L2-to-pointwise kernel gains, with no Ddelta feedthrough. -/
theorem direct_original_output_arithmetic :
    (183423 / 1000000 : ℝ) ≤ (43 / 100 : ℝ) ^ 2 ∧
    (3233741 / 1000000 : ℝ) ≤ (9 / 5 : ℝ) ^ 2 ∧
    (41957 / 100000 : ℝ) ≤ (13 / 20 : ℝ) ^ 2 ∧
    (3907007 / 500000 : ℝ) ≤ (14 / 5 : ℝ) ^ 2 ∧
    (223 / 100 : ℝ) ^ 2 < (28 / 5 : ℝ) ∧
    (69 / 20 : ℝ) ^ 2 < 12 := by
  norm_num

theorem original_domain_under_J_one
    {P NP KP J : ℝ}
    (hbridge : P ≤ (Real.sqrt NP + KP * Real.sqrt J) ^ 2)
    (hNP : NP ≤ (183423 / 1000000 : ℝ))
    (hKP0 : 0 ≤ KP) (hKP2 : KP ^ 2 ≤ (3233741 / 1000000 : ℝ))
    (hJ : J ≤ 1) : P < (28 / 5 : ℝ) := by
  have hN : NP ≤ (43 / 100 : ℝ) ^ 2 := hNP.trans (by norm_num)
  have hK : KP ≤ (9 / 5 : ℝ) := by nlinarith
  have hJsq : J ≤ (1 : ℝ) ^ 2 := by simpa using hJ
  have hP : P ≤ (223 / 100 : ℝ) ^ 2 :=
    rational_envelope_admission (n := (43 / 100 : ℝ))
      (h := (9 / 5 : ℝ)) (j := (1 : ℝ)) hbridge
      (by norm_num) hKP0 (by norm_num) hN hK hJsq (by norm_num)
  exact hP.trans_lt (by norm_num)

theorem original_terminal_under_J_one
    {T NT KT J : ℝ}
    (hbridge : T ≤ (Real.sqrt NT + KT * Real.sqrt J) ^ 2)
    (hNT : NT ≤ (41957 / 100000 : ℝ))
    (hKT0 : 0 ≤ KT) (hKT2 : KT ^ 2 ≤ (3907007 / 500000 : ℝ))
    (hJ : J ≤ 1) : T < 12 := by
  have hN : NT ≤ (13 / 20 : ℝ) ^ 2 := hNT.trans (by norm_num)
  have hK : KT ≤ (14 / 5 : ℝ) := by nlinarith
  have hJsq : J ≤ (1 : ℝ) ^ 2 := by simpa using hJ
  have hT : T ≤ (69 / 20 : ℝ) ^ 2 :=
    rational_envelope_admission (n := (13 / 20 : ℝ))
      (h := (14 / 5 : ℝ)) (j := (1 : ℝ)) hbridge
      (by norm_num) hKT0 (by norm_num) hN hK hJsq (by norm_num)
  exact hT.trans_lt (by norm_num)

#eval ((5 / 8 : ℚ) * (350003 / 3000000 : ℚ) ^ 2 * (165 / 7 : ℚ))
#eval ((10 / 13 : ℚ) * (200739 / 4000000 : ℚ) ^ 2 * 45)
#print axioms rational_envelope_admission
#print axioms residual_point_one_admission
#print axioms feedback_amplitude_bound
#print axioms direct_channel_scalar_bounds
#print axioms supplied_gain_arithmetic
#print axioms actual_reference_cost_under_J_cap
#print axioms final_gain_arithmetic
#print axioms final_reference_cost_under_J_cap
#print axioms direct_original_output_arithmetic
#print axioms original_domain_under_J_one
#print axioms original_terminal_under_J_one

end RouteBCoupledGainBridge
