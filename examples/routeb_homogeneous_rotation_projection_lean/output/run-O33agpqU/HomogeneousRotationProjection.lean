import Mathlib

set_option autoImplicit false

namespace RouteBHomogeneousRotationProjection

noncomputable section

abbrev V3 := Fin 3
abbrev V4 := Fin 4
abbrev Vec3 := V3 → ℝ
abbrev Mat3 := Matrix V3 V3 ℝ
abbrev Frame4 := Matrix V4 V4 ℝ

def embed3 (i : V3) : V4 := ⟨i.val, by omega⟩

def rotationBlock (F : Frame4) : Mat3 :=
  fun i j => F (embed3 i) (embed3 j)

def homogeneous (R : Mat3) (p : Vec3) : Frame4 := fun i j =>
  if hi : i.val < 3 then
    if hj : j.val < 3 then R ⟨i.val, hi⟩ ⟨j.val, hj⟩
    else if j.val = 3 then p ⟨i.val, hi⟩ else 0
  else if i.val = 3 then if j.val = 3 then 1 else 0 else 0

theorem homogeneous_rotationBlock (R : Mat3) (p : Vec3) :
    rotationBlock (homogeneous R p) = R := by
  funext i j
  simp [rotationBlock, embed3, homogeneous]

theorem homogeneous_rotationBlock_mul
    (R S : Mat3) (p q : Vec3) :
    rotationBlock (homogeneous R p * homogeneous S q) = R * S := by
  funext i j
  fin_cases i <;> fin_cases j <;>
    simp [rotationBlock, embed3, homogeneous, Matrix.mul_apply,
      Fin.sum_univ_succ]

#print axioms homogeneous_rotationBlock
#print axioms homogeneous_rotationBlock_mul

end
end RouteBHomogeneousRotationProjection
