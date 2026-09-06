import SourceContractAdapter

set_option autoImplicit false

namespace RouteBSingleBodyContractInstantiation

noncomputable section

open RouteBBodySemanticCore
open RouteBBodyContractCore
open RouteBSourceContractAdapter

abbrev IMat := RouteBBodyContractCore.IMat

theorem link4_source_cutoff (q : Fin 6 → ℝ) (a : Fin 3) :
    contractJv (sourceContract q) 3 a 4 = 0 := by
  exact block45_contract_link4_cutoff (sourceContract q) a

theorem link5_source_active (q : Fin 6 → ℝ) (a : Fin 3) :
    contractJv (sourceContract q) 4 a 4 =
      cross3 ((sourceContract q).axes 4) (fun b =>
        bodyCom (sourceContract q).origins 4 b -
          (sourceContract q).origins (prevOrigin 4) b) a := by
  exact block45_contract_link5_active (sourceContract q) a

theorem link4_source_mass_eq_frame_mass
    (q : Fin 6 → ℝ) (mass : ℝ) (inertia : IMat) :
    contractMass (sourceContract q) 3 mass inertia =
      contractMass (frameContract q) 3 mass inertia := by
  exact source_contract_body_mass_eq_frame_contract_body_mass q 3 mass inertia

theorem link5_source_mass_eq_frame_mass
    (q : Fin 6 → ℝ) (mass : ℝ) (inertia : IMat) :
    contractMass (sourceContract q) 4 mass inertia =
      contractMass (frameContract q) 4 mass inertia := by
  exact source_contract_body_mass_eq_frame_contract_body_mass q 4 mass inertia

#print axioms link4_source_cutoff
#print axioms link5_source_active
#print axioms link4_source_mass_eq_frame_mass
#print axioms link5_source_mass_eq_frame_mass

end
end RouteBSingleBodyContractInstantiation
