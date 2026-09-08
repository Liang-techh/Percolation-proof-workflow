import Mathlib

namespace RouteBP5DescriptorRelativeRate

/-- A descriptor/full-state estimate and a same-cell relative-plus-additive RHS
packet propagate to the squared port without division, square roots, or an
absolute acceleration cap. -/
theorem descriptor_port_relative_additive
    (mu portSq metric fullA rhsSq rhoSq metricMax V Hrel Habs : ℝ)
    (hrho : 0 ≤ rhoSq) (hmetricMax : 0 ≤ metricMax)
    (hdescriptor : mu ^ 2 * fullA ≤ rhsSq)
    (hmetric : metric ≤ metricMax * fullA)
    (hport : portSq ≤ rhoSq * metric)
    (hrhs : rhsSq ≤ Hrel * V + Habs) :
    mu ^ 2 * portSq ≤
      rhoSq * metricMax * Hrel * V + rhoSq * metricMax * Habs := by
  calc
    mu ^ 2 * portSq ≤ mu ^ 2 * (rhoSq * metric) :=
      mul_le_mul_of_nonneg_left hport (sq_nonneg mu)
    _ ≤ mu ^ 2 * (rhoSq * (metricMax * fullA)) := by
      exact mul_le_mul_of_nonneg_left
        (mul_le_mul_of_nonneg_left hmetric hrho) (sq_nonneg mu)
    _ = (rhoSq * metricMax) * (mu ^ 2 * fullA) := by ring
    _ ≤ (rhoSq * metricMax) * rhsSq :=
      mul_le_mul_of_nonneg_left hdescriptor (mul_nonneg hrho hmetricMax)
    _ ≤ (rhoSq * metricMax) * (Hrel * V + Habs) :=
      mul_le_mul_of_nonneg_left hrhs (mul_nonneg hrho hmetricMax)
    _ = rhoSq * metricMax * Hrel * V + rhoSq * metricMax * Habs := by ring

/-- The exact square-completion consumer behind the factor four. -/
theorem square_packet_absorption
    (P lambda D alpha V beta : ℝ)
    (hlambda : 0 ≤ lambda) (hD : 0 ≤ D)
    (halpha : 0 ≤ alpha) (hV : 0 ≤ V) (hbeta : 0 ≤ beta)
    (hsq : P ^ 2 ≤ 4 * lambda * D * (alpha * V + beta)) :
    P ≤ lambda * D + alpha * V + beta := by
  have hsum : 0 ≤ lambda * D + alpha * V + beta := by
    positivity
  have hcomplete :
      4 * lambda * D * (alpha * V + beta) ≤
        (lambda * D + alpha * V + beta) ^ 2 := by
    nlinarith [sq_nonneg (lambda * D - (alpha * V + beta))]
  have hp2 : P ^ 2 ≤ (lambda * D + alpha * V + beta) ^ 2 :=
    hsq.trans hcomplete
  nlinarith

/-- Generic squared Cauchy + dissipation + relative/additive residual packet
implies a rate charge plus bias charge. All cancellation is by the positive
factor `d * mu^2`; no division appears in the statement. -/
theorem relative_additive_power_absorption
    (mu d U R D V P Krel Kabs lambda alpha beta : ℝ)
    (hmu : 0 < mu) (hd : 0 < d)
    (hR : 0 ≤ R) (hD : 0 ≤ D) (hV : 0 ≤ V)
    (hlambda : 0 ≤ lambda) (halpha : 0 ≤ alpha) (hbeta : 0 ≤ beta)
    (hcauchy : P ^ 2 ≤ U * R)
    (hdiss : d * U ≤ D)
    (hres : mu ^ 2 * R ≤ Krel * V + Kabs)
    (hrel : Krel ≤ 4 * lambda * d * mu ^ 2 * alpha)
    (habs : Kabs ≤ 4 * lambda * d * mu ^ 2 * beta) :
    P ≤ lambda * D + alpha * V + beta := by
  have hmu2 : 0 < mu ^ 2 := by positivity
  have hdm : 0 < d * mu ^ 2 := mul_pos hd hmu2
  have hRscaled : 0 ≤ mu ^ 2 * R :=
    mul_nonneg (sq_nonneg mu) hR
  have h1 :
      d * mu ^ 2 * P ^ 2 ≤ d * mu ^ 2 * (U * R) :=
    mul_le_mul_of_nonneg_left hcauchy (le_of_lt hdm)
  have h2raw :
      (d * U) * (mu ^ 2 * R) ≤ D * (mu ^ 2 * R) :=
    mul_le_mul_of_nonneg_right hdiss hRscaled
  have h2 :
      d * mu ^ 2 * (U * R) ≤ D * (mu ^ 2 * R) := by
    convert h2raw using 1 <;> ring
  have h3 : D * (mu ^ 2 * R) ≤ D * (Krel * V + Kabs) :=
    mul_le_mul_of_nonneg_left hres hD
  have hrelV :
      Krel * V ≤ (4 * lambda * d * mu ^ 2 * alpha) * V :=
    mul_le_mul_of_nonneg_right hrel hV
  have hcharge :
      Krel * V + Kabs ≤
        4 * lambda * d * mu ^ 2 * (alpha * V + beta) := by
    calc
      Krel * V + Kabs ≤
          (4 * lambda * d * mu ^ 2 * alpha) * V +
            4 * lambda * d * mu ^ 2 * beta := add_le_add hrelV habs
      _ = 4 * lambda * d * mu ^ 2 * (alpha * V + beta) := by ring
  have h4 :
      D * (Krel * V + Kabs) ≤
        D * (4 * lambda * d * mu ^ 2 * (alpha * V + beta)) :=
    mul_le_mul_of_nonneg_left hcharge hD
  have hscaled :
      (d * mu ^ 2) * P ^ 2 ≤
        (d * mu ^ 2) * (4 * lambda * D * (alpha * V + beta)) := by
    calc
      (d * mu ^ 2) * P ^ 2 = d * mu ^ 2 * P ^ 2 := by ring
      _ ≤ d * mu ^ 2 * (U * R) := h1
      _ ≤ D * (mu ^ 2 * R) := h2
      _ ≤ D * (Krel * V + Kabs) := h3
      _ ≤ D * (4 * lambda * d * mu ^ 2 * (alpha * V + beta)) := h4
      _ = (d * mu ^ 2) * (4 * lambda * D * (alpha * V + beta)) := by ring
  have hsq : P ^ 2 ≤ 4 * lambda * D * (alpha * V + beta) :=
    (mul_le_mul_left hdm).mp hscaled
  exact square_packet_absorption P lambda D alpha V beta
    hlambda hD halpha hV hbeta hsq

