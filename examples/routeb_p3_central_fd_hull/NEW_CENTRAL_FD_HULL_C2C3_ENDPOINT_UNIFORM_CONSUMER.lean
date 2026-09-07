import NEW_CENTRAL_FD_HULL_C2C3_SOURCE_BINDING
import Mathlib.Data.Finset.Lattice
import Mathlib.Tactic

/-!
# P3 C2/C3 endpoint-uniform margin consumer

This sidecar consumes the existing `C2C3SourceBinding` without redefining it.
It makes the endpoint-to-margin chain explicit: the same covered box supplies
the source derivative hulls, Taylor/remainder lower enclosure, rounded
endpoint identity, positive per-box gap, and cap/load upper chain.  The DH
`sourceM + sourceC + sourceG` identity remains an independent premise and is
only reported alongside the margin.

This is a conditional exact-real proof-attempt and remains OPEN_UNCOMPILED.
-/

set_option autoImplicit false

namespace RouteBP3CentralFDHullC2C3EndpointUniformConsumer

noncomputable section

open RouteBP3CentralFDHullC2C3SourceBinding

structure EndpointUniformConsumer (D B : Type*) [DecidableEq B] where
  source : C2C3SourceBinding D B
  boxes_nonempty : source.boxes.Nonempty
  offsetRadius : B → ℝ
  gapLower : B → ℝ
  weightedLoad : D → ℝ
  capLoad : D → ℝ
  capLoadUpper : B → ℝ
  capMaxLoad : D → ℝ

  gap_lower_positive : ∀ b, b ∈ source.boxes → 0 < gapLower b
  gap_lower_to_endpoint : ∀ b, b ∈ source.boxes →
    gapLower b ≤ source.endpointLower b

  /- This is the exact source-function Taylor/remainder lower enclosure. -/
  taylor_lower_enclosure : ∀ b, b ∈ source.boxes → ∀ x, source.region b x →
    source.endpointLower b ≤
      source.sourceFunction x
        - source.firstDerivativeHull b * offsetRadius b
        - source.secondDerivativeHull b * offsetRadius b ^ 2 / 2
        - source.remainderBound b

  /- The derivative-hull/remainder expression is compared at the same point. -/
  taylor_to_cap_gap : ∀ b, b ∈ source.boxes → ∀ x, source.region b x →
    source.sourceFunction x
        - source.firstDerivativeHull b * offsetRadius b
        - source.secondDerivativeHull b * offsetRadius b ^ 2 / 2
        - source.remainderBound b ≤ capLoad x - weightedLoad x

  cap_load_upper_sound : ∀ b, b ∈ source.boxes → ∀ x, source.region b x →
    capLoad x ≤ capLoadUpper b
  cap_upper_to_capMax : ∀ b, b ∈ source.boxes → ∀ x, source.region b x →
    capLoadUpper b ≤ capMaxLoad x

def commonMu {D B : Type*} [DecidableEq B]
    (C : EndpointUniformConsumer D B) : ℝ :=
  C.source.boxes.inf' C.boxes_nonempty C.gapLower

theorem common_mu_positive
    {D B : Type*} [DecidableEq B]
    (C : EndpointUniformConsumer D B) : 0 < commonMu C := by
  have hMem : commonMu C ∈ C.source.boxes.image C.gapLower := by
    exact Finset.inf'_mem C.source.boxes C.boxes_nonempty C.gapLower
  rcases hMem with ⟨b, hb, hValue⟩
  rw [← hValue]
  exact C.gap_lower_positive b hb

theorem common_mu_lower_at
    {D B : Type*} [DecidableEq B]
    (C : EndpointUniformConsumer D B) (b : B) (hb : b ∈ C.source.boxes) :
    commonMu C ≤ C.gapLower b := by
  exact Finset.inf'_le C.source.boxes C.boxes_nonempty C.gapLower hb

