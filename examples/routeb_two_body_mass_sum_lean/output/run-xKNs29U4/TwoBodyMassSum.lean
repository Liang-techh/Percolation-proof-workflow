import SingleBodyContractInstantiation

set_option autoImplicit false

namespace RouteBTwoBodyMassSum

noncomputable section

open RouteBBodyContractCore
open RouteBSourceContractAdapter
open RouteBSingleBodyContractInstantiation

abbrev IMat := RouteBBodyContractCore.IMat
abbrev MassMat := Mat 6 6

def block45MassSum (c : KinematicContract)
    (mass4 mass5 : ℝ) (inertia4 inertia5 : IMat) : MassMat :=
  fun i j =>
    contractMass c 3 mass4 inertia4 i j +
    contractMass c 4 mass5 inertia5 i j

theorem block45_source_mass_sum_eq_frame_mass_sum
    (q : Fin 6 → ℝ) (mass4 mass5 : ℝ)
    (inertia4 inertia5 : IMat) :
    block45MassSum (sourceContract q) mass4 mass5 inertia4 inertia5 =
      block45MassSum (frameContract q) mass4 mass5 inertia4 inertia5 := by
  funext i j
  rw [link4_source_mass_eq_frame_mass q mass4 inertia4,
      link5_source_mass_eq_frame_mass q mass5 inertia5]

theorem block45_source_mass_sum_entry
    (q : Fin 6 → ℝ) (mass4 mass5 : ℝ)
    (inertia4 inertia5 : IMat) (i j : Fin 6) :
    block45MassSum (sourceContract q) mass4 mass5 inertia4 inertia5 i j =
      contractMass (sourceContract q) 3 mass4 inertia4 i j +
      contractMass (sourceContract q) 4 mass5 inertia5 i j := by
  rfl

#print axioms block45_source_mass_sum_eq_frame_mass_sum
#print axioms block45_source_mass_sum_entry

end
end RouteBTwoBodyMassSum
