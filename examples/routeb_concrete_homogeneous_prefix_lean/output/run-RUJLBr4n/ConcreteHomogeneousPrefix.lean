import FrameSlotAccessor
import HomogeneousPrefixProjection

set_option autoImplicit false

namespace RouteBConcreteHomogeneousPrefix

noncomputable section

open RouteBFrameSlotAccessor
open RouteBRealDHStep
open RouteBHomogeneousRotationProjection
open RouteBHomogeneousPrefixProjection

abbrev V3 := Fin 3
abbrev V4 := Fin 4
abbrev Vec3 := V3 → ℝ
abbrev Mat3 := Matrix V3 V3 ℝ
abbrev RealFrame := Matrix V4 V4 ℝ

def sourceEmbed3 (i : V3) : V4 :=
  ⟨i.val, by omega⟩

def stepRotation (q : Fin 6 → ℝ) : Fin 6 → Mat3 :=
  fun k => fun i j => routeBRealStepMatrix k (q k)
    (RouteBHomogeneousRotationProjection.embed3 i)
    (RouteBHomogeneousRotationProjection.embed3 j)

def stepTranslation (q : Fin 6 → ℝ) : Fin 6 → Vec3 :=
  fun k => fun i => routeBRealStepMatrix k (q k)
    (RouteBHomogeneousRotationProjection.embed3 i) 3

theorem frame_eq_homogeneous
    (F : RealFrame) (R : Mat3) (p : Vec3)
    (hR : ∀ i j, F (RouteBHomogeneousRotationProjection.embed3 i)
      (RouteBHomogeneousRotationProjection.embed3 j) = R i j)
    (hp : ∀ i, F (RouteBHomogeneousRotationProjection.embed3 i) 3 = p i)
    (hbot : ∀ j : Fin 4, F 3 j = if j.val = 3 then 1 else 0) :
    F = homogeneous R p := by
  funext i j
  fin_cases i <;> fin_cases j <;>
    simp [homogeneous, hR, hp, hbot,
      RouteBHomogeneousRotationProjection.embed3]

theorem routeB_step_is_homogeneous (q : Fin 6 → ℝ) (k : Fin 6) :
    routeBRealStepMatrix k (q k) =
      homogeneous (stepRotation q k) (stepTranslation q k) := by
  apply frame_eq_homogeneous
  · intro i j
    rfl
  · intro i
    rfl
  · intro j
    fin_cases j <;> simp [routeBRealStepMatrix, realDHStep]

theorem routeB_frame_slot_eq_homogeneousPrefix
    (q : Fin 6 → ℝ) (i : Fin 7) :
    routeBFrameSlot q i =
      homogeneousPrefix (stepRotation q) (stepTranslation q) i := by
  fin_cases i
  · rfl
  · simp only [routeBFrameSlot, prefixFrame, homogeneousPrefix,
      routeBStepFunction, Matrix.one_mul]
    rw [routeB_step_is_homogeneous q 0]
  · simp only [routeBFrameSlot, prefixFrame, homogeneousPrefix,
      routeBStepFunction, Matrix.one_mul]
    rw [routeB_step_is_homogeneous q 0, routeB_step_is_homogeneous q 1]
  · simp only [routeBFrameSlot, prefixFrame, homogeneousPrefix,
      routeBStepFunction, Matrix.one_mul]
    rw [routeB_step_is_homogeneous q 0, routeB_step_is_homogeneous q 1,
      routeB_step_is_homogeneous q 2]
  · simp only [routeBFrameSlot, prefixFrame, homogeneousPrefix,
      routeBStepFunction, Matrix.one_mul]
    rw [routeB_step_is_homogeneous q 0, routeB_step_is_homogeneous q 1,
      routeB_step_is_homogeneous q 2, routeB_step_is_homogeneous q 3]
  · simp only [routeBFrameSlot, prefixFrame, homogeneousPrefix,
      routeBStepFunction, Matrix.one_mul]
    rw [routeB_step_is_homogeneous q 0, routeB_step_is_homogeneous q 1,
      routeB_step_is_homogeneous q 2, routeB_step_is_homogeneous q 3,
      routeB_step_is_homogeneous q 4]
  · simp only [routeBFrameSlot, prefixFrame, homogeneousPrefix,
      routeBStepFunction, Matrix.one_mul]
    rw [routeB_step_is_homogeneous q 0, routeB_step_is_homogeneous q 1,
      routeB_step_is_homogeneous q 2, routeB_step_is_homogeneous q 3,
      routeB_step_is_homogeneous q 4, routeB_step_is_homogeneous q 5]

theorem routeB_frame_slot_rotationBlock_eq_rotationPrefix
    (q : Fin 6 → ℝ) (i : Fin 7) :
    rotationBlock (routeBFrameSlot q i) =
      rotationPrefix (stepRotation q) i := by
  rw [routeB_frame_slot_eq_homogeneousPrefix]
  exact homogeneousPrefix_rotationBlock_eq (stepRotation q) (stepTranslation q) i

#print axioms routeB_step_is_homogeneous
#print axioms routeB_frame_slot_eq_homogeneousPrefix
#print axioms routeB_frame_slot_rotationBlock_eq_rotationPrefix

end
end RouteBConcreteHomogeneousPrefix
