import Mathlib

namespace RouteBP5CenterBiasMixedSmallGain

/-- Minimal source-independent kernel interface for a positive-semidefinite
quadratic energy on a real module.  Concrete metric/source construction is
intentionally outside this sidecar. -/
structure PSDQuadraticModuleKernel (A : Type*) [AddCommGroup A] [Module ℝ A] where
  Q : A → ℝ
  B : A → A → ℝ
  q_nonneg : ∀ x, 0 ≤ Q x
  q_add : ∀ x y, Q (x + y) = Q x + Q y + 2 * B x y
  q_sub : ∀ x y, Q (x - y) = Q x + Q y - 2 * B x y
  q_smul : ∀ a x, Q (a • x) = a ^ 2 * Q x
  b_smul_left : ∀ a x y, B (a • x) y = a * B x y
  b_smul_right : ∀ a x y, B x (a • y) = a * B x y

/-- Exact weighted quadratic identity behind the root-free biased-center split. -/
theorem weighted_quadratic_bias_identity
    {A : Type*} [AddCommGroup A] [Module ℝ A]
    (K : PSDQuadraticModuleKernel A) (x b : A) (r s : ℝ) :
    (r + s) * (s * K.Q x + r * K.Q b) - r * s * K.Q (x + b) =
      K.Q (s • x - r • b) := by
  rw [K.q_sub, K.q_smul, K.q_smul, K.b_smul_left,
    K.b_smul_right, K.q_add]
  ring

/-- Root-free two-block Young inequality.  The algebraic inequality itself does
not require positive weights; positivity is needed only by later monotone
multiplication steps. -/
theorem quadratic_add_weighted
    {A : Type*} [AddCommGroup A] [Module ℝ A]
    (K : PSDQuadraticModuleKernel A) (x b : A) (r s : ℝ) :
    r * s * K.Q (x + b) ≤ (r + s) * (s * K.Q x + r * K.Q b) := by
  have hid := weighted_quadratic_bias_identity K x b r s
  have hnonneg := K.q_nonneg (s • x - r • b)
  nlinarith

/-- Centered comparator plus a bias cap gives the exact cross-multiplied linear
biased-displacement packet. -/
theorem biased_displacement_linear_le
    {A : Type*} [AddCommGroup A] [Module ℝ A]
    (K : PSDQuadraticModuleKernel A) (x b : A)
    (r s m V Bcap : ℝ)
    (hr : 0 ≤ r) (hs : 0 ≤ s) (hm : 0 ≤ m)
    (hx : m * K.Q x ≤ V) (hb : K.Q b ≤ Bcap) :
    r * s * m * K.Q (x + b) ≤
      (r + s) * (s * V + r * m * Bcap) := by
  have hbase := quadratic_add_weighted K x b r s
  have hbaseM := mul_le_mul_of_nonneg_left hbase hm
  have hxS := mul_le_mul_of_nonneg_left hx hs
  have hbRM := mul_le_mul_of_nonneg_left hb (mul_nonneg hr hm)
  have hsum :
      s * (m * K.Q x) + r * m * K.Q b ≤
        s * V + r * m * Bcap := by
    linarith
  have hsumScaled :=
    mul_le_mul_of_nonneg_left hsum (add_nonneg hr hs)
  calc
    r * s * m * K.Q (x + b) = m * (r * s * K.Q (x + b)) := by ring
    _ ≤ m * ((r + s) * (s * K.Q x + r * K.Q b)) := hbaseM
    _ = (r + s) * (s * (m * K.Q x) + r * m * K.Q b) := by ring
    _ ≤ (r + s) * (s * V + r * m * Bcap) := hsumScaled

