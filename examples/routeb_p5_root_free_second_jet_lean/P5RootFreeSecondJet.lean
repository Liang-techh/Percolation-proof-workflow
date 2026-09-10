import Mathlib

namespace RouteBP5RootFreeSecondJet

/-- Minimal typed kernel-facing interface for a positive-semidefinite quadratic
energy.  The source-facing metric construction is deliberately outside this
sidecar; the trusted consumer needs only nonnegativity, the PSD cross-square
leaf, and exact add/sub expansion. -/
structure PSDQuadraticKernel (A : Type*) [AddCommGroup A] where
  Q : A → ℝ
  B : A → A → ℝ
  q_nonneg : ∀ x, 0 ≤ Q x
  cross_sq_le : ∀ x y, (B x y) ^ 2 ≤ Q x * Q y
  q_add : ∀ x y, Q (x + y) = Q x + Q y + 2 * B x y
  q_sub : ∀ x y, Q (x - y) = Q x + Q y - 2 * B x y

/-- Independent component-energy caps turn the intrinsic PSD cross-square leaf
into a cap-level product bound. -/
theorem cross_sq_le_cap_product
    {A : Type*} [AddCommGroup A]
    (K : PSDQuadraticKernel A) (x y : A) (U V : ℝ)
    (hx : K.Q x ≤ U) (hy : K.Q y ≤ V)
    (hU : 0 ≤ U) :
    (K.B x y) ^ 2 ≤ U * V := by
  have hxy : K.Q x * K.Q y ≤ U * K.Q y :=
    mul_le_mul_of_nonneg_right hx (K.q_nonneg y)
  have huv : U * K.Q y ≤ U * V :=
    mul_le_mul_of_nonneg_left hy hU
  exact le_trans (K.cross_sq_le x y) (le_trans hxy huv)

/-- Root-free upper cross-term branch.  The nonnegative guard on `C` is part of
the trusted checker; the squared discriminant alone is intentionally not
sufficient. -/
theorem two_cross_upper_of_discriminant
    (b U V C : ℝ)
    (hcross : b ^ 2 ≤ U * V)
    (hC : 0 ≤ C)
    (hdisc : 4 * U * V ≤ C ^ 2) :
    2 * b ≤ C := by
  have hsq : (2 * b) ^ 2 ≤ C ^ 2 := by
    nlinarith [hcross, hdisc]
  by_contra hnot
  have hgt : C < 2 * b := lt_of_not_ge hnot
  have hsum : 0 < 2 * b + C := by linarith
  have hprod : 0 < (2 * b - C) * (2 * b + C) :=
    mul_pos (sub_pos.mpr hgt) hsum
  have hid : (2 * b - C) * (2 * b + C) = (2 * b) ^ 2 - C ^ 2 := by
    ring
  rw [hid] at hprod
  linarith

/-- Symmetric lower cross-term branch, obtained by applying the same guarded
square test to `-b`. -/
theorem two_cross_lower_of_discriminant
    (b U V C : ℝ)
    (hcross : b ^ 2 ≤ U * V)
    (hC : 0 ≤ C)
    (hdisc : 4 * U * V ≤ C ^ 2) :
    -C ≤ 2 * b := by
  have hcrossNeg : (-b) ^ 2 ≤ U * V := by
    simpa using hcross
  have hupper :=
    two_cross_upper_of_discriminant (-b) U V C hcrossNeg hC hdisc
  linarith

/-- Exact two-channel addition envelope from the branch guard and squared
discriminant. -/
theorem quadratic_two_term_discriminant_add
    {A : Type*} [AddCommGroup A]
    (K : PSDQuadraticKernel A) (x y : A) (U V H : ℝ)
    (hx : K.Q x ≤ U) (hy : K.Q y ≤ V)
    (hU : 0 ≤ U)
    (hC : 0 ≤ H - U - V)
    (hdisc : 4 * U * V ≤ (H - U - V) ^ 2) :
    K.Q (x + y) ≤ H := by
  have hcross : (K.B x y) ^ 2 ≤ U * V :=
    cross_sq_le_cap_product K x y U V hx hy hU
  have hupper : 2 * K.B x y ≤ H - U - V :=
    two_cross_upper_of_discriminant
      (K.B x y) U V (H - U - V) hcross hC hdisc
  rw [K.q_add x y]
  linarith

