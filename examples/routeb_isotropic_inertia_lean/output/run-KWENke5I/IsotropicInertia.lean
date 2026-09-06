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

theorem rotated_isotropic_eq
    (R : Mat3) (s : ℝ)
    (hR : ∀ i k : V, ∑ a : V, R i a * R k a =
      if i = k then 1 else 0) :
    rotatedIsotropic R s = scalarIdentity s := by
  funext i k
  simp only [rotatedIsotropic, Matrix.mul_apply, Matrix.transpose_apply,
    scalarIdentity]
  calc
    (∑ j : V, (∑ a : V, R i a * (if a = j then s else 0)) * R k j) =
        ∑ j : V, ∑ a : V, (R i a * (if a = j then s else 0)) * R k j := by
      apply Finset.sum_congr rfl
      intro j hj
      simpa only using
        (Finset.sum_mul (Finset.univ : Finset V)
          (fun a : V => R i a * (if a = j then s else 0)) (R k j))
    _ = ∑ a : V, ∑ j : V, (R i a * (if a = j then s else 0)) * R k j := by
      rw [Finset.sum_comm]
    _ =
        ∑ x : V, s * (R i x * R k x) := by
      apply Finset.sum_congr rfl
      intro x hx
      rw [Finset.sum_eq_single_of_mem (a := x) (by simp)
        (fun y hy hxy => by
          simp [Ne.symm hxy])]
      simp [mul_left_comm, mul_comm]
    _ = s * (∑ x : V, R i x * R k x) := by
      rw [Finset.mul_sum]
    _ = s * (if i = k then 1 else 0) := by rw [hR i k]
    _ = if i = k then s else 0 := by
      by_cases h : i = k <;> simp [h]

#print axioms rotated_isotropic_eq

end
end RouteBIsotropicInertia
