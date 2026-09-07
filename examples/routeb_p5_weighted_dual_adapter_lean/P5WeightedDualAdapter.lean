import Mathlib.Data.Fin.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic

/-!
# Route-B P5 weighted-dual execution-remainder adapter

This source-independent sidecar formalizes the diagonal rational adapter from
`review-T-P5-014-liuguanyi-20260907T0417.md`.

It deliberately starts *after* a source/checker has produced actual
execution-error bounds in identified generalized-force coordinates.  It does
not authenticate Julia/DH/Float64 sources, produce interval bounds, prove P8
coverage, or close P5/M4.

The weighted power consumer itself already has a separate sidecar under
`routeb_p5_weighted_dual_residual_lean`; this file focuses on the new interface
lemmas needed to turn source boxes/normalizations into that consumer's dual
quantity.
-/

open scoped BigOperators

set_option autoImplicit false

namespace RouteBP5WeightedDualAdapter

noncomputable section

abbrev Vec6 := Fin 6 → ℝ

/-- Diagonal damping-dual quadratic quantity `sum r_i^2 / d_i`. -/
def weightedDual (d r : Vec6) : ℝ :=
  ∑ i, r i ^ 2 / d i

/-- Diagonal damping quadratic quantity `sum d_i v_i^2`. -/
def dampingSq (d v : Vec6) : ℝ :=
  ∑ i, d i * v i ^ 2

/-- Mechanical power pairing in the same generalized-force coordinates. -/
def power (r v : Vec6) : ℝ :=
  ∑ i, r i * v i

/-- An implementation-only diagonal scaling of a raw error vector. -/
def diagonalScale (s e : Vec6) : Vec6 :=
  fun i => s i * e i

/-- Positive damping weights make the diagonal dual quadratic nonnegative. -/
theorem weightedDual_nonneg
    (d r : Vec6) (hd : ∀ i, 0 < d i) :
    0 ≤ weightedDual d r := by
  unfold weightedDual
  exact Finset.sum_nonneg fun i _ =>
    div_nonneg (sq_nonneg (r i)) (le_of_lt (hd i))

/-- A componentwise force box in the *same generalized-force coordinates*
produces the exact diagonal weighted-dual box cap. -/
theorem box_to_weightedDual
    (d r eps : Vec6)
    (hd : ∀ i, 0 < d i)
    (hr : ∀ i, |r i| ≤ eps i) :
    weightedDual d r ≤ ∑ i, eps i ^ 2 / d i := by
  unfold weightedDual
  apply Finset.sum_le_sum
  intro i hi
  have hbounds : -eps i ≤ r i ∧ r i ≤ eps i := (abs_le).mp (hr i)
  have hsq : r i ^ 2 ≤ eps i ^ 2 := by
    nlinarith [sq_nonneg (eps i - r i), sq_nonneg (eps i + r i)]
  exact (div_le_div_iff_of_pos_right (hd i)).2 hsq

/-- The direct division-free rate-budget consumer for a componentwise source
box.  No unrelated Euclidean norm is introduced. -/
theorem box_to_rate_budget
    (d r eps : Vec6) (gR BR : ℝ)
    (hd : ∀ i, 0 < d i)
    (hr : ∀ i, |r i| ≤ eps i)
    (hbudget : ∑ i, eps i ^ 2 / d i ≤ 4 * gR * BR) :
    weightedDual d r ≤ 4 * gR * BR := by
  exact le_trans (box_to_weightedDual d r eps hd hr) hbudget

/-- Diagonal implementation normalization is not a coordinate-invariant no-op:
its scale factors remain explicitly inside the weighted dual metric. -/
theorem diagonal_normalization_dual_identity
    (d s e : Vec6) :
    weightedDual d (diagonalScale s e) =
      ∑ i, s i ^ 2 * e i ^ 2 / d i := by
  unfold weightedDual diagonalScale
  apply Finset.sum_congr rfl
  intro i hi
  ring

