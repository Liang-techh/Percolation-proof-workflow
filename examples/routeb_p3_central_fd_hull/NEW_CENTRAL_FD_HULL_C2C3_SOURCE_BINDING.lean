import Mathlib.Data.Real.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Tactic

/-!
# P3 C2/C3 derivative-hull to source-function binding

This sidecar isolates the missing source-binding seam.  A Taylor hull is not
usable for the deployed DH coefficient unless the value and all derivative
fields refer to the same exact-real source function, the same selected box,
the same rounded endpoints, and an explicit domain-to-box coverage witness.

The file is a conditional proof-attempt only.  It contains no concrete
Float64/source implementation and remains OPEN_UNCOMPILED.
-/

set_option autoImplicit false

namespace RouteBP3CentralFDHullC2C3SourceBinding

noncomputable section

structure C2C3SourceBinding (D B : Type*) [DecidableEq B] where
  domain : D → Prop
  boxes : Finset B
  region : B → D → Prop
  boxOf : D → B

  sourceFunction : D → ℝ
  sourceFirstDerivative : D → ℝ
  sourceSecondDerivative : D → ℝ
  sourceThirdDerivative : D → ℝ
  sourceM : D → ℝ
  sourceC : D → ℝ
  sourceG : D → ℝ
  source_dh_identity : ∀ x, domain x →
    sourceFunction x = sourceM x + sourceC x + sourceG x

  taylorFunction : D → ℝ
  taylorFirstDerivative : D → ℝ
  taylorSecondDerivative : D → ℝ
  taylorThirdDerivative : D → ℝ
  firstDerivativeHull : B → ℝ
  secondDerivativeHull : B → ℝ
  thirdDerivativeHull : B → ℝ
  endpointLower : B → ℝ
  endpointUpper : B → ℝ
  roundedLower : B → ℝ
  roundedUpper : B → ℝ
  remainderBound : B → ℝ

  same_function : ∀ b, b ∈ boxes → ∀ x, region b x →
    taylorFunction x = sourceFunction x
  same_first_derivative : ∀ b, b ∈ boxes → ∀ x, region b x →
    taylorFirstDerivative x = sourceFirstDerivative x
  same_second_derivative : ∀ b, b ∈ boxes → ∀ x, region b x →
    taylorSecondDerivative x = sourceSecondDerivative x
  same_third_derivative : ∀ b, b ∈ boxes → ∀ x, region b x →
    taylorThirdDerivative x = sourceThirdDerivative x

  taylor_first_hull_sound : ∀ b, b ∈ boxes → ∀ x, region b x →
    |taylorFirstDerivative x| ≤ firstDerivativeHull b
  taylor_second_hull_sound : ∀ b, b ∈ boxes → ∀ x, region b x →
    |taylorSecondDerivative x| ≤ secondDerivativeHull b
  taylor_third_hull_sound : ∀ b, b ∈ boxes → ∀ x, region b x →
    |taylorThirdDerivative x| ≤ thirdDerivativeHull b

  same_rounded_endpoints : ∀ b, b ∈ boxes →
    roundedLower b = endpointLower b ∧ roundedUpper b = endpointUpper b
  rounded_endpoint_order : ∀ b, b ∈ boxes → endpointLower b ≤ endpointUpper b
  remainder_bound_nonneg : ∀ b, b ∈ boxes → 0 ≤ remainderBound b

  coverage : ∀ x, domain x →
    boxOf x ∈ boxes ∧ region (boxOf x) x

