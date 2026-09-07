import NEW_P4_032_DualScaleUniformization

/-!
OPEN_UNCOMPILED. Direction-typed nominal/allocation audit.
No Lean/Lake run; no mutation of existing contracts or registry.
The old cap, comparison and target allocation types remain in use.
-/

set_option autoImplicit false

namespace RouteBP4032NominalDirectionAudit

open RouteBP4032UniformParameterBridge
open RouteBP4032ResidualMarginConsumer
open RouteBP4032Body6SchurScalarAdapter
open RouteBP4032MinimalResidualBudgetAdapter
open RouteBP4032DualScaleComposition
open RouteBP4032DualScaleUniformization

noncomputable section

structure NominalUpper {X : Type*} (f : ParameterField X)
    (m : MarginField X) (expression : X → ℝ) : Prop where
  bound : ∀ x, f.domain x → m.nominal x ≤ expression x

structure NominalLower {X : Type*} (f : ParameterField X)
    (m : MarginField X) (expression : X → ℝ) : Prop where
  bound : ∀ x, f.domain x → expression x ≤ m.nominal x

/-- Distinct from the EXISTING TargetAllocation: this RHS is expression,
not nominal. It becomes sufficient only with NominalLower. -/
structure ExpressionAllocation {X : Type*} (f : ParameterField X)
    (m : MarginField X) (scale expression : X → ℝ) (qCap target : ℝ) : Prop where
  bound : ∀ x, f.domain x →
    target + m.gain x * (scale x * qCap) ≤ expression x

def allocation_via_lower {X : Type*} (f : ParameterField X)
    (m : MarginField X) (scale expression : X → ℝ) (qCap target : ℝ)
    (lo : NominalLower f m expression)
    (a : ExpressionAllocation f m scale expression qCap target) :
    TargetAllocation f m scale qCap target where
  lower := fun x hx => (a.bound x hx).trans (lo.bound x hx)

/-- The upper direction only transfers an ALREADY proved nominal
allocation to expression. It cannot be used as the preceding constructor. -/
def expression_allocation_necessary {X : Type*} (f : ParameterField X)
    (m : MarginField X) (scale expression : X → ℝ) (qCap target : ℝ)
    (hi : NominalUpper f m expression)
    (a : TargetAllocation f m scale qCap target) :
    ExpressionAllocation f m scale expression qCap target where
  bound := fun x hx => (a.lower x hx).trans (hi.bound x hx)

theorem both_directions_force_equality {X : Type*} (f : ParameterField X)
    (m : MarginField X) (expression : X → ℝ)
    (hi : NominalUpper f m expression) (lo : NominalLower f m expression) :
    ∀ x, f.domain x → m.nominal x = expression x := by
  intro x hx
  exact le_antisymm (hi.bound x hx) (lo.bound x hx)

def bodyExpression {X : Type*} (d : RemainderField X) (s : ScaleFields X) : X → ℝ :=
  fun x => d.offset x + (s.front x).value * (d.mu x * frontEnergy (d.front x))

def upperFromComposition {X : Type*} (f : ParameterField X)
    (d : RemainderField X) (m : MarginField X) (s : ScaleFields X)
    (b : CompositionContract f d m s) : NominalUpper f m (bodyExpression d s) where
  bound := b.nominal_bound

def lowerFromUniform {X : Type*} (f : ParameterField X)
    (d : RemainderField X) (m : MarginField X) (s : ScaleFields X)
    (u : UniformData f d m s) : NominalLower f m (bodyExpression d s) where
  bound := u.nominal_realization

/-- Audit finding: the CURRENT pair of contracts specializes nominal to
the exact expression. This is stronger than a conservative upper budget. -/
theorem current_uniform_nominal_is_exact {X : Type*} (f : ParameterField X)
    (d : RemainderField X) (m : MarginField X) (s : ScaleFields X)
    (b : CompositionContract f d m s) (u : UniformData f d m s) :
    ∀ x, f.domain x → m.nominal x = bodyExpression d s x :=
  both_directions_force_equality f m (bodyExpression d s)
    (upperFromComposition f d m s b) (lowerFromUniform f d m s u)

/-- Cap evidence and sign/normalization comparison remain explicit; an
allocation by itself never establishes a margin or verifies qCap. -/
theorem margin_via_nominal_lower {X : Type*} (f : ParameterField X)
    (m : MarginField X) (scale expression : X → ℝ) (qCap target : ℝ)
    (budget : CapEvidence f qCap) (comparison : ScaledComparison f m scale)
    (lo : NominalLower f m expression)
    (a : ExpressionAllocation f m scale expression qCap target) :
    ∀ x, f.domain x → target ≤ m.margin x :=
  conditional_residual_margin f qCap budget m scale comparison target
    (allocation_via_lower f m scale expression qCap target lo a)

structure NonnegativeTarget (target : ℝ) : Prop where
  nonnegative : 0 ≤ target

theorem nonnegative_margin (target margin : ℝ) (ht : NonnegativeTarget target)
    (h : target ≤ margin) : 0 ≤ margin := ht.nonnegative.trans h

theorem positive_margin (target margin : ℝ) (ht : 0 < target)
    (h : target ≤ margin) : 0 < margin := ht.trans_le h

/-- Wrong nominal direction: q=qCap=0 and gain=scale=1. All quantities
here are nonnegative, but allocation to expression does not allocate nominal. -/
theorem wrong_direction_counterexample :
    ∃ nominal expression loss target margin : ℝ,
      0 ≤ nominal ∧ 0 ≤ expression ∧ loss = 0 ∧ 0 ≤ target ∧
      nominal ≤ expression ∧ target + loss ≤ expression ∧
      nominal - loss ≤ margin ∧ nominal < target + loss ∧ margin < target := by
  refine ⟨0, 1, 0, 1, 0, ?_⟩
  norm_num

/-- Even with nominal=expression and correct allocation, an unproved
qCap invalidates the margin conclusion. gain=scale=1 throughout. -/
theorem missing_cap_counterexample :
    ∃ nominal expression q qCap target margin : ℝ,
      0 ≤ nominal ∧ nominal = expression ∧ 0 ≤ q ∧ 0 ≤ qCap ∧
      target + qCap ≤ nominal ∧ nominal - q ≤ margin ∧ qCap < q ∧ margin < target := by
  refine ⟨1, 1, 2, 1, 0, -1, ?_⟩
  norm_num

/-- A negative target can be validly attained at a negative margin.
Here nominal=expression=0, q=qCap=1 and gain=scale=1. -/
theorem negative_target_counterexample :
    ∃ nominal q qCap target margin : ℝ,
      0 ≤ nominal ∧ 0 ≤ q ∧ q ≤ qCap ∧ 0 ≤ qCap ∧
      target + qCap ≤ nominal ∧ nominal - q ≤ margin ∧
      target ≤ margin ∧ target < 0 ∧ margin < 0 := by
  refine ⟨0, 1, 1, -1, -1, ?_⟩
  norm_num

end

-- Future audit commands only; NOT executed in this round.
#print axioms allocation_via_lower
#print axioms expression_allocation_necessary
#print axioms current_uniform_nominal_is_exact
#print axioms margin_via_nominal_lower
#print axioms nonnegative_margin
#print axioms positive_margin
#print axioms wrong_direction_counterexample
#print axioms missing_cap_counterexample
#print axioms negative_target_counterexample

end RouteBP4032NominalDirectionAudit
