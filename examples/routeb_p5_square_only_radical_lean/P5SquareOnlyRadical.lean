import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# Route-B P5 square-only radical cancellation

Source-independent Lean decomposition of the square-only lane from
`review-T-P5-058-guyuefangyuan-20260908T0120.md`.

The purpose of this file is deliberately narrow: once a downstream consumer
uses only a pointwise square, the common radical factor can be cancelled at the
quadratic level without carrying the sign/parity data needed by a centered
signed difference.  Source factor discovery, executable cancellation at the
original 0/0 point, Float64/libm semantics, and P8 coverage remain outside this
sidecar.
-/

set_option autoImplicit false

namespace RouteBP5SquareOnlyRadical

noncomputable section

/-- The semantic consumer split that must remain explicit at the checker boundary. -/
inductive RadicalConsumerKind where
  | pointwiseSquare
  | centeredSignedDifference
  deriving DecidableEq

/-- Only the pointwise-square consumer may use the parity-free cancellation lane. -/
def squareOnlyAdmissible : RadicalConsumerKind → Prop
  | .pointwiseSquare => True
  | .centeredSignedDifference => False

theorem pointwise_square_is_square_only_admissible :
    squareOnlyAdmissible .pointwiseSquare := by
  trivial

theorem centered_signed_is_not_square_only_admissible :
    ¬ squareOnlyAdmissible .centeredSignedDifference := by
  simp [squareOnlyAdmissible]

/-- Squaring a normalized radical quotient removes the square root from the denominator. -/
theorem normalized_square_eq_ratio
    (A G : ℝ) (hA : 0 ≤ A) :
    (G / Real.sqrt A) ^ 2 = G ^ 2 / A := by
  rw [div_pow, Real.sq_sqrt hA]

/--
If the squared numerator and radicand share a strictly positive common factor
`a`, it cancels from the pointwise square.  `a` is intentionally abstract: a
source factor packet may later instantiate it with an even power such as
`h^(2*m)` without exposing a parity branch to this theorem.
-/
theorem normalized_square_factor_cancel
    (a S G W : ℝ)
    (ha : 0 < a) (hS : 0 < S)
    (hGsq : G ^ 2 = a * W) :
    S * (G / Real.sqrt (a * S)) ^ 2 = W := by
  have hAS : 0 ≤ a * S := le_of_lt (mul_pos ha hS)
  rw [normalized_square_eq_ratio (a * S) G hAS, hGsq]
  field_simp [ne_of_gt ha, ne_of_gt hS]

/--
Balanced specialization: the reduced square is `J^2 / S`, with no parity or
fixed-sign hypothesis.  Only the positive common factor away from the original
root is needed for the equality to the original radical quotient.
-/
theorem balanced_square_extension_no_parity
    (a S G J : ℝ)
    (ha : 0 < a) (hS : 0 < S)
    (hGsq : G ^ 2 = a * J ^ 2) :
    S * (G / Real.sqrt (a * S)) ^ 2 = J ^ 2 := by
  exact normalized_square_factor_cancel a S G (J ^ 2) ha hS hGsq

/-- Pure algebraic cancellation interface for a source that already supplies a common factor. -/
theorem common_factor_square_cancel
    (a S u W : ℝ)
    (ha : a ≠ 0)
    (hpacket : (a * S) * u ^ 2 = a * W) :
    S * u ^ 2 = W := by
  have hzero : a * (S * u ^ 2 - W) = 0 := by
    calc
      a * (S * u ^ 2 - W) = (a * S) * u ^ 2 - a * W := by ring
      _ = 0 := sub_eq_zero.mpr hpacket
  rcases mul_eq_zero.mp hzero with ha0 | hrest
  · exact (ha ha0).elim
  · exact sub_eq_zero.mp hrest

