import Mathlib

namespace RouteBP4TransverseSchurReserve

/-- Triangle-envelope bridge for a residual split into a same-coordinate term,
    a same-coordinate remainder, and a transverse remainder. -/
theorem decomposed_residual_abs_bound
    (c beta gamma y z e b : ℝ)
    (hc : 0 ≤ c)
    (he : |e| ≤ beta * |y|)
    (hb : |b| ≤ gamma * |z|) :
    |c * y + e + b| ≤ (c + beta) * |y| + gamma * |z| := by
  have hcy : |c * y| = c * |y| := by
    rw [abs_mul, abs_of_nonneg hc]
  have hce : |c * y + e| ≤ c * |y| + beta * |y| := by
    calc
      |c * y + e| ≤ |c * y| + |e| := abs_add _ _
      _ ≤ c * |y| + beta * |y| := by rw [hcy]; exact add_le_add_left he _
  calc
    |c * y + e + b| ≤ |c * y + e| + |b| := abs_add _ _
    _ ≤ (c * |y| + beta * |y|) + gamma * |z| := add_le_add hce hb
    _ = (c + beta) * |y| + gamma * |z| := by ring

/-- Division-free algebraic identity behind the sharp transverse reserve. -/
theorem transverse_gap_identity
    (p d a gamma h Y Z Delta : ℝ)
    (hDelta : Delta = p * d - a^2) :
    Delta * (p * d * Y^2 + p * h * Z^2 - (a * Y + gamma * Z)^2) =
      (Delta * Y - a * gamma * Z)^2 +
        p * (Delta * h - d * gamma^2) * Z^2 := by
  rw [hDelta]
  ring

/-- The relative-plus-transverse envelope fits inside the quadratic Schur
    budget whenever the strict unused reserve pays for the transverse term. -/
