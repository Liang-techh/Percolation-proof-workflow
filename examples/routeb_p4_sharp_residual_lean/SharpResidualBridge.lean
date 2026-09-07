import Mathlib.Tactic

/-!
  Route-B P4: sharp one-channel residual/Schur interface.

  This is the exact-real algebraic child suggested by T-P4-005.  It separates
  the necessary-and-sufficient scalar PSD condition from the later task of
  bounding a deployed DH residual on a covered cell.
-/

set_option autoImplicit false

namespace RouteBP4SharpResidual

def quadratic (p d r y x : ℝ) : ℝ :=
  p * x ^ 2 + 2 * x * r + d * y ^ 2

theorem schur_residual_nonnegative_iff
    (p d r y : ℝ) (hp : 0 < p) :
    (∀ x : ℝ, 0 ≤ quadratic p d r y x) ↔ r ^ 2 ≤ p * d * y ^ 2 := by
  constructor
  · intro hnonneg
    have hmul : 0 ≤ p * quadratic p d r y (-r / p) :=
      mul_nonneg hp.le (hnonneg (-r / p))
    have hident : p * quadratic p d r y (-r / p) = p * d * y ^ 2 - r ^ 2 := by
      simp only [quadratic, div_eq_mul_inv]
      field_simp [ne_of_gt hp]; ring
    rw [hident] at hmul
    nlinarith
  · intro hbound x
    have hrem : 0 ≤ p * d * y ^ 2 - r ^ 2 := by
      nlinarith
    have hprod : 0 ≤ p * quadratic p d r y x := by
      have hsquare : 0 ≤ (p * x + r) ^ 2 := sq_nonneg _
      calc
        0 ≤ (p * x + r) ^ 2 + (p * d * y ^ 2 - r ^ 2) := by
          nlinarith
        _ = p * quadratic p d r y x := by
          simp [quadratic]
          ring
    have hq : quadratic p d r y x =
        (p * quadratic p d r y x) / p := by
      field_simp [ne_of_gt hp]
    rw [hq]
    exact div_nonneg hprod hp.le

theorem one_channel_residual_envelope
    (m remote drift y alpha beta gamma c : ℝ)
    (_ha : 0 ≤ alpha) (_hb : 0 ≤ beta) (_hg : 0 ≤ gamma)
    (hc : 0 ≤ c)
    (hm : |m| ≤ alpha * |y|)
    (hr : |remote| ≤ beta * |y|)
    (hd : |drift| ≤ gamma * |y|)
    (hsum : alpha + beta + gamma ≤ c) :
    (m + remote + drift) ^ 2 ≤ c ^ 2 * y ^ 2 := by
  have habs : |m + remote + drift| ≤ c * |y| := by
    calc
      |m + remote + drift| ≤ |m| + |remote| + |drift| := by
        calc
          |m + remote + drift| ≤ |m + remote| + |drift| := abs_add_le _ _
          _ ≤ |m| + |remote| + |drift| := by
            gcongr
            exact abs_add_le _ _
      _ ≤ (alpha + beta + gamma) * |y| := by
        nlinarith [hm, hr, hd, abs_nonneg y]
      _ ≤ c * |y| := by
        exact mul_le_mul_of_nonneg_right hsum (abs_nonneg y)
  have hbounds : -(c * |y|) ≤ m + remote + drift ∧
      m + remote + drift ≤ c * |y| := (abs_le.mp habs)
  have hleft : -(c * |y|) ≤ m + remote + drift := hbounds.1
  have hright : m + remote + drift ≤ c * |y| := hbounds.2
  have hA : 0 ≤ c * |y| := mul_nonneg hc (abs_nonneg y)
  have hprod : 0 ≤ (c * |y| - (m + remote + drift)) *
      (c * |y| + (m + remote + drift)) := by
    exact mul_nonneg (sub_nonneg.mpr hright) (by linarith)
  have hyabs : |y| ^ 2 = y ^ 2 := sq_abs y
  nlinarith

theorem quarter_budget_strict :
    (1 / 4 : ℝ) ^ 2 < (3 / 5 : ℝ) * (116667666666667 / 1000000000000000 : ℝ) := by
  norm_num

#print axioms schur_residual_nonnegative_iff
#print axioms one_channel_residual_envelope
#print axioms quarter_budget_strict

end RouteBP4SharpResidual
