import NEW_P4_032_RelativeAdditive

/-!
UNCOMPILED, source-independent absorption proof attempt.
Consumes the existing relative/additive theorem and typed defect branches.
No Cauchy, parameter regrouping, Schur identity, sqrt, or concrete source.
The scalar Schur/PMI comparison and feedback closure are explicit premises.
-/

set_option autoImplicit false

namespace RouteBP4032SchurPMIAbsorption

open RouteBP4032BlockDefects
open RouteBP4032DefectNormBudget
open RouteBP4032WeightedThreeTerm
open RouteBP4032RelativeAdditive

noncomputable section

/-- A positive, division-free slack for the normalized unit-coefficient
channel. Merely rhoEff <= 1 is insufficient. -/
structure Slack (p : Parameters) (delta : ℝ) : Prop where
  positive : 0 < delta
  allocation : rhoEff p + delta ≤ 1

theorem strict_iff_positive_slack (p : Parameters) :
    rhoEff p < 1 ↔ ∃ delta : ℝ, Slack p delta := by
  constructor
  · intro h
    exact ⟨1 - rhoEff p, ⟨by linarith, by linarith⟩⟩
  · rintro ⟨delta, h⟩
    have hp := h.positive
    have ha := h.allocation
    linarith

def exactSlack (p : Parameters) (h : rhoEff p < 1) :
    Slack p (1 - rhoEff p) :=
  ⟨by linarith, by linarith⟩

/-- Evidence at the SAME energy/residual point; q is a nonnegative squared
residual budget. The coercive inequality retains the additive debit. -/
structure AbsorbedAt (p : Parameters) (energy q delta : ℝ) : Prop where
  slack : Slack p delta
  energy_nonnegative : 0 ≤ energy
  residual_nonnegative : 0 ≤ q
  relative : q ≤ rhoEff p * energy + biasEff p
  coercive : delta * energy - biasEff p ≤ energy - q

theorem absorb_relative_additive (p : Parameters) (energy q delta : ℝ)
    (hs : Slack p delta) (hE : 0 ≤ energy) (hq : 0 ≤ q)
    (hrel : q ≤ rhoEff p * energy + biasEff p) :
    AbsorbedAt p energy q delta := by
  refine ⟨hs, hE, hq, hrel, ?_⟩
  have hscaled := mul_le_mul_of_nonneg_right hs.allocation hE
  nlinarith

/-- Supplied normalized Schur/PMI lower comparison. All cross terms and
metric/normalization changes must already be justified in this premise.
No matrix positivity or Schur-complement identity is inferred here. -/
structure SchurPMIBinding (energy q margin : ℝ) : Prop where
  lower : energy - q ≤ margin

theorem schur_pmi_margin (p : Parameters) (energy q delta margin : ℝ)
    (budget : AbsorbedAt p energy q delta)
    (binding : SchurPMIBinding energy q margin) :
    delta * energy - biasEff p ≤ margin :=
  budget.coercive.trans binding.lower

/-- Positive slack does not alone remove B_eff. This extra allocation is
sufficient for a nonnegative scalar Schur/PMI margin. -/
theorem schur_pmi_nonnegative (p : Parameters) (energy q delta margin : ℝ)
    (budget : AbsorbedAt p energy q delta)
    (binding : SchurPMIBinding energy q margin)
    (hBias : biasEff p ≤ delta * energy) : 0 ≤ margin := by
  have h := schur_pmi_margin p energy q delta margin budget binding
  linarith

/-- Additional feedback closure needed to bound energy itself. It is NOT
implied by a residual upper bound or by the Schur/PMI lower comparison. -/
structure FeedbackBinding (energy q base : ℝ) : Prop where
  base_nonnegative : 0 ≤ base
  upper : energy ≤ base + q

/-- Division-free and quotient forms, with the same positive slack. -/
structure ClosedBudget (p : Parameters) (energy q base delta : ℝ) : Prop where
  slack_positive : 0 < delta
  energy_scaled : delta * energy ≤ base + biasEff p
  residual_scaled : delta * q ≤ rhoEff p * base + biasEff p
  energy_affine : energy ≤ base / delta + biasEff p / delta
  residual_affine : q ≤ (rhoEff p / delta) * base + biasEff p / delta

