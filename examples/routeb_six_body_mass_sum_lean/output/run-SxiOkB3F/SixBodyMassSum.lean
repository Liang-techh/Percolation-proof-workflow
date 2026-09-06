import SourceContractAdapter

set_option autoImplicit false

namespace RouteBSixBodyMassSum

noncomputable section

open RouteBBodySemanticCore
open RouteBBodyContractCore
open RouteBSourceContractAdapter

abbrev IMat := RouteBBodyContractCore.IMat
abbrev MassMat := RouteBBodySemanticCore.Mat 6 6

def sixBodyMassSum (c : KinematicContract)
    (m : Fin 6 → ℝ) (inertia : Fin 6 → IMat) : MassMat :=
  fun i j => ∑ body : Fin 6, contractMass c body (m body) (inertia body) i j

theorem source_six_body_mass_sum_eq_frame_six_body_mass_sum
    (q : Fin 6 → ℝ) (m : Fin 6 → ℝ) (inertia : Fin 6 → IMat) :
    sixBodyMassSum (sourceContract q) m inertia =
      sixBodyMassSum (frameContract q) m inertia := by
  funext i j
  apply Finset.sum_congr rfl
  intro body hbody
  have h := source_contract_body_mass_eq_frame_contract_body_mass q body
    (m body) (inertia body)
  exact congrArg (fun M : MassMat => M i j) h

theorem six_body_mass_sum_entry
    (c : KinematicContract) (m : Fin 6 → ℝ)
    (inertia : Fin 6 → IMat) (i j : Fin 6) :
    sixBodyMassSum c m inertia i j =
      ∑ body : Fin 6, contractMass c body (m body) (inertia body) i j := by
  rfl

#print axioms source_six_body_mass_sum_eq_frame_six_body_mass_sum
#print axioms six_body_mass_sum_entry

end
end RouteBSixBodyMassSum