theorem source_endpoint_to_common_uniform_margin
    {D B : Type*} [DecidableEq B]
    (C : EndpointUniformConsumer D B) (x : D) (hx : C.source.domain x) :
    |C.source.sourceFirstDerivative x| ≤
        C.source.firstDerivativeHull (C.source.boxOf x) ∧
      |C.source.sourceSecondDerivative x| ≤
        C.source.secondDerivativeHull (C.source.boxOf x) ∧
      |C.source.sourceThirdDerivative x| ≤
        C.source.thirdDerivativeHull (C.source.boxOf x) ∧
      C.source.roundedLower (C.source.boxOf x) =
        C.source.endpointLower (C.source.boxOf x) ∧
      C.source.roundedUpper (C.source.boxOf x) =
        C.source.endpointUpper (C.source.boxOf x) ∧
      0 < commonMu C ∧
      C.weightedLoad x + commonMu C ≤ C.capMaxLoad x := by
  have hCoverage := C.source.coverage x hx
  have hb : C.source.boxOf x ∈ C.source.boxes := hCoverage.1
  have hRegion : C.source.region (C.source.boxOf x) x := hCoverage.2
  have hHulls := source_derivative_hull_at_covered_point C.source x hx
  have hRounding := same_rounded_endpoints_at_covered_box C.source x hx
  have hGapPos : 0 < commonMu C := common_mu_positive C
  have hMuLower : commonMu C ≤ C.gapLower (C.source.boxOf x) :=
    common_mu_lower_at C (C.source.boxOf x) hb
  have hGapEndpoint :
      C.gapLower (C.source.boxOf x) ≤
        C.source.endpointLower (C.source.boxOf x) :=
    C.gap_lower_to_endpoint (C.source.boxOf x) hb
  have hTaylor := C.taylor_lower_enclosure (C.source.boxOf x) hb x hRegion
  have hCapGap := C.taylor_to_cap_gap (C.source.boxOf x) hb x hRegion
  have hCapUpper := C.cap_load_upper_sound (C.source.boxOf x) hb x hRegion
  have hCapMax := C.cap_upper_to_capMax (C.source.boxOf x) hb x hRegion
  have hUniformMargin :
      C.weightedLoad x + commonMu C ≤ C.capMaxLoad x := by
    linarith
  exact ⟨hHulls.1, hHulls.2.1, hHulls.2.2, hRounding.1, hRounding.2,
    hGapPos, hUniformMargin⟩

theorem source_endpoint_to_common_consumer_strict
    {D B : Type*} [DecidableEq B]
    (C : EndpointUniformConsumer D B) (consumer : D → ℝ)
    (hConsumer : ∀ x, C.source.domain x → consumer x ≤ C.weightedLoad x) :
    ∀ x, C.source.domain x → consumer x < C.capMaxLoad x := by
  intro x hx
  have hMargin := source_endpoint_to_common_uniform_margin C x hx
  exact lt_of_le_of_lt (hConsumer x hx) (by linarith [hMargin.2.2.2.2.2.2])

/-! The DH identity is deliberately not used to manufacture the margin. -/

theorem source_dh_identity_remains_separate
    {D B : Type*} [DecidableEq B]
    (C : EndpointUniformConsumer D B) (x : D) (hx : C.source.domain x) :
    C.source.sourceFunction x =
      C.source.sourceM x + C.source.sourceC x + C.source.sourceG x := by
  exact source_dh_identity_at_covered_point C.source x hx

end

end RouteBP3CentralFDHullC2C3EndpointUniformConsumer

#print axioms RouteBP3CentralFDHullC2C3EndpointUniformConsumer.common_mu_positive
#print axioms RouteBP3CentralFDHullC2C3EndpointUniformConsumer.common_mu_lower_at
#print axioms RouteBP3CentralFDHullC2C3EndpointUniformConsumer.source_endpoint_to_common_uniform_margin
#print axioms RouteBP3CentralFDHullC2C3EndpointUniformConsumer.source_endpoint_to_common_consumer_strict
#print axioms RouteBP3CentralFDHullC2C3EndpointUniformConsumer.source_dh_identity_remains_separate
