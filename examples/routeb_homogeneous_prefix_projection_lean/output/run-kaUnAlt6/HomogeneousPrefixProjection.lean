import HomogeneousRotationProjection
import RotationPrefixOrthogonality

set_option autoImplicit false

namespace RouteBHomogeneousPrefixProjection

noncomputable section

open RouteBHomogeneousRotationProjection
open RouteBRotationPrefixOrthogonality

abbrev V3 := Fin 3
abbrev V4 := Fin 4
abbrev Vec3 := V3 → ℝ
abbrev Mat3 := Matrix V3 V3 ℝ
abbrev Frame4 := Matrix V4 V4 ℝ

def homogeneousPrefix (r : Fin 6 → Mat3) (p : Fin 6 → Vec3) (i : Fin 7) : Frame4 :=
  match i.val with
  | 0 => 1
  | 1 => homogeneous (r 0) (p 0)
  | 2 => homogeneous (r 0) (p 0) * homogeneous (r 1) (p 1)
  | 3 => (homogeneous (r 0) (p 0) * homogeneous (r 1) (p 1)) * homogeneous (r 2) (p 2)
  | 4 => ((homogeneous (r 0) (p 0) * homogeneous (r 1) (p 1)) * homogeneous (r 2) (p 2)) * homogeneous (r 3) (p 3)
  | 5 => (((homogeneous (r 0) (p 0) * homogeneous (r 1) (p 1)) * homogeneous (r 2) (p 2)) * homogeneous (r 3) (p 3)) * homogeneous (r 4) (p 4)
  | 6 => ((((homogeneous (r 0) (p 0) * homogeneous (r 1) (p 1)) * homogeneous (r 2) (p 2)) * homogeneous (r 3) (p 3)) * homogeneous (r 4) (p 4)) * homogeneous (r 5) (p 5)
  | _ => 1

def rotationPrefix (r : Fin 6 → Mat3) (i : Fin 7) : Mat3 :=
  prefixAt r i

theorem rotationBlock_one :
    rotationBlock (1 : Frame4) = (1 : Mat3) := by
  funext i j
  fin_cases i <;> fin_cases j <;> simp [rotationBlock, embed3]

def homogeneousMulTranslation (R : Mat3) (p : Vec3) (q : Vec3) : Vec3 :=
  p + R.mulVec q

theorem homogeneous_mul
    (R S : Mat3) (p q : Vec3) :
    homogeneous R p * homogeneous S q =
      homogeneous (R * S) (homogeneousMulTranslation R p q) := by
  funext i j
  fin_cases i <;> fin_cases j <;>
    simp [homogeneous, homogeneousMulTranslation, Matrix.mul_apply,
      Matrix.mulVec, dotProduct, Fin.sum_univ_succ] <;> ring

theorem homogeneousPrefix_rotationBlock_eq
    (r : Fin 6 → Mat3) (p : Fin 6 → Vec3) (i : Fin 7) :
    rotationBlock (homogeneousPrefix r p i) = rotationPrefix r i := by
  fin_cases i
  · simpa [homogeneousPrefix, rotationPrefix, prefixAt] using rotationBlock_one
  · simpa [homogeneousPrefix, rotationPrefix, prefixAt] using
      homogeneous_rotationBlock (r 0) (p 0)
  · simpa [homogeneousPrefix, rotationPrefix, prefixAt] using
      homogeneous_rotationBlock_mul (r 0) (r 1) (p 0) (p 1)
  · simp only [homogeneousPrefix, rotationPrefix, prefixAt]
    rw [homogeneous_mul, homogeneous_mul, homogeneous_rotationBlock]
    simp
  · simp only [homogeneousPrefix, rotationPrefix, prefixAt]
    rw [homogeneous_mul, homogeneous_mul, homogeneous_mul, homogeneous_rotationBlock]
    simp
  · simp only [homogeneousPrefix, rotationPrefix, prefixAt]
    rw [homogeneous_mul, homogeneous_mul, homogeneous_mul, homogeneous_mul,
      homogeneous_rotationBlock]
    simp
  · simp only [homogeneousPrefix, rotationPrefix, prefixAt]
    rw [homogeneous_mul, homogeneous_mul, homogeneous_mul, homogeneous_mul,
      homogeneous_mul, homogeneous_rotationBlock]
    simp

#print axioms rotationBlock_one
#print axioms homogeneousPrefix_rotationBlock_eq

end
end RouteBHomogeneousPrefixProjection
