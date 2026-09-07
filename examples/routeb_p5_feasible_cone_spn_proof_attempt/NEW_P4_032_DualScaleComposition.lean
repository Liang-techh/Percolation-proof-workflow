import NEW_P4_032_Body6SchurScalarAdapter
import NEW_P4_032_MinimalResidualBudgetAdapter

/-!
OPEN_UNCOMPILED. Typed composition of TWO independent scalar scales.
No implicit coercions or equality between the scale wrappers.
Consumes the existing BODY6 adapter and minimal residual consumer.
No Lean/Lake run, registry change, source/coverage or matrix PSD claim.
-/

set_option autoImplicit false

namespace RouteBP4032DualScaleComposition

open NEW_BODY6_SLICE_SCHURMARGIN20260907
open RouteBP4032UniformParameterBridge
open RouteBP4032ResidualMarginConsumer
open RouteBP4032Body6SchurScalarAdapter
open RouteBP4032MinimalResidualBudgetAdapter

noncomputable section

structure FrontQuadraticScale where
  value : ℝ

structure ResidualScalarScale where
  value : ℝ

structure ScaleFields (X : Type*) where
  front : X → FrontQuadraticScale
  residual : X → ResidualScalarScale

def residualValues {X : Type*} (s : ScaleFields X) : X → ℝ :=
  fun x => (s.residual x).value

/-- alpha acts on Q; beta acts on q. The residual effective gain is g*beta,
not alpha*g*beta unless a DIFFERENT comparison explicitly supplies it. -/
structure CompositionContract {X : Type*} (f : ParameterField X)
    (d : RemainderField X) (m : MarginField X) (s : ScaleFields X) : Prop where
  front_binding : ∀ x, f.domain x → d.scale x = (s.front x).value
  front_nonnegative : ∀ x, f.domain x → 0 ≤ (s.front x).value
  residual_nonnegative : ∀ x, f.domain x → 0 ≤ (s.residual x).value
  gain_nonnegative : ∀ x, f.domain x → 0 ≤ m.gain x
  remainder_margin : ∀ x, f.domain x → RemainderMargin (d.remainder x) (d.mu x)
  nominal_bound : ∀ x, f.domain x → m.nominal x ≤
    d.offset x + (s.front x).value * (d.mu x * frontEnergy (d.front x))
  normalization_comparison : ∀ x, f.domain x →
    d.offset x + (s.front x).value * frontQuadratic (d.remainder x) (d.front x) -
      m.gain x * ((s.residual x).value * f.residual x) ≤ m.margin x

/-- Supply BODY6 with alpha as its quadratic scale and g*beta as its gain. -/
def toBodyEvidence {X : Type*} (f : ParameterField X)
    (d : RemainderField X) (m : MarginField X) (s : ScaleFields X)
    (b : CompositionContract f d m s) :
    ScalarBridgeEvidence f d (effectiveMargin m (residualValues s)) where
  remainder_margin := b.remainder_margin
  scale_nonnegative := by
    intro x hx
    rw [b.front_binding x hx]
    exact b.front_nonnegative x hx
  gain_nonnegative := fun x hx =>
    mul_nonneg (b.gain_nonnegative x hx) (b.residual_nonnegative x hx)
  nominal_bound := by
    intro x hx
    change m.nominal x ≤ d.offset x + d.scale x * (d.mu x * frontEnergy (d.front x))
    rw [b.front_binding x hx]
    exact b.nominal_bound x hx
  normalized_comparison := by
    intro x hx
    change d.offset x + d.scale x * frontQuadratic (d.remainder x) (d.front x) -
      (m.gain x * (s.residual x).value) * f.residual x ≤ m.margin x
    rw [b.front_binding x hx]
    simpa only [mul_assoc] using b.normalization_comparison x hx

