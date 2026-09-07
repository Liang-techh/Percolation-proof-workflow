import Mathlib.Data.Real.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Tactic

/-!
# P3 source-specific Route-B real binding

This is a proof-attempt contract for the current six-DOF Route-B semantics.
It separates the exact-real DH/C/G/central-FD source identity from the
per-box Taylor and gap consumer.  The deployed Float64 implementation must
still supply the exact-real and interval bindings represented by the fields.
-/

set_option autoImplicit false

namespace RouteBP3CentralFDHullRouteBRealBinding

noncomputable section

abbrev I6 := Fin 6
abbrev Q6 := I6 → ℝ
abbrev V6 := I6 → ℝ
abbrev Matrix6 := I6 → I6 → ℝ
abbrev State6 := Q6 × Q6

def shiftQ6 (q : Q6) (k : I6) (δ : ℝ) : Q6 :=
  fun j => q j + if j = k then δ else 0

def identityMatrix6 : Matrix6 :=
  fun i j => if i = j then 1 else 0

structure RouteBExactSource where
  M_DH : Q6 → Matrix6
  M : Q6 → Matrix6
  potential : Q6 → ℝ
  dM : Q6 → I6 → Matrix6
  Cfd : Q6 → Q6 → V6
  Gfd : Q6 → V6
  fdStep : ℝ
  massRegularization : ℝ
  fd_step_exact_target : fdStep = 1 / 100000
  mass_regularization_exact_target : massRegularization = 1 / 1000000
  mass_regularized : ∀ q i j,
    M q i j = M_DH q i j + massRegularization * identityMatrix6 i j
  central_dM : ∀ q k i j,
    dM q k i j =
      (M (shiftQ6 q k fdStep) i j - M (shiftQ6 q k (-fdStep)) i j) /
        (2 * fdStep)
  christoffel_Cfd : ∀ q dq i,
    Cfd q dq i =
      ∑ j, ∑ k,
        ((dM q k i j + dM q j i k - dM q i j k) / 2) * dq j * dq k
  central_Gfd : ∀ q k,
    Gfd q k =
      (potential (shiftQ6 q k fdStep) - potential (shiftQ6 q k (-fdStep))) /
        (2 * fdStep)

structure RouteBPerBoxTaylorBinding (B : Type*) [DecidableEq B] where
  domain : State6 → Prop
  boxes : Finset B
  region : B → State6 → Prop
  boxOf : State6 → B
  selectedIndex : I6
  taylorFunction : State6 → ℝ
  firstDerivativeHull : B → ℝ
  secondDerivativeHull : B → ℝ
  thirdDerivativeHull : B → ℝ
  offsetRadius : B → ℝ
  remainderBound : B → ℝ
  endpointLower : B → ℝ
  endpointUpper : B → ℝ
  gapLower : B → ℝ
  weightedLoad : State6 → ℝ
  capLoad : State6 → ℝ
  capLoadUpper : B → ℝ
  capMaxLoad : State6 → ℝ
  regularity : B → Prop
  regularity_sound : ∀ b, b ∈ boxes → regularity b
  offset_radius_nonneg : ∀ b, b ∈ boxes → 0 ≤ offsetRadius b
  remainder_bound_nonneg : ∀ b, b ∈ boxes → 0 ≤ remainderBound b
  rounding_endpoint_sound : ∀ b, b ∈ boxes → regularity b →
    endpointLower b ≤ endpointUpper b
  taylor_lower_enclosure : ∀ b, b ∈ boxes → regularity b → ∀ x, region b x →
    endpointLower b ≤
      taylorFunction x - firstDerivativeHull b * offsetRadius b
        - secondDerivativeHull b * offsetRadius b ^ 2 / 2
        - remainderBound b
  gapLower_positive : ∀ b, b ∈ boxes → 0 < gapLower b
  gapLower_to_endpoint : ∀ b, b ∈ boxes → gapLower b ≤ endpointLower b
  taylor_to_cap_gap : ∀ b, b ∈ boxes → ∀ x, region b x →
    taylorFunction x - firstDerivativeHull b * offsetRadius b
        - secondDerivativeHull b * offsetRadius b ^ 2 / 2
        - remainderBound b ≤ capLoad x - weightedLoad x
  capLoad_upper_sound : ∀ b, b ∈ boxes → regularity b → ∀ x, region b x →
    capLoad x ≤ capLoadUpper b
  capUpper_to_capMax : ∀ b, b ∈ boxes → regularity b → ∀ x, region b x →
    capLoadUpper b ≤ capMaxLoad x

