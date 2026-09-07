import Mathlib

set_option autoImplicit false

namespace RouteBO0Fin2NormConversionCandidate

noncomputable section

abbrev Vec2 := Fin 2 → ℝ

def normInf (y : Vec2) : ℝ := max |y 0| |y 1|

def norm2 (y : Vec2) : ℝ := Real.sqrt (y 0 ^ 2 + y 1 ^ 2)

theorem normInf_nonneg (y : Vec2) : 0 ≤ normInf y := by
  unfold normInf
  exact le_max_of_le_left (abs_nonneg _)

theorem norm2_le_two_normInf (y : Vec2) :
    norm2 y ≤ 2 * normInf y := by
  unfold norm2 normInf
  have hmax : 0 ≤ max |y 0| |y 1| :=
    le_max_of_le_left (abs_nonneg _)
  have ha0 : 0 ≤ |y 0| := abs_nonneg _
  have ha1 : 0 ≤ |y 1| := abs_nonneg _
  have h0 : y 0 ^ 2 ≤ (max |y 0| |y 1|) ^ 2 := by
    have h0' : |y 0| ≤ max |y 0| |y 1| := le_max_left _ _
    nlinarith [sq_abs (y 0), sq_nonneg (max |y 0| |y 1|)]
  have h1 : y 1 ^ 2 ≤ (max |y 0| |y 1|) ^ 2 := by
    have h1' : |y 1| ≤ max |y 0| |y 1| := le_max_right _ _
    nlinarith [sq_abs (y 1), sq_nonneg (max |y 0| |y 1|)]
  have hsqrt :
      Real.sqrt (y 0 ^ 2 + y 1 ^ 2) ≤
        Real.sqrt (4 * (max |y 0| |y 1|) ^ 2) := by
    apply Real.sqrt_le_sqrt
    nlinarith [h0, h1]
  have hfour : Real.sqrt (4 * (max |y 0| |y 1|) ^ 2) =
      2 * max |y 0| |y 1| := by
    have hsq : (4 : ℝ) * (max |y 0| |y 1|) ^ 2 =
        (2 * max |y 0| |y 1|) ^ 2 := by ring
    rw [hsq, Real.sqrt_sq_eq_abs]
    rw [abs_of_nonneg (by nlinarith [hmax])]
  rw [hfour] at hsqrt
  exact hsqrt

theorem normInf_le_norm2 (y : Vec2) :
    normInf y ≤ norm2 y := by
  unfold normInf norm2
  have h0 : |y 0| ≤ Real.sqrt (y 0 ^ 2 + y 1 ^ 2) := by
    rw [← Real.sqrt_sq_eq_abs (y 0)]
    gcongr
    nlinarith [sq_nonneg (y 1)]
  have h1 : |y 1| ≤ Real.sqrt (y 0 ^ 2 + y 1 ^ 2) := by
    rw [← Real.sqrt_sq_eq_abs (y 1)]
    gcongr
    nlinarith [sq_nonneg (y 0)]
  exact max_le h0 h1

theorem fin2_euclidean_weighted_adapter
    (a r : Vec2) (epsilon s weighted : ℝ)
    (hε : 0 ≤ epsilon) (hs : 0 < s)
    (h_output : normInf r ≤ epsilon * normInf a)
    (h_input : norm2 a ≤ weighted / s) :
    norm2 r ≤ (2 * epsilon / s) * weighted := by
  have ha_inf : normInf a ≤ norm2 a := normInf_le_norm2 a
  have hr2 : norm2 r ≤ 2 * normInf r := norm2_le_two_normInf r
  have hnonneg_a : 0 ≤ normInf a := normInf_nonneg a
  have hright' : 2 * normInf r ≤ 2 * (epsilon * normInf a) :=
    mul_le_mul_of_nonneg_left h_output (show 0 ≤ (2 : ℝ) by norm_num)
  have hright : 2 * normInf r ≤ 2 * epsilon * normInf a := by
    simpa [mul_assoc] using hright'
  have hinput' : epsilon * normInf a ≤ epsilon * norm2 a :=
    mul_le_mul_of_nonneg_left ha_inf hε
  have hscale : epsilon * norm2 a ≤ epsilon * (weighted / s) :=
    mul_le_mul_of_nonneg_left h_input hε
  have hweighted' : 2 * (epsilon * normInf a) ≤
      2 * (epsilon * (weighted / s)) :=
    mul_le_mul_of_nonneg_left (hinput'.trans hscale)
      (show 0 ≤ (2 : ℝ) by norm_num)
  have hweighted : 2 * epsilon * normInf a ≤
      2 * epsilon * (weighted / s) := by
    simpa [mul_assoc] using hweighted'
  calc
    norm2 r ≤ 2 * normInf r := hr2
    _ ≤ 2 * epsilon * normInf a := hright
    _ ≤ 2 * epsilon * (weighted / s) := hweighted
    _ = (2 * epsilon / s) * weighted := by
      ring

end
end RouteBO0Fin2NormConversionCandidate
