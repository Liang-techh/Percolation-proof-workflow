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
  fun k => fun i j => routeBRealStepMatrix k (q k) (sourceEmbed3 i) (sourceEmbed3 j)

def stepTranslation (q : Fin 6 → ℝ) : Fin 6 → Vec3 :=
  fun k => fun i => routeBRealStepMatrix k (q k) (sourceEmbed3 i) 3

theorem routeB_step_is_homogeneous (q : Fin 6 → ℝ) (k : Fin 6) :
    routeBRealStepMatrix k (q k) =
      homogeneous (stepRotation q k) (stepTranslation q k) := by
  funext i j
  fin_cases i <;> fin_cases j <;>
    simp [stepRotation, stepTranslation, routeBRealStepMatrix,
      sourceEmbed3, realDHStep, homogeneous]

theorem routeB_frame_slot_eq_homogeneousPrefix
    (q : Fin 6 → ℝ) (i : Fin 7) :
    routeBFrameSlot q i =
      homogeneousPrefix (stepRotation q) (stepTranslation q) i := by
  fin_cases i
  · rfl
  · simp only [routeBFrameSlot, prefixFrame, homogeneousPrefix,
      routeBStepFunction, Matrix.one_mul]
    rw [routeB_step_is_homogeneous]
  · simp only [routeBFrameSlot, prefixFrame, homogeneousPrefix,
      routeBStepFunction, Matrix.one_mul]
    rw [routeB_step_is_homogeneous, routeB_step_is_homogeneous]
  · simp only [routeBFrameSlot, prefixFrame, homogeneousPrefix,
      routeBStepFunction, Matrix.one_mul]
    rw [routeB_step_is_homogeneous, routeB_step_is_homogeneous,
      routeB_step_is_homogeneous]
  · simp only [routeBFrameSlot, prefixFrame, homogeneousPrefix,
      routeBStepFunction, Matrix.one_mul]
    rw [routeB_step_is_homogeneous, routeB_step_is_homogeneous,
      routeB_step_is_homogeneous, routeB_step_is_homogeneous]
  · simp only [routeBFrameSlot, prefixFrame, homogeneousPrefix,
      routeBStepFunction, Matrix.one_mul]
    rw [routeB_step_is_homogeneous, routeB_step_is_homogeneous,
      routeB_step_is_homogeneous, routeB_step_is_homogeneous,
      routeB_step_is_homogeneous]
  · simp only [routeBFrameSlot, prefixFrame, homogeneousPrefix,
      routeBStepFunction, Matrix.one_mul]
    rw [routeB_step_is_homogeneous, routeB_step_is_homogeneous,
      routeB_step_is_homogeneous, routeB_step_is_homogeneous,
      routeB_step_is_homogeneous, routeB_step_is_homogeneous]

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
