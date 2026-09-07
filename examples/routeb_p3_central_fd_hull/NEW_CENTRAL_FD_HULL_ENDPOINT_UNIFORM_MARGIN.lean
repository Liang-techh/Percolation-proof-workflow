import Mathlib.Data.Real.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Data.Finset.Lattice
import Mathlib.Tactic

/-!
# P3 finite-box endpoint certificate to common uniform margin

This sidecar combines a nonempty finite `inf'` gap with a same-point box map
and endpoint/rounding soundness.  The common margin is propagated through the
per-box endpoint-to-cap chain; consumer and admission layers remain separate.
-/

set_option autoImplicit false

namespace RouteBP3CentralFDHullEndpointUniformMargin

noncomputable section

structure EndpointUniformMarginCertificate (D B : Type*) [DecidableEq B] where
  domain : D → Prop
  boxes : Finset B
  boxes_nonempty : boxes.Nonempty
  boxOf : D → B
  region : B → D → Prop
  gapLower : B → ℝ
  endpointLower : B → ℝ
  endpointUpper : B → ℝ
  weightedLoad : D → ℝ
  capLoad : D → ℝ
  capLoadUpper : B → ℝ
  capMaxLoad : D → ℝ
  rounding_interval_sound : B → Prop
  interval_sound : ∀ b, b ∈ boxes → rounding_interval_sound b
  gap_lower_positive : ∀ b, b ∈ boxes → 0 < gapLower b
  endpoint_order : ∀ b, b ∈ boxes → rounding_interval_sound b →
    endpointLower b ≤ endpointUpper b
  gap_lower_to_endpoint : ∀ b, b ∈ boxes → gapLower b ≤ endpointLower b
  endpoint_lower_sound : ∀ b, b ∈ boxes → rounding_interval_sound b →
    ∀ x, region b x → endpointLower b ≤ capLoad x - weightedLoad x
  cap_load_upper_sound : ∀ b, b ∈ boxes → rounding_interval_sound b →
    ∀ x, region b x → capLoad x ≤ capLoadUpper b
  cap_upper_to_capMax : ∀ b, b ∈ boxes → rounding_interval_sound b →
    ∀ x, region b x → capLoadUpper b ≤ capMaxLoad x
  mapping_in_boxes : ∀ x, domain x → boxOf x ∈ boxes
  mapping_in_region : ∀ x, domain x → region (boxOf x) x

def commonMu
    {D B : Type*} [DecidableEq B]
    (C : EndpointUniformMarginCertificate D B) : ℝ :=
  C.boxes.inf' C.boxes_nonempty C.gapLower

theorem common_mu_positive
    {D B : Type*} [DecidableEq B]
    (C : EndpointUniformMarginCertificate D B) : 0 < commonMu C := by
  have hMem : commonMu C ∈ C.boxes.image C.gapLower := by
    exact Finset.inf'_mem C.boxes C.boxes_nonempty C.gapLower
  rcases hMem with ⟨b, hb, hValue⟩
  rw [← hValue]
  exact C.gap_lower_positive b hb

theorem common_mu_lower_at
    {D B : Type*} [DecidableEq B]
    (C : EndpointUniformMarginCertificate D B) (b : B) (hb : b ∈ C.boxes) :
    commonMu C ≤ C.gapLower b := by
  exact Finset.inf'_le C.boxes C.boxes_nonempty C.gapLower hb

theorem endpoint_to_common_uniform_margin
    {D B : Type*} [DecidableEq B]
    (C : EndpointUniformMarginCertificate D B) :
    ∀ x, C.domain x →
      0 < commonMu C ∧
        C.weightedLoad x + commonMu C ≤ C.capMaxLoad x ∧
        C.weightedLoad x < C.capMaxLoad x := by
  intro x hx
  have hb : C.boxOf x ∈ C.boxes := C.mapping_in_boxes x hx
  have hRegion : C.region (C.boxOf x) x := C.mapping_in_region x hx
  have hSound : C.rounding_interval_sound (C.boxOf x) :=
    C.interval_sound (C.boxOf x) hb
  have hGapPos : 0 < commonMu C := common_mu_positive C
  have hMuLower : commonMu C ≤ C.gapLower (C.boxOf x) :=
    common_mu_lower_at C (C.boxOf x) hb
  have hGapEndpoint :
      C.gapLower (C.boxOf x) ≤ C.endpointLower (C.boxOf x) :=
    C.gap_lower_to_endpoint (C.boxOf x) hb
  have hEndpointCap :
      C.endpointLower (C.boxOf x) ≤
        C.capLoad x - C.weightedLoad x :=
    C.endpoint_lower_sound (C.boxOf x) hb hSound x hRegion
  have hCapUpper : C.capLoad x ≤ C.capLoadUpper (C.boxOf x) :=
    C.cap_load_upper_sound (C.boxOf x) hb hSound x hRegion
  have hCapMax : C.capLoadUpper (C.boxOf x) ≤ C.capMaxLoad x :=
    C.cap_upper_to_capMax (C.boxOf x) hb hSound x hRegion
  have hBoxMargin :
      C.weightedLoad x + C.gapLower (C.boxOf x) ≤ C.capMaxLoad x := by
    linarith
  have hUniformMargin :
      C.weightedLoad x + commonMu C ≤ C.capMaxLoad x := by
    linarith
  exact ⟨hGapPos, hUniformMargin, by linarith⟩

theorem endpoint_to_common_consumer_strict
    {D B : Type*} [DecidableEq B]
    (C : EndpointUniformMarginCertificate D B)
    (consumer : D → ℝ)
    (hConsumer : ∀ x, C.domain x → consumer x ≤ C.weightedLoad x) :
    ∀ x, C.domain x → consumer x < C.capMaxLoad x := by
  intro x hx
  have hWeighted := (endpoint_to_common_uniform_margin C x hx).2.2
  exact lt_of_le_of_lt (hConsumer x hx) hWeighted

theorem empty_boxes_endpoint_obstruction :
    ¬ (∅ : Finset Bool).Nonempty := by
  simp

theorem zero_common_mu_endpoint_obstruction :
    ¬ ((0 : ℝ) < 0) := by
  norm_num

def brokenBoxes : Finset Bool := {false}

def brokenBoxOf (_ : Bool) : Bool := false

def brokenRegion (b x : Bool) : Prop := b = false ∧ x = false

theorem broken_endpoint_coverage_obstruction :
    ∃ x : Bool, ¬ (brokenBoxOf x ∈ brokenBoxes ∧
      brokenRegion (brokenBoxOf x) x) := by
  refine ⟨true, ?_⟩
  simp [brokenBoxOf, brokenBoxes, brokenRegion]

end

end RouteBP3CentralFDHullEndpointUniformMargin

#print axioms RouteBP3CentralFDHullEndpointUniformMargin.common_mu_positive
#print axioms RouteBP3CentralFDHullEndpointUniformMargin.endpoint_to_common_uniform_margin
#print axioms RouteBP3CentralFDHullEndpointUniformMargin.endpoint_to_common_consumer_strict
#print axioms RouteBP3CentralFDHullEndpointUniformMargin.broken_endpoint_coverage_obstruction
