import Mathlib

set_option autoImplicit false

namespace RouteBMassRegularizer

noncomputable section

abbrev Mat (n : ℕ) := Fin n → Fin n → ℝ
abbrev Vec (n : ℕ) := Fin n → ℝ

def addMassRegularizer (M : Mat 6) : Mat 6 :=
  fun i j => M i j + if i = j then (1 / 1000000 : ℝ) else 0

theorem addMassRegularizer_diag (M : Mat 6) (i : Fin 6) :
    addMassRegularizer M i i = M i i + (1 / 1000000 : ℝ) := by
  simp [addMassRegularizer]

theorem addMassRegularizer_offdiag (M : Mat 6) {i j : Fin 6} (hij : i ≠ j) :
    addMassRegularizer M i j = M i j := by
  simp [addMassRegularizer, hij]

theorem regularized_entry (q : Vec 6) (i j : Fin 6)
    (unregularizedDHMass evalFourierMass : Vec 6 → Mat 6)
    (h_unreg : unregularizedDHMass q i j = evalFourierMass q i j) :
    addMassRegularizer (unregularizedDHMass q) i j =
      evalFourierMass q i j + if i = j then (1 / 1000000 : ℝ) else 0 := by
  simp [addMassRegularizer, h_unreg]

theorem regularizer_is_constant (M : Mat 6) (i j : Fin 6) :
    addMassRegularizer M i j - M i j =
      if i = j then (1 / 1000000 : ℝ) else 0 := by
  simp [addMassRegularizer]

theorem regularizer_offdiag_derivative (M : Mat 6) {i j : Fin 6} (hij : i ≠ j) :
    addMassRegularizer M i j - M i j = 0 := by
  simp [addMassRegularizer, hij]

end
end RouteBMassRegularizer

#print axioms RouteBMassRegularizer.addMassRegularizer_diag
#print axioms RouteBMassRegularizer.addMassRegularizer_offdiag
#print axioms RouteBMassRegularizer.regularized_entry
#print axioms RouteBMassRegularizer.regularizer_is_constant
#print axioms RouteBMassRegularizer.regularizer_offdiag_derivative
