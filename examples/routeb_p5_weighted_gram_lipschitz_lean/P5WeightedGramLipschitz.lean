import Mathlib

namespace RouteBP5WeightedGramLipschitz

/-- A signed scalar cross term is controlled by one absolute Gram bound and the
standard `2|xy| ≤ x²+y²` inequality. This is the local algebraic leaf behind
row-wise weighted Gram domination. -/
theorem signed_cross_term_le
    (h c x y : ℝ)
    (hc : |h| ≤ c) :
    2 * h * x * y ≤ c * (x ^ 2 + y ^ 2) := by
  have hc0 : 0 ≤ c := le_trans (abs_nonneg h) hc
  have hxy : 2 * |x * y| ≤ x ^ 2 + y ^ 2 := by
    rw [abs_mul]
    have hs : 0 ≤ (|x| - |y|) ^ 2 := sq_nonneg (|x| - |y|)
    have hx : |x| ^ 2 = x ^ 2 := by simp
    have hy : |y| ^ 2 = y ^ 2 := by simp
    nlinarith
  have habs : 2 * h * x * y ≤ 2 * |h| * |x * y| := by
    calc
      2 * h * x * y ≤ |2 * h * x * y| := le_abs_self _
      _ = 2 * |h| * |x * y| := by simp [abs_mul]; ring
  have hh : 2 * |h| * |x * y| ≤ 2 * c * |x * y| := by
    have hm := mul_le_mul_of_nonneg_right hc (mul_nonneg (by norm_num) (abs_nonneg (x * y)))
    simpa [mul_assoc, mul_left_comm, mul_comm] using hm
  have hscale : 2 * c * |x * y| ≤ c * (x ^ 2 + y ^ 2) := by
    have hm := mul_le_mul_of_nonneg_left hxy hc0
    simpa [mul_assoc, mul_left_comm, mul_comm] using hm
  exact le_trans habs (le_trans hh hscale)

/-- Two-dimensional weighted Gram row certificate. The off-diagonal entry is
bounded only after the signed Gram sum has been formed. -/
theorem weighted_gram_row_upper_2x2
    (h11 h22 h12 a1 a2 c w1 w2 Lambda x y : ℝ)
    (hd1 : h11 ≤ a1)
    (hd2 : h22 ≤ a2)
    (hc : |h12| ≤ c)
    (hr1 : a1 + c ≤ Lambda * w1)
    (hr2 : a2 + c ≤ Lambda * w2) :
    h11 * x ^ 2 + 2 * h12 * x * y + h22 * y ^ 2
      ≤ Lambda * (w1 * x ^ 2 + w2 * y ^ 2) := by
  have hx0 : 0 ≤ x ^ 2 := sq_nonneg x
  have hy0 : 0 ≤ y ^ 2 := sq_nonneg y
  have hd1x : h11 * x ^ 2 ≤ a1 * x ^ 2 :=
    mul_le_mul_of_nonneg_right hd1 hx0
  have hd2y : h22 * y ^ 2 ≤ a2 * y ^ 2 :=
    mul_le_mul_of_nonneg_right hd2 hy0
  have hcross : 2 * h12 * x * y ≤ c * (x ^ 2 + y ^ 2) :=
    signed_cross_term_le h12 c x y hc
  calc
    h11 * x ^ 2 + 2 * h12 * x * y + h22 * y ^ 2
        ≤ a1 * x ^ 2 + c * (x ^ 2 + y ^ 2) + a2 * y ^ 2 := by
          linarith
    _ = (a1 + c) * x ^ 2 + (a2 + c) * y ^ 2 := by ring
    _ ≤ (Lambda * w1) * x ^ 2 + (Lambda * w2) * y ^ 2 := by
      exact add_le_add
        (mul_le_mul_of_nonneg_right hr1 hx0)
        (mul_le_mul_of_nonneg_right hr2 hy0)
    _ = Lambda * (w1 * x ^ 2 + w2 * y ^ 2) := by ring

