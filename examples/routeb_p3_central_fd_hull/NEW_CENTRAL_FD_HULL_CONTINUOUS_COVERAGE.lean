import Mathlib.Data.Real.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Tactic

/-!
# P3 interval certificate to domain coverage bridge

The domain type is intentionally abstract.  A finite box family reaches a
whole-domain conclusion only through an explicit point-to-box map and its
coverage proof; no finite grid or sampled receipt supplies that proof.
-/

set_option autoImplicit false

namespace RouteBP3CentralFDHullContinuousCoverage

noncomputable section

structure ContinuousCoverageCertificate (D B : Type*) [DecidableEq B] where
  domain : D → Prop
  boxes : Finset B
  region : B → D → Prop
  boxOf : D → B
  weightedLoad : D → ℝ
  capLoad : D → ℝ
  capLoadUpper : B → ℝ
  capMaxLoad : D → ℝ
  gapLower : B → ℝ
  rounding_interval_sound : B → Prop
  interval_sound : ∀ b, b ∈ boxes → rounding_interval_sound b
  gap_lower_positive : ∀ b, b ∈ boxes → 0 < gapLower b
  gap_lower_sound : ∀ b, b ∈ boxes → rounding_interval_sound b →
    ∀ x, region b x → gapLower b ≤ capLoad x - weightedLoad x
  cap_load_upper_sound : ∀ b, b ∈ boxes → rounding_interval_sound b →
    ∀ x, region b x → capLoad x ≤ capLoadUpper b
  cap_upper_to_capMax : ∀ b, b ∈ boxes → rounding_interval_sound b →
    ∀ x, region b x → capLoadUpper b ≤ capMaxLoad x
  mapping_in_boxes : ∀ x, domain x → boxOf x ∈ boxes
  mapping_in_region : ∀ x, domain x → region (boxOf x) x

theorem continuous_coverage_strict_slack
    {D B : Type*} [DecidableEq B]
    (C : ContinuousCoverageCertificate D B) :
    ∀ x, C.domain x →
      C.weightedLoad x + C.gapLower (C.boxOf x) ≤ C.capMaxLoad x ∧
        C.weightedLoad x < C.capMaxLoad x := by
  intro x hx
  let b := C.boxOf x
  have hb : b ∈ C.boxes := C.mapping_in_boxes x hx
  have hRegion : C.region b x := C.mapping_in_region x hx
  have hSound : C.rounding_interval_sound b := C.interval_sound b hb
  have hGapPos : 0 < C.gapLower b := C.gap_lower_positive b hb
  have hGapLower :
      C.gapLower b ≤ C.capLoad x - C.weightedLoad x :=
    C.gap_lower_sound b hb hSound x hRegion
  have hCapUpper : C.capLoad x ≤ C.capLoadUpper b :=
    C.cap_load_upper_sound b hb hSound x hRegion
  have hCapMax : C.capLoadUpper b ≤ C.capMaxLoad x :=
    C.cap_upper_to_capMax b hb hSound x hRegion
  have hMargin :
      C.weightedLoad x + C.gapLower b ≤ C.capMaxLoad x := by
    linarith
  constructor
  · exact hMargin
  · linarith [hGapPos]

theorem continuous_coverage_consumer_strict
    {D B : Type*} [DecidableEq B]
    (C : ContinuousCoverageCertificate D B)
    (consumer : D → ℝ)
    (hConsumer : ∀ x, C.domain x → consumer x ≤ C.weightedLoad x) :
    ∀ x, C.domain x → consumer x < C.capMaxLoad x := by
  intro x hx
  exact lt_of_le_of_lt (hConsumer x hx)
    (continuous_coverage_strict_slack C x hx).2

/-! An omitted point defeats an attempted finite-box coverage claim. -/

def omittedPointBoxes : Finset Bool := {false}

def omittedPointRegion (b x : Bool) : Prop := b = false ∧ x = false

def omittedPointMap (_ : Bool) : Bool := false

theorem omitted_point_breaks_domain_coverage :
    ∃ x : Bool, ¬ (omittedPointMap x ∈ omittedPointBoxes ∧
      omittedPointRegion (omittedPointMap x) x) := by
  refine ⟨true, ?_⟩
  simp [omittedPointMap, omittedPointBoxes, omittedPointRegion]

theorem finite_grid_or_sample_not_continuous_coverage :
    (∀ x, x ∈ omittedPointBoxes → True) ∧
      (∃ x, ¬ (omittedPointMap x ∈ omittedPointBoxes ∧
        omittedPointRegion (omittedPointMap x) x)) := by
  constructor
  · intro x hx
    trivial
  · exact omitted_point_breaks_domain_coverage

end

end RouteBP3CentralFDHullContinuousCoverage

#print axioms RouteBP3CentralFDHullContinuousCoverage.continuous_coverage_strict_slack
#print axioms RouteBP3CentralFDHullContinuousCoverage.continuous_coverage_consumer_strict
#print axioms RouteBP3CentralFDHullContinuousCoverage.omitted_point_breaks_domain_coverage
