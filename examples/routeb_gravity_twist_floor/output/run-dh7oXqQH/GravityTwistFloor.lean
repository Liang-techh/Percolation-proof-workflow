import Mathlib.Analysis.SpecialFunctions.Trigonometric.Bounds
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-! A global, source-coefficient gravity floor with four independent real coordinates.
No joint domain, positivity assumption on R, or unproved trigonometric premise.
The identification with the external Fourier source is a separate obligation.
-/
namespace RouteBGravityTwistFloor
noncomputable section

def Psi (z : ℝ) : ℝ := z ^ 2 / 2 + Real.cos z - 1
def A : ℝ := 762237 / 200000
def B : ℝ := 242307 / 200000
def C : ℝ := 20601 / 400000
def R (u s x y : ℝ) : ℝ :=
  A * Psi u + B * Psi s + C * Psi (s + y) +
    C * Real.sin s * (1 - Real.cos x) * Real.sin y

theorem psi_nonneg (z : ℝ) : 0 ≤ Psi z := by
  have := Real.one_sub_sq_div_two_le_cos (x := z)
  dsimp [Psi]
  linarith

theorem sin_sq_double_bound (z : ℝ) :
    Real.sin z ^ 2 ≤ 4 * Real.sin (z / 2) ^ 2 := by
  have h := Real.sin_two_mul (z / 2)
  have hz : 2 * (z / 2) = z := by ring
  rw [hz] at h
  have hc := Real.cos_sq_le_one (z / 2)
  have hm := mul_nonneg (sq_nonneg (Real.sin (z / 2))) (sub_nonneg.mpr hc)
  have he : Real.sin z ^ 2 =
      4 * Real.sin (z / 2) ^ 2 * Real.cos (z / 2) ^ 2 := by rw [h]; ring
  nlinarith only [he, hm]

/-- Quarter-angle lower bound using only elementary trigonometric identities. -/
theorem psi_ge_quarter_sin (z : ℝ) : 8 * Real.sin (z / 4) ^ 4 ≤ Psi z := by
  have hc := Real.cos_two_mul (z / 2)
  have hs := Real.sin_two_mul (z / 4)
  have hz : 2 * (z / 2) = z := by ring
  have hz' : 2 * (z / 4) = z / 2 := by ring
  rw [hz] at hc
  rw [hz'] at hs
  have hs2 : Real.sin (z / 2) ^ 2 =
      4 * Real.sin (z / 4) ^ 2 * Real.cos (z / 4) ^ 2 := by rw [hs]; ring
  have hu := Real.sin_sq_add_cos_sq (z / 2)
  have hunit := congrArg (fun v : ℝ => Real.sin (z / 4) ^ 2 * v)
    (Real.sin_sq_add_cos_sq (z / 4))
  have hb := Real.sin_sq_le_sq (x := z / 4)
  dsimp [Psi]
  nlinarith only [hc, hs2, hu, hunit, hb]

theorem psi_ge_sin_fourth (z : ℝ) : Real.sin z ^ 4 / 32 ≤ Psi z := by
  have h1 := sin_sq_double_bound z
  have h2 := sin_sq_double_bound (z / 2)
  have hz : z / 2 / 2 = z / 4 := by ring
  rw [hz] at h2
  have h : Real.sin z ^ 2 ≤ 16 * Real.sin (z / 4) ^ 2 := by linarith
  have hm := mul_nonneg (sub_nonneg.mpr h)
    (show 0 ≤ 16 * Real.sin (z / 4) ^ 2 + Real.sin z ^ 2 by positivity)
  have hp := psi_ge_quarter_sin z
  nlinarith only [hm, hp]

theorem twist_product_bound (s y : ℝ) :
    -(2 * Real.sin s ^ 2 + Real.sin (s + y) ^ 2 / 4) ≤
      Real.sin s * Real.sin y := by
  have hid : Real.sin y =
      Real.sin (s + y) * Real.cos s - Real.cos (s + y) * Real.sin s := by
    have h := Real.sin_sub (s + y) s
    simpa using h
  have hcos := Real.cos_sq_le_one s
  have hm := mul_nonneg (sq_nonneg (Real.sin (s + y))) (sub_nonneg.mpr hcos)
  have hcross := sq_nonneg (Real.sin s + Real.sin (s + y) * Real.cos s / 2)
  have hrem := mul_nonneg (sq_nonneg (Real.sin s))
    (sub_nonneg.mpr (Real.cos_le_one (s + y)))
  rw [hid]
  nlinarith

theorem exact_constant : 32 * C ^ 2 / B + C / 2 ≤ (1 : ℝ) / 10 := by
  norm_num [B, C]

theorem exact_constant_value :
    32 * C ^ 2 / B + C / 2 = (18932319 : ℝ) / 197600000 := by
  norm_num [B, C]

theorem exact_constant_margin :
    (1 : ℝ) / 10 - (32 * C ^ 2 / B + C / 2) = 827681 / 197600000 := by
  norm_num [B, C]

theorem gravity_floor_rho (u s x y : ℝ) :
    -(1 - Real.cos x) ^ 2 / 10 ≤ R u s x y := by
  have hu := psi_nonneg u
  have hs := psi_ge_sin_fourth s
  have hsy := psi_ge_sin_fourth (s + y)
  have hr : 0 ≤ 1 - Real.cos x := sub_nonneg.mpr (Real.cos_le_one x)
  have ht := mul_le_mul_of_nonneg_left (twist_product_bound s y) hr
  have hsq1 := sq_nonneg (Real.sin s ^ 2 - (32 * C / B) * (1 - Real.cos x))
  have hsq2 := sq_nonneg (Real.sin (s + y) ^ 2 - 4 * (1 - Real.cos x))
  dsimp [R, A, B, C] at *
  nlinarith [sq_nonneg (1 - Real.cos x)]

/-- The requested all-real floor; all four coordinates are independent. -/
theorem gravity_twist_floor (u s x y : ℝ) : -(x ^ 4) / 40 ≤ R u s x y := by
  have hf := gravity_floor_rho u s x y
  have hr : 0 ≤ 1 - Real.cos x := sub_nonneg.mpr (Real.cos_le_one x)
  have hupper := Real.one_sub_sq_div_two_le_cos (x := x)
  have hm := mul_nonneg
    (show 0 ≤ x ^ 2 / 2 - (1 - Real.cos x) by linarith)
    (show 0 ≤ x ^ 2 / 2 + (1 - Real.cos x) by positivity)
  nlinarith

/-- Consequence for the signed energy gap, with its kinetic term left explicit. -/
theorem signed_gap_upper (kinetic u s x y : ℝ) :
    kinetic - R u s x y ≤ kinetic + x ^ 4 / 40 := by
  linarith [gravity_twist_floor u s x y]

end RouteBGravityTwistFloor

#print axioms RouteBGravityTwistFloor.psi_ge_sin_fourth
#print axioms RouteBGravityTwistFloor.gravity_twist_floor
#print axioms RouteBGravityTwistFloor.signed_gap_upper