theorem source_derivative_hull_at_covered_point
    {D B : Type*} [DecidableEq B]
    (E : C2C3SourceBinding D B) (x : D) (hx : E.domain x) :
    |E.sourceFirstDerivative x| ≤
        E.firstDerivativeHull (E.boxOf x) ∧
      |E.sourceSecondDerivative x| ≤ E.secondDerivativeHull (E.boxOf x) ∧
      |E.sourceThirdDerivative x| ≤ E.thirdDerivativeHull (E.boxOf x) := by
  have hCoverage := E.coverage x hx
  have hBox : E.boxOf x ∈ E.boxes := hCoverage.1
  have hRegion : E.region (E.boxOf x) x := hCoverage.2
  have hFirst := E.taylor_first_hull_sound (E.boxOf x) hBox x hRegion
  have hSecond := E.taylor_second_hull_sound (E.boxOf x) hBox x hRegion
  have hThird := E.taylor_third_hull_sound (E.boxOf x) hBox x hRegion
  rw [E.same_first_derivative (E.boxOf x) hBox x hRegion] at hFirst
  rw [E.same_second_derivative (E.boxOf x) hBox x hRegion] at hSecond
  rw [E.same_third_derivative (E.boxOf x) hBox x hRegion] at hThird
  exact ⟨hFirst, hSecond, hThird⟩

theorem source_dh_identity_at_covered_point
    {D B : Type*} [DecidableEq B]
    (E : C2C3SourceBinding D B) (x : D) (hx : E.domain x) :
    E.sourceFunction x = E.sourceM x + E.sourceC x + E.sourceG x := by
  exact E.source_dh_identity x hx

theorem same_rounded_endpoints_at_covered_box
    {D B : Type*} [DecidableEq B]
    (E : C2C3SourceBinding D B) (x : D) (hx : E.domain x) :
    E.roundedLower (E.boxOf x) = E.endpointLower (E.boxOf x) ∧
      E.roundedUpper (E.boxOf x) = E.endpointUpper (E.boxOf x) := by
  exact E.same_rounded_endpoints (E.boxOf x) (E.coverage x hx).1

theorem source_value_binding_at_covered_point
    {D B : Type*} [DecidableEq B]
    (E : C2C3SourceBinding D B) (x : D) (hx : E.domain x) :
    E.taylorFunction x = E.sourceFunction x := by
  exact E.same_function (E.boxOf x) (E.coverage x hx).1 x (E.coverage x hx).2

/-! Minimal obstructions when one binding seam is omitted. -/

def candidateFunction : Bool → ℝ := fun _ => 1

def sourceFunction : Bool → ℝ := fun _ => 0

theorem missing_same_function_obstruction :
    ¬ (∀ x, candidateFunction x = sourceFunction x) := by
  intro h
  have hFalse := h false
  norm_num [candidateFunction, sourceFunction] at hFalse

def obstructionDomain : Bool → Prop := fun _ => True

def obstructionBoxes : Finset Bool := {false}

def obstructionRegion : Bool → Bool → Prop :=
  fun b x => b = false ∧ x = false

def obstructionBoxOf (_ : Bool) : Bool := false

theorem missing_same_box_coverage_obstruction :
    ∃ x, obstructionDomain x ∧
      ¬ (obstructionBoxOf x ∈ obstructionBoxes ∧
        obstructionRegion (obstructionBoxOf x) x) := by
  refine ⟨true, trivial, ?_⟩
  simp [obstructionBoxOf, obstructionBoxes, obstructionRegion]

def certifiedRoundedLower : Bool → ℝ := fun _ => 0

def sourceRoundedLower : Bool → ℝ := fun _ => 1

theorem missing_same_rounding_obstruction :
    ¬ (∀ b, sourceRoundedLower b = certifiedRoundedLower b) := by
  intro h
  have hFalse := h false
  norm_num [sourceRoundedLower, certifiedRoundedLower] at hFalse

end

end RouteBP3CentralFDHullC2C3SourceBinding

#print axioms RouteBP3CentralFDHullC2C3SourceBinding.source_derivative_hull_at_covered_point
#print axioms RouteBP3CentralFDHullC2C3SourceBinding.source_dh_identity_at_covered_point
#print axioms RouteBP3CentralFDHullC2C3SourceBinding.same_rounded_endpoints_at_covered_box
#print axioms RouteBP3CentralFDHullC2C3SourceBinding.source_value_binding_at_covered_point
#print axioms RouteBP3CentralFDHullC2C3SourceBinding.missing_same_function_obstruction
#print axioms RouteBP3CentralFDHullC2C3SourceBinding.missing_same_box_coverage_obstruction
#print axioms RouteBP3CentralFDHullC2C3SourceBinding.missing_same_rounding_obstruction
