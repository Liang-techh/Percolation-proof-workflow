import NEW_P4_032_WeightedThreeTerm

/-!
UNCOMPILED source-independent relative-plus-additive budget skeleton.
No Lean/Lake run, sqrt, concrete parameters, source/coverage/admission claim.
Consumes the existing weighted theorem; does not repeat Cauchy or a defect
convention adapter. All parameters below belong to one compatible budget.
-/

set_option autoImplicit false

namespace RouteBP4032RelativeAdditive

open RouteBP4032BlockDefects
open RouteBP4032DefectNormBudget
open RouteBP4032WeightedThreeTerm

noncomputable section

/-- Fixed parameter packet for one certified cell/metric/normalization.
Weights retain strict positivity and their reciprocal-sum admissibility proof. -/
structure Parameters where
  weights : Weights
  rhoA : ℝ
  tau : ℝ
  kappaD : ℝ
  kappaB : ℝ
  biasD : ℝ
  biasB : ℝ
  rhoA_nonnegative : 0 ≤ rhoA
  tau_nonnegative : 0 ≤ tau
  kappaD_nonnegative : 0 ≤ kappaD
  kappaB_nonnegative : 0 ≤ kappaB
  biasD_nonnegative : 0 ≤ biasD
  biasB_nonnegative : 0 ≤ biasB

/-- Same-point squared defect budgets. ED/EB are squared quantities, not
norm caps, and energy is the SAME scalar used by the port-energy bound. -/
structure EnvelopesAt (p : Parameters) (energy ED EB : ℝ) : Prop where
  energy_nonnegative : 0 ≤ energy
  ED_nonnegative : 0 ≤ ED
  EB_nonnegative : 0 ≤ EB
  distal : ED ≤ p.kappaD * energy + p.biasD
  local_port : EB ≤ p.kappaB * energy + p.biasB

def weightedBudget (p : Parameters) (energy ED EB : ℝ) : ℝ :=
  p.weights.value 0 * (p.rhoA * energy) +
    p.weights.value 1 * (p.tau^2 * ED) + p.weights.value 2 * EB

def rhoEff (p : Parameters) : ℝ :=
  p.weights.value 0 * p.rhoA + p.weights.value 1 * p.tau^2 * p.kappaD +
    p.weights.value 2 * p.kappaB

def biasEff (p : Parameters) : ℝ :=
  p.weights.value 1 * p.tau^2 * p.biasD + p.weights.value 2 * p.biasB

theorem effective_coefficients_nonnegative (p : Parameters) :
    0 ≤ rhoEff p ∧ 0 ≤ biasEff p := by
  constructor
  · exact add_nonneg
      (add_nonneg (mul_nonneg (p.weights.positive 0).le p.rhoA_nonnegative)
        (mul_nonneg (mul_nonneg (p.weights.positive 1).le (sq_nonneg p.tau)) p.kappaD_nonnegative))
      (mul_nonneg (p.weights.positive 2).le p.kappaB_nonnegative)
  · exact add_nonneg
      (mul_nonneg (mul_nonneg (p.weights.positive 1).le (sq_nonneg p.tau)) p.biasD_nonnegative)
      (mul_nonneg (p.weights.positive 2).le p.biasB_nonnegative)

/-- Pure parameter regrouping; tau is squared exactly once. -/
theorem affine_budget_identity (p : Parameters) (energy : ℝ) :
    weightedBudget p energy (p.kappaD * energy + p.biasD)
      (p.kappaB * energy + p.biasB) = rhoEff p * energy + biasEff p := by
  unfold weightedBudget rhoEff biasEff
  ring

theorem weighted_budget_le_relative_additive (p : Parameters) (energy ED EB : ℝ)
    (env : EnvelopesAt p energy ED EB) :
    weightedBudget p energy ED EB ≤ rhoEff p * energy + biasEff p := by
  have hd : p.weights.value 1 * (p.tau^2 * ED) ≤
      p.weights.value 1 * (p.tau^2 * (p.kappaD * energy + p.biasD)) :=
    mul_le_mul_of_nonneg_left (mul_le_mul_of_nonneg_left env.distal (sq_nonneg p.tau))
      (p.weights.positive 1).le
  have hb : p.weights.value 2 * EB ≤
      p.weights.value 2 * (p.kappaB * energy + p.biasB) :=
    mul_le_mul_of_nonneg_left env.local_port (p.weights.positive 2).le
  calc
    weightedBudget p energy ED EB ≤
        weightedBudget p energy (p.kappaD * energy + p.biasD)
          (p.kappaB * energy + p.biasB) :=
      add_le_add (add_le_add_left hd (p.weights.value 0 * (p.rhoA * energy))) hb
    _ = _ := affine_budget_identity p energy

