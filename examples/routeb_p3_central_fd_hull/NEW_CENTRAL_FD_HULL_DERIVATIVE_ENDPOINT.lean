import Mathlib.Data.Real.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Tactic

/-!
# P3 derivative-hull endpoint to gap bridge

This sidecar keeps function values, derivative/offset bounds, remainder
budgets, rounded endpoints, and per-box gap/cap inequalities explicit.  The
bridge consumes a sound enclosure premise; sampled positivity is not used as a
substitute.
-/

set_option autoImplicit false

namespace RouteBP3CentralFDHullDerivativeEndpoint

noncomputable section

structure DerivativeEndpointCertificate (D B : Type*) [DecidableEq B] where
  domain : D → Prop
  boxes : Finset B
  region : B → D → Prop
  functionValue : D → ℝ
  derivativeBound : B → ℝ
  offsetBound : B → ℝ
  remainderBound : B → ℝ
  endpointLower : B → ℝ
  endpointUpper : B → ℝ
  gapLower : B → ℝ
  weightedLoad : D → ℝ
  capLoad : D → ℝ
  rounding_interval_sound : B → Prop
  interval_sound : ∀ b, b ∈ boxes → rounding_interval_sound b
  derivative_bound_nonneg : ∀ b, b ∈ boxes → 0 ≤ derivativeBound b
  offset_bound_nonneg : ∀ b, b ∈ boxes → 0 ≤ offsetBound b
  remainder_bound_nonneg : ∀ b, b ∈ boxes → 0 ≤ remainderBound b
  endpoint_lower_positive : ∀ b, b ∈ boxes → 0 < endpointLower b
  gap_lower_positive : ∀ b, b ∈ boxes → 0 < gapLower b
  rounding_enclosure_sound : ∀ b, b ∈ boxes → rounding_interval_sound b →
    endpointLower b ≤ endpointUpper b
  endpoint_lower_from_derivative_hull :
    ∀ b, b ∈ boxes → rounding_interval_sound b → ∀ x, region b x →
      endpointLower b ≤
        functionValue x - derivativeBound b * offsetBound b - remainderBound b
  function_to_cap_gap :
    ∀ b, b ∈ boxes → ∀ x, region b x →
      functionValue x - derivativeBound b * offsetBound b - remainderBound b ≤
        capLoad x - weightedLoad x
  gap_lower_to_endpoint : ∀ b, b ∈ boxes → gapLower b ≤ endpointLower b

theorem derivative_endpoint_to_gap_lower
    {D B : Type*} [DecidableEq B]
    (C : DerivativeEndpointCertificate D B) :
    ∀ b, b ∈ C.boxes → ∀ x, C.region b x →
      C.gapLower b ≤ C.capLoad x - C.weightedLoad x := by
  intro b hb x hRegion
  have hSound : C.rounding_interval_sound b := C.interval_sound b hb
  have hEndpoint :
      C.endpointLower b ≤
        C.functionValue x - C.derivativeBound b * C.offsetBound b -
          C.remainderBound b :=
    C.endpoint_lower_from_derivative_hull b hb hSound x hRegion
  have hCap := C.function_to_cap_gap b hb x hRegion
  exact (C.gap_lower_to_endpoint b hb).trans (hEndpoint.trans hCap)

theorem derivative_endpoint_gap_consumer
    {D B : Type*} [DecidableEq B]
    (C : DerivativeEndpointCertificate D B) :
    ∀ b, b ∈ C.boxes → ∀ x, C.region b x →
      0 < C.gapLower b ∧
        C.gapLower b ≤ C.capLoad x - C.weightedLoad x := by
  intro b hb x hRegion
  exact ⟨C.gap_lower_positive b hb,
    derivative_endpoint_to_gap_lower C b hb x hRegion⟩

/-! Sampled positivity does not establish the omitted-point hull premise. -/

def sampledFunctionValue : Bool → ℝ
  | false => 1
  | true => -1

theorem sampled_positivity_not_global_hull :
    0 < sampledFunctionValue false ∧
      ∃ x, sampledFunctionValue x ≤ 0 := by
  constructor
  · norm_num [sampledFunctionValue]
  · exact ⟨true, by norm_num [sampledFunctionValue]⟩

/-! A claimed remainder smaller than the exact remainder is not sound. -/

def exactRemainder : ℝ := 1

def claimedRemainder : ℝ := 0

theorem unsound_remainder_bound_obstruction :
    ¬ exactRemainder ≤ claimedRemainder := by
  norm_num [exactRemainder, claimedRemainder]

end

end RouteBP3CentralFDHullDerivativeEndpoint

#print axioms RouteBP3CentralFDHullDerivativeEndpoint.derivative_endpoint_to_gap_lower
#print axioms RouteBP3CentralFDHullDerivativeEndpoint.derivative_endpoint_gap_consumer
#print axioms RouteBP3CentralFDHullDerivativeEndpoint.unsound_remainder_bound_obstruction
