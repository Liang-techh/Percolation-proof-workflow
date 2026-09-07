import NEW_P4_032_ResidualMarginConsumer

/-!
OPEN_UNCOMPILED. Minimal residual-budget adapter, with explicit domain,
qCap, residual scaling, comparison and target allocation.
The core consumes a proved cap without reconstructing its energy origin.
No Lean/Lake run, variable division, sqrt, source or PSD claim.
-/

set_option autoImplicit false

namespace RouteBP4032MinimalResidualBudgetAdapter

open RouteBP4032UniformParameterBridge
open RouteBP4032ResidualMarginConsumer

noncomputable section

/-- A proved cap for exactly f.residual on f.domain. Nonnegative scalar
budget semantics are retained even when not needed by the last inequality. -/
structure CapEvidence {X : Type*} (f : ParameterField X) (qCap : ℝ) : Prop where
  cap_nonnegative : 0 ≤ qCap
  residual_nonnegative : ∀ x, f.domain x → 0 ≤ f.residual x
  bound : ∀ x, f.domain x → f.residual x ≤ qCap

/-- Existing energy/relative/bias/feedback evidence is consumed here once.
The result keeps the EXACT a.qCap; no unrelated allowance is substituted. -/
def capFromAllowance {X : Type*} (f : ParameterField X)
    (e : LocalEvidence f) (u : UniformParameters f)
    (hc : UniformEnergyCap f u) (a : ResidualAllowance f u) : CapEvidence f a.qCap where
  cap_nonnegative := a.nonnegative
  residual_nonnegative := e.residual_nonnegative
  bound := residual_le_allowance f e u hc a

/-- residualScale acts on the scalar q itself. It is not automatically a
vector coordinate scale, nor the BODY6 quadratic normalization factor. -/
structure ScaledComparison {X : Type*} (f : ParameterField X)
    (m : MarginField X) (residualScale : X → ℝ) : Prop where
  gain_nonnegative : ∀ x, f.domain x → 0 ≤ m.gain x
  scale_nonnegative : ∀ x, f.domain x → 0 ≤ residualScale x
  lower : ∀ x, f.domain x →
    m.nominal x - m.gain x * (residualScale x * f.residual x) ≤ m.margin x

structure TargetAllocation {X : Type*} (f : ParameterField X)
    (m : MarginField X) (residualScale : X → ℝ) (qCap target : ℝ) : Prop where
  lower : ∀ x, f.domain x →
    target + m.gain x * (residualScale x * qCap) ≤ m.nominal x

/-- Gain absorbs the explicitly supplied residual-scalar scale only. -/
def effectiveMargin {X : Type*} (m : MarginField X)
    (residualScale : X → ℝ) : MarginField X where
  nominal := m.nominal
  gain := fun x => m.gain x * residualScale x
  margin := m.margin

def toSchurComparison {X : Type*} (f : ParameterField X)
    (m : MarginField X) (residualScale : X → ℝ)
    (c : ScaledComparison f m residualScale) :
    SchurPMIComparison f (effectiveMargin m residualScale) where
  gain_nonnegative := fun x hx => mul_nonneg (c.gain_nonnegative x hx)
    (c.scale_nonnegative x hx)
  lower := by
    intro x hx
    change m.nominal x - (m.gain x * residualScale x) * f.residual x ≤ m.margin x
    simpa only [mul_assoc] using c.lower x hx

/-- Compatibility with the old allocation type uses a.qCap definitionally. -/
def toMarginAllocation {X : Type*} (f : ParameterField X)
    (u : UniformParameters f) (a : ResidualAllowance f u)
    (m : MarginField X) (residualScale : X → ℝ) (target : ℝ)
    (h : TargetAllocation f m residualScale a.qCap target) :
    MarginAllocation f u a (effectiveMargin m residualScale) target where
  lower := by
    intro x hx
    change target + (m.gain x * residualScale x) * a.qCap ≤ m.nominal x
    simpa only [mul_assoc] using h.lower x hx

/-- Minimal core: only the cap, signs, comparison and allocation are needed
after the upstream cap has been proved. The output is a scalar margin. -/
theorem conditional_residual_margin {X : Type*} (f : ParameterField X)
    (qCap : ℝ) (budget : CapEvidence f qCap)
    (m : MarginField X) (residualScale : X → ℝ)
    (comparison : ScaledComparison f m residualScale)
    (target : ℝ) (allocation : TargetAllocation f m residualScale qCap target) :
    ∀ x, f.domain x → target ≤ m.margin x := by
  intro x hx
  have hc := toSchurComparison f m residualScale comparison
  have hweighted := mul_le_mul_of_nonneg_left (budget.bound x hx)
    (hc.gain_nonnegative x hx)
  have hcomparison := hc.lower x hx
  have hallocation := allocation.lower x hx
  change (m.gain x * residualScale x) * f.residual x ≤
    (m.gain x * residualScale x) * qCap at hweighted
  change m.nominal x - (m.gain x * residualScale x) * f.residual x ≤
    m.margin x at hcomparison
  rw [← mul_assoc] at hallocation
  linarith

/-- All signs, comparison and allocation hold, but q exceeds qCap and the
claimed target fails. Merely naming a cap is not cap evidence. -/
theorem missing_qCap_witness :
    ∃ q qCap gain scale nominal target margin : ℝ,
      0 ≤ q ∧ 0 ≤ qCap ∧ 0 ≤ gain ∧ 0 ≤ scale ∧
      target + gain * (scale * qCap) ≤ nominal ∧
      nominal - gain * (scale * q) ≤ margin ∧ qCap < q ∧ margin < target := by
  refine ⟨2, 1, 1, 1, 1, 0, -1, ?_⟩
  norm_num

/-- Here q<=qCap DOES hold. Dropping scale>=0 reverses cap substitution
and permits the target to fail despite comparison and allocation. -/
theorem missing_scale_sign_witness :
    ∃ q qCap gain scale nominal target margin : ℝ,
      0 ≤ q ∧ q ≤ qCap ∧ 0 ≤ qCap ∧ 0 ≤ gain ∧ scale < 0 ∧
      target + gain * (scale * qCap) ≤ nominal ∧
      nominal - gain * (scale * q) ≤ margin ∧ margin < target := by
  refine ⟨0, 1, 1, -1, -1, 0, -1, ?_⟩
  norm_num

end

-- Future audit commands only; NOT executed in this round.
#print axioms capFromAllowance
#print axioms toSchurComparison
#print axioms toMarginAllocation
#print axioms conditional_residual_margin
#print axioms missing_qCap_witness
#print axioms missing_scale_sign_witness

end RouteBP4032MinimalResidualBudgetAdapter