structure RouteBRealBinding (B : Type*) [DecidableEq B] where
  source : RouteBExactSource
  boxTaylor : RouteBPerBoxTaylorBinding B
  domain_binding : ∀ b, b ∈ boxTaylor.boxes → ∀ x, boxTaylor.region b x →
    boxTaylor.domain x
  M_entry : Q6 → ℝ
  C_entry : State6 → ℝ
  G_entry : Q6 → ℝ
  M_binding : ∀ q,
    M_entry q = source.M q boxTaylor.selectedIndex boxTaylor.selectedIndex
  C_binding : ∀ x,
    C_entry x = source.Cfd x.1 x.2 boxTaylor.selectedIndex
  G_binding : ∀ q,
    G_entry q = source.Gfd q boxTaylor.selectedIndex
  coefficient_function_identity : ∀ x, boxTaylor.domain x →
    boxTaylor.taylorFunction x = M_entry x.1 + C_entry x + G_entry x.1

theorem routeB_same_box_function_identity
    {B : Type*} [DecidableEq B]
    (E : RouteBRealBinding B) (b : B) (hb : b ∈ E.boxTaylor.boxes)
    (x : State6) (hRegion : E.boxTaylor.region b x) :
    E.boxTaylor.taylorFunction x =
      E.source.M x.1 E.boxTaylor.selectedIndex E.boxTaylor.selectedIndex +
        E.source.Cfd x.1 x.2 E.boxTaylor.selectedIndex +
        E.source.Gfd x.1 E.boxTaylor.selectedIndex := by
  have hDomain := E.domain_binding b hb x hRegion
  rw [E.coefficient_function_identity x hDomain,
    E.M_binding x.1, E.C_binding x, E.G_binding x.1]

theorem routeB_taylor_to_per_box_gap
    {B : Type*} [DecidableEq B]
    (E : RouteBRealBinding B) :
    ∀ b, b ∈ E.boxTaylor.boxes → ∀ x, E.boxTaylor.region b x →
      0 < E.boxTaylor.gapLower b ∧
        E.boxTaylor.gapLower b ≤
          E.boxTaylor.capLoad x - E.boxTaylor.weightedLoad x ∧
        E.boxTaylor.taylorFunction x =
          E.source.M x.1 E.boxTaylor.selectedIndex E.boxTaylor.selectedIndex +
            E.source.Cfd x.1 x.2 E.boxTaylor.selectedIndex +
            E.source.Gfd x.1 E.boxTaylor.selectedIndex := by
  intro b hb x hRegion
  have hRegular := E.boxTaylor.regularity_sound b hb
  have hTaylor := E.boxTaylor.taylor_lower_enclosure b hb hRegular x hRegion
  have hCapGap := E.boxTaylor.taylor_to_cap_gap b hb x hRegion
  have hGapEndpoint := E.boxTaylor.gapLower_to_endpoint b hb
  have hGapLower :
      E.boxTaylor.gapLower b ≤
        E.boxTaylor.capLoad x - E.boxTaylor.weightedLoad x := by
    linarith
  refine ⟨E.boxTaylor.gapLower_positive b hb, hGapLower, ?_⟩
  exact routeB_same_box_function_identity E b hb x hRegion

/-! An arbitrary coefficient function does not satisfy the source identity. -/

def arbitraryCoefficient : Bool → ℝ
  | false => 1
  | true => 0

theorem arbitrary_function_identity_obstruction :
    ¬ (∀ x, arbitraryCoefficient x = 0 + 0) := by
  intro h
  have hFalse := h false
  norm_num [arbitraryCoefficient] at hFalse

/-! A domain restriction cannot be silently widened to the full state space. -/

def localRouteBDomain : Bool → Prop := fun x => x = false

theorem wrong_domain_binding_obstruction :
    ∃ x : Bool, ¬ localRouteBDomain x := by
  exact ⟨true, by simp [localRouteBDomain]⟩

end

end RouteBP3CentralFDHullRouteBRealBinding

#print axioms RouteBP3CentralFDHullRouteBRealBinding.routeB_same_box_function_identity
#print axioms RouteBP3CentralFDHullRouteBRealBinding.routeB_taylor_to_per_box_gap
#print axioms RouteBP3CentralFDHullRouteBRealBinding.arbitrary_function_identity_obstruction
#print axioms RouteBP3CentralFDHullRouteBRealBinding.wrong_domain_binding_obstruction
