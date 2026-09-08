import Mathlib

noncomputable section

namespace RouteBP5AnalyticUnitPullback

/-- Exact rational unit from the worked T-P5-064 example. -/
def workedUnit (z : ℝ) : ℝ := (3 - z) / (2 + z)

/-- A certified positive multiplier cannot hide a zero of the transported contact factor. -/
theorem positive_multiplier_zero_iff
    (u x : ℝ)
    (hu : 0 < u) :
    u * x = 0 ↔ x = 0 := by
  constructor
  · intro h
    exact (mul_eq_zero.mp h).resolve_left (ne_of_gt hu)
  · intro hx
    simp [hx]

/-- A positive unit cannot cancel a genuine jump between two contact values. -/
theorem positive_unit_does_not_cancel_jump
    (u x y : ℝ)
    (hu : 0 < u)
    (hxy : x ≠ y) :
    u * x ≠ u * y := by
  intro h
  have hz : u * (x - y) = 0 := by
    nlinarith
  have hdiff : x - y = 0 :=
    (mul_eq_zero.mp hz).resolve_left (ne_of_gt hu)
  exact hxy (sub_eq_zero.mp hdiff)

/-- A claimed unit lower margin immediately implies that the multiplier is nonzero. -/
theorem lower_margin_implies_nonzero
    (b u : ℝ)
    (hb : 0 < b)
    (hbu : b ≤ |u|) :
    u ≠ 0 := by
  intro hu
  subst u
  norm_num at hbu
  linarith

/-- Exact pullback identity for the rational worked example with one reciprocal unit factor. -/
theorem worked_unit_pullback_identity
    (z : ℝ)
    (hz : z ≠ 0)
    (hu : 2 + z ≠ 0) :
    ((3 - z) * z ^ 2) / ((2 + z) * z) = workedUnit z * z := by
  dsimp [workedUnit]
  field_simp [hz, hu]

/-- On the certified half-box, the worked-example denominator stays strictly positive. -/
theorem worked_unit_den_pos
    (z : ℝ)
    (hlow : -(1 / 2 : ℝ) ≤ z) :
    0 < 2 + z := by
  nlinarith

/-- Exact rational lower envelope `1 ≤ (3-z)/(2+z)` on `[-1/2,1/2]`. -/
theorem worked_unit_lower
    (z : ℝ)
    (hlow : -(1 / 2 : ℝ) ≤ z)
    (hupp : z ≤ (1 / 2 : ℝ)) :
    1 ≤ workedUnit z := by
  have hden : 0 < 2 + z := worked_unit_den_pos z hlow
  dsimp [workedUnit]
  exact (le_div_iff₀ hden).2 (by nlinarith)

/-- Exact rational upper envelope `(3-z)/(2+z) ≤ 7/3` on `[-1/2,1/2]`. -/
theorem worked_unit_upper
    (z : ℝ)
    (hlow : -(1 / 2 : ℝ) ≤ z)
    (_hupp : z ≤ (1 / 2 : ℝ)) :
    workedUnit z ≤ (7 / 3 : ℝ) := by
  have hden : 0 < 2 + z := worked_unit_den_pos z hlow
  dsimp [workedUnit]
  exact (div_le_iff₀ hden).2 (by nlinarith)

/-- Difference identity underlying the exact rational Lipschitz charge for the worked unit. -/
theorem worked_unit_difference_identity
    (z w : ℝ)
    (hz : 2 + z ≠ 0)
    (hw : 2 + w ≠ 0) :
    workedUnit z - workedUnit w =
      5 * (w - z) / ((2 + z) * (2 + w)) := by
  dsimp [workedUnit]
  field_simp [hz, hw]
  ring

/-- The worked unit has the fully rational Lipschitz bound `20/9` on the certified box. -/
theorem worked_unit_lipschitz
    (z w : ℝ)
    (hzlow : -(1 / 2 : ℝ) ≤ z)
    (_hzup : z ≤ (1 / 2 : ℝ))
    (hwlow : -(1 / 2 : ℝ) ≤ w)
    (_hwup : w ≤ (1 / 2 : ℝ)) :
    |workedUnit z - workedUnit w| ≤ (20 / 9 : ℝ) * |z - w| := by
  have hzpos : 0 < 2 + z := worked_unit_den_pos z hzlow
  have hwpos : 0 < 2 + w := worked_unit_den_pos w hwlow
  have hzlower : (3 / 2 : ℝ) ≤ 2 + z := by nlinarith
  have hwlower : (3 / 2 : ℝ) ≤ 2 + w := by nlinarith
  have hprod : (9 / 4 : ℝ) ≤ (2 + z) * (2 + w) := by
    have h := mul_le_mul hzlower hwlower (by norm_num : (0 : ℝ) ≤ 3 / 2) (le_of_lt hzpos)
    nlinarith
  have hprodpos : 0 < (2 + z) * (2 + w) := mul_pos hzpos hwpos
  rw [worked_unit_difference_identity z w (ne_of_gt hzpos) (ne_of_gt hwpos)]
  rw [abs_div, abs_mul, abs_of_pos hprodpos]
  have h5 : |(5 : ℝ)| = 5 := by norm_num
  rw [h5, abs_sub_comm w z]
  apply (div_le_iff₀ hprodpos).2
  have hscale := mul_le_mul_of_nonneg_left hprod (abs_nonneg (z - w))
  nlinarith

