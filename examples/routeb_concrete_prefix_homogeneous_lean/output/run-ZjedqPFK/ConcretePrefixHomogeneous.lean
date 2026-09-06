import FrameSlotAccessor
import ConcreteStepHomogeneous
import HomogeneousPrefixProjection

set_option autoImplicit false

namespace RouteBConcretePrefixHomogeneous

noncomputable section

open RouteBFrameSlotAccessor
open RouteBConcreteStepHomogeneous
open RouteBHomogeneousPrefixProjection

abbrev V3 := Fin 3
abbrev V6 := Fin 6
abbrev V7 := Fin 7
abbrev Mat3 := Matrix V3 V3 ℝ
abbrev Vec3 := V3 → ℝ
abbrev RealFrame := Matrix (Fin 4) (Fin 4) ℝ

theorem prefixFrame_eq_homogeneousPrefix_of_stepwise
    (s : V6 → RealFrame) (r : V6 → Mat3) (p : V6 → Vec3)
    (i : V7) (h : ∀ k, s k = homogeneous (r k) (p k)) :
    prefixFrame s i = homogeneousPrefix r p i := by
  fin_cases i <;> simp [prefixFrame, homogeneousPrefix, h]

theorem routeBFrameSlot_eq_homogeneousPrefix (q : V6 → ℝ) (i : V7) :
    routeBFrameSlot q i =
      homogeneousPrefix
        (fun k => stepRotation k (q k))
        (fun k => stepTranslation k (q k)) i := by
  exact prefixFrame_eq_homogeneousPrefix_of_stepwise
    (routeBStepFunction q)
    (fun k => stepRotation k (q k))
    (fun k => stepTranslation k (q k)) i
    (fun k => routeB_step_is_homogeneous k (q k))

theorem routeBFrameSlot_origin_eq_homogeneousPrefix_origin
    (q : V6 → ℝ) (i : V7) :
    origin (routeBFrameSlot q i) =
      origin (homogeneousPrefix
        (fun k => stepRotation k (q k))
        (fun k => stepTranslation k (q k)) i) := by
  exact congrArg origin (routeBFrameSlot_eq_homogeneousPrefix q i)

theorem routeBFrameSlot_axis_eq_homogeneousPrefix_axis
    (q : V6 → ℝ) (i : V7) :
    zAxis (routeBFrameSlot q i) =
      zAxis (homogeneousPrefix
        (fun k => stepRotation k (q k))
        (fun k => stepTranslation k (q k)) i) := by
  exact congrArg zAxis (routeBFrameSlot_eq_homogeneousPrefix q i)

#print axioms prefixFrame_eq_homogeneousPrefix_of_stepwise
#print axioms routeBFrameSlot_eq_homogeneousPrefix
#print axioms routeBFrameSlot_origin_eq_homogeneousPrefix_origin
#print axioms routeBFrameSlot_axis_eq_homogeneousPrefix_axis

end
end RouteBConcretePrefixHomogeneous
