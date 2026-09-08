import Mathlib

noncomputable section

namespace RouteBP5ZeroContactFactor

/-- Quadratic polynomial in the coefficient order used by T-P5-056. -/
def quadPoly (a b c t : ℝ) : ℝ :=
  a * t ^ 2 + b * t + c

/-- Cubic polynomial in the coefficient order used by T-P5-056. -/
def cubicPoly (a b c d t : ℝ) : ℝ :=
  a * t ^ 3 + b * t ^ 2 + c * t + d

/--
Division-free quadratic repeated-root equations give the exact square factor.
No root discovery is trusted here: `r` is only a witness checked by identities.
-/
theorem quadratic_repeated_root_factor_identity
    (a b c r t : ℝ)
    (hb : b + 2 * a * r = 0)
    (hc : c - a * r ^ 2 = 0) :
    quadPoly a b c t = a * (t - r) ^ 2 := by
  have hb' : b = -2 * a * r := by
    linarith
  have hc' : c = a * r ^ 2 := by
    linarith
  rw [hb', hc']
  dsimp [quadPoly]
  ring

/-- Once the quadratic factor identity is checked, a nonnegative leading factor is globally sufficient. -/
theorem quadratic_repeated_root_nonneg
    (a b c r t : ℝ)
    (ha : 0 ≤ a)
    (hb : b + 2 * a * r = 0)
    (hc : c - a * r ^ 2 = 0) :
    0 ≤ quadPoly a b c t := by
  rw [quadratic_repeated_root_factor_identity a b c r t hb hc]
  exact mul_nonneg ha (sq_nonneg (t - r))

/-- The quadratic witness equations also certify exact contact at the proposed root. -/
theorem quadratic_repeated_root_contact
    (a b c r : ℝ)
    (hb : b + 2 * a * r = 0)
    (hc : c - a * r ^ 2 = 0) :
    quadPoly a b c r = 0 := by
  rw [quadratic_repeated_root_factor_identity a b c r r hb hc]
  ring

/-- An affine factor is nonnegative on `[0,1]` when both endpoint values are nonnegative. -/
theorem affine_nonneg_of_endpoint_values
    (s q t : ℝ)
    (ht0 : 0 ≤ t)
    (ht1 : t ≤ 1)
    (hq0 : 0 ≤ q)
    (hq1 : 0 ≤ s + q) :
    0 ≤ s * t + q := by
  have h1t : 0 ≤ 1 - t := by
    linarith
  have hleft : 0 ≤ (1 - t) * q := mul_nonneg h1t hq0
  have hright : 0 ≤ t * (s + q) := mul_nonneg ht0 hq1
  nlinarith

/--
Division-free cubic repeated-root equations give a square times an affine factor.
These are exactly the trusted equations proposed by the mathematical review.
-/
theorem cubic_repeated_root_factor_identity
    (a b c d r t : ℝ)
    (hc : c + 3 * a * r ^ 2 + 2 * b * r = 0)
    (hd : d - 2 * a * r ^ 3 - b * r ^ 2 = 0) :
    cubicPoly a b c d t =
      (t - r) ^ 2 * (a * t + (b + 2 * a * r)) := by
  have hc' : c = -(3 * a * r ^ 2 + 2 * b * r) := by
    linarith
  have hd' : d = 2 * a * r ^ 3 + b * r ^ 2 := by
    linarith
  rw [hc', hd']
  dsimp [cubicPoly]
  ring

/-- The cubic witness equations certify exact contact at the proposed root. -/
theorem cubic_repeated_root_contact
    (a b c d r : ℝ)
    (hc : c + 3 * a * r ^ 2 + 2 * b * r = 0)
    (hd : d - 2 * a * r ^ 3 - b * r ^ 2 = 0) :
    cubicPoly a b c d r = 0 := by
  rw [cubic_repeated_root_factor_identity a b c d r r hc hd]
  ring

/--
Cubic zero-contact consumer.  The square is automatically nonnegative; only
both endpoint values of the remaining affine factor need sign checks.
-/
theorem cubic_repeated_root_nonneg_on_unit
    (a b c d r t : ℝ)
    (hc : c + 3 * a * r ^ 2 + 2 * b * r = 0)
    (hd : d - 2 * a * r ^ 3 - b * r ^ 2 = 0)
    (hL0 : 0 ≤ b + 2 * a * r)
    (hL1 : 0 ≤ a + b + 2 * a * r)
    (ht0 : 0 ≤ t)
    (ht1 : t ≤ 1) :
    0 ≤ cubicPoly a b c d t := by
  rw [cubic_repeated_root_factor_identity a b c d r t hc hd]
  have hL : 0 ≤ a * t + (b + 2 * a * r) := by
    apply affine_nonneg_of_endpoint_values a (b + 2 * a * r) t ht0 ht1 hL0
    nlinarith
  exact mul_nonneg (sq_nonneg (t - r)) hL

/-- A left-endpoint zero factors without requiring an even-multiplicity root. -/
theorem left_endpoint_factor_identity
    (a b c d t : ℝ)
    (hd : d = 0) :
    cubicPoly a b c d t = t * (a * t ^ 2 + b * t + c) := by
  rw [hd]
  dsimp [cubicPoly]
  ring

