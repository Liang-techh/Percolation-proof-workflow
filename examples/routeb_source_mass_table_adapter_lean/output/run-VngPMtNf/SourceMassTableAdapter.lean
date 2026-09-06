import SourceContractAdapter
import ContractMassFunctionalAdapter
import RegularizedSixBodyMass

set_option autoImplicit false

namespace RouteBSourceMassTableAdapter

noncomputable section

open RouteBBodySemanticCore
open RouteBBodyContractCore
open RouteBSourceContractAdapter
open RouteBContractMassFunctionalAdapter
open RouteBMassFunctional
open RouteBIsotropicInertia
open RouteBMassRegularizer
open RouteBRegularizedSixBodyMass

abbrev V3 := Fin 3
abbrev V6 := Fin 6
abbrev Mat3x3 := V3 → V3 → ℝ
abbrev Mat6x6 := V6 → V6 → ℝ

def sourceMassTable : V6 → ℝ :=
  ![1, 4 / 5, 3 / 5, 2 / 5, 3 / 10, 3 / 20]

def sourceInertiaScalarTable : V6 → ℝ :=
  ![1 / 3, 1 / 5, 7 / 60, 1 / 15, 1 / 30, 1 / 60]

def sourceInertiaTable : V6 → Mat3x3 :=
  fun body => scalarIdentity (sourceInertiaScalarTable body)

def sourceContractMass : (V6 → ℝ) → Mat6x6 :=
  fun q =>
    addMassRegularizer
      (contractMassSum (sourceContract q) sourceMassTable sourceInertiaTable)

theorem sourceContractMass_eq_regularized_generic
    (q : V6 → ℝ) :
    sourceContractMass q =
      addMassRegularizer
        (massFromLinks sourceMassTable
          (fun body => contractJv (sourceContract q) body)
          (fun body => contractJw (sourceContract q) body)
          sourceInertiaTable) := by
  unfold sourceContractMass
  rw [contractMassSum_eq_massFromLinks]

theorem sourceContractMass_entry
    (q : V6 → ℝ) (i j : V6) :
    sourceContractMass q i j =
      (∑ body : V6,
        (sourceMassTable body *
          (∑ a : V3,
            (contractJv (sourceContract q) body) a i *
              (contractJv (sourceContract q) body) a j) +
         sourceInertiaScalarTable body *
          (∑ a : V3,
            (contractJw (sourceContract q) body) a i *
              (contractJw (sourceContract q) body) a j))) +
      if i = j then (1 / 1000000 : ℝ) else 0 := by
  rw [sourceContractMass_eq_regularized_generic]
  simpa [sourceInertiaTable] using
    (regularized_massFromLinks_scalarIdentity
      sourceMassTable sourceInertiaScalarTable
      (fun body => contractJv (sourceContract q) body)
      (fun body => contractJw (sourceContract q) body) i j)

#print axioms sourceContractMass_eq_regularized_generic
#print axioms sourceContractMass_entry

end
end RouteBSourceMassTableAdapter