/-- On `0 ≤ V ≤ R`, the biased displacement packet squares without roots and
uses only `V^2 ≤ R V`.  This is T-P5-118 equations (1.5)-(1.8). -/
theorem biased_displacement_sq_le
    {A : Type*} [AddCommGroup A] [Module ℝ A]
    (K : PSDQuadraticModuleKernel A) (x b : A)
    (r s m V Bcap R : ℝ)
    (hr : 0 ≤ r) (hs : 0 ≤ s) (hm : 0 ≤ m)
    (hV : 0 ≤ V) (hB : 0 ≤ Bcap)
    (hx : m * K.Q x ≤ V) (hb : K.Q b ≤ Bcap)
    (hVR : V ≤ R) :
    r ^ 2 * s ^ 2 * m ^ 2 * K.Q (x + b) ^ 2 ≤
      (r + s) ^ 2 *
        ((s ^ 2 * R + 2 * r * s * m * Bcap) * V +
          r ^ 2 * m ^ 2 * Bcap ^ 2) := by
  have hlin := biased_displacement_linear_le K x b r s m V Bcap hr hs hm hx hb
  have hL0 : 0 ≤ r * s * m * K.Q (x + b) := by
    positivity
  have hU0 : 0 ≤ (r + s) * (s * V + r * m * Bcap) := by
    positivity
  have hsq :
      (r * s * m * K.Q (x + b)) * (r * s * m * K.Q (x + b)) ≤
        ((r + s) * (s * V + r * m * Bcap)) *
          ((r + s) * (s * V + r * m * Bcap)) :=
    mul_le_mul hlin hlin hL0 hU0
  have hV2 : V * V ≤ R * V :=
    mul_le_mul_of_nonneg_right hVR hV
  have hscaledV2 : s ^ 2 * (V * V) ≤ s ^ 2 * (R * V) :=
    mul_le_mul_of_nonneg_left hV2 (sq_nonneg s)
  have hinside :
      (s * V + r * m * Bcap) ^ 2 ≤
        (s ^ 2 * R + 2 * r * s * m * Bcap) * V +
          r ^ 2 * m ^ 2 * Bcap ^ 2 := by
    nlinarith [hscaledV2]
  have houtside :=
    mul_le_mul_of_nonneg_left hinside (sq_nonneg (r + s))
  calc
    r ^ 2 * s ^ 2 * m ^ 2 * K.Q (x + b) ^ 2 =
        (r * s * m * K.Q (x + b)) * (r * s * m * K.Q (x + b)) := by ring
    _ ≤ ((r + s) * (s * V + r * m * Bcap)) *
        ((r + s) * (s * V + r * m * Bcap)) := hsq
    _ = (r + s) ^ 2 * (s * V + r * m * Bcap) ^ 2 := by ring
    _ ≤ (r + s) ^ 2 *
        ((s ^ 2 * R + 2 * r * s * m * Bcap) * V +
          r ^ 2 * m ^ 2 * Bcap ^ 2) := houtside

/-- The cross-multiplied relative/additive gates absorb a mixed power-square
packet without dividing by the positive common scale `D`. -/
theorem mixed_power_square_bound
    (D H A C V Qd pA alpha beta theta : ℝ)
    (hD : 0 < D) (hV : 0 ≤ V) (hQd : 0 ≤ Qd)
    (hpower : 4 * D * pA ^ 2 ≤ H * (A * V + C) * Qd)
    (hrel : H * A ≤ 16 * D * alpha * theta)
    (hadd : H * C ≤ 16 * D * beta * theta) :
    pA ^ 2 ≤ 4 * theta * (alpha * V + beta) * Qd := by
  have hrelV := mul_le_mul_of_nonneg_right hrel hV
  have hsum :
      H * (A * V + C) ≤ 16 * D * theta * (alpha * V + beta) := by
    nlinarith [hrelV, hadd]
  have hsumQ := mul_le_mul_of_nonneg_right hsum hQd
  have hfactored :
      (4 * D) * pA ^ 2 ≤
        (4 * D) * (4 * theta * (alpha * V + beta) * Qd) := by
    calc
      (4 * D) * pA ^ 2 = 4 * D * pA ^ 2 := by ring
      _ ≤ H * (A * V + C) * Qd := hpower
      _ ≤ (16 * D * theta * (alpha * V + beta)) * Qd := hsumQ
      _ = (4 * D) * (4 * theta * (alpha * V + beta) * Qd) := by ring
  have h4D : 0 < 4 * D := by positivity
  exact (mul_le_mul_left h4D).mp hfactored

/-- Square completion converts the absorbed power-square packet into the linear
upper bound needed by the Lyapunov ledger. -/
theorem square_completion_power_absorption
    (V Qd pA alpha beta theta : ℝ)
    (hV : 0 ≤ V) (hQd : 0 ≤ Qd)
    (halpha : 0 ≤ alpha) (hbeta : 0 ≤ beta) (htheta : 0 ≤ theta)
    (hsq : pA ^ 2 ≤ 4 * theta * (alpha * V + beta) * Qd) :
    pA ≤ alpha * V + beta + theta * Qd := by
  let X : ℝ := alpha * V + beta
  let Y : ℝ := theta * Qd
  change pA ≤ X + Y
  have hX : 0 ≤ X := by
    dsimp [X]
    positivity
  have hY : 0 ≤ Y := by
    dsimp [Y]
    positivity
  have hcompletion : 4 * X * Y ≤ (X + Y) ^ 2 := by
    nlinarith [sq_nonneg (X - Y)]
  have hpSq : pA ^ 2 ≤ (X + Y) ^ 2 := by
    calc
      pA ^ 2 ≤ 4 * theta * (alpha * V + beta) * Qd := hsq
      _ = 4 * X * Y := by simp [X, Y]; ring
      _ ≤ (X + Y) ^ 2 := hcompletion
  have hXY : 0 ≤ X + Y := add_nonneg hX hY
  by_contra hnot
  have hgt : X + Y < pA := lt_of_not_ge hnot
  have hminus : 0 < pA - (X + Y) := sub_pos.mpr hgt
  have hplus : 0 < pA + (X + Y) := by linarith
  have hprod : 0 < (pA - (X + Y)) * (pA + (X + Y)) :=
    mul_pos hminus hplus
  have hid :
      (pA - (X + Y)) * (pA + (X + Y)) = pA ^ 2 - (X + Y) ^ 2 := by
    ring
  rw [hid] at hprod
  nlinarith