/-- Left-endpoint factor consumer: only the one-sided factor `t ≥ 0` is needed. -/
theorem left_endpoint_factor_nonneg
    (a b c d t : ℝ)
    (hd : d = 0)
    (ht0 : 0 ≤ t)
    (hquot : 0 ≤ a * t ^ 2 + b * t + c) :
    0 ≤ cubicPoly a b c d t := by
  rw [left_endpoint_factor_identity a b c d t hd]
  exact mul_nonneg ht0 hquot

/-- A right-endpoint zero has an exact one-sided `(1-t)` factor. -/
theorem right_endpoint_factor_identity
    (a b c d t : ℝ)
    (hsum : a + b + c + d = 0) :
    cubicPoly a b c d t =
      (1 - t) * (-a * t ^ 2 - (a + b) * t + d) := by
  have hd : d = -a - b - c := by
    linarith
  rw [hd]
  dsimp [cubicPoly]
  ring

/-- Right-endpoint factor consumer: only the one-sided factor `1-t ≥ 0` is needed. -/
theorem right_endpoint_factor_nonneg
    (a b c d t : ℝ)
    (hsum : a + b + c + d = 0)
    (ht1 : t ≤ 1)
    (hquot : 0 ≤ -a * t ^ 2 - (a + b) * t + d) :
    0 ≤ cubicPoly a b c d t := by
  rw [right_endpoint_factor_identity a b c d t hsum]
  exact mul_nonneg (by linarith) hquot

/-- The canonical non-dyadic zero-contact obstruction is exactly a repeated-root square. -/
theorem one_third_square_regression
    (t : ℝ) :
    quadPoly 1 (-(2 / 3)) (1 / 9) t = (t - 1 / 3) ^ 2 := by
  dsimp [quadPoly]
  ring

/-- The same polynomial receives an immediate exact nonnegative certificate. -/
theorem one_third_square_nonneg_regression
    (t : ℝ) :
    0 ≤ quadPoly 1 (-(2 / 3)) (1 / 9) t := by
  rw [one_third_square_regression]
  exact sq_nonneg (t - 1 / 3)

/-- Merely finding rational roots is unsound: this simple-root polynomial is negative between them. -/
theorem simple_root_negative_regression :
    quadPoly 1 (-1) (2 / 9) (1 / 3) = 0 ∧
      quadPoly 1 (-1) (2 / 9) (2 / 3) = 0 ∧
      quadPoly 1 (-1) (2 / 9) 0 = 2 / 9 ∧
      quadPoly 1 (-1) (2 / 9) 1 = 2 / 9 ∧
      quadPoly 1 (-1) (2 / 9) (1 / 2) = -(1 / 36 : ℝ) := by
  norm_num [quadPoly]

/-- A simple endpoint root is compatible with one-sided nonnegativity. -/
theorem endpoint_simple_root_regression :
    quadPoly 0 1 0 0 = 0 ∧
      ∀ t : ℝ, 0 ≤ t → 0 ≤ quadPoly 0 1 0 t := by
  constructor
  · norm_num [quadPoly]
  · intro t ht
    simpa [quadPoly] using ht

/--
Typed P5 seam: independently certified quadratic `Rtr` and cubic `Rdet`
zero-contact packets may feed an already-proved two-remainder consumer.
This theorem does not bind deployed source coefficients or P8 coverage.
-/
theorem zero_contact_packets_feed_two_remainder_consumer
    (P : Prop)
    (Rtr Rdet t : ℝ)
    (qa qb qc qr : ℝ)
    (ca cb cc cd cr : ℝ)
    (hRtr : Rtr = quadPoly qa qb qc t)
    (hRdet : Rdet = cubicPoly ca cb cc cd t)
    (hqa : 0 ≤ qa)
    (hqb : qb + 2 * qa * qr = 0)
    (hqc : qc - qa * qr ^ 2 = 0)
    (hcc : cc + 3 * ca * cr ^ 2 + 2 * cb * cr = 0)
    (hcd : cd - 2 * ca * cr ^ 3 - cb * cr ^ 2 = 0)
    (hL0 : 0 ≤ cb + 2 * ca * cr)
    (hL1 : 0 ≤ ca + cb + 2 * ca * cr)
    (ht0 : 0 ≤ t)
    (ht1 : t ≤ 1)
    (hconsumer : 0 ≤ Rtr → 0 ≤ Rdet → P) :
    P := by
  apply hconsumer
  · rw [hRtr]
    exact quadratic_repeated_root_nonneg qa qb qc qr t hqa hqb hqc
  · rw [hRdet]
    exact cubic_repeated_root_nonneg_on_unit
      ca cb cc cd cr t hcc hcd hL0 hL1 ht0 ht1

#print axioms quadratic_repeated_root_factor_identity
#print axioms quadratic_repeated_root_nonneg
#print axioms quadratic_repeated_root_contact
#print axioms affine_nonneg_of_endpoint_values
#print axioms cubic_repeated_root_factor_identity
#print axioms cubic_repeated_root_contact
#print axioms cubic_repeated_root_nonneg_on_unit
#print axioms left_endpoint_factor_identity
#print axioms left_endpoint_factor_nonneg
#print axioms right_endpoint_factor_identity
#print axioms right_endpoint_factor_nonneg
#print axioms one_third_square_regression
#print axioms one_third_square_nonneg_regression
#print axioms simple_root_negative_regression
#print axioms endpoint_simple_root_regression
#print axioms zero_contact_packets_feed_two_remainder_consumer

end RouteBP5ZeroContactFactor