theorem close_affine_budget (p : Parameters) (energy q base delta : ℝ)
    (budget : AbsorbedAt p energy q delta)
    (binding : FeedbackBinding energy q base) :
    ClosedBudget p energy q base delta := by
  have hcoeff := effective_coefficients_nonnegative p
  have henergy : delta * energy ≤ base + biasEff p := by
    have hgap := budget.coercive
    have hclosure := binding.upper
    linarith
  have hresidual : delta * q ≤ rhoEff p * base + biasEff p := by
    have hr := mul_le_mul_of_nonneg_left budget.relative budget.slack.positive.le
    have he := mul_le_mul_of_nonneg_left henergy hcoeff.1
    have hb := mul_le_mul_of_nonneg_right budget.slack.allocation hcoeff.2
    nlinarith
  refine ⟨budget.slack.positive, henergy, hresidual, ?_, ?_⟩
  · have hdiv : energy ≤ (base + biasEff p) / delta :=
      (le_div_iff₀ budget.slack.positive).2 (by nlinarith [henergy])
    simpa only [add_div] using hdiv
  · have hdiv : q ≤ (rhoEff p * base + biasEff p) / delta :=
      (le_div_iff₀ budget.slack.positive).2 (by nlinarith [hresidual])
    calc
      q ≤ (rhoEff p * base + biasEff p) / delta := hdiv
      _ = (rhoEff p / delta) * base + biasEff p / delta := by ring

/-- Direct exact-slack bridge from the already supplied relative budget. -/
theorem close_of_strict (p : Parameters) (energy q base : ℝ)
    (hstrict : rhoEff p < 1) (hE : 0 ≤ energy) (hq : 0 ≤ q)
    (hrel : q ≤ rhoEff p * energy + biasEff p)
    (binding : FeedbackBinding energy q base) :
    ClosedBudget p energy q base (1 - rhoEff p) :=
  close_affine_budget p energy q base (1 - rhoEff p)
    (absorb_relative_additive p energy q (1 - rhoEff p)
      (exactSlack p hstrict) hE hq hrel) binding

/-- Division-free allocation to a supplied final residual allowance. -/
theorem residual_allocation (p : Parameters) (energy q base delta available : ℝ)
    (budget : ClosedBudget p energy q base delta)
    (hAvailable : 0 ≤ available)
    (hAllocation : rhoEff p * base + biasEff p ≤ delta * available) :
    q ≤ available := by
  exact (mul_le_mul_left budget.slack_positive).mp
    (budget.residual_scaled.trans hAllocation)

/-- Force branch: distal operator is MBD*J, and q is the squared Euclidean
norm of the typed generalized force. Feed the result to either consumer. -/
theorem force_absorption (p : Parameters) (R : BB) (MBD : BD) (J : DD)
    (aB : BlockAcceleration) (rB : PortGeneralizedForce)
    (eD : DistalForceDefect) (eB : LocalPortDefect) (energy ED EB delta : ℝ)
    (env : EnvelopesAt p energy ED EB) (hs : Slack p delta)
    (identity : rB.value = R *ᵥ aB.value + forceTerm MBD J eD + eB.value)
    (hPort : (norm2 (R *ᵥ aB.value))^2 ≤ p.rhoA * energy)
    (hT : ActionBound (MBD * J) p.tau)
    (hD : (norm2 eD.value)^2 ≤ ED) (hB : (norm2 eB.value)^2 ≤ EB) :
    AbsorbedAt p energy ((norm2 rB.value)^2) delta :=
  absorb_relative_additive p energy ((norm2 rB.value)^2) delta hs
    env.energy_nonnegative (sq_nonneg _)
    (force_relative_additive p R MBD J aB rB eD eB energy ED EB
      env identity hPort hT hD hB)

/-- Acceleration branch: distal operator is MBD alone. No implicit defect
convention conversion or insertion of an additional J. -/
theorem accel_absorption (p : Parameters) (R : BB) (MBD : BD)
    (aB : BlockAcceleration) (rB : PortGeneralizedForce)
    (eD : DistalAccelDefect) (eB : LocalPortDefect) (energy ED EB delta : ℝ)
    (env : EnvelopesAt p energy ED EB) (hs : Slack p delta)
    (identity : rB.value = R *ᵥ aB.value + accelTerm MBD eD + eB.value)
    (hPort : (norm2 (R *ᵥ aB.value))^2 ≤ p.rhoA * energy)
    (hT : ActionBound MBD p.tau)
    (hD : (norm2 eD.value)^2 ≤ ED) (hB : (norm2 eB.value)^2 ≤ EB) :
    AbsorbedAt p energy ((norm2 rB.value)^2) delta :=
  absorb_relative_additive p energy ((norm2 rB.value)^2) delta hs
    env.energy_nonnegative (sq_nonneg _)
    (accel_relative_additive p R MBD aB rB eD eB energy ED EB
      env identity hPort hT hD hB)

end

-- Future audit commands only; NOT executed in this round.
#print axioms strict_iff_positive_slack
#print axioms absorb_relative_additive
#print axioms schur_pmi_margin
#print axioms schur_pmi_nonnegative
#print axioms close_affine_budget
#print axioms close_of_strict
#print axioms residual_allocation
#print axioms force_absorption
#print axioms accel_absorption

end RouteBP4032SchurPMIAbsorption
