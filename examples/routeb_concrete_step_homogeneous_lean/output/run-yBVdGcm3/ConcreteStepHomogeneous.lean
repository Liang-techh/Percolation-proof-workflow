import RealDHStep
import HomogeneousRotationProjection

set_option autoImplicit false

namespace RouteBConcreteStepHomogeneous

noncomputable section

open RouteBRealDHStep
open RouteBHomogeneousRotationProjection

abbrev V3 := Fin 3
abbrev V4 := Fin 4
abbrev Vec3 := V3 → ℝ
abbrev Mat3 := Matrix V3 V3 ℝ
abbrev RealFrame := Matrix V4 V4 ℝ

def stepRotation (k : Fin 6) (q : ℝ) : Mat3 :=
  fun i j => routeBRealStepMatrix k q (embed3 i) (embed3 j)

def stepTranslation (k : Fin 6) (q : ℝ) : Vec3 :=
  fun i => routeBRealStepMatrix k q (embed3 i) 3

theorem frame_eq_homogeneous
    (F : RealFrame) (R : Mat3) (p : Vec3)
    (hR : ∀ i j, F (embed3 i) (embed3 j) = R i j)
    (hp : ∀ i, F (embed3 i) 3 = p i)
    (hbot : ∀ j : Fin 4, F 3 j = if j.val = 3 then 1 else 0) :
    F = homogeneous R p := by
  funext i j
  fin_cases i <;> fin_cases j
  · exact hR 0 0
  · exact hR 0 1
  · exact hR 0 2
  · exact hp 0
  · exact hR 1 0
  · exact hR 1 1
  · exact hR 1 2
  · exact hp 1
  · exact hR 2 0
  · exact hR 2 1
  · exact hR 2 2
  · exact hp 2
  · simpa [homogeneous] using hbot 0
  · simpa [homogeneous] using hbot 1
  · simpa [homogeneous] using hbot 2
  · simpa [homogeneous] using hbot 3

theorem routeB_step_is_homogeneous (k : Fin 6) (q : ℝ) :
    routeBRealStepMatrix k q =
      homogeneous (stepRotation k q) (stepTranslation k q) := by
  apply frame_eq_homogeneous
  · intro i j
    rfl
  · intro i
    rfl
  · intro j
    fin_cases j <;> simp [routeBRealStepMatrix, realDHStep]

#print axioms frame_eq_homogeneous
#print axioms routeB_step_is_homogeneous

end
end RouteBConcreteStepHomogeneous
