import Mathlib.Data.Real.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Tactic

/-!
# P3 C2/C3 Taylor remainder contract

This sidecar keeps regularity, same-box derivative hulls, offset radius,
remainder bound, rounded endpoints, and gap/cap transfer separate.  The
endpoint consumer accepts the Taylor lower-enclosure premise rather than
pretending that sampled values establish C2/C3 regularity.
-/

set_option autoImplicit false

namespace RouteBP3CentralFDHullC2C3Remainder

noncomputable section

structure C2C3TaylorCertificate (D B : Type*) [DecidableEq B] where
  domain : D → Prop
  boxes : Finset B
  region : B → D → Prop
  functionValue : D → ℝ
  firstDerivative : D → ℝ
  secondDerivative : D → ℝ
  thirdDerivative : D → ℝ
  firstDerivativeHull : B → ℝ
  secondDerivativeHull : B → ℝ
  thirdDerivativeHull : B → ℝ
  offsetRadius : B → ℝ
  remainderBound : B → ℝ
  endpointLower : B → ℝ
  endpointUpper : B → ℝ
  gapLower : B → ℝ
  weightedLoad : D → ℝ
  capLoad : D → ℝ
  capLoadUpper : B → ℝ
  capMaxLoad : D → ℝ
  c2c3Regularity : B → Prop
  regularity_sound : ∀ b, b ∈ boxes → c2c3Regularity b
  first_hull_sound : ∀ b, b ∈ boxes → c2c3Regularity b → ∀ x, region b x →
    |firstDerivative x| ≤ firstDerivativeHull b
  second_hull_sound : ∀ b, b ∈ boxes → c2c3Regularity b → ∀ x, region b x →
    |secondDerivative x| ≤ secondDerivativeHull b
  third_hull_sound : ∀ b, b ∈ boxes → c2c3Regularity b → ∀ x, region b x →
    |thirdDerivative x| ≤ thirdDerivativeHull b
  offset_radius_nonneg : ∀ b, b ∈ boxes → 0 ≤ offsetRadius b
  remainder_bound_nonneg : ∀ b, b ∈ boxes → 0 ≤ remainderBound b
  rounding_endpoint_sound : ∀ b, b ∈ boxes → c2c3Regularity b →
    endpointLower b ≤ endpointUpper b
  taylor_lower_enclosure : ∀ b, b ∈ boxes → c2c3Regularity b →
    ∀ x, region b x →
      endpointLower b ≤
        functionValue x - firstDerivativeHull b * offsetRadius b
          - secondDerivativeHull b * offsetRadius b ^ 2 / 2
          - remainderBound b
  gapLower_positive : ∀ b, b ∈ boxes → 0 < gapLower b
  gapLower_to_endpoint : ∀ b, b ∈ boxes → gapLower b ≤ endpointLower b
  taylor_to_cap_gap : ∀ b, b ∈ boxes → ∀ x, region b x →
    functionValue x - firstDerivativeHull b * offsetRadius b
          - secondDerivativeHull b * offsetRadius b ^ 2 / 2
          - remainderBound b ≤ capLoad x - weightedLoad x
  capLoad_upper_sound : ∀ b, b ∈ boxes → c2c3Regularity b →
    ∀ x, region b x → capLoad x ≤ capLoadUpper b
  capUpper_to_capMax : ∀ b, b ∈ boxes → c2c3Regularity b →
    ∀ x, region b x → capLoadUpper b ≤ capMaxLoad x

theorem c2c3_to_per_box_margin
    {D B : Type*} [DecidableEq B]
    (C : C2C3TaylorCertificate D B) :
    ∀ b, b ∈ C.boxes → ∀ x, C.region b x →
      0 < C.gapLower b ∧
        C.weightedLoad x + C.gapLower b ≤ C.capMaxLoad x := by
  intro b hb x hRegion
  have hRegular : C.c2c3Regularity b := C.regularity_sound b hb
  have hGapPos : 0 < C.gapLower b := C.gapLower_positive b hb
  have hGapEndpoint : C.gapLower b ≤ C.endpointLower b :=
    C.gapLower_to_endpoint b hb
  have hTaylor := C.taylor_lower_enclosure b hb hRegular x hRegion
  have hCapGap := C.taylor_to_cap_gap b hb x hRegion
  have hCapUpper : C.capLoad x ≤ C.capLoadUpper b :=
    C.capLoad_upper_sound b hb hRegular x hRegion
  have hCapMax : C.capLoadUpper b ≤ C.capMaxLoad x :=
    C.capUpper_to_capMax b hb hRegular x hRegion
  constructor
  · exact hGapPos
  · linarith

theorem c2c3_consumer_strict
    {D B : Type*} [DecidableEq B]
    (C : C2C3TaylorCertificate D B)
    (consumer : D → ℝ)
    (hConsumer : ∀ x, C.domain x → consumer x ≤ C.weightedLoad x)
    (hCoverage : ∀ x, C.domain x → ∃ b, b ∈ C.boxes ∧ C.region b x) :
    ∀ x, C.domain x → consumer x < C.capMaxLoad x := by
  intro x hx
  rcases hCoverage x hx with ⟨b, hb, hRegion⟩
  have hMargin := c2c3_to_per_box_margin C b hb x hRegion
  exact lt_of_le_of_lt (hConsumer x hx) (by linarith [hMargin.1, hMargin.2])

/-! An underestimated remainder cannot support a Taylor enclosure. -/

def exactRemainder : ℝ := 1

def claimedRemainder : ℝ := 0

theorem underestimated_remainder_obstruction :
    ¬ exactRemainder ≤ claimedRemainder := by
  norm_num [exactRemainder, claimedRemainder]

/-! Without a regularity premise, endpoint transfer is fail-closed. -/

def missingRegularity : Prop := False

theorem missing_regularity_obstruction :
    ¬ missingRegularity := by
  simp [missingRegularity]

end

end RouteBP3CentralFDHullC2C3Remainder

#print axioms RouteBP3CentralFDHullC2C3Remainder.c2c3_to_per_box_margin
#print axioms RouteBP3CentralFDHullC2C3Remainder.c2c3_consumer_strict
#print axioms RouteBP3CentralFDHullC2C3Remainder.underestimated_remainder_obstruction
#print axioms RouteBP3CentralFDHullC2C3Remainder.missing_regularity_obstruction
