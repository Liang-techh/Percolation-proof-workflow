import SixBodyIsotropicMass
import MassRegularizer

set_option autoImplicit false

namespace RouteBRegularizedSixBodyMass

noncomputable section

open RouteBMassFunctional
open RouteBIsotropicInertia
open RouteBSixBodyIsotropicMass
open RouteBMassRegularizer

abbrev V3 := Fin 3
abbrev V6 := Fin 6
abbrev Mat3x6 := V3 → V6 → ℝ

theorem regularized_massFromLinks_scalarIdentity
    (mass scalar : V6 → ℝ)
    (Jv Jw : V6 → Mat3x6) (i j : V6) :
    addMassRegularizer
        (massFromLinks mass Jv Jw (fun k => scalarIdentity (scalar k))) i j =
      (∑ k : V6,
        (mass k * (∑ a : V3, Jv k a i * Jv k a j) +
          scalar k * (∑ a : V3, Jw k a i * Jw k a j))) +
        if i = j then (1 / 1000000 : ℝ) else 0 := by
  rw [addMassRegularizer]
  rw [massFromLinks_scalarIdentity]

theorem regularized_massFromLinks_offdiag
    (mass scalar : V6 → ℝ)
    (Jv Jw : V6 → Mat3x6) {i j : V6} (hij : i ≠ j) :
    addMassRegularizer
        (massFromLinks mass Jv Jw (fun k => scalarIdentity (scalar k))) i j =
      ∑ k : V6,
        (mass k * (∑ a : V3, Jv k a i * Jv k a j) +
          scalar k * (∑ a : V3, Jw k a i * Jw k a j)) := by
  rw [regularized_massFromLinks_scalarIdentity]
  simp [hij]

#print axioms regularized_massFromLinks_scalarIdentity
#print axioms regularized_massFromLinks_offdiag

end
end RouteBRegularizedSixBodyMass