/--
Division-free pointwise bound for the reduced square packet
`S*W = P*J^2`.  In the mathematical review, `P` is `h^(2*k)` and `HP` is its
cellwise amplitude bound `H^(2*k)`.
-/
theorem cancelled_square_pointwise_bound
    (s0 S W P J MJ HP : ℝ)
    (hs : s0 ≤ S) (hW : 0 ≤ W)
    (hpacket : S * W = P * J ^ 2)
    (hP : 0 ≤ P) (hPHP : P ≤ HP)
    (hJ : J ^ 2 ≤ MJ ^ 2) :
    s0 * W ≤ HP * MJ ^ 2 := by
  have hleft : s0 * W ≤ S * W :=
    mul_le_mul_of_nonneg_right hs hW
  have hHP : 0 ≤ HP := le_trans hP hPHP
  have hright : P * J ^ 2 ≤ HP * MJ ^ 2 :=
    mul_le_mul hPHP hJ (sq_nonneg J) hHP
  calc
    s0 * W ≤ S * W := hleft
    _ = P * J ^ 2 := hpacket
    _ ≤ HP * MJ ^ 2 := hright

/-- Balanced (`k=0`, hence `P=1`) pointwise bound; no `h` amplitude enters. -/
theorem balanced_square_pointwise_bound
    (s0 S W J MJ : ℝ)
    (hs : s0 ≤ S) (hW : 0 ≤ W)
    (hpacket : S * W = J ^ 2)
    (hJ : J ^ 2 ≤ MJ ^ 2) :
    s0 * W ≤ MJ ^ 2 := by
  calc
    s0 * W ≤ S * W := mul_le_mul_of_nonneg_right hs hW
    _ = J ^ 2 := hpacket
    _ ≤ MJ ^ 2 := hJ

/-- Exact two-point telescoping identity for the balanced reduced square `W=J^2/S`. -/
theorem balanced_square_difference_identity
    (S S0 W W0 J J0 : ℝ)
    (hSW : S * W = J ^ 2)
    (hS0W0 : S0 * W0 = J0 ^ 2) :
    S * S0 * (W - W0) =
      S0 * (J ^ 2 - J0 ^ 2) + J0 ^ 2 * (S0 - S) := by
  calc
    S * S0 * (W - W0) = S0 * (S * W) - S * (S0 * W0) := by ring
    _ = S0 * J ^ 2 - S * J0 ^ 2 := by rw [hSW, hS0W0]
    _ = S0 * (J ^ 2 - J0 ^ 2) + J0 ^ 2 * (S0 - S) := by ring

/-- Exact two-point telescoping identity for the general reduced packet `S*W=P*J^2`. -/
theorem cancelled_square_difference_identity
    (S S0 W W0 P P0 J J0 : ℝ)
    (hSW : S * W = P * J ^ 2)
    (hS0W0 : S0 * W0 = P0 * J0 ^ 2) :
    S * S0 * (W - W0) =
      S0 * (P * J ^ 2 - P0 * J0 ^ 2) +
        (P0 * J0 ^ 2) * (S0 - S) := by
  calc
    S * S0 * (W - W0) = S0 * (S * W) - S * (S0 * W0) := by ring
    _ = S0 * (P * J ^ 2) - S * (P0 * J0 ^ 2) := by rw [hSW, hS0W0]
    _ = S0 * (P * J ^ 2 - P0 * J0 ^ 2) +
          (P0 * J0 ^ 2) * (S0 - S) := by ring

/-- Standard exact amplitude/variation estimate for the squared numerator. -/
theorem square_difference_abs_bound
    (J J0 MJ dJ : ℝ)
    (hJ : |J| ≤ MJ) (hJ0 : |J0| ≤ MJ)
    (hdJ : |J - J0| ≤ dJ) :
    |J ^ 2 - J0 ^ 2| ≤ 2 * MJ * dJ := by
  have hdJ0 : 0 ≤ dJ := le_trans (abs_nonneg (J - J0)) hdJ
  have hsum : |J + J0| ≤ 2 * MJ := by
    calc
      |J + J0| ≤ |J| + |J0| := abs_add_le J J0
      _ ≤ MJ + MJ := add_le_add hJ hJ0
      _ = 2 * MJ := by ring
  have hprod : |J - J0| * |J + J0| ≤ dJ * (2 * MJ) :=
    mul_le_mul hdJ hsum (abs_nonneg (J + J0)) hdJ0
  calc
    |J ^ 2 - J0 ^ 2| = |(J - J0) * (J + J0)| := by congr 1 <;> ring
    _ = |J - J0| * |J + J0| := abs_mul (J - J0) (J + J0)
    _ ≤ dJ * (2 * MJ) := hprod
    _ = 2 * MJ * dJ := by ring

