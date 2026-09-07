import NEW_BODY6_SLICE_SCHURMARGIN20260907
import NEW_P4_032_ResidualMarginConsumer

/-!
UNCOMPILED minimal BODY6 RemainderMargin -> scalar comparison adapter.
The external quadratic margin is consumed, never synthesized.
The BODY6 Front has dimension 3; no identification with a P4 port is made.
Residual, normalization and target relations remain explicit premises.
-/

set_option autoImplicit false

namespace RouteBP4032Body6SchurScalarAdapter

open NEW_BODY6_SLICE_SCHURMARGIN20260907
open RouteBP4032UniformParameterBridge
open RouteBP4032ResidualMarginConsumer
open scoped BigOperators

noncomputable section

def frontEnergy (v : Front) : ℝ := ∑ i : Fin 3, v i ^ 2

def frontQuadratic (R : FrontBlock) (v : Front) : ℝ :=
  ∑ i : Fin 3, v i * frontAction R v i

/-- Pointwise BODY6 objects and the explicitly selected scalar conversion.
The type does not identify them with a source, physical metric or P4 q. -/
structure RemainderField (X : Type*) where
  remainder : X → FrontBlock
  mu : X → ℝ
  front : X → Front
  scale : X → ℝ
  offset : X → ℝ

/-- Every bridge premise is over f.domain and its SAME residual scalar.
nominal is allowed to be a conservative lower budget. The normalized
comparison must account for all coordinate/metric changes and cross terms. -/
structure ScalarBridgeEvidence {X : Type*} (f : ParameterField X)
    (d : RemainderField X) (m : MarginField X) : Prop where
  remainder_margin : ∀ x, f.domain x → RemainderMargin (d.remainder x) (d.mu x)
  scale_nonnegative : ∀ x, f.domain x → 0 ≤ d.scale x
  gain_nonnegative : ∀ x, f.domain x → 0 ≤ m.gain x
  nominal_bound : ∀ x, f.domain x →
    m.nominal x ≤ d.offset x + d.scale x * (d.mu x * frontEnergy (d.front x))
  normalized_comparison : ∀ x, f.domain x →
    d.offset x + d.scale x * frontQuadratic (d.remainder x) (d.front x) -
      m.gain x * f.residual x ≤ m.margin x

/-- Actual type adapter: evaluates the supplied BODY6 quadratic bound at
front(x), scales monotonically, and uses the external scalar comparison. -/
def toSchurPMIComparison {X : Type*} (f : ParameterField X)
    (d : RemainderField X) (m : MarginField X) (b : ScalarBridgeEvidence f d m) :
    SchurPMIComparison f m where
  gain_nonnegative := b.gain_nonnegative
  lower := by
    intro x hx
    have hbody : d.mu x * frontEnergy (d.front x) ≤
        frontQuadratic (d.remainder x) (d.front x) :=
      (b.remainder_margin x hx).2.2 (d.front x)
    have hscaled := mul_le_mul_of_nonneg_left hbody (b.scale_nonnegative x hx)
    have hnominal := b.nominal_bound x hx
    have hcomparison := b.normalized_comparison x hx
    linarith

/-- End-to-end conditional scalar margin. The target/nominal relation is
supplied through the EXISTING MarginAllocation, not inferred from mu.
All residual, uniform energy, bias and feedback inputs remain explicit. -/
theorem conditional_body6_scalar_margin {X : Type*} (f : ParameterField X)
    (e : LocalEvidence f) (u : UniformParameters f)
    (hc : UniformEnergyCap f u) (a : ResidualAllowance f u)
    (d : RemainderField X) (m : MarginField X) (b : ScalarBridgeEvidence f d m)
    (target : ℝ) (allocation : MarginAllocation f u a m target) :
    ∀ x, f.domain x → target ≤ m.margin x :=
  conditional_margin f e u hc a m (toSchurPMIComparison f d m b) target allocation

/-- A quadratic lower bound does not identify an unrelated target margin.
Exact scalar witness only; no claimed physical source realization. -/
theorem missing_comparison_witness :
    ∃ lower quadratic q gain targetMargin : ℝ,
      0 ≤ lower ∧ lower ≤ quadratic ∧ q = 0 ∧ 0 ≤ gain ∧
        targetMargin < lower - gain * q := by
  refine ⟨1, 1, 0, 1, -1, ?_⟩
  norm_num

/-- Negative scaling reverses a strict quadratic lower comparison.
Dropping normalization sign evidence is therefore unsound. -/
theorem negative_scale_witness :
    ∃ lower quadratic scale : ℝ,
      0 ≤ lower ∧ lower ≤ quadratic ∧ scale < 0 ∧
        scale * quadratic < scale * lower := by
  refine ⟨1, 2, -1, ?_⟩
  norm_num

end

-- Future audit commands only; NOT executed in this round.
#print axioms toSchurPMIComparison
#print axioms conditional_body6_scalar_margin
#print axioms missing_comparison_witness
#print axioms negative_scale_witness

end RouteBP4032Body6SchurScalarAdapter
