import IsotropicLinkMass

set_option autoImplicit false

namespace RouteBSixBodyIsotropicMass

noncomputable section

open RouteBMassFunctional
open RouteBIsotropicInertia
open RouteBIsotropicLinkMass

abbrev V3 := Fin 3
abbrev V6 := Fin 6
abbrev Mat3x6 := V3 → V6 → ℝ
abbrev Mat6x6 := V6 → V6 → ℝ

theorem massFromLinks_scalarIdentity
    (mass scalar : V6 → ℝ)
    (Jv Jw : V6 → Mat3x6) (i j : V6) :
    massFromLinks mass Jv Jw (fun k => scalarIdentity (scalar k)) i j =
      ∑ k : V6,
        (mass k * (∑ a : V3, Jv k a i * Jv k a j) +
          scalar k * (∑ a : V3, Jw k a i * Jw k a j)) := by
  simp only [massFromLinks]
  apply Finset.sum_congr rfl
  intro k hk
  exact linkMass_scalarIdentity (Jv k) (Jw k) (mass k) (scalar k) i j

theorem massFromLinks_scalarIdentity_congruent
    (mass scalar : V6 → ℝ)
    (Jv Jw : V6 → Mat3x6) (i j : V6)
    (hJv : ∀ k a x, Jv k a x = 0)
    (hJw : ∀ k a x, Jw k a x = 0) :
    massFromLinks mass Jv Jw (fun k => scalarIdentity (scalar k)) i j = 0 := by
  rw [massFromLinks_scalarIdentity]
  simp [hJv, hJw]

#print axioms massFromLinks_scalarIdentity
#print axioms massFromLinks_scalarIdentity_congruent

end
end RouteBSixBodyIsotropicMass