theorem relative_additive_budget_nonnegative (p : Parameters) (energy ED EB : ℝ)
    (env : EnvelopesAt p energy ED EB) : 0 ≤ rhoEff p * energy + biasEff p := by
  have h := effective_coefficients_nonnegative p
  exact add_nonneg (mul_nonneg h.1 env.energy_nonnegative) h.2

/-- General interface for an already established weighted squared budget. -/
theorem consume_weighted_budget (p : Parameters) (q energy ED EB : ℝ)
    (env : EnvelopesAt p energy ED EB)
    (hWeighted : q ≤ weightedBudget p energy ED EB) :
    q ≤ rhoEff p * energy + biasEff p :=
  hWeighted.trans (weighted_budget_le_relative_additive p energy ED EB env)

/-- Force defect branch: its action certificate concerns MBD*J. -/
theorem force_relative_additive (p : Parameters) (R : BB) (MBD : BD) (J : DD)
    (aB : BlockAcceleration) (rB : PortGeneralizedForce)
    (eD : DistalForceDefect) (eB : LocalPortDefect) (energy ED EB : ℝ)
    (env : EnvelopesAt p energy ED EB)
    (identity : rB.value = R *ᵥ aB.value + forceTerm MBD J eD + eB.value)
    (hPort : (norm2 (R *ᵥ aB.value))^2 ≤ p.rhoA * energy)
    (hT : ActionBound (MBD * J) p.tau)
    (hD : (norm2 eD.value)^2 ≤ ED) (hB : (norm2 eB.value)^2 ≤ EB) :
    (norm2 rB.value)^2 ≤ rhoEff p * energy + biasEff p := by
  apply consume_weighted_budget p ((norm2 rB.value)^2) energy ED EB env
  exact force_defect_budget p.weights R MBD J aB rB eD eB p.rhoA energy p.tau ED EB
    identity hPort hT hD hB

/-- Acceleration defect branch: its action certificate concerns MBD alone. -/
theorem accel_relative_additive (p : Parameters) (R : BB) (MBD : BD)
    (aB : BlockAcceleration) (rB : PortGeneralizedForce)
    (eD : DistalAccelDefect) (eB : LocalPortDefect) (energy ED EB : ℝ)
    (env : EnvelopesAt p energy ED EB)
    (identity : rB.value = R *ᵥ aB.value + accelTerm MBD eD + eB.value)
    (hPort : (norm2 (R *ᵥ aB.value))^2 ≤ p.rhoA * energy)
    (hT : ActionBound MBD p.tau)
    (hD : (norm2 eD.value)^2 ≤ ED) (hB : (norm2 eB.value)^2 ≤ EB) :
    (norm2 rB.value)^2 ≤ rhoEff p * energy + biasEff p := by
  apply consume_weighted_budget p ((norm2 rB.value)^2) energy ED EB env
  exact accel_defect_budget p.weights R MBD aB rB eD eB p.rhoA energy p.tau ED EB
    identity hPort hT hD hB

/-- Removing additive load requires explicit zero-bias identities; it is not
inferred from positive weights, small energy, or a source-independent theorem. -/
theorem zero_bias_corollary (p : Parameters) (q energy : ℝ)
    (hD : p.biasD = 0) (hB : p.biasB = 0)
    (h : q ≤ rhoEff p * energy + biasEff p) : q ≤ rhoEff p * energy := by
  simpa only [biasEff, hD, hB, mul_zero, add_zero] using h

end

-- Future audit commands only; NOT executed in this round.
#print axioms effective_coefficients_nonnegative
#print axioms affine_budget_identity
#print axioms weighted_budget_le_relative_additive
#print axioms consume_weighted_budget
#print axioms force_relative_additive
#print axioms accel_relative_additive
#print axioms zero_bias_corollary

end RouteBP4032RelativeAdditive