theorem transverse_square_budget
    (p d a gamma h r y z : ℝ)
    (hp : 0 < p)
    (ha : 0 ≤ a)
    (hgamma : 0 ≤ gamma)
    (hDelta : 0 < p * d - a^2)
    (hr : |r| ≤ a * |y| + gamma * |z|)
    (hreserve : d * gamma^2 ≤ (p * d - a^2) * h) :
    r^2 ≤ p * (d * y^2 + h * z^2) := by
  let Delta : ℝ := p * d - a^2
  let Y : ℝ := |y|
  let Z : ℝ := |z|
  let L : ℝ := a * Y + gamma * Z
  have hDelta' : 0 < Delta := by simpa [Delta] using hDelta
  have hreserve' : 0 ≤ Delta * h - d * gamma^2 := by
    exact sub_nonneg.mpr (by simpa [Delta] using hreserve)
  have hRhs :
      0 ≤ (Delta * Y - a * gamma * Z)^2 +
        p * (Delta * h - d * gamma^2) * Z^2 := by
    exact add_nonneg (sq_nonneg _) (mul_nonneg (mul_nonneg (le_of_lt hp) hreserve') (sq_nonneg Z))
  have hId := transverse_gap_identity p d a gamma h Y Z Delta (by simp [Delta])
  have hProd :
      0 ≤ Delta * (p * d * Y^2 + p * h * Z^2 - (a * Y + gamma * Z)^2) := by
    rw [hId]
    exact hRhs
  have hBracket :
      0 ≤ p * d * Y^2 + p * h * Z^2 - (a * Y + gamma * Z)^2 := by
    exact (mul_nonneg_iff_of_pos_left hDelta').mp hProd
  have hL : 0 ≤ L := by
    exact add_nonneg (mul_nonneg ha (abs_nonneg y)) (mul_nonneg hgamma (abs_nonneg z))
  have hrL : |r| ≤ L := by simpa [L, Y, Z] using hr
  have hAbsSq : |r|^2 ≤ L^2 := by
    have h1 : 0 ≤ L - |r| := sub_nonneg.mpr hrL
    have h2 : 0 ≤ L + |r| := add_nonneg hL (abs_nonneg r)
    have hprod := mul_nonneg h1 h2
    nlinarith
  have hLSq : L^2 ≤ p * (d * y^2 + h * z^2) := by
    have hY : Y^2 = y^2 := by simp [Y, sq_abs]
    have hZ : Z^2 = z^2 := by simp [Z, sq_abs]
    have hBracket' := hBracket
    rw [hY, hZ] at hBracket'
    simpa [L, Y, Z] using (show
      (a * |y| + gamma * |z|)^2 ≤ p * (d * y^2 + h * z^2) by nlinarith)
  have hrSq : r^2 = |r|^2 := by simp [sq_abs]
  rw [hrSq]
  exact le_trans hAbsSq hLSq

/-- Completion of the square in the Schur variable `x`. -/
theorem schur_from_square_budget
    (p d h x y z r : ℝ)
    (hp : 0 < p)
    (hr : r^2 ≤ p * (d * y^2 + h * z^2)) :
    0 ≤ p * x^2 + 2 * x * r + d * y^2 + h * z^2 := by
  have hgap : 0 ≤ p * (d * y^2 + h * z^2) - r^2 := sub_nonneg.mpr hr
  have hsum :
      0 ≤ (p * x + r)^2 + (p * (d * y^2 + h * z^2) - r^2) :=
    add_nonneg (sq_nonneg _) hgap
  have hmul :
      0 ≤ p * (p * x^2 + 2 * x * r + d * y^2 + h * z^2) := by
    calc
      0 ≤ (p * x + r)^2 + (p * (d * y^2 + h * z^2) - r^2) := hsum
      _ = p * (p * x^2 + 2 * x * r + d * y^2 + h * z^2) := by ring
  exact (mul_nonneg_iff_of_pos_left hp).mp hmul

/-- Sharp positive-side robust Schur theorem from T-P4-014.  No division and
    no square root occur in the hypotheses. -/
theorem relative_plus_transverse_schur
    (p d c beta gamma h x y z e b : ℝ)
    (hp : 0 < p)
    (hc : 0 ≤ c)
    (hbeta : 0 ≤ beta)
    (hgamma : 0 ≤ gamma)
    (hDelta : 0 < p * d - (c + beta)^2)
    (he : |e| ≤ beta * |y|)
    (hb : |b| ≤ gamma * |z|)
    (hreserve : d * gamma^2 ≤ (p * d - (c + beta)^2) * h) :
    0 ≤ p * x^2 + 2 * x * (c * y + e + b) + d * y^2 + h * z^2 := by
  have hr := decomposed_residual_abs_bound c beta gamma y z e b hc he hb
  have hsq := transverse_square_budget p d (c + beta) gamma h (c * y + e + b) y z
    hp (add_nonneg hc hbeta) hgamma hDelta hr hreserve
  exact schur_from_square_budget p d h x y z (c * y + e + b) hp hsq

/-- Exact block-4 constants imported from the sharp P4 sidecar / T-P4-014. -/
def p4 : ℝ := 3 / 5

def d4 : ℝ := 116667666666667 / 1000000000000000

theorem block4_quarter_coefficient :
    (1 / 100 : ℝ) + 6 / 25 = 1 / 4 := by norm_num

theorem block4_delta_exact :
    p4 * d4 - ((1 / 100 : ℝ) + 6 / 25)^2 =
      37503000000001 / 5000000000000000 := by
  norm_num [p4, d4]

/-- The integer-scaled condition used by the source/checker lane is exactly
    sufficient for the block-4 transverse reserve. -/
theorem block4_reserve_from_integer_condition
    (gamma h : ℝ)
    (hreserve :
      583338333333335 * gamma^2 ≤ 37503000000001 * h) :
    d4 * gamma^2 ≤
      (p4 * d4 - ((1 / 100 : ℝ) + 6 / 25)^2) * h := by
  rw [block4_delta_exact]
  dsimp [d4]
  nlinarith

/-- Concrete block-4 corollary: quarter-relative residual plus a transverse
    residual is absorbed by `h*z^2` under the exact integer reserve test. -/
theorem block4_quarter_plus_transverse
    (gamma h x y z e b : ℝ)
    (hgamma : 0 ≤ gamma)
    (he : |e| ≤ (6 / 25 : ℝ) * |y|)
    (hb : |b| ≤ gamma * |z|)
    (hreserve :
      583338333333335 * gamma^2 ≤ 37503000000001 * h) :
    0 ≤ p4 * x^2 + 2 * x * ((1 / 100 : ℝ) * y + e + b) + d4 * y^2 + h * z^2 := by
  apply relative_plus_transverse_schur
  · norm_num [p4]
  · norm_num
  · norm_num
  · exact hgamma
  · rw [block4_delta_exact]
    norm_num
  · exact he
  · exact hb
  · exact block4_reserve_from_integer_condition gamma h hreserve

#print axioms decomposed_residual_abs_bound
#print axioms transverse_gap_identity
#print axioms transverse_square_budget
#print axioms schur_from_square_budget
#print axioms relative_plus_transverse_schur
#print axioms block4_quarter_coefficient
#print axioms block4_delta_exact
#print axioms block4_reserve_from_integer_condition
#print axioms block4_quarter_plus_transverse

end RouteBP4TransverseSchurReserve
