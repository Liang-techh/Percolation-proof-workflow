import SourceContractAdapter

set_option autoImplicit false

namespace RouteBB45OriginsAxesBridge

noncomputable section

open RouteBFrameOriginAxis
open RouteBFrameSlotAccessor
open RouteBBodySemanticCore
open RouteBSourceContractAdapter

abbrev Joint := Fin 6
abbrev Slot := Fin 7
abbrev Axis := Fin 3
abbrev Vec3 := Axis → ℝ
abbrev RealFrame := Matrix (Fin 4) (Fin 4) ℝ

/- Exact-real transcription of the Julia frame loop: the frame at a slot is
   the prefix before the next DH step.  This definition contains no Float64
   or machine trigonometry. -/
def exactDHStep (joint : Joint) (q : Joint → ℝ) : RealFrame :=
  routeBRealStepMatrix joint (q joint)

def exactFrameSlot (q : Joint → ℝ) (slot : Slot) : RealFrame :=
  prefixFrame (fun joint => exactDHStep joint q) slot

def exactOrigin (q : Joint → ℝ) (slot : Slot) : Vec3 :=
  origin (exactFrameSlot q slot)

def exactParentAxis (q : Joint → ℝ) (joint : Joint) : Vec3 :=
  zAxis (exactFrameSlot q (prevOrigin joint))

theorem exactFrameSlot_eq_routeBFrameSlot (q : Joint → ℝ) (slot : Slot) :
    exactFrameSlot q slot = routeBFrameSlot q slot := by
  rfl

theorem exact_origin_slot_eq_source (q : Joint → ℝ) (slot : Slot) :
    exactOrigin q slot = (sourceContract q).origins slot := by
  funext a
  unfold exactOrigin sourceContract
  rw [exactFrameSlot_eq_routeBFrameSlot]
  exact congrFun (routeB_source_origin_slot q slot).symm a

theorem exact_parent_axis_eq_source (q : Joint → ℝ) (joint : Joint) :
    exactParentAxis q joint = (sourceContract q).axes joint := by
  funext a
  unfold exactParentAxis sourceContract
  rw [exactFrameSlot_eq_routeBFrameSlot]
  exact congrFun (routeB_source_axis_slot q (prevOrigin joint)).symm a

/- The seven slot statements are exposed as one Fin-indexed theorem and as
   six parent-axis statements, so the index transport is kernel-checked. -/
theorem seven_origins_source_contract (q : Joint → ℝ) (slot : Slot) :
    exactOrigin q slot = (sourceContract q).origins slot := by
  exact exact_origin_slot_eq_source q slot

theorem six_parent_axes_source_contract (q : Joint → ℝ) (joint : Joint) :
    exactParentAxis q joint = (sourceContract q).axes joint := by
  exact exact_parent_axis_eq_source q joint

theorem origins_function_eq_source_contract (q : Joint → ℝ) :
    exactOrigin q = (sourceContract q).origins := by
  funext slot
  exact seven_origins_source_contract q slot

theorem parent_axes_function_eq_source_contract (q : Joint → ℝ) :
    exactParentAxis q = (sourceContract q).axes := by
  funext joint
  exact six_parent_axes_source_contract q joint

theorem seven_slot_origin_axis_bridge (q : Joint → ℝ) :
    (exactOrigin q 0 = (sourceContract q).origins 0) ∧
    (exactOrigin q 1 = (sourceContract q).origins 1) ∧
    (exactOrigin q 2 = (sourceContract q).origins 2) ∧
    (exactOrigin q 3 = (sourceContract q).origins 3) ∧
    (exactOrigin q 4 = (sourceContract q).origins 4) ∧
    (exactOrigin q 5 = (sourceContract q).origins 5) ∧
    (exactOrigin q 6 = (sourceContract q).origins 6) := by
  constructor
  · exact seven_origins_source_contract q 0
  constructor
  · exact seven_origins_source_contract q 1
  constructor
  · exact seven_origins_source_contract q 2
  constructor
  · exact seven_origins_source_contract q 3
  constructor
  · exact seven_origins_source_contract q 4
  constructor
  · exact seven_origins_source_contract q 5
  · exact seven_origins_source_contract q 6

#print axioms exactFrameSlot_eq_routeBFrameSlot
#print axioms exact_origin_slot_eq_source
#print axioms exact_parent_axis_eq_source
#print axioms seven_origins_source_contract
#print axioms six_parent_axes_source_contract
#print axioms origins_function_eq_source_contract
#print axioms parent_axes_function_eq_source_contract
#print axioms seven_slot_origin_axis_bridge

end
end RouteBB45OriginsAxesBridge