/-- If the over-cancelled even factor vanishes at the root, the reduced pointwise square vanishes. -/
theorem cancelled_square_zero_at_factor_zero
    (S W P J : ℝ)
    (hS : S ≠ 0)
    (hpacket : S * W = P * J ^ 2)
    (hP : P = 0) :
    W = 0 := by
  have hSW : S * W = 0 := by simpa [hP] using hpacket
  rcases mul_eq_zero.mp hSW with hS0 | hW0
  · exact (hS hS0).elim
  · exact hW0

/-- Exact balanced-odd regression: the pointwise square is constant away from zero. -/
theorem balanced_odd_pointwise_square_constant
    (t : ℝ) (ht : t ≠ 0) :
    (t / |t|) ^ 2 = 1 := by
  by_cases hnonneg : 0 ≤ t
  · rw [abs_of_nonneg hnonneg]
    field_simp [ht]
  · have hneg : t < 0 := lt_of_not_ge hnonneg
    rw [abs_of_neg hneg]
    field_simp [ht]

/-- Exact negative control: the signed centered jump remains four across a sign change. -/
theorem balanced_odd_centered_signed_jump
    (eps : ℝ) (heps : 0 < eps) :
    (eps / |eps| - (-eps) / |-eps|) ^ 2 = 4 := by
  have heps0 : eps ≠ 0 := ne_of_gt heps
  rw [abs_of_pos heps, abs_neg, abs_of_pos heps]
  field_simp [heps0]
  norm_num

/-- Yet the corresponding pointwise-square variation is exactly zero. -/
theorem balanced_odd_square_variation_zero
    (eps : ℝ) (heps : 0 < eps) :
    (eps / |eps|) ^ 2 - ((-eps) / |-eps|) ^ 2 = 0 := by
  have heps0 : eps ≠ 0 := ne_of_gt heps
  have hneg0 : -eps ≠ 0 := neg_ne_zero.mpr heps0
  rw [balanced_odd_pointwise_square_constant eps heps0,
      balanced_odd_pointwise_square_constant (-eps) hneg0]
  norm_num

#print axioms RouteBP5SquareOnlyRadical.pointwise_square_is_square_only_admissible
#print axioms RouteBP5SquareOnlyRadical.centered_signed_is_not_square_only_admissible
#print axioms RouteBP5SquareOnlyRadical.normalized_square_eq_ratio
#print axioms RouteBP5SquareOnlyRadical.normalized_square_factor_cancel
#print axioms RouteBP5SquareOnlyRadical.balanced_square_extension_no_parity
#print axioms RouteBP5SquareOnlyRadical.common_factor_square_cancel
#print axioms RouteBP5SquareOnlyRadical.cancelled_square_pointwise_bound
#print axioms RouteBP5SquareOnlyRadical.balanced_square_pointwise_bound
#print axioms RouteBP5SquareOnlyRadical.balanced_square_difference_identity
#print axioms RouteBP5SquareOnlyRadical.cancelled_square_difference_identity
#print axioms RouteBP5SquareOnlyRadical.square_difference_abs_bound
#print axioms RouteBP5SquareOnlyRadical.cancelled_square_zero_at_factor_zero
#print axioms RouteBP5SquareOnlyRadical.balanced_odd_pointwise_square_constant
#print axioms RouteBP5SquareOnlyRadical.balanced_odd_centered_signed_jump
#print axioms RouteBP5SquareOnlyRadical.balanced_odd_square_variation_zero

end

end RouteBP5SquareOnlyRadical
