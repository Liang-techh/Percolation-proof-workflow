import Mathlib.Data.Real.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Tactic

/-!
# P3 DH coefficient identity to C2/C3 Taylor bridge

The Taylor/remainder side and the DH coefficient identity side are separate
records.  A bridge binds the same function, box, and domain point before any
gap/cap conclusion is exported.
-/

set_option autoImplicit false

namespace RouteBP3CentralFDHullDHCoefficientBridge

noncomputable section

structure TaylorRemainderSide (D B : Type*) [DecidableEq B] where
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
  regularity : B → Prop
  regularity_sound : ∀ b, b ∈ boxes → regularity b
  derivative_hull_sound : ∀ b, b ∈ boxes → regularity b → ∀ x, region b x →
    |firstDerivative x| ≤ firstDerivativeHull b ∧
      |secondDerivative x| ≤ secondDerivativeHull b ∧
      |thirdDerivative x| ≤ thirdDerivativeHull b
  offset_radius_nonneg : ∀ b, b ∈ boxes → 0 ≤ offsetRadius b
  remainder_bound_nonneg : ∀ b, b ∈ boxes → 0 ≤ remainderBound b
  rounding_endpoint_sound : ∀ b, b ∈ boxes → regularity b →
    endpointLower b ≤ endpointUpper b
  taylor_lower_enclosure : ∀ b, b ∈ boxes → regularity b →
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
  capLoad_upper_sound : ∀ b, b ∈ boxes → regularity b →
    ∀ x, region b x → capLoad x ≤ capLoadUpper b
  capUpper_to_capMax : ∀ b, b ∈ boxes → regularity b →
    ∀ x, region b x → capLoadUpper b ≤ capMaxLoad x

structure DHCoefficientIdentitySide (D : Type*) where
  domain : D → Prop
  M : D → ℝ
  C : D → ℝ
  G : D → ℝ
  identity : ∀ x, domain x → M x = C x + G x

structure DHToTaylorBridge (D B : Type*) [DecidableEq B] where
  taylor : TaylorRemainderSide D B
  dh : DHCoefficientIdentitySide D
  domain : D → Prop
  domain_binding : ∀ b, b ∈ taylor.boxes → ∀ x, taylor.region b x → domain x
  dh_domain_binding : ∀ x, domain x → dh.domain x
  function_binding : ∀ b, b ∈ taylor.boxes → ∀ x, taylor.region b x →
    taylor.functionValue x = dh.M x

theorem dh_identity_at_same_box_point
    {D B : Type*} [DecidableEq B]
    (E : DHToTaylorBridge D B) (b : B) (hb : b ∈ E.taylor.boxes)
    (x : D) (hRegion : E.taylor.region b x) :
    E.taylor.functionValue x = E.dh.M x ∧
      E.dh.M x = E.dh.C x + E.dh.G x := by
  have hDomain : E.domain x := E.domain_binding b hb x hRegion
  have hDHDomain : E.dh.domain x := E.dh_domain_binding x hDomain
  exact ⟨E.function_binding b hb x hRegion, E.dh.identity x hDHDomain⟩

theorem dh_taylor_to_per_box_gap
    {D B : Type*} [DecidableEq B]
    (E : DHToTaylorBridge D B) :
    ∀ b, b ∈ E.taylor.boxes → ∀ x, E.taylor.region b x →
      0 < E.taylor.gapLower b ∧
        E.taylor.gapLower b ≤
          E.taylor.capLoad x - E.taylor.weightedLoad x ∧
        E.taylor.functionValue x = E.dh.C x + E.dh.G x := by
  intro b hb x hRegion
  have hRegular : E.taylor.regularity b := E.taylor.regularity_sound b hb
  have hDHIdentity := dh_identity_at_same_box_point E b hb x hRegion
  have hTaylor := E.taylor.taylor_lower_enclosure b hb hRegular x hRegion
  have hCapGap := E.taylor.taylor_to_cap_gap b hb x hRegion
  have hGapEndpoint := E.taylor.gapLower_to_endpoint b hb
  have hGapLower :
      E.taylor.gapLower b ≤
        E.taylor.capLoad x - E.taylor.weightedLoad x := by
    linarith
  refine ⟨E.taylor.gapLower_positive b hb, hGapLower, ?_⟩
  calc
    E.taylor.functionValue x = E.dh.M x := hDHIdentity.1
    _ = E.dh.C x + E.dh.G x := hDHIdentity.2

/-! An arbitrary function need not satisfy the DH coefficient identity. -/

def arbitraryM : Bool → ℝ
  | false => 1
  | true => 0

def arbitraryC : Bool → ℝ := fun _ => 0

def arbitraryG : Bool → ℝ := fun _ => 0

theorem arbitrary_function_identity_obstruction :
    ¬ (∀ x, arbitraryM x = arbitraryC x + arbitraryG x) := by
  intro hIdentity
  have hFalse := hIdentity false
  norm_num [arbitraryM, arbitraryC, arbitraryG] at hFalse

/-! A wrong domain binding leaves a point outside the DH identity premise. -/

def wrongDomain : Bool → Prop := fun x => x = false

theorem wrong_domain_binding_obstruction :
    ∃ x : Bool, ¬ wrongDomain x := by
  exact ⟨true, by simp [wrongDomain]⟩

end

end RouteBP3CentralFDHullDHCoefficientBridge

#print axioms RouteBP3CentralFDHullDHCoefficientBridge.dh_identity_at_same_box_point
#print axioms RouteBP3CentralFDHullDHCoefficientBridge.dh_taylor_to_per_box_gap
#print axioms RouteBP3CentralFDHullDHCoefficientBridge.arbitrary_function_identity_obstruction
#print axioms RouteBP3CentralFDHullDHCoefficientBridge.wrong_domain_binding_obstruction
