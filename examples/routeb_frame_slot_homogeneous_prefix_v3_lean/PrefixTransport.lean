import HomogeneousPrefixProjection
import FrameSlotAccessor

set_option autoImplicit false

namespace RouteBFrameSlotHomogeneousPrefixV3

noncomputable section

open RouteBHomogeneousPrefixProjection
open RouteBHomogeneousRotationProjection
open RouteBFrameSlotAccessor

abbrev V6 := Fin 6
abbrev V7 := Fin 7
abbrev Mat3 := Matrix (Fin 3) (Fin 3) ℝ
abbrev Vec3 := (Fin 3) → ℝ
abbrev Frame4 := Matrix (Fin 4) (Fin 4) ℝ

theorem prefixFrame_eq_homogeneousPrefix_of_step
    (s : V6 → Frame4) (r : V6 → Mat3) (p : V6 → Vec3)
    (h : ∀ k, s k = homogeneous (r k) (p k)) (i : V7) :
    prefixFrame s i = homogeneousPrefix r p i := by
  fin_cases i
  · rfl
  · simp only [prefixFrame, homogeneousPrefix]
    rw [h 0]
    simp only [one_mul]
  · simp only [prefixFrame, homogeneousPrefix]
    rw [h 0, h 1]
    simp only [one_mul]
  · simp only [prefixFrame, homogeneousPrefix]
    rw [h 0, h 1, h 2]
    simp only [one_mul]
  · simp only [prefixFrame, homogeneousPrefix]
    rw [h 0, h 1, h 2, h 3]
    simp only [one_mul]
  · simp only [prefixFrame, homogeneousPrefix]
    rw [h 0, h 1, h 2, h 3, h 4]
    simp only [one_mul]
  · simp only [prefixFrame, homogeneousPrefix]
    rw [h 0, h 1, h 2, h 3, h 4, h 5]
    simp only [one_mul]

#print axioms prefixFrame_eq_homogeneousPrefix_of_step

end
end RouteBFrameSlotHomogeneousPrefixV3
