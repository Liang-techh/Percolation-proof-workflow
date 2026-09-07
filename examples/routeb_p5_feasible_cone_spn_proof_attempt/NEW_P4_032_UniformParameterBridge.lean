import NEW_P4_032_SchurPMIAbsorption
import NEW_P4_032_DomainUniformContraction

/-!
UNCOMPILED bounded parameter bridge. Reuses both existing theorem chains.
The total additive field is base + biasEff, never biasEff alone unless
base is actually zero. All evidence is indexed by one ParameterField.
No new scalar contraction, variable division, sqrt, or source binding.
-/

set_option autoImplicit false

namespace RouteBP4032UniformParameterBridge

open RouteBP4032RelativeAdditive
open RouteBP4032SchurPMIAbsorption
open RouteBP4032DomainUniformContraction

noncomputable section

/-- Parameters may vary by point; no uniform bound follows from the type.
ED/EB are the upstream squared defect budgets, not norm caps. -/
structure ParameterField (X : Type*) where
  domain : X → Prop
  params : X → Parameters
  energy : X → ℝ
  residual : X → ℝ
  ED : X → ℝ
  EB : X → ℝ
  base : X → ℝ

/-- Residual and feedback evidence use exactly the same point, parameter
packet, energy and domain. Feedback is an independent required premise. -/
structure LocalEvidence {X : Type*} (f : ParameterField X) : Prop where
  envelopes : ∀ x, f.domain x →
    EnvelopesAt (f.params x) (f.energy x) (f.ED x) (f.EB x)
  residual_nonnegative : ∀ x, f.domain x → 0 ≤ f.residual x
  relative : ∀ x, f.domain x →
    f.residual x ≤ rhoEff (f.params x) * f.energy x + biasEff (f.params x)
  feedback : ∀ x, f.domain x →
    FeedbackBinding (f.energy x) (f.residual x) (f.base x)

/-- Optional entry directly from the prior weighted-budget theorem.
Already proved force/accel relative bounds can instead fill LocalEvidence
without redoing weighted Cauchy or a defect convention conversion. -/
def ofWeighted {X : Type*} (f : ParameterField X)
    (env : ∀ x, f.domain x →
      EnvelopesAt (f.params x) (f.energy x) (f.ED x) (f.EB x))
    (hq : ∀ x, f.domain x → 0 ≤ f.residual x)
    (hw : ∀ x, f.domain x → f.residual x ≤
      weightedBudget (f.params x) (f.energy x) (f.ED x) (f.EB x))
    (hf : ∀ x, f.domain x →
      FeedbackBinding (f.energy x) (f.residual x) (f.base x)) : LocalEvidence f where
  envelopes := env
  residual_nonnegative := hq
  relative := fun x hx => consume_weighted_budget (f.params x) (f.residual x)
    (f.energy x) (f.ED x) (f.EB x) (env x hx) (hw x hx)
  feedback := hf

/-- Explicit effective-coefficient bounds on the entire stated domain.
biasBar bounds the TOTAL base + additive-defect budget. -/
structure UniformParameters {X : Type*} (f : ParameterField X) where
  rhoBar : ℝ
  biasBar : ℝ
  cap : ℝ
  rhoBar_nonnegative : 0 ≤ rhoBar
  rhoBar_strict : rhoBar < 1
  biasBar_nonnegative : 0 ≤ biasBar
  cap_nonnegative : 0 ≤ cap
  relative_bound : ∀ x, f.domain x → rhoEff (f.params x) ≤ rhoBar
  additive_bound : ∀ x, f.domain x → f.base x + biasEff (f.params x) ≤ biasBar
  allocation : biasBar ≤ (1 - rhoBar) * cap

