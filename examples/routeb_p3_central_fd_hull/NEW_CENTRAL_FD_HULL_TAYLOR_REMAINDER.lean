import Mathlib.Data.Real.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Tactic

/-!
# P3 Taylor/interval remainder certificate

This sidecar exposes the exact-real inputs needed to produce a per-box margin
for the endpoint-uniform consumer: function values, derivative hull, offset,
remainder bound, rounded endpoints, and gap/cap inequalities.  It does not
claim that a concrete Taylor or interval implementation supplies them.
-/

set_option autoImplicit false

namespace RouteBP3CentralFDHullTaylorRemainder

noncomputable section

structure TaylorRemainderCertificate (D B : Type*) [DecidableEq B] where
  domain : D → Prop
  boxes : Finset B
  region : B → D → Prop
  functionValue : D → ℝ
  derivativeHull : B → ℝ
  offsetBound : B → ℝ
  remainderBound : B → ℝ
  endpointLower : B → ℝ
  endpointUpper : B → ℝ
  gapLower : B → ℝ
  weightedLoad : D → ℝ
  capLoad : D → ℝ
  capLoadUpper : B → ℝ
  capMaxLoad : D → ℝ
  rounding_interval_sound : B → Prop
  interval_sound : ∀ b, b ∈ boxes → rounding_interval_sound b
  derivative_hull_nonneg : ∀ b, b ∈ boxes → 0 ≤ derivativeHull b
  offset_bound_nonneg : ∀ b, b ∈ boxes → 0 ≤ offsetBound b
  remainder_bound_nonneg : ∀ b, b ∈ boxes → 0 ≤ remainderBound b
  endpoint_order : ∀ b, b ∈ boxes → rounding_interval_sound b →
    endpointLower b ≤ endpointUpper b
  taylor_lower_sound : ∀ b, b ∈ boxes → rounding_interval_sound b →
    ∀ x, region b x →
      endpointLower b ≤
        functionValue x - derivativeHull b * offsetBound b - remainderBound b
  gapLower_positive : ∀ b, b ∈ boxes → 0 < gapLower b
  gapLower_to_endpoint : ∀ b, b ∈ boxes → gapLower b ≤ endpointLower b
  function_to_cap_gap : ∀ b, b ∈ boxes → ∀ x, region b x →
    functionValue x - derivativeHull b * offsetBound b - remainderBound b ≤
      capLoad x - weightedLoad x
  capLoad_upper_sound : ∀ b, b ∈ boxes → rounding_interval_sound b →
    ∀ x, region b x → capLoad x ≤ capLoadUpper b
  capUpper_to_capMax : ∀ b, b ∈ boxes → rounding_interval_sound b →
    ∀ x, region b x → capLoadUpper b ≤ capMaxLoad x

theorem taylor_remainder_to_per_box_margin
    {D B : Type*} [DecidableEq B]
    (C : TaylorRemainderCertificate D B) :
    ∀ b, b ∈ C.boxes → ∀ x, C.region b x →
      0 < C.gapLower b ∧
        C.weightedLoad x + C.gapLower b ≤ C.capMaxLoad x := by
  intro b hb x hRegion
  have hSound : C.rounding_interval_sound b := C.interval_sound b hb
  have hGapPos : 0 < C.gapLower b := C.gapLower_positive b hb
  have hGapEndpoint : C.gapLower b ≤ C.endpointLower b :=
    C.gapLower_to_endpoint b hb
  have hTaylor :
      C.endpointLower b ≤
        C.functionValue x - C.derivativeHull b * C.offsetBound b -
          C.remainderBound b :=
    C.taylor_lower_sound b hb hSound x hRegion
  have hFunctionCap := C.function_to_cap_gap b hb x hRegion
  have hCapUpper : C.capLoad x ≤ C.capLoadUpper b :=
    C.capLoad_upper_sound b hb hSound x hRegion
  have hCapMax : C.capLoadUpper b ≤ C.capMaxLoad x :=
    C.capUpper_to_capMax b hb hSound x hRegion
  constructor
  · exact hGapPos
  · linarith

theorem taylor_remainder_consumer_strict
    {D B : Type*} [DecidableEq B]
    (C : TaylorRemainderCertificate D B)
    (consumer : D → ℝ)
    (hConsumer : ∀ x, C.domain x → consumer x ≤ C.weightedLoad x)
    (hCoverage : ∀ x, C.domain x → ∃ b, b ∈ C.boxes ∧ C.region b x) :
    ∀ x, C.domain x → consumer x < C.capMaxLoad x := by
  intro x hx
  rcases hCoverage x hx with ⟨b, hb, hRegion⟩
  have hMargin := taylor_remainder_to_per_box_margin C b hb x hRegion
  exact lt_of_le_of_lt (hConsumer x hx) (by
    linarith [hMargin.1, hMargin.2])

/-! An underestimated remainder invalidates the Taylor lower enclosure. -/

def exactRemainder : ℝ := 1

def claimedRemainder : ℝ := 0

theorem underestimated_remainder_obstruction :
    ¬ exactRemainder ≤ claimedRemainder := by
  norm_num [exactRemainder, claimedRemainder]

/-! A finite box list can omit a domain point. -/

def incompleteBoxes : Finset Bool := {false}

def incompleteRegion (b x : Bool) : Prop := b = false ∧ x = false

theorem omitted_point_coverage_obstruction :
    ∃ x : Bool, ¬ ∃ b, b ∈ incompleteBoxes ∧ incompleteRegion b x := by
  refine ⟨true, ?_⟩
  simp [incompleteBoxes, incompleteRegion]

end

end RouteBP3CentralFDHullTaylorRemainder

#print axioms RouteBP3CentralFDHullTaylorRemainder.taylor_remainder_to_per_box_margin
#print axioms RouteBP3CentralFDHullTaylorRemainder.taylor_remainder_consumer_strict
#print axioms RouteBP3CentralFDHullTaylorRemainder.underestimated_remainder_obstruction
#print axioms RouteBP3CentralFDHullTaylorRemainder.omitted_point_coverage_obstruction
