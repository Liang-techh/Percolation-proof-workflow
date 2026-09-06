import SourceContractAdapter
import ContractMassFunctionalAdapter
import SourceMassTableMinimal

set_option autoImplicit false

namespace RouteBAgentSourceMassBinding

noncomputable section

open RouteBBodyContractCore
open RouteBBodySemanticCore
open RouteBMassFunctional
open RouteBSourceContractAdapter
open RouteBSourceMassTableMinimal

abbrev V3 := Fin 3
abbrev V6 := Fin 6
abbrev Mat3 := V3 → V3 → ℝ
abbrev Mat6 := V6 → V6 → ℝ

def sourceMass (body : V6) : ℝ := sourceMassTable body

def sourceInertia (body : V6) : Mat3 :=
  scalarIdentity (sourceInertiaScalarTable body)

def sourceBodyMass (q : V6 → ℝ) (body : V6) : Mat6 :=
  contractMass (sourceContract q) body (sourceMass body) (sourceInertia body)

def sourceMassSum (q : V6 → ℝ) : Mat6 :=
  fun i j => ∑ body : V6, sourceBodyMass q body i j

theorem source_mass_index_transport (j : RouteBFin6IndexAdapter.JuliaIndex) :
    sourceMass (RouteBFin6IndexAdapter.fromJulia j) =
      (sourceMassTable (RouteBFin6IndexAdapter.fromJulia j) : ℝ) := by
  rfl

theorem source_inertia_index_transport (j : RouteBFin6IndexAdapter.JuliaIndex) :
    sourceInertia (RouteBFin6IndexAdapter.fromJulia j) =
      scalarIdentity
        (sourceInertiaScalarTable (RouteBFin6IndexAdapter.fromJulia j)) := by
  rfl

theorem source_body_mass_eq_contract_mass
    (q : V6 → ℝ) (body : V6) :
    sourceBodyMass q body =
      contractMass (sourceContract q) body
        (sourceMassTable body)
        (scalarIdentity (sourceInertiaScalarTable body)) := by
  rfl

theorem source_mass_sum_eq_contract_mass_sum
    (q : V6 → ℝ) :
    sourceMassSum q =
      RouteBMassFunctional.massFromLinks
        (fun body => (sourceMassTable body : ℝ))
        (fun body => contractJv (sourceContract q) body)
        (fun body => contractJw (sourceContract q) body)
        (fun body => scalarIdentity (sourceInertiaScalarTable body)) := by
  funext i j
  simp only [sourceMassSum, sourceBodyMass, sourceMass, sourceInertia,
    contractMass]
  rfl

theorem minimum_functional_binding_interface
    (q : V6 → ℝ) (idealMass : V6 → Mat6)
    (hIdeal : idealMass = sourceMassSum q) :
    idealMass =
      RouteBMassFunctional.massFromLinks
        (fun body => (sourceMassTable body : ℝ))
        (fun body => contractJv (sourceContract q) body)
        (fun body => contractJw (sourceContract q) body)
        (fun body => scalarIdentity (sourceInertiaScalarTable body)) := by
  rw [hIdeal, source_mass_sum_eq_contract_mass_sum]

#print axioms source_mass_index_transport
#print axioms source_inertia_index_transport
#print axioms source_body_mass_eq_contract_mass
#print axioms source_mass_sum_eq_contract_mass_sum
#print axioms minimum_functional_binding_interface

end
end RouteBAgentSourceMassBinding