/-- Sup envelopes multiply exactly for a unit/contact/reduced triple. -/
theorem triple_product_abs_bound
    (U P R BU BP MR : ℝ)
    (hBU : 0 ≤ BU)
    (hBP : 0 ≤ BP)
    (_hMR : 0 ≤ MR)
    (hU : |U| ≤ BU)
    (hP : |P| ≤ BP)
    (hR : |R| ≤ MR) :
    |U * P * R| ≤ BU * BP * MR := by
  have hUP : |U * P| ≤ BU * BP := by
    rw [abs_mul]
    exact mul_le_mul hU hP (abs_nonneg P) hBU
  calc
    |U * P * R| = |U * P| * |R| := by rw [abs_mul]
    _ ≤ (BU * BP) * MR :=
      mul_le_mul hUP hR (abs_nonneg R) (mul_nonneg hBU hBP)
    _ = BU * BP * MR := by ring

/-- Exact telescoping decomposition for three multiplicative factors. -/
theorem triple_product_difference_identity
    (U U' P P' R R' : ℝ) :
    U * P * R - U' * P' * R' =
      (U - U') * P * R + U' * (P - P') * R + U' * P' * (R - R') := by
  ring

/--
Typed T-P5-064 consumer seam: one unit Lipschitz charge plus the contact and reduced-packet
charges gives the three-term composition bound, with no source-discovery assumptions hidden here.
-/
theorem unit_contact_times_reduced_lipschitz
    (U U' P P' R R' BU BP MR LU LP LR d : ℝ)
    (hBU : 0 ≤ BU)
    (hBP : 0 ≤ BP)
    (hMR : 0 ≤ MR)
    (hLU : 0 ≤ LU)
    (hLP : 0 ≤ LP)
    (hLR : 0 ≤ LR)
    (hd : 0 ≤ d)
    (hU' : |U'| ≤ BU)
    (hP : |P| ≤ BP)
    (hP' : |P'| ≤ BP)
    (hR : |R| ≤ MR)
    (hUd : |U - U'| ≤ LU * d)
    (hPd : |P - P'| ≤ LP * d)
    (hRd : |R - R'| ≤ LR * d) :
    |U * P * R - U' * P' * R'| ≤
      (LU * BP * MR + BU * LP * MR + BU * BP * LR) * d := by
  have hA : |(U - U') * P * R| ≤ (LU * d) * BP * MR :=
    triple_product_abs_bound (U - U') P R (LU * d) BP MR
      (mul_nonneg hLU hd) hBP hMR hUd hP hR
  have hB : |U' * (P - P') * R| ≤ BU * (LP * d) * MR :=
    triple_product_abs_bound U' (P - P') R BU (LP * d) MR
      hBU (mul_nonneg hLP hd) hMR hU' hPd hR
  have hC : |U' * P' * (R - R')| ≤ BU * BP * (LR * d) :=
    triple_product_abs_bound U' P' (R - R') BU BP (LR * d)
      hBU hBP (mul_nonneg hLR hd) hU' hP' hRd
  rw [triple_product_difference_identity]
  calc
    |(U - U') * P * R + U' * (P - P') * R + U' * P' * (R - R')| ≤
        |(U - U') * P * R + U' * (P - P') * R| + |U' * P' * (R - R')| :=
      abs_add_le _ _
    _ ≤ (|(U - U') * P * R| + |U' * (P - P') * R|) + |U' * P' * (R - R')| := by
      exact add_le_add_right (abs_add_le _ _) _
    _ ≤ ((LU * d) * BP * MR + BU * (LP * d) * MR) + BU * BP * (LR * d) := by
      exact add_le_add (add_le_add hA hB) hC
    _ = (LU * BP * MR + BU * LP * MR + BU * BP * LR) * d := by ring

/-- A hidden zero has no uniform positive unit margin even though every punctured point is nonzero. -/
theorem hidden_zero_no_uniform_margin
    (m : ℝ)
    (hm : 0 < m) :
    ∃ z : ℝ, z ≠ 0 ∧ |z| < m := by
  refine ⟨m / 2, ?_, ?_⟩
  · exact ne_of_gt (by nlinarith)
  · rw [abs_of_pos (by nlinarith : 0 < m / 2)]
    nlinarith

/-- Sharp fail-closed regression: the hidden unit `u(z)=z` makes the reciprocal unbounded near contact. -/
theorem hidden_zero_not_unit_counterexample
    (B : ℝ)
    (hB : 0 ≤ B) :
    ∃ z : ℝ, z ≠ 0 ∧ |z| ≤ 1 ∧ B < 1 / |z| := by
  let z : ℝ := 1 / (B + 1)
  have hden : 0 < B + 1 := by nlinarith
  have hzpos : 0 < z := by
    dsimp [z]
    positivity
  have habs : |z| = z := abs_of_pos hzpos
  have hzle : |z| ≤ 1 := by
    rw [habs]
    dsimp [z]
    exact (div_le_iff₀ hden).2 (by nlinarith)
  have hrecip : 1 / |z| = B + 1 := by
    rw [habs]
    dsimp [z]
    field_simp [ne_of_gt hden]
  refine ⟨z, ne_of_gt hzpos, hzle, ?_⟩
  rw [hrecip]
  nlinarith

#print axioms positive_multiplier_zero_iff
#print axioms positive_unit_does_not_cancel_jump
#print axioms lower_margin_implies_nonzero
#print axioms worked_unit_pullback_identity
#print axioms worked_unit_den_pos
#print axioms worked_unit_lower
#print axioms worked_unit_upper
#print axioms worked_unit_difference_identity
#print axioms worked_unit_lipschitz
#print axioms triple_product_abs_bound
#print axioms triple_product_difference_identity
#print axioms unit_contact_times_reduced_lipschitz
#print axioms hidden_zero_no_uniform_margin
#print axioms hidden_zero_not_unit_counterexample

end RouteBP5AnalyticUnitPullback
