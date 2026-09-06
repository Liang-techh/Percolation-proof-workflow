import SourceContractAdapter

set_option autoImplicit false

namespace RouteBB45SourceComparator

noncomputable section

open RouteBFrameOriginAxis
open RouteBFrameSlotAccessor
open RouteBRealDHStep
open RouteBBodySemanticCore
open RouteBBodyContractCore
open RouteBSourceContractAdapter

abbrev Body := Fin 6
abbrev Slot := Fin 7
abbrev Joint := Fin 6
abbrev Axis := Fin 3
abbrev Vec3 := Axis → ℝ
abbrev RealFrame := Matrix (Fin 4) (Fin 4) ℝ

/-
  These are the exact-real counterparts of the three arrays constructed by
  `fk_frames` in the original Julia source:

    Tc[1] = I;  z[:,ii] = Tc[end][:,3];
    Tc[ii+1] = Tc[end] * A(ii);  o[:,ii+1] = Tc[ii+1][:,4].

  `prefixFrame` has the same parent-before-current ordering as that loop.
  No Float64 or machine trigonometric operation is present here.
-/
def juliaExactDHStep (joint : Joint) (q : ℝ) : RealFrame :=
  routeBRealStepMatrix joint q

def juliaExactFrameSlot (q : Joint → ℝ) (slot : Slot) : RealFrame :=
  prefixFrame (fun joint => juliaExactDHStep joint (q joint)) slot

def juliaExactOrigin (q : Joint → ℝ) (slot : Slot) : Vec3 :=
  origin (juliaExactFrameSlot q slot)

def juliaExactParentAxis (q : Joint → ℝ) (joint : Joint) : Vec3 :=
  zAxis (juliaExactFrameSlot q (RouteBBodySemanticCore.prevOrigin joint))

def juliaExactContract (q : Joint → ℝ) : KinematicContract where
  origins := juliaExactOrigin q
  axes := juliaExactParentAxis q

theorem dh_step_exact_real_bridge (q : Joint → ℝ) (joint : Joint) :
    juliaExactDHStep joint (q joint) = routeBRealStepMatrix joint (q joint) := by
  rfl

theorem dh_prefix_slot_exact_real_bridge (q : Joint → ℝ) (slot : Slot) :
    juliaExactFrameSlot q slot = routeBFrameSlot q slot := by
  rfl

theorem origin_slot_exact_real_bridge (q : Joint → ℝ) (slot : Slot) (a : Axis) :
    juliaExactOrigin q slot a =
      (routeBSourceOrigins q).getD slot.val (0 : Vec3) a := by
  unfold juliaExactOrigin
  rw [dh_prefix_slot_exact_real_bridge]
  exact congrFun (routeB_source_origin_slot q slot).symm a

theorem parent_axis_exact_real_bridge (q : Joint → ℝ) (joint : Joint) (a : Axis) :
    juliaExactParentAxis q joint a =
      (routeBSourceAxes q).getD joint.val (0 : Vec3) a := by
  unfold juliaExactParentAxis
  rw [dh_prefix_slot_exact_real_bridge]
  have h := routeB_source_axis_slot q (RouteBBodySemanticCore.prevOrigin joint)
  exact congrFun h.symm a

/- Function-level equality is the comparator seam consumed by the source
   contract.  The preceding slot lemmas keep the list/getD and parent-index
   transports explicit instead of hiding them in a mass theorem. -/
theorem julia_origin_function_eq_sourceContract (q : Joint → ℝ) :
    (juliaExactContract q).origins = (sourceContract q).origins := by
  funext slot a
  exact origin_slot_exact_real_bridge q slot a

theorem julia_parent_axis_function_eq_sourceContract (q : Joint → ℝ) :
    (juliaExactContract q).axes = (sourceContract q).axes := by
  funext joint a
  unfold juliaExactContract sourceContract
  exact parent_axis_exact_real_bridge q joint a

theorem com_exact_real_bridge (q : Joint → ℝ) (body : Body) (a : Axis) :
    bodyCom (juliaExactContract q).origins body a =
      bodyCom (sourceContract q).origins body a := by
  have hOrigins := julia_origin_function_eq_sourceContract q
  simp only [bodyCom, RouteBBodySemanticCore.midpoint]
  rw [congrFun (congrFun hOrigins (RouteBBodySemanticCore.prevOrigin body)) a]
  rw [congrFun (congrFun hOrigins (RouteBBodySemanticCore.nextOrigin body)) a]

theorem source_body_mass_extensional_bridge
    (q : Joint → ℝ) (body : Body) (mass : ℝ)
    (inertia : RouteBBodyContractCore.IMat) :
    contractMass (juliaExactContract q) body mass inertia =
      contractMass (sourceContract q) body mass inertia := by
  apply contractMass_congruent
  · intro slot a
    exact congrFun (congrFun (julia_origin_function_eq_sourceContract q) slot) a
  · intro joint a
    exact congrFun
      (congrFun (julia_parent_axis_function_eq_sourceContract q) joint) a

theorem source_body_mass_extensional_bridge_all_bodies
    (q : Joint → ℝ) (mass : Body → ℝ)
    (inertia : Body → RouteBBodyContractCore.IMat) :
    (fun body => contractMass (juliaExactContract q) body (mass body)
      (inertia body)) =
    (fun body => contractMass (sourceContract q) body (mass body)
      (inertia body)) := by
  funext body
  exact source_body_mass_extensional_bridge q body (mass body) (inertia body)

theorem source_mass_sum_extensional_bridge
    (q : Joint → ℝ) (mass : Body → ℝ)
    (inertia : Body → RouteBBodyContractCore.IMat) :
    (fun i j => ∑ body : Body,
      contractMass (juliaExactContract q) body (mass body) (inertia body) i j) =
    (fun i j => ∑ body : Body,
      contractMass (sourceContract q) body (mass body) (inertia body) i j) := by
  funext i j
  apply Finset.sum_congr rfl
  intro body hmem
  exact congrFun (congrFun
    (source_body_mass_extensional_bridge q body (mass body) (inertia body)) i) j

#print axioms dh_step_exact_real_bridge
#print axioms dh_prefix_slot_exact_real_bridge
#print axioms origin_slot_exact_real_bridge
#print axioms parent_axis_exact_real_bridge
#print axioms julia_origin_function_eq_sourceContract
#print axioms julia_parent_axis_function_eq_sourceContract
#print axioms com_exact_real_bridge
#print axioms source_body_mass_extensional_bridge
#print axioms source_body_mass_extensional_bridge_all_bodies
#print axioms source_mass_sum_extensional_bridge

end
end RouteBB45SourceComparator
