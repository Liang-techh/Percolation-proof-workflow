import NEW_P4_032_UniformParameterBridge

/-!
UNCOMPILED source-independent residual-to-scalar-margin consumer.
No matrix PSD, solver acceptance, Schur identity or physical binding claim.
All closure/uniform allocations are supplied through the preceding bridge.
No variable division, sqrt, or repeated contraction proof.
-/

set_option autoImplicit false

namespace RouteBP4032ResidualMarginConsumer

open RouteBP4032RelativeAdditive
open RouteBP4032UniformParameterBridge

noncomputable section

/-- The final consumer explicitly receives the uniform energy conclusion.
The constructor below is only a call to the preceding bridge theorem. -/
structure UniformEnergyCap {X : Type*} (f : ParameterField X)
    (u : UniformParameters f) : Prop where
  bound : ∀ x, f.domain x → f.energy x ≤ u.cap

def energyCapOfBridge {X : Type*} (f : ParameterField X)
    (e : LocalEvidence f) (u : UniformParameters f) : UniformEnergyCap f u where
  bound := uniform_parameter_cap f e u

/-- qCap bounds the residual SCALAR used by LocalEvidence and comparison.
In a norm-square instantiation qCap is a squared budget, not a norm cap. -/
structure ResidualAllowance {X : Type*} (f : ParameterField X)
    (u : UniformParameters f) where
  qCap : ℝ
  nonnegative : 0 ≤ qCap
  allocation : ∀ x, f.domain x →
    rhoEff (f.params x) * u.cap + biasEff (f.params x) ≤ qCap

/-- A conservative explicit constructor: u.biasBar bounds base+B_eff,
and base>=0 allows it to bound B_eff alone as well. No base is discarded
from the feedback allocation stored in u. -/
def allowanceFromTotalBias {X : Type*} (f : ParameterField X)
    (e : LocalEvidence f) (u : UniformParameters f) : ResidualAllowance f u where
  qCap := u.rhoBar * u.cap + u.biasBar
  nonnegative := add_nonneg (mul_nonneg u.rhoBar_nonnegative u.cap_nonnegative)
    u.biasBar_nonnegative
  allocation := by
    intro x hx
    have hr := mul_le_mul_of_nonneg_right (u.relative_bound x hx) u.cap_nonnegative
    have hb := u.additive_bound x hx
    have hbase := (e.feedback x hx).base_nonnegative
    linarith

/-- A sharper optional constructor when a separate B_eff cap is supplied. -/
def allowanceFromDefectBias {X : Type*} (f : ParameterField X)
    (u : UniformParameters f) (defectBiasBar : ℝ)
    (hb0 : 0 ≤ defectBiasBar)
    (hb : ∀ x, f.domain x → biasEff (f.params x) ≤ defectBiasBar) :
    ResidualAllowance f u where
  qCap := u.rhoBar * u.cap + defectBiasBar
  nonnegative := add_nonneg (mul_nonneg u.rhoBar_nonnegative u.cap_nonnegative) hb0
  allocation := fun x hx => add_le_add
    (mul_le_mul_of_nonneg_right (u.relative_bound x hx) u.cap_nonnegative) (hb x hx)

theorem residual_le_allowance {X : Type*} (f : ParameterField X)
    (e : LocalEvidence f) (u : UniformParameters f)
    (hc : UniformEnergyCap f u) (a : ResidualAllowance f u) :
    ∀ x, f.domain x → f.residual x ≤ a.qCap := by
  intro x hx
  have hmul := mul_le_mul_of_nonneg_left (hc.bound x hx)
    (effective_coefficients_nonnegative (f.params x)).1
  exact (e.relative x hx).trans
    ((add_le_add_right hmul (biasEff (f.params x))).trans (a.allocation x hx))

structure MarginField (X : Type*) where
  nominal : X → ℝ
  gain : X → ℝ
  margin : X → ℝ

/-- Supplied scalar Schur/PMI comparison for the SAME residual. Cross
terms, transformations and any matrix interpretation must be justified
by the caller before providing lower. A solver flag cannot fill it. -/
structure SchurPMIComparison {X : Type*} (f : ParameterField X)
    (m : MarginField X) : Prop where
  gain_nonnegative : ∀ x, f.domain x → 0 ≤ m.gain x
  lower : ∀ x, f.domain x →
    m.nominal x - m.gain x * f.residual x ≤ m.margin x

/-- Independent margin allocation, in addition to the bias/feedback
allocation in UniformParameters. target may be any real scalar floor. -/
structure MarginAllocation {X : Type*} (f : ParameterField X)
    (u : UniformParameters f) (a : ResidualAllowance f u)
    (m : MarginField X) (target : ℝ) : Prop where
  lower : ∀ x, f.domain x → target + m.gain x * a.qCap ≤ m.nominal x

/-- Conditional scalar margin only. Inputs explicitly include energy cap,
relative residual evidence, feedback/bias allocation, comparison and the
nominal margin allocation. No positivity of a matrix is concluded. -/
theorem conditional_margin {X : Type*} (f : ParameterField X)
    (e : LocalEvidence f) (u : UniformParameters f)
    (hc : UniformEnergyCap f u) (a : ResidualAllowance f u)
    (m : MarginField X) (comparison : SchurPMIComparison f m)
    (target : ℝ) (allocation : MarginAllocation f u a m target) :
    ∀ x, f.domain x → target ≤ m.margin x := by
  intro x hx
  have hq := residual_le_allowance f e u hc a x hx
  have hweighted := mul_le_mul_of_nonneg_left hq (comparison.gain_nonnegative x hx)
  have hcomparison := comparison.lower x hx
  have hallocation := allocation.lower x hx
  linarith

/-- Exact scalar obstruction: zero residual and zero energy, with a valid
strict-contraction closure and comparison, can still have negative margin
when the nominal allocation for target=0 is absent. No source instance. -/
theorem zero_residual_negative_margin :
    ∃ energy q nominal gain margin : ℝ,
      0 ≤ energy ∧ energy ≤ 0 ∧ 0 ≤ q ∧
      q ≤ (0.5 : ℝ) * energy + 0 ∧ energy ≤ 0 + q ∧
      0 ≤ gain ∧ nominal - gain * q ≤ margin ∧ margin < 0 := by
  refine ⟨0, 0, -1, 1, -1, ?_⟩
  norm_num

end

-- Future audit commands only; NOT executed in this round.
#print axioms energyCapOfBridge
#print axioms allowanceFromTotalBias
#print axioms allowanceFromDefectBias
#print axioms residual_le_allowance
#print axioms conditional_margin
#print axioms zero_residual_negative_margin

end RouteBP4032ResidualMarginConsumer
