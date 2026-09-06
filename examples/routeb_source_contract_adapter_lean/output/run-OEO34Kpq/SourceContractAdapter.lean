import FrameSlotAccessor
import BodyContractCore

set_option autoImplicit false

namespace RouteBSourceContractAdapter

noncomputable section

open RouteBFrameOriginAxis
open RouteBFrameSlotAccessor
open RouteBBodyContractCore

abbrev Vec3 := Fin 3 → ℝ

/- The source-facing contract reads the exact seven frame slots already
   isolated by the slot bridge.  The concrete frame contract keeps the same
   values but does not read the source list. -/
def sourceContract (q : Fin 6 → ℝ) : KinematicContract where
  origins := fun i => (routeBSourceOrigins q).getD i.val (0 : Vec3)
  axes := fun i => (routeBSourceAxes q).getD i.val (0 : Vec3)

def frameContract (q : Fin 6 → ℝ) : KinematicContract where
  origins := fun i => origin (routeBFrameSlot q i)
  axes := fun i => zAxis (routeBFrameSlot q (prevOrigin i))

theorem source_origin_function_eq_frame_contract (q : Fin 6 → ℝ) :
    (sourceContract q).origins = (frameContract q).origins := by
  funext i
  exact routeB_source_origin_slot q i

theorem source_axis_function_eq_frame_contract (q : Fin 6 → ℝ) :
    (sourceContract q).axes = (frameContract q).axes := by
  funext i
  exact routeB_source_axis_slot q (prevOrigin i)

theorem source_contract_eq_frame_contract (q : Fin 6 → ℝ) :
    sourceContract q = frameContract q := by
  apply KinematicContract.ext
  · funext i
    exact routeB_source_origin_slot q i
  · funext i
    exact routeB_source_axis_slot q (prevOrigin i)

theorem source_contract_body_mass_eq_frame_contract_body_mass
    (q : Fin 6 → ℝ) (body : Fin 6) (mass : ℝ)
    (inertia : IMat) :
    contractMass (sourceContract q) body mass inertia =
      contractMass (frameContract q) body mass inertia := by
  apply contractMass_congruent
  · intro i a
    exact congrFun (congrFun (source_origin_function_eq_frame_contract q) i) a
  · intro j a
    exact congrFun (congrFun (source_axis_function_eq_frame_contract q) j) a

#print axioms source_origin_function_eq_frame_contract
#print axioms source_axis_function_eq_frame_contract
#print axioms source_contract_eq_frame_contract
#print axioms source_contract_body_mass_eq_frame_contract_body_mass

end
end RouteBSourceContractAdapter
