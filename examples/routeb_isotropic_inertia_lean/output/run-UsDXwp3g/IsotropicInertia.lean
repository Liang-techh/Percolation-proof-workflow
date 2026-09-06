import Mathlib

set_option autoImplicit false

namespace RouteBIsotropicInertia

noncomputable section

abbrev V := Fin 3
abbrev Mat3 := Matrix V V ℝ

def scalarIdentity (s : ℝ) : Mat3 := fun i j => if i = j then s else 0

def rotatedIsotropic (R : Mat3) (s : ℝ) : Mat3 :=
  R * scalarIdentity s * R.transpose

theorem scalarIdentity_apply (s : ℝ) (i j : V) :
    scalarIdentity s i j = if i = j then s else 0 := by
  rfl

theorem rotatedIsotropic_apply (R : Mat3) (s : ℝ) (i k : V) :
    rotatedIsotropic R s i k =
      ∑ a : V, ∑ b : V, R i a * scalarIdentity s a b * R k b := by
  simp only [rotatedIsotropic, Matrix.mul_apply, Matrix.transpose_apply]
  rfl

theorem rotated_isotropic_eq
    (R : Mat3) (s : ℝ)
    (hR : ∀ i k : V, ∑ a : V, R i a * R k a =
      if i = k then 1 else 0) :
    rotatedIsotropic R s = scalarIdentity s := by
  funext i k
  simp only [rotatedIsotropic, Matrix.mul_apply, Matrix.transpose_apply,
    scalarIdentity]
  calc
    (∑ x : V, ∑ x_1 : V, R i x * (if x = x_1 then s else 0) * R k x_1) =
        ∑ x : V, s * (R i x * R k x) := by
      apply Finset.sum_congr rfl
      intro x hx
      simp only [Finset.mul_sum]
      rw [Finset.sum_eq_single x]
      · simp [mul_assoc, mul_left_comm, mul_comm]
      · intro y hy hxy
        simp [hxy]
      · exact False.elim (by simp at hx)
    _ = s * (∑ x : V, R i x * R k x) := by
      rw [Finset.mul_sum]
    _ = s * (if i = k then 1 else 0) := by rw [hR i k]
    _ = if i = k then s else 0 := by
      by_cases h : i = k <;> simp [h]

#print axioms rotated_isotropic_eq

end
end RouteBIsotropicInertia