/-- A raw component box transported by a diagonal implementation scaling gives
its exact generalized-force weighted-dual cap. -/
theorem diagonal_box_to_weightedDual
    (d s e eta : Vec6)
    (hd : ∀ i, 0 < d i)
    (he : ∀ i, |e i| ≤ eta i) :
    weightedDual d (diagonalScale s e) ≤
      ∑ i, s i ^ 2 * eta i ^ 2 / d i := by
  rw [diagonal_normalization_dual_identity]
  apply Finset.sum_le_sum
  intro i hi
  have hbounds : -eta i ≤ e i ∧ e i ≤ eta i := (abs_le).mp (he i)
  have hesq : e i ^ 2 ≤ eta i ^ 2 := by
    nlinarith [sq_nonneg (eta i - e i), sq_nonneg (eta i + e i)]
  have hsnonneg : 0 ≤ s i ^ 2 := sq_nonneg (s i)
  have hscaled : s i ^ 2 * e i ^ 2 ≤ s i ^ 2 * eta i ^ 2 :=
    mul_le_mul_of_nonneg_left hesq hsnonneg
  exact (div_le_div_iff_of_pos_right (hd i)).2 hscaled

/-- Coordinatewise square budgets imply a global relative dual budget without
square roots.  The hypotheses are intentionally stated in force coordinates. -/
theorem local_relative_to_weightedDual
    (d r kappa : Vec6) (A : ℝ)
    (hd : ∀ i, 0 < d i)
    (hr : ∀ i, r i ^ 2 ≤ kappa i * d i * A) :
    weightedDual d r ≤ (∑ i, kappa i) * A := by
  unfold weightedDual
  calc
    (∑ i, r i ^ 2 / d i) ≤ ∑ i, kappa i * A := by
      apply Finset.sum_le_sum
      intro i hi
      apply (div_le_iff₀ (hd i)).2
      have h := hr i
      nlinarith
    _ = (∑ i, kappa i) * A := by
      rw [Finset.sum_mul]

/-- A nonzero fixed scalar force bias cannot satisfy a homogeneous damping
estimate uniformly near zero velocity.  This is the one-coordinate witness
behind the review's finite-dimensional obstruction. -/
theorem fixed_bias_not_uniformly_relative_scalar
    (d r gamma : ℝ)
    (hd : 0 < d) (hr : r ≠ 0) (hgamma : 0 ≤ gamma) :
    ∃ v : ℝ, gamma * (d * v ^ 2) < |r * v| := by
  let t : ℝ := 1 / (gamma + 1)
  let v : ℝ := t * r / d
  have hgp : 0 < gamma + 1 := by linarith
  have ht : 0 < t := by
    dsimp [t]
    positivity
  have hr2 : 0 < r ^ 2 := sq_pos_of_ne_zero hr
  have hq : 0 < r ^ 2 / d := div_pos hr2 hd
  have hgt : gamma * t < 1 := by
    dsimp [t]
    rw [div_lt_iff₀ hgp]
    nlinarith
  have hvD : d * v ^ 2 = t ^ 2 * (r ^ 2 / d) := by
    dsimp [v]
    field_simp [ne_of_gt hd]
    ring
  have hpraw : r * v = t * (r ^ 2 / d) := by
    dsimp [v]
    field_simp [ne_of_gt hd]
    ring
  have hppos : 0 < r * v := by
    rw [hpraw]
    exact mul_pos ht hq
  have hpabs : |r * v| = t * (r ^ 2 / d) := by
    rw [abs_of_pos hppos, hpraw]
  refine ⟨v, ?_⟩
  rw [hvD, hpabs]
  have hmul := mul_lt_mul_of_pos_right hgt (mul_pos ht hq)
  nlinarith

/-- If a damping coordinate is identically undamped, any nonzero fixed force in
that coordinate defeats every finite damping-only power bound. -/
theorem undamped_direction_obstruction_scalar
    (r C : ℝ) (hr : r ≠ 0) :
    ∃ v : ℝ, C * (0 * v ^ 2) < |r * v| := by
  refine ⟨1, ?_⟩
  simpa using (abs_pos.mpr hr)

#print axioms weightedDual_nonneg
#print axioms box_to_weightedDual
#print axioms box_to_rate_budget
#print axioms diagonal_normalization_dual_identity
#print axioms diagonal_box_to_weightedDual
#print axioms local_relative_to_weightedDual
#print axioms fixed_bias_not_uniformly_relative_scalar
#print axioms undamped_direction_obstruction_scalar

end

end RouteBP5WeightedDualAdapter