/-- Reuse the BODY6 theorem, then expose its result in the residual
adapter's original gain/scale convention without multiplying beta twice. -/
def toScaledComparison {X : Type*} (f : ParameterField X)
    (d : RemainderField X) (m : MarginField X) (s : ScaleFields X)
    (b : CompositionContract f d m s) : ScaledComparison f m (residualValues s) where
  gain_nonnegative := b.gain_nonnegative
  scale_nonnegative := b.residual_nonnegative
  lower := by
    intro x hx
    have h := (RouteBP4032Body6SchurScalarAdapter.toSchurPMIComparison f d
      (effectiveMargin m (residualValues s)) (toBodyEvidence f d m s b)).lower x hx
    change m.nominal x - (m.gain x * residualValues s x) * f.residual x ≤
      m.margin x at h
    simpa only [mul_assoc] using h

/-- Both adapters compose on the same domain, residual and exact qCap.
Only a conditional scalar margin is returned. -/
theorem composed_scalar_margin {X : Type*} (f : ParameterField X)
    (qCap : ℝ) (budget : CapEvidence f qCap)
    (d : RemainderField X) (m : MarginField X) (s : ScaleFields X)
    (b : CompositionContract f d m s) (target : ℝ)
    (allocation : TargetAllocation f m (residualValues s) qCap target) :
    ∀ x, f.domain x → target ≤ m.margin x :=
  conditional_residual_margin f qCap budget m (residualValues s)
    (toScaledComparison f d m s b) target allocation

/-- Scalar premises with offset=0, intentionally omitting the three scale/
gain signs, so each sign failure can be exhibited independently below. -/
def ScalarPremises (alpha beta gain lower quadratic q qCap nominal target margin : ℝ) : Prop :=
  0 ≤ lower ∧ lower ≤ quadratic ∧ 0 ≤ q ∧ q ≤ qCap ∧ 0 ≤ qCap ∧
  nominal ≤ alpha * lower ∧ alpha * quadratic - gain * (beta * q) ≤ margin ∧
  target + gain * (beta * qCap) ≤ nominal

/-- Only alpha is negative; the front lower-bound scaling fails. -/
theorem negative_front_scale_counterexample :
    ScalarPremises (-1) 1 1 1 2 0 0 (-1) (-1) (-2) ∧ (-2 : ℝ) < -1 := by
  norm_num [ScalarPremises]

/-- Only beta is negative; replacing q by qCap fails. -/
theorem negative_residual_scale_counterexample :
    ScalarPremises 1 (-1) 1 1 1 0 1 1 2 1 ∧ (1 : ℝ) < 2 := by
  norm_num [ScalarPremises]

/-- Only gain is negative; the residual effective gain is negative. -/
theorem negative_gain_counterexample :
    ScalarPremises 1 1 (-1) 1 1 0 1 1 2 1 ∧ (1 : ℝ) < 2 := by
  norm_num [ScalarPremises]

/-- Positive unequal scales alpha=1,beta=2. The true normalized margin is
-1. Incorrectly replacing beta by alpha makes target=0 appear allocated. -/
theorem false_scale_identification_counterexample :
    ∃ alpha beta gain lower quadratic q qCap nominal target margin : ℝ,
      0 ≤ alpha ∧ 0 ≤ beta ∧ 0 ≤ gain ∧ alpha ≠ beta ∧
      0 ≤ lower ∧ lower ≤ quadratic ∧ 0 ≤ q ∧ q ≤ qCap ∧ 0 ≤ qCap ∧
      nominal ≤ alpha * lower ∧ alpha * quadratic - gain * (beta * q) ≤ margin ∧
      target + gain * (alpha * qCap) ≤ nominal ∧
      ¬ (target + gain * (beta * qCap) ≤ nominal) ∧ margin < target := by
  refine ⟨1, 2, 1, 1, 1, 1, 1, 1, 0, -1, ?_⟩
  norm_num

end

-- Future audit commands only; NOT executed in this round.
#print axioms toBodyEvidence
#print axioms toScaledComparison
#print axioms composed_scalar_margin
#print axioms negative_front_scale_counterexample
#print axioms negative_residual_scale_counterexample
#print axioms negative_gain_counterexample
#print axioms false_scale_identification_counterexample

end RouteBP4032DualScaleComposition
