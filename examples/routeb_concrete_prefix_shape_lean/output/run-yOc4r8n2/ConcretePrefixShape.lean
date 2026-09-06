import FramePrefixIndex
import ConcreteStepHomogeneous
import HomogeneousPrefixProjection

set_option autoImplicit false

namespace RouteBConcretePrefixShape

noncomputable section

open RouteBFramePrefixIndex
open RouteBRealDHStep
open RouteBConcreteStepHomogeneous
open RouteBHomogeneousPrefixProjection

abbrev V3 := Fin 3
abbrev V4 := Fin 4
abbrev Vec3 := V3 → ℝ
abbrev Mat3 := Matrix V3 V3 ℝ
abbrev RealFrame := Matrix V4 V4 ℝ

def concreteRotation (q : Fin 6 → ℝ) : Fin 6 → Mat3 :=
  fun k => stepRotation k (q k)

def concreteTranslation (q : Fin 6 → ℝ) : Fin 6 → Vec3 :=
  fun k => stepTranslation k (q k)

def concretePrefix (q : Fin 6 → ℝ) (i : Fin 7) : RealFrame :=
  match i.val with
  | 0 => 1
  | 1 => 1 * routeBRealStepMatrix 0 (q 0)
  | 2 => (1 * routeBRealStepMatrix 0 (q 0)) * routeBRealStepMatrix 1 (q 1)
  | 3 => ((1 * routeBRealStepMatrix 0 (q 0)) * routeBRealStepMatrix 1 (q 1)) *
      routeBRealStepMatrix 2 (q 2)
  | 4 => (((1 * routeBRealStepMatrix 0 (q 0)) * routeBRealStepMatrix 1 (q 1)) *
      routeBRealStepMatrix 2 (q 2)) * routeBRealStepMatrix 3 (q 3)
  | 5 => ((((1 * routeBRealStepMatrix 0 (q 0)) * routeBRealStepMatrix 1 (q 1)) *
      routeBRealStepMatrix 2 (q 2)) * routeBRealStepMatrix 3 (q 3)) *
      routeBRealStepMatrix 4 (q 4)
  | 6 => (((((1 * routeBRealStepMatrix 0 (q 0)) * routeBRealStepMatrix 1 (q 1)) *
      routeBRealStepMatrix 2 (q 2)) * routeBRealStepMatrix 3 (q 3)) *
      routeBRealStepMatrix 4 (q 4)) * routeBRealStepMatrix 5 (q 5)
  | _ => 1

theorem concrete_step_eq_homogeneous (q : Fin 6 → ℝ) (k : Fin 6) :
    routeBRealStepMatrix k (q k) =
      homogeneous (concreteRotation q k) (concreteTranslation q k) := by
  simpa [concreteRotation, concreteTranslation] using
    (routeBConcreteStepHomogeneous.routeB_step_is_homogeneous k (q k))

theorem concretePrefix_eq_homogeneousPrefix
    (q : Fin 6 → ℝ) (i : Fin 7) :
    concretePrefix q i =
      homogeneousPrefix (concreteRotation q) (concreteTranslation q) i := by
  fin_cases i
  · rfl
  · simp only [concretePrefix, homogeneousPrefix]
    rw [concrete_step_eq_homogeneous q 0]
  · simp only [concretePrefix, homogeneousPrefix]
    rw [concrete_step_eq_homogeneous q 0, concrete_step_eq_homogeneous q 1]
  · simp only [concretePrefix, homogeneousPrefix]
    rw [concrete_step_eq_homogeneous q 0, concrete_step_eq_homogeneous q 1,
      concrete_step_eq_homogeneous q 2]
  · simp only [concretePrefix, homogeneousPrefix]
    rw [concrete_step_eq_homogeneous q 0, concrete_step_eq_homogeneous q 1,
      concrete_step_eq_homogeneous q 2, concrete_step_eq_homogeneous q 3]
  · simp only [concretePrefix, homogeneousPrefix]
    rw [concrete_step_eq_homogeneous q 0, concrete_step_eq_homogeneous q 1,
      concrete_step_eq_homogeneous q 2, concrete_step_eq_homogeneous q 3,
      concrete_step_eq_homogeneous q 4]
  · simp only [concretePrefix, homogeneousPrefix]
    rw [concrete_step_eq_homogeneous q 0, concrete_step_eq_homogeneous q 1,
      concrete_step_eq_homogeneous q 2, concrete_step_eq_homogeneous q 3,
      concrete_step_eq_homogeneous q 4, concrete_step_eq_homogeneous q 5]

#print axioms concrete_step_eq_homogeneous
#print axioms concretePrefix_eq_homogeneousPrefix

end
end RouteBConcretePrefixShape
