import MassFunctional
import IsotropicInertia

set_option autoImplicit false

namespace RouteBIsotropicLinkMass

noncomputable section

open RouteBMassFunctional
open RouteBIsotropicInertia

abbrev V3 := Fin 3
abbrev V6 := Fin 6
abbrev Mat3x6 := V3 → V6 → ℝ
abbrev Mat6x6 := V6 → V6 → ℝ

theorem weightedGram_scalarIdentity
    (J : Mat3x6) (scalar : ℝ) (i j : V6) :
    weightedGram J (scalarIdentity scalar) i j =
      scalar * (∑ a : V3, J a i * J a j) := by
  simp only [weightedGram, scalarIdentity]
  calc
    (∑ a : V3, ∑ b : V3, J a i * (if a = b then scalar else 0) * J b j) =
        ∑ a : V3, ∑ b : V3, (J a i * (if a = b then scalar else 0)) * J b j := by
      rfl
    _ = ∑ a : V3, scalar * (J a i * J a j) := by
      apply Finset.sum_congr rfl
      intro a ha
      rw [Finset.sum_eq_single_of_mem (a := a) (by simp)
        (fun b hb hab => by simp [Ne.symm hab])]
      simp [mul_left_comm, mul_comm, mul_assoc]
    _ = scalar * (∑ a : V3, J a i * J a j) := by
      rw [Finset.mul_sum]

theorem linkMass_scalarIdentity
    (Jv Jw : Mat3x6) (mass scalar : ℝ) (i j : V6) :
    linkMass Jv Jw mass (scalarIdentity scalar) i j =
      mass * (∑ a : V3, Jv a i * Jv a j) +
        scalar * (∑ a : V3, Jw a i * Jw a j) := by
  rw [linkMass, weightedGram_scalarIdentity]

#print axioms weightedGram_scalarIdentity

end
end RouteBIsotropicLinkMass