/-- Exact two-channel subtraction envelope from the same root-free gate. -/
theorem quadratic_two_term_discriminant_sub
    {A : Type*} [AddCommGroup A]
    (K : PSDQuadraticKernel A) (x y : A) (U V H : ℝ)
    (hx : K.Q x ≤ U) (hy : K.Q y ≤ V)
    (hU : 0 ≤ U)
    (hC : 0 ≤ H - U - V)
    (hdisc : 4 * U * V ≤ (H - U - V) ^ 2) :
    K.Q (x - y) ≤ H := by
  have hcross : (K.B x y) ^ 2 ≤ U * V :=
    cross_sq_le_cap_product K x y U V hx hy hU
  have hlower : -(H - U - V) ≤ 2 * K.B x y :=
    two_cross_lower_of_discriminant
      (K.B x y) U V (H - U - V) hcross hC hdisc
  rw [K.q_sub x y]
  linarith

/-- The inner guard together with nonnegative component caps already forces the
auxiliary aggregate cap `Kmc` to be nonnegative. -/
theorem inner_guard_forces_aux_nonneg
    (Um Uc Kmc : ℝ)
    (hUm : 0 ≤ Um) (hUc : 0 ≤ Uc)
    (hguard : 0 ≤ Kmc - Um - Uc) :
    0 ≤ Kmc := by
  linarith

/-- Preferred T-P5-115 trusted consumer.  It first certifies `m+c` by one
root-free discriminant gate and then certifies `r-(m+c)` by a second gate.
There is no division, square root, fixed Young parameter, or matrix inverse. -/
theorem second_jet_independent_energy_nested
    {A : Type*} [AddCommGroup A]
    (QK : PSDQuadraticKernel A) (r m c : A)
    (Ur Um Uc Kmc H2 : ℝ)
    (hr : QK.Q r ≤ Ur) (hm : QK.Q m ≤ Um) (hc : QK.Q c ≤ Uc)
    (hUr : 0 ≤ Ur) (hUm : 0 ≤ Um) (hUc : 0 ≤ Uc)
    (hInnerGuard : 0 ≤ Kmc - Um - Uc)
    (hInnerDisc : 4 * Um * Uc ≤ (Kmc - Um - Uc) ^ 2)
    (hOuterGuard : 0 ≤ H2 - Ur - Kmc)
    (hOuterDisc : 4 * Ur * Kmc ≤ (H2 - Ur - Kmc) ^ 2) :
    QK.Q (r - m - c) ≤ H2 := by
  have hKmc : 0 ≤ Kmc :=
    inner_guard_forces_aux_nonneg Um Uc Kmc hUm hUc hInnerGuard
  have hmc : QK.Q (m + c) ≤ Kmc :=
    quadratic_two_term_discriminant_add
      QK m c Um Uc Kmc hm hc hUm hInnerGuard hInnerDisc
  have hout : QK.Q (r - (m + c)) ≤ H2 :=
    quadratic_two_term_discriminant_sub
      QK r (m + c) Ur Kmc H2 hr hmc hUr hOuterGuard hOuterDisc
  have hshape : r - (m + c) = r - m - c := by
    abel
  rw [hshape] at hout
  exact hout

/-- Coefficient-level homogeneous specialization.  All four certificate gates
are checked before multiplying by the common nonnegative scale `Z2`. -/
theorem second_jet_independent_energy_homogeneous
    {A : Type*} [AddCommGroup A]
    (QK : PSDQuadraticKernel A) (r m c : A)
    (ur um uc k h Z2 : ℝ)
    (hr : QK.Q r ≤ ur * Z2)
    (hm : QK.Q m ≤ um * Z2)
    (hc : QK.Q c ≤ uc * Z2)
    (hur : 0 ≤ ur) (hum : 0 ≤ um) (huc : 0 ≤ uc) (hZ2 : 0 ≤ Z2)
    (hInnerGuard : 0 ≤ k - um - uc)
    (hInnerDisc : 4 * um * uc ≤ (k - um - uc) ^ 2)
    (hOuterGuard : 0 ≤ h - ur - k)
    (hOuterDisc : 4 * ur * k ≤ (h - ur - k) ^ 2) :
    QK.Q (r - m - c) ≤ h * Z2 := by
  have hUr : 0 ≤ ur * Z2 := mul_nonneg hur hZ2
  have hUm : 0 ≤ um * Z2 := mul_nonneg hum hZ2
  have hUc : 0 ≤ uc * Z2 := mul_nonneg huc hZ2
  have hInnerGuardScaled :
      0 ≤ k * Z2 - um * Z2 - uc * Z2 := by
    calc
      0 ≤ (k - um - uc) * Z2 := mul_nonneg hInnerGuard hZ2
      _ = k * Z2 - um * Z2 - uc * Z2 := by ring
  have hInnerDiscScaled :
      4 * (um * Z2) * (uc * Z2) ≤
        (k * Z2 - um * Z2 - uc * Z2) ^ 2 := by
    calc
      4 * (um * Z2) * (uc * Z2) =
          (4 * um * uc) * Z2 ^ 2 := by ring
      _ ≤ ((k - um - uc) ^ 2) * Z2 ^ 2 :=
        mul_le_mul_of_nonneg_right hInnerDisc (sq_nonneg Z2)
      _ = (k * Z2 - um * Z2 - uc * Z2) ^ 2 := by ring
  have hOuterGuardScaled :
      0 ≤ h * Z2 - ur * Z2 - k * Z2 := by
    calc
      0 ≤ (h - ur - k) * Z2 := mul_nonneg hOuterGuard hZ2
      _ = h * Z2 - ur * Z2 - k * Z2 := by ring
  have hOuterDiscScaled :
      4 * (ur * Z2) * (k * Z2) ≤
        (h * Z2 - ur * Z2 - k * Z2) ^ 2 := by
    calc
      4 * (ur * Z2) * (k * Z2) =
          (4 * ur * k) * Z2 ^ 2 := by ring
      _ ≤ ((h - ur - k) ^ 2) * Z2 ^ 2 :=
        mul_le_mul_of_nonneg_right hOuterDisc (sq_nonneg Z2)
      _ = (h * Z2 - ur * Z2 - k * Z2) ^ 2 := by ring
  exact second_jet_independent_energy_nested
    QK r m c (ur * Z2) (um * Z2) (uc * Z2) (k * Z2) (h * Z2)
    hr hm hc hUr hUm hUc hInnerGuardScaled hInnerDiscScaled
    hOuterGuardScaled hOuterDiscScaled

