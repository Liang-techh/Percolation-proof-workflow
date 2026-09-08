import Mathlib

noncomputable section

namespace RouteBP5QuadraticFormParity

/-- Two-channel symmetric quadratic form with cross coefficient `c`. -/
def qform2 (a b c x y : ℝ) : ℝ :=
  a * x ^ 2 + 2 * c * x * y + b * y ^ 2

/-- Structural gate for a balanced even/odd pair: the opposite-parity cross coefficient vanishes. -/
def OppositeParityGate (c : ℝ) : Prop :=
  c = 0

/-- A common sign disappears from a same-parity balanced product. -/
theorem balanced_pair_same_parity_cancel
    (sigma x y : ℝ)
    (hsigma : sigma ^ 2 = 1) :
    (sigma * x) * (sigma * y) = x * y := by
  calc
    (sigma * x) * (sigma * y) = sigma ^ 2 * (x * y) := by ring
    _ = x * y := by rw [hsigma]; ring

/-- Flipping exactly one balanced parity flips the mixed product. -/
theorem balanced_pair_opposite_parity_flip
    (x y : ℝ) :
    (-x) * y = -(x * y) := by
  ring

/-- Any pair carrying at least one positive excess power vanishes at the common zero. -/
theorem positive_excess_pair_vanishes_at_zero
    (k : ℕ)
    (z : ℝ) :
    (0 : ℝ) ^ (k + 1) * z = 0 := by
  simp

/-- Exact jump formula for an opposite-parity balanced two-channel quadratic form. -/
theorem opposite_parity_quadratic_jump
    (a b c x y : ℝ) :
    qform2 a b c x y - qform2 a b c x (-y) = 4 * c * x * y := by
  dsimp [qform2]
  ring

/-- The structural cross-zero gate is sufficient for opposite-parity invariance. -/
theorem opposite_parity_cross_zero_invariant
    (a b c x y : ℝ)
    (hgate : OppositeParityGate c) :
    qform2 a b c x y = qform2 a b c x (-y) := by
  rw [show c = 0 from hgate]
  dsimp [qform2]
  ring

/-- For a fixed contact vector, invariance is exactly the scalar cancellation `c*x*y = 0`. -/
theorem particular_contact_invariance_iff
    (a b c x y : ℝ) :
    qform2 a b c x y = qform2 a b c x (-y) ↔ c * x * y = 0 := by
  constructor
  · intro h
    have hjump := opposite_parity_quadratic_jump a b c x y
    nlinarith
  · intro hxy
    have hjump := opposite_parity_quadratic_jump a b c x y
    nlinarith

/-- Universal opposite-parity invariance is equivalent to the structural block gate. -/
theorem opposite_parity_gate_iff_universal_invariant
    (a b c : ℝ) :
    OppositeParityGate c ↔
      ∀ x y : ℝ, qform2 a b c x y = qform2 a b c x (-y) := by
  constructor
  · intro hgate x y
    exact opposite_parity_cross_zero_invariant a b c x y hgate
  · intro hall
    have h11 := hall 1 1
    dsimp [OppositeParityGate]
    dsimp [qform2] at h11
    nlinarith

/-- Flipping both balanced odd channels leaves every symmetric quadratic form unchanged. -/
theorem all_odd_quadratic_invariant
    (a b c x y : ℝ) :
    qform2 a b c (-x) (-y) = qform2 a b c x y := by
  dsimp [qform2]
  ring

/-- Diagonal square information is insensitive to independent sign flips. -/
theorem diagonal_squares_ignore_sign
    (x y : ℝ) :
    (-x) ^ 2 = x ^ 2 ∧ (-y) ^ 2 = y ^ 2 := by
  constructor <;> ring

/-- The rational matrix used in the sharp counterexample is uniformly coercive. -/
theorem counterexample_matrix_coercive
    (x y : ℝ) :
    (1 / 2 : ℝ) * (x ^ 2 + y ^ 2) ≤ qform2 1 1 (1 / 2) x y := by
  have hs : 0 ≤ (x + y) ^ 2 := sq_nonneg (x + y)
  dsimp [qform2]
  nlinarith

/-- Exact one-sided values for the positive-definite mixed-energy counterexample. -/
theorem quadratic_form_parity_counterexample :
    qform2 1 1 (1 / 2) 1 1 = 3 ∧
      qform2 1 1 (1 / 2) 1 (-1) = 1 := by
  norm_num [qform2]

/-- Both diagonal squares pass while the mixed quadratic form still changes across the sign flip. -/
theorem square_only_pass_does_not_imply_mixed_invariance :
    ((-1 : ℝ) ^ 2 = 1) ∧
      ((1 : ℝ) ^ 2 = 1) ∧
      qform2 1 1 (1 / 2) 1 1 ≠ qform2 1 1 (1 / 2) 1 (-1) := by
  norm_num [qform2]

/-- A single accidental contact cancellation is weaker than the structural gate. -/
theorem accidental_contact_cancellation_not_structural :
    qform2 1 1 1 0 1 = qform2 1 1 1 0 (-1) ∧
      ¬ OppositeParityGate (1 : ℝ) := by
  norm_num [qform2, OppositeParityGate]

/--
Typed consumer seam: a mixed quadratic consumer must receive the explicit
opposite-parity structural gate; diagonal square facts alone are not accepted.
-/
theorem mixed_quadratic_consumer_of_parity_gate
    (P : Prop)
    (a b c x y : ℝ)
    (hgate : OppositeParityGate c)
    (hconsumer : qform2 a b c x y = qform2 a b c x (-y) → P) :
    P := by
  exact hconsumer (opposite_parity_cross_zero_invariant a b c x y hgate)

#print axioms balanced_pair_same_parity_cancel
#print axioms balanced_pair_opposite_parity_flip
#print axioms positive_excess_pair_vanishes_at_zero
#print axioms opposite_parity_quadratic_jump
#print axioms opposite_parity_cross_zero_invariant
#print axioms particular_contact_invariance_iff
#print axioms opposite_parity_gate_iff_universal_invariant
#print axioms all_odd_quadratic_invariant
#print axioms diagonal_squares_ignore_sign
#print axioms counterexample_matrix_coercive
#print axioms quadratic_form_parity_counterexample
#print axioms square_only_pass_does_not_imply_mixed_invariance
#print axioms accidental_contact_cancellation_not_structural
#print axioms mixed_quadratic_consumer_of_parity_gate

end RouteBP5QuadraticFormParity
