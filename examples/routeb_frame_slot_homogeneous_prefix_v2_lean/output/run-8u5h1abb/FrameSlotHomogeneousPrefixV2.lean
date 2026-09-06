import ConcreteStepHomogeneous
import HomogeneousPrefixProjection
import FrameSlotAccessor

set_option autoImplicit false

namespace RouteBFrameSlotHomogeneousPrefixV2

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

/- The key shape lemma.  It transports six pointwise step equalities through
   the explicitly parenthesized seven-slot prefix, without opening Matrix
   multiplication or any concrete DH entries. -/
theorem prefixFrame_eq_homogeneousPrefix_of_step
    (s : V6 → Frame4) (r : V6 → Mat3) (p : V6 → Vec3)
    (h : ∀ k, s k = homogeneous (r k) (p k)) (i : V7) :
    prefixFrame s i = homogeneousPrefix r p i := by
  fin_cases i
  · rfl
  · rw [h 0]
  · simp only [prefixFrame, homogeneousPrefix]
    rw [h 0, h 1]
    simp
  · simp only [prefixFrame, homogeneousPrefix]
    rw [h 0, h 1, h 2]
    simp
  · simp only [prefixFrame, homogeneousPrefix]
    rw [h 0, h 1, h 2, h 3]
    simp
  · simp only [prefixFrame, homogeneousPrefix]
    rw [h 0, h 1, h 2, h 3, h 4]
    simp
  · simp only [prefixFrame, homogeneousPrefix]
    rw [h 0, h 1, h 2, h 3, h 4, h 5]
    simp

theorem routeBFrameSlot_eq_routeBHomogeneousPrefix
    (q : V6 → ℝ) (i : V7) :
    routeBFrameSlot q i = routeBHomogeneousPrefix q i := by
  exact prefixFrame_eq_homogeneousPrefix_of_step
    (routeBStepFunction q)
    (fun k => stepRotation k (q k))
    (fun k => stepTranslation k (q k))
    (fun k => routeB_step_is_homogeneous k (q k)) i

#print axioms prefixFrame_eq_homogeneousPrefix_of_step
#print axioms routeBFrameSlot_eq_routeBHomogeneousPrefix

end
end RouteBFrameSlotHomogeneousPrefixV2
