import ConcreteStepHomogeneous
import HomogeneousPrefixProjection
import FrameSlotAccessor

set_option autoImplicit false

namespace RouteBFrameSlotHomogeneousPrefix

noncomputable section

open RouteBConcreteStepHomogeneous
open RouteBHomogeneousPrefixProjection
open RouteBFrameSlotAccessor

abbrev V6 := Fin 6
abbrev V7 := Fin 7
abbrev Mat3 := Matrix (Fin 3) (Fin 3) ℝ
abbrev Vec3 := (Fin 3) → ℝ
abbrev Frame4 := Matrix (Fin 4) (Fin 4) ℝ

def routeBHomogeneousPrefix (q : V6 → ℝ) (i : V7) : Frame4 :=
  homogeneousPrefix
    (fun k => stepRotation k (q k))
    (fun k => stepTranslation k (q k)) i

theorem routeBFrameSlot_eq_routeBHomogeneousPrefix
    (q : V6 → ℝ) (i : V7) :
    routeBFrameSlot q i = routeBHomogeneousPrefix q i := by
  fin_cases i <;>
    simp [routeBFrameSlot, routeBHomogeneousPrefix, prefixFrame,
      homogeneousPrefix, routeBStepFunction, routeB_step_is_homogeneous]

theorem routeBFrameSlot_rotationBlock_eq_rotationPrefix
    (q : V6 → ℝ) (i : V7) :
    rotationBlock (routeBFrameSlot q i) =
      rotationPrefix (fun k => stepRotation k (q k)) i := by
  rw [routeBFrameSlot_eq_routeBHomogeneousPrefix]
  exact homogeneousPrefix_rotationBlock_eq _ _ _

#print axioms routeBFrameSlot_eq_routeBHomogeneousPrefix
#print axioms routeBFrameSlot_rotationBlock_eq_rotationPrefix

end
end RouteBFrameSlotHomogeneousPrefix
