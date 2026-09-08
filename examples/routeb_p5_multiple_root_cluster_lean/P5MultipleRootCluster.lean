import Mathlib

noncomputable section

namespace RouteBP5MultipleRootCluster

/-- A signed perturbation has the same absolute-value enclosure when `|sigma| = 1`. -/
theorem signed_error_bounds
    (sigma e eps : ℝ)
    (hsigma : |sigma| = 1)
    (he : |e| ≤ eps) :
    -eps ≤ sigma * e ∧ sigma * e ≤ eps := by
  have h : |sigma * e| ≤ eps := by
    rw [abs_mul, hsigma, one_mul]
    exact he
  exact abs_le.mp h

/--
Pointwise, division-free root estimate for a multiple-contact packet
`u*z^k + e = 0`.  Root discovery and continuity are intentionally outside
this arithmetic leaf.
-/
theorem multiple_contact_root_mul_pow_le
    (m eps u e z : ℝ) (k : ℕ)
    (hu : m ≤ |u|)
    (he : |e| ≤ eps)
    (hzero : u * z ^ k + e = 0) :
    m * |z| ^ k ≤ eps := by
  have hzero' : u * z ^ k = -e := by
    linarith
  calc
    m * |z| ^ k ≤ |u| * |z| ^ k :=
      mul_le_mul_of_nonneg_right hu (pow_nonneg (abs_nonneg z) k)
    _ = |u * z ^ k| := by rw [abs_mul, abs_pow]
    _ = |e| := by rw [hzero', abs_neg]
    _ ≤ eps := he

/-- Strict reserve `eps < m*delta^k` excludes every root from `|z| ≥ delta`. -/
theorem multiple_contact_root_inside_of_strict
    (m eps delta z : ℝ) (k : ℕ)
    (hm : 0 < m)
    (hdelta : 0 ≤ delta)
    (hroot : m * |z| ^ k ≤ eps)
    (hstrict : eps < m * delta ^ k) :
    |z| < delta := by
  by_contra hnot
  have hdz : delta ≤ |z| := le_of_not_gt hnot
  have hpow : delta ^ k ≤ |z| ^ k := pow_le_pow_left₀ hdelta hdz k
  have hmul : m * delta ^ k ≤ m * |z| ^ k :=
    mul_le_mul_of_nonneg_left hpow (le_of_lt hm)
  exact (not_lt_of_ge (le_trans hmul hroot)) hstrict

/-- Combined root-cluster consumer: no radicals are formed. -/
theorem multiple_contact_root_cluster
    (m eps delta u e z : ℝ) (k : ℕ)
    (hm : 0 < m)
    (hdelta : 0 ≤ delta)
    (hu : m ≤ |u|)
    (he : |e| ≤ eps)
    (hzero : u * z ^ k + e = 0)
    (hstrict : eps < m * delta ^ k) :
    |z| < delta := by
  apply multiple_contact_root_inside_of_strict m eps delta z k hm hdelta
  · exact multiple_contact_root_mul_pow_le m eps u e z k hu he hzero
  · exact hstrict

/-- Right outer wing: the signed value keeps a positive reserve. -/
theorem multiple_contact_right_outer_reserve
    (sigma m eps delta u e h z : ℝ) (k : ℕ)
    (hm : 0 ≤ m)
    (hdelta : 0 ≤ delta)
    (hz : delta ≤ z)
    (hu : m ≤ sigma * u)
    (hsigma : |sigma| = 1)
    (he : |e| ≤ eps)
    (hdef : h = u * z ^ k + e) :
    m * delta ^ k - eps ≤ sigma * h := by
  have hz0 : 0 ≤ z := le_trans hdelta hz
  have hpow : delta ^ k ≤ z ^ k := pow_le_pow_left₀ hdelta hz k
  have hmain1 : m * delta ^ k ≤ m * z ^ k :=
    mul_le_mul_of_nonneg_left hpow hm
  have hmain2 : m * z ^ k ≤ (sigma * u) * z ^ k :=
    mul_le_mul_of_nonneg_right hu (pow_nonneg hz0 k)
  have herr : -eps ≤ sigma * e :=
    (signed_error_bounds sigma e eps hsigma he).1
  calc
    m * delta ^ k - eps ≤ (sigma * u) * z ^ k + sigma * e := by
      linarith
    _ = sigma * h := by rw [hdef]; ring

/-- Left outer wing for even multiplicity: the sign is the same as on the right. -/
theorem multiple_contact_left_outer_reserve_even
    (sigma m eps delta u e h z : ℝ) (k : ℕ)
    (hk : Even k)
    (hm : 0 ≤ m)
    (hdelta : 0 ≤ delta)
    (hz : z ≤ -delta)
    (hu : m ≤ sigma * u)
    (hsigma : |sigma| = 1)
    (he : |e| ≤ eps)
    (hdef : h = u * z ^ k + e) :
    m * delta ^ k - eps ≤ sigma * h := by
  have hz0 : z ≤ 0 := by linarith
  have hdz : delta ≤ |z| := by
    rw [abs_of_nonpos hz0]
    linarith
  have hpowAbs : delta ^ k ≤ |z| ^ k := pow_le_pow_left₀ hdelta hdz k
  have hpow : delta ^ k ≤ z ^ k := by
    rw [← hk.pow_abs z]
    exact hpowAbs
  have hmain1 : m * delta ^ k ≤ m * z ^ k :=
    mul_le_mul_of_nonneg_left hpow hm
  have hmain2 : m * z ^ k ≤ (sigma * u) * z ^ k :=
    mul_le_mul_of_nonneg_right hu (hk.pow_nonneg z)
  have herr : -eps ≤ sigma * e :=
    (signed_error_bounds sigma e eps hsigma he).1
  calc
    m * delta ^ k - eps ≤ (sigma * u) * z ^ k + sigma * e := by
      linarith
    _ = sigma * h := by rw [hdef]; ring

/-- Left outer wing for odd multiplicity: the signed reserve flips sign. -/
theorem multiple_contact_left_outer_reserve_odd
    (sigma m eps delta u e h z : ℝ) (k : ℕ)
    (hk : Odd k)
    (hm : 0 ≤ m)
    (hdelta : 0 ≤ delta)
    (hz : z ≤ -delta)
    (hu : m ≤ sigma * u)
    (hsigma : |sigma| = 1)
    (he : |e| ≤ eps)
    (hdef : h = u * z ^ k + e) :
    sigma * h ≤ -(m * delta ^ k - eps) := by
  have hz0 : z ≤ 0 := by linarith
  have hdz : delta ≤ -z := by linarith
  have hpowNeg : delta ^ k ≤ (-z) ^ k := pow_le_pow_left₀ hdelta hdz k
  have hpow : z ^ k ≤ -(delta ^ k) := by
    rw [hk.neg_pow] at hpowNeg
    linarith
  have hzpow0 : z ^ k ≤ 0 := hk.pow_nonpos hz0
  have hmain1 : (sigma * u) * z ^ k ≤ m * z ^ k :=
    mul_le_mul_of_nonpos_right hu hzpow0
  have hmain2 : m * z ^ k ≤ m * (-(delta ^ k)) :=
    mul_le_mul_of_nonneg_left hpow hm
  have herr : sigma * e ≤ eps :=
    (signed_error_bounds sigma e eps hsigma he).2
  calc
    sigma * h = (sigma * u) * z ^ k + sigma * e := by rw [hdef]; ring
    _ ≤ -(m * delta ^ k - eps) := by
      linarith

/-- Equality at the reserve boundary is not a nonvanishing certificate. -/
theorem equality_boundary_can_touch
    (m delta : ℝ) (k : ℕ) :
    m * delta ^ k - m * delta ^ k = 0 := by
  ring

/-- Even double contact plus a strictly positive vertical shift has no real zero. -/
theorem double_contact_positive_shift_no_root
    (z q : ℝ)
    (hq : 0 < q) :
    0 < z ^ 2 + q := by
  nlinarith [sq_nonneg z]

/-- The opposite vertical shift factors into two simple-root branches. -/
theorem double_contact_negative_shift_factor
    (z a : ℝ) :
    z ^ 2 - a ^ 2 = (z - a) * (z + a) := by
  ring

/-- The split branch has exact roots at `±a`. -/
theorem double_contact_negative_shift_roots
    (a : ℝ) :
    ((a : ℝ) ^ 2 - a ^ 2 = 0) ∧ ((-a : ℝ) ^ 2 - a ^ 2 = 0) := by
  constructor <;> ring

/-- Lower-order perturbations factor through the lower contact order `j`. -/
theorem lower_order_perturbation_factor
    (z a : ℝ) (j d : ℕ) :
    z ^ (j + d) + a * z ^ j = z ^ j * (z ^ d + a) := by
  rw [pow_add]
  ring

/-- A tiny linear perturbation of a double contact creates two simple candidate roots. -/
theorem double_contact_linear_unfolding
    (z a : ℝ) :
    z ^ 2 + a * z = z * (z + a) := by
  ring

/-- Concrete regression: the old even contact can migrate to odd simple contacts. -/
theorem double_contact_linear_unfolding_roots
    (a : ℝ) :
    (0 : ℝ) ^ 2 + a * 0 = 0 ∧
      (-a : ℝ) ^ 2 + a * (-a) = 0 := by
  constructor <;> ring

#print axioms signed_error_bounds
#print axioms multiple_contact_root_mul_pow_le
#print axioms multiple_contact_root_inside_of_strict
#print axioms multiple_contact_root_cluster
#print axioms multiple_contact_right_outer_reserve
#print axioms multiple_contact_left_outer_reserve_even
#print axioms multiple_contact_left_outer_reserve_odd
#print axioms equality_boundary_can_touch
#print axioms double_contact_positive_shift_no_root
#print axioms double_contact_negative_shift_factor
#print axioms double_contact_negative_shift_roots
#print axioms lower_order_perturbation_factor
#print axioms double_contact_linear_unfolding
#print axioms double_contact_linear_unfolding_roots

end RouteBP5MultipleRootCluster