/-- Endpoint regression: when one energy cap is zero, the inner gate accepts the
other cap exactly; no artificial positive Young parameter is required. -/
theorem zero_cap_endpoint_gate_exact
    (Uc : ℝ) (_hUc : 0 ≤ Uc) :
    0 ≤ Uc - 0 - Uc ∧
      4 * 0 * Uc ≤ (Uc - 0 - Uc) ^ 2 := by
  constructor <;> nlinarith

/-- Exact imbalanced regression from the mathematical handoff: `Kmc=4` and
`H2=144` satisfy both guarded discriminant gates for caps `(100,1,1)`. -/
theorem imbalanced_100_1_1_certificate :
    0 ≤ (4 : ℝ) - 1 - 1 ∧
      4 * 1 * 1 ≤ ((4 : ℝ) - 1 - 1) ^ 2 ∧
      0 ≤ (144 : ℝ) - 100 - 4 ∧
      4 * 100 * 4 ≤ ((144 : ℝ) - 100 - 4) ^ 2 := by
  norm_num

/-- The new cap in the imbalanced regression is strictly below the collapsed
factor-3 fallback. -/
theorem imbalanced_144_beats_factor_three :
    (144 : ℝ) < 3 * (100 + 1 + 1) := by
  norm_num

/-- Rational non-square regression: no square-root computation is needed in the
trusted checker. -/
theorem nonsquare_1_2_3_certificate :
    0 ≤ (10 : ℝ) - 2 - 3 ∧
      4 * 2 * 3 ≤ ((10 : ℝ) - 2 - 3) ^ 2 ∧
      0 ≤ (87 / 5 : ℝ) - 1 - 10 ∧
      4 * 1 * 10 ≤ ((87 / 5 : ℝ) - 1 - 10) ^ 2 := by
  norm_num

/-- Fail-closed regression: the squared inner test can pass while its required
nonnegative branch guard fails. -/
theorem squared_inner_test_without_guard_is_unsound :
    4 * (1 : ℝ) * 1 ≤ ((0 : ℝ) - 1 - 1) ^ 2 ∧
      ¬ 0 ≤ (0 : ℝ) - 1 - 1 ∧
      (1 + 1 : ℝ) ^ 2 > 0 := by
  norm_num

/-- A diagonal sum is not an aggregate-energy cap without correlation data:
for the scalar quadratic energy and aligned unit inputs, `Q(1+1)=4>2`. -/
theorem diagonal_sum_without_cross_allowance_is_unsound :
    (1 + 1 : ℝ) ^ 2 > 1 ^ 2 + 1 ^ 2 := by
  norm_num

#print axioms cross_sq_le_cap_product
#print axioms two_cross_upper_of_discriminant
#print axioms two_cross_lower_of_discriminant
#print axioms quadratic_two_term_discriminant_add
#print axioms quadratic_two_term_discriminant_sub
#print axioms inner_guard_forces_aux_nonneg
#print axioms second_jet_independent_energy_nested
#print axioms second_jet_independent_energy_homogeneous
#print axioms zero_cap_endpoint_gate_exact
#print axioms imbalanced_100_1_1_certificate
#print axioms imbalanced_144_beats_factor_three
#print axioms nonsquare_1_2_3_certificate
#print axioms squared_inner_test_without_guard_is_unsound
#print axioms diagonal_sum_without_cross_allowance_is_unsound

end RouteBP5RootFreeSecondJet