/-- Pointwise squared-Lipschitz bound for a 2x2 Jacobian from its signed weighted
Gram entries. No square root, inverse or eigenvalue appears in the statement. -/
theorem weighted_jacobian_pointwise_sq_le_2x2
    (j11 j12 j21 j22 w1 w2 a1 a2 c Lambda x y : ℝ)
    (hd1 : w1 * j11 ^ 2 + w2 * j21 ^ 2 ≤ a1)
    (hd2 : w1 * j12 ^ 2 + w2 * j22 ^ 2 ≤ a2)
    (hc : |w1 * j11 * j12 + w2 * j21 * j22| ≤ c)
    (hr1 : a1 + c ≤ Lambda * w1)
    (hr2 : a2 + c ≤ Lambda * w2) :
    w1 * (j11 * x + j12 * y) ^ 2 +
        w2 * (j21 * x + j22 * y) ^ 2
      ≤ Lambda * (w1 * x ^ 2 + w2 * y ^ 2) := by
  let h11 : ℝ := w1 * j11 ^ 2 + w2 * j21 ^ 2
  let h22 : ℝ := w1 * j12 ^ 2 + w2 * j22 ^ 2
  let h12 : ℝ := w1 * j11 * j12 + w2 * j21 * j22
  have hrow := weighted_gram_row_upper_2x2
    h11 h22 h12 a1 a2 c w1 w2 Lambda x y hd1 hd2 hc hr1 hr2
  dsimp [h11, h22, h12] at hrow
  calc
    w1 * (j11 * x + j12 * y) ^ 2 +
        w2 * (j21 * x + j22 * y) ^ 2
        = (w1 * j11 ^ 2 + w2 * j21 ^ 2) * x ^ 2 +
            2 * (w1 * j11 * j12 + w2 * j21 * j22) * x * y +
            (w1 * j12 ^ 2 + w2 * j22 ^ 2) * y ^ 2 := by ring
    _ ≤ Lambda * (w1 * x ^ 2 + w2 * y ^ 2) := hrow

/-- One output-row term of the denominator-cleared implicit weighted Gram
identity. If `A = d J` and `Delta = eta*d^2`, the cleared polynomial term is
exactly `Delta` times the original Gram term. -/
theorem cleared_implicit_weighted_gram_term_identity
    (w eta d Delta Aij Aik Jij Jik : ℝ)
    (hAij : Aij = d * Jij)
    (hAik : Aik = d * Jik)
    (hDelta : Delta = eta * d ^ 2) :
    w * eta * Aij * Aik = Delta * (w * Jij * Jik) := by
  rw [hAij, hAik, hDelta]
  ring

/-- Finite signed summation preserves the denominator-cleared weighted Gram
identity. Absolute values are intentionally not taken inside the sum. -/
theorem cleared_implicit_weighted_gram_sum_identity
    {n : ℕ}
    (w eta d Aij Aik Jij Jik : Fin n → ℝ)
    (Delta : ℝ)
    (hAij : ∀ i, Aij i = d i * Jij i)
    (hAik : ∀ i, Aik i = d i * Jik i)
    (hDelta : ∀ i, Delta = eta i * (d i) ^ 2) :
    (∑ i, w i * eta i * Aij i * Aik i)
      = Delta * ∑ i, w i * Jij i * Jik i := by
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro i hi
  exact cleared_implicit_weighted_gram_term_identity
    (w i) (eta i) (d i) Delta (Aij i) (Aik i) (Jij i) (Jik i)
    (hAij i) (hAik i) (hDelta i)

/-- Exact cancellation regression: the signed cross Gram entry of
`[[1,1],[1,-1]]` with unit weights vanishes. -/
theorem signed_gram_cross_cancellation_example :
    (1 : ℝ) * 1 * 1 + 1 * 1 * (-1) = 0 := by
  norm_num

/-- The same example has exact squared weighted gain `Lambda = 2`; this records
why signed Gram formation must happen before absolute-value fallback. -/
theorem signed_gram_cancellation_gain_example (x y : ℝ) :
    (x + y) ^ 2 + (x - y) ^ 2 = 2 * (x ^ 2 + y ^ 2) := by
  ring

#print axioms signed_cross_term_le
#print axioms weighted_gram_row_upper_2x2
#print axioms weighted_jacobian_pointwise_sq_le_2x2
#print axioms cleared_implicit_weighted_gram_term_identity
#print axioms cleared_implicit_weighted_gram_sum_identity
#print axioms signed_gram_cross_cancellation_example
#print axioms signed_gram_cancellation_gain_example

end RouteBP5WeightedGramLipschitz