/-- Constructor for separately supplied base and defect-bias uniform caps.
No primitive parameter maximization or rhoEff regrouping is performed. -/
def ofSeparateBiasBounds {X : Type*} (f : ParameterField X)
    (rhoBar baseBar defectBiasBar cap : ℝ)
    (hr0 : 0 ≤ rhoBar) (hr1 : rhoBar < 1)
    (hb0 : 0 ≤ baseBar) (hd0 : 0 ≤ defectBiasBar) (hc0 : 0 ≤ cap)
    (hr : ∀ x, f.domain x → rhoEff (f.params x) ≤ rhoBar)
    (hb : ∀ x, f.domain x → f.base x ≤ baseBar)
    (hd : ∀ x, f.domain x → biasEff (f.params x) ≤ defectBiasBar)
    (ha : baseBar + defectBiasBar ≤ (1 - rhoBar) * cap) : UniformParameters f where
  rhoBar := rhoBar
  biasBar := baseBar + defectBiasBar
  cap := cap
  rhoBar_nonnegative := hr0
  rhoBar_strict := hr1
  biasBar_nonnegative := add_nonneg hb0 hd0
  cap_nonnegative := hc0
  relative_bound := hr
  additive_bound := fun x hx => add_le_add (hb x hx) (hd x hx)
  allocation := ha

/-- Definitional adapter into the existing domain-uniform interface. -/
def toBudgetField {X : Type*} (f : ParameterField X) : BudgetField X where
  domain := f.domain
  energy := f.energy
  bias := fun x => f.base x + biasEff (f.params x)
  rho := fun x => rhoEff (f.params x)

def toUniformBudget {X : Type*} (f : ParameterField X)
    (u : UniformParameters f) : UniformBudget (toBudgetField f) where
  rhoBar := u.rhoBar
  biasBar := u.biasBar
  cap := u.cap
  rhoBar_nonnegative := u.rhoBar_nonnegative
  rhoBar_strict := u.rhoBar_strict
  biasBar_nonnegative := u.biasBar_nonnegative
  cap_nonnegative := u.cap_nonnegative
  rho_bound := u.relative_bound
  bias_bound := u.additive_bound
  allocation := u.allocation

/-- Assemble closure from the supplied residual and feedback inequalities;
strict pointwise coefficients follow from the uniform bound, not conversely. -/
def toPointwiseClosure {X : Type*} (f : ParameterField X)
    (e : LocalEvidence f) (u : UniformParameters f) : PointwiseClosure (toBudgetField f) where
  energy_nonnegative := fun x hx => (e.envelopes x hx).energy_nonnegative
  bias_nonnegative := fun x hx => add_nonneg (e.feedback x hx).base_nonnegative
    (effective_coefficients_nonnegative (f.params x)).2
  rho_nonnegative := fun x _ => (effective_coefficients_nonnegative (f.params x)).1
  strict := fun x hx => (u.relative_bound x hx).trans_lt u.rhoBar_strict
  closure := by
    intro x hx
    change f.energy x ≤ (f.base x + biasEff (f.params x)) +
      rhoEff (f.params x) * f.energy x
    have hr := e.relative x hx
    have hf := (e.feedback x hx).upper
    linarith

/-- Final consumer: invokes the existing uniform_cap unchanged. -/
theorem uniform_parameter_cap {X : Type*} (f : ParameterField X)
    (e : LocalEvidence f) (u : UniformParameters f) :
    ∀ x, f.domain x → f.energy x ≤ u.cap :=
  uniform_cap (toBudgetField f) (toPointwiseClosure f e u) (toUniformBudget f u)

/-- A supplied in-domain point with rhoEff>=1 blocks this uniform packet.
This is a contract obstruction, not a physical instability assertion. -/
theorem bad_point_blocks_uniform_parameters {X : Type*} (f : ParameterField X)
    (x : X) (hx : f.domain x) (hbad : 1 ≤ rhoEff (f.params x)) :
    ¬ Nonempty (UniformParameters f) := by
  rintro ⟨u⟩
  have hstrict := (u.relative_bound x hx).trans_lt u.rhoBar_strict
  linarith

end

-- Future audit commands only; NOT executed in this round.
#print axioms ofWeighted
#print axioms ofSeparateBiasBounds
#print axioms toUniformBudget
#print axioms toPointwiseClosure
#print axioms uniform_parameter_cap
#print axioms bad_point_blocks_uniform_parameters

end RouteBP4032UniformParameterBridge