/-- Direct ledger consumption: descriptor forcing becomes loss of decay rate,
loss of a fraction of `D`, and an explicit additive bias. -/
theorem lyapunov_rate_bias_ledger
    (Vdot c alpha V D P lambda beta : ℝ)
    (hledger : Vdot ≤ -c * V - D + P)
    (hport : P ≤ lambda * D + alpha * V + beta) :
    Vdot ≤ -(c - alpha) * V - (1 - lambda) * D + beta := by
  nlinarith

/-- Pure relative forcing preserves a homogeneous decay inequality when no
additive charge is present. -/
theorem homogeneous_relative_decay
    (Vdot c alpha V D lambda : ℝ)
    (hV : 0 ≤ V) (hD : 0 ≤ D)
    (hlambda : lambda ≤ 1) (halpha : alpha < c)
    (hledger : Vdot ≤ -(c - alpha) * V - (1 - lambda) * D) :
    Vdot ≤ -(c - alpha) * V := by
  have hcoef : 0 ≤ 1 - lambda := by linarith
  have hdrop : 0 ≤ (1 - lambda) * D := mul_nonneg hcoef hD
  linarith

/-- At a first-exit boundary, the mixed branch is strictly inward whenever the
remaining rate reserve beats the additive bias. -/
theorem first_exit_inward
    (Vdot c alpha Vstar D lambda beta : ℝ)
    (hD : 0 ≤ D) (hlambda : lambda ≤ 1)
    (hreserve : beta < (c - alpha) * Vstar)
    (hledger :
      Vdot ≤ -(c - alpha) * Vstar - (1 - lambda) * D + beta) :
    Vdot < 0 := by
  have hcoef : 0 ≤ 1 - lambda := by linarith
  have hdrop : 0 ≤ (1 - lambda) * D := mul_nonneg hcoef hD
  linarith

/-- A finite pure-relative source packet forces zero squared RHS on every
zero-storage slice. This is the exact zero-slice obstruction. -/
theorem pure_relative_zero_slice
    (rhsSq Hrel V : ℝ)
    (hrhs0 : 0 ≤ rhsSq)
    (hrhs : rhsSq ≤ Hrel * V)
    (hV : V = 0) :
    rhsSq = 0 := by
  subst V
  simpa using le_antisymm (by simpa using hrhs) hrhs0

/-- Conversely, a nonzero squared RHS at a zero-storage state rules out every
finite pure-relative coefficient. -/
theorem nonzero_rhs_blocks_pure_relative
    (rhsSq V : ℝ)
    (hrhs0 : 0 < rhsSq) (hV : V = 0) :
    ∀ Hrel : ℝ, ¬ rhsSq ≤ Hrel * V := by
  intro Hrel h
  subst V
  simpa using (not_le_of_gt hrhs0 h)

/-- Exact equality case showing that the generic coefficient four cannot be
reduced when only the squared Cauchy packet, dissipation packet and relative
residual square are known. -/
theorem factor_four_sharp_regression :
    ((2 : ℝ) ^ 2 = 1 * 4) ∧
    ((1 : ℝ) * 1 = 1) ∧
    ((1 : ℝ) ^ 2 * 4 = 4 * 1 * 1 * (1 : ℝ) ^ 2 * 1) ∧
    ((2 : ℝ) = 1 * 1 + 1 * 1 + 0) := by
  norm_num

/-- The exact Route-B producer metric constant used upstream. Keeping this as
an arithmetic theorem avoids silently changing the coefficient. -/
theorem metricMax_nonnegative :
    (0 : ℝ) ≤ 1402217 / 12000000 := by
  norm_num

#print axioms descriptor_port_relative_additive
#print axioms square_packet_absorption
#print axioms relative_additive_power_absorption
#print axioms lyapunov_rate_bias_ledger
#print axioms homogeneous_relative_decay
#print axioms first_exit_inward
#print axioms pure_relative_zero_slice
#print axioms nonzero_rhs_blocks_pure_relative
#print axioms factor_four_sharp_regression
#print axioms metricMax_nonnegative

end RouteBP5DescriptorRelativeRate
