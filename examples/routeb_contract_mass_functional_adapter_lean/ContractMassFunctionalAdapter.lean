import BodyContractCore
import MassFunctional

set_option autoImplicit false

namespace RouteBContractMassFunctionalAdapter

noncomputable section

open RouteBBodyContractCore
open RouteBBodySemanticCore
open RouteBMassFunctional

abbrev V3 := Fin 3
abbrev V6 := Fin 6
abbrev Mat3x6 := V3 → V6 → ℝ
abbrev Mat3x3 := V3 → V3 → ℝ
abbrev Mat6x6 := V6 → V6 → ℝ

theorem semantic_linkMass_eq_functional_linkMass
    (Jv Jw : Mat3x6) (mass : ℝ) (inertia : Mat3x3) :
    RouteBBodySemanticCore.linkMass Jv Jw mass inertia =
      RouteBMassFunctional.linkMass Jv Jw mass inertia := by
  rfl

theorem contractMass_eq_functional_linkMass
    (c : KinematicContract) (body : V6) (mass : ℝ) (inertia : Mat3x3) :
    contractMass c body mass inertia =
      RouteBMassFunctional.linkMass (contractJv c body) (contractJw c body)
        mass inertia := by
  rfl

def contractMassSum
    (c : KinematicContract) (mass : V6 → ℝ) (inertia : V6 → Mat3x3) : Mat6x6 :=
  fun i j => ∑ body : V6, contractMass c body (mass body) (inertia body) i j

theorem contractMassSum_eq_massFromLinks
    (c : KinematicContract) (mass : V6 → ℝ) (inertia : V6 → Mat3x3) :
    contractMassSum c mass inertia =
      RouteBMassFunctional.massFromLinks mass
        (fun body => contractJv c body)
        (fun body => contractJw c body) inertia := by
  rfl

#print axioms semantic_linkMass_eq_functional_linkMass
#print axioms contractMass_eq_functional_linkMass
#print axioms contractMassSum_eq_massFromLinks

end
end RouteBContractMassFunctionalAdapter