/-- T-P5-118 mixed biased-anchor power absorption with the uncancelled trusted
coefficient gates.  `D` and `H` are the already formed positive/common and
second-jet coefficients, so the checker never divides by them. -/
theorem biased_anchor_power_absorption
    (D H A C V Qd pA alpha beta theta : ℝ)
    (hD : 0 < D) (hV : 0 ≤ V) (hQd : 0 ≤ Qd)
    (halpha : 0 ≤ alpha) (hbeta : 0 ≤ beta) (htheta : 0 ≤ theta)
    (hpower : 4 * D * pA ^ 2 ≤ H * (A * V + C) * Qd)
    (hrel : H * A ≤ 16 * D * alpha * theta)
    (hadd : H * C ≤ 16 * D * beta * theta) :
    pA ≤ alpha * V + beta + theta * Qd := by
  have hsq :=
    mixed_power_square_bound D H A C V Qd pA alpha beta theta
      hD hV hQd hpower hrel hadd
  exact square_completion_power_absorption
    V Qd pA alpha beta theta hV hQd halpha hbeta htheta hsq

/-- Substitution of the mixed power bound into the nominal Lyapunov ledger. -/
theorem biased_anchor_mixed_small_gain
    (Vdot c V Qd pA alpha beta theta : ℝ)
    (hledger : Vdot ≤ -c * V - Qd + pA)
    (hpA : pA ≤ alpha * V + beta + theta * Qd) :
    Vdot ≤ -(c - alpha) * V - (1 - theta) * Qd + beta := by
  linarith

/-- Strict requested rate/dissipation charges leave strict retained reserves. -/
theorem mixed_small_gain_strict_reserves
    (c alpha theta : ℝ) (halpha : alpha < c) (htheta : theta < 1) :
    0 < c - alpha ∧ 0 < 1 - theta := by
  constructor <;> linarith

/-- Division-free ultimate-radius boundary gate.  It needs only the already
formed mixed-small-gain ledger and the rational comparison `beta ≤ (c-alpha)R0`. -/
theorem mixed_small_gain_boundary_inward
    (Vdot c alpha beta theta Qd V R0 : ℝ)
    (hsg : Vdot ≤ -(c - alpha) * V - (1 - theta) * Qd + beta)
    (hV : V = R0)
    (hbeta : beta ≤ (c - alpha) * R0)
    (htheta : theta ≤ 1) (hQd : 0 ≤ Qd) :
    Vdot ≤ 0 := by
  rw [hV] at hsg
  have hdiss : 0 ≤ (1 - theta) * Qd :=
    mul_nonneg (sub_nonneg.mpr htheta) hQd
  linarith

/-- Exact scalar obstruction from T-P5-118: the saturated nonzero-bias power
packet and nominal ledger can permit an outward derivative at zero storage, so
no positive zero-floor dissipation reserve follows from those premises alone. -/
theorem nonzero_bias_zero_floor_counterexample :
    ∃ V Qd Qdelta pA Vdot : ℝ,
      V = 0 ∧ Qd = 1 ∧ Qdelta = 4 ∧ pA = 2 ∧ Vdot = 1 ∧
      4 * pA ^ 2 = Qdelta ^ 2 * Qd ∧
      Vdot ≤ -Qd + pA ∧
      ∀ dKeep : ℝ, 0 < dKeep → ¬ Vdot ≤ -dKeep * Qd := by
  refine ⟨0, 1, 4, 2, 1, rfl, rfl, rfl, rfl, rfl, ?_, ?_, ?_⟩
  · norm_num
  · norm_num
  · intro dKeep hd hcontr
    norm_num at hcontr
    nlinarith

#print axioms weighted_quadratic_bias_identity
#print axioms quadratic_add_weighted
#print axioms biased_displacement_linear_le
#print axioms biased_displacement_sq_le
#print axioms mixed_power_square_bound
#print axioms square_completion_power_absorption
#print axioms biased_anchor_power_absorption
#print axioms biased_anchor_mixed_small_gain
#print axioms mixed_small_gain_strict_reserves
#print axioms mixed_small_gain_boundary_inward
#print axioms nonzero_bias_zero_floor_counterexample

end RouteBP5CenterBiasMixedSmallGain
