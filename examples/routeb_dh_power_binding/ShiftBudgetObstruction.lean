import StorageObstruction

namespace RouteBShiftBudgetObstruction

open RouteBStorageObstruction

/- Even optimizing the constant shift cannot rescue THIS coarse comparison
   factor. This is not an impossibility theorem for the original dynamics. -/
theorem shift_lower_of_slice_nonnegative (C : ℝ)
    (hshift : ∀ t, 0 ≤ sliceEnergy t + C) :
    (749689 / 3200000 : ℝ) ≤ C := by
  have h := hshift 1
  have hu := slice_energy_upper 1 (by norm_num)
  norm_num at hu
  linarith

theorem shift_lower_of_storage_nonnegative
    (W : (Fin 6 → ℝ) → ℝ) (C : ℝ)
    (hslice : ∀ t, W ![0, t, 0, 0, 0, 0] = sliceEnergy t)
    (hshift : ∀ q, 0 ≤ W q + C) :
    (749689 / 3200000 : ℝ) ≤ C := by
  apply shift_lower_of_slice_nonnegative C
  intro t
  have h := hshift ![0, t, 0, 0, 0, 0]
  rwa [hslice] at h

theorem coarse_budget_exceeds_target (C Ecap : ℝ)
    (hC : (749689 / 3200000 : ℝ) ≤ C) (hcap : 0 ≤ Ecap) :
    (28 / 5 : ℝ) < (1600000 / 9401 : ℝ) * (Ecap + C) := by
  linarith

theorem no_coarse_terminal_budget (W : (Fin 6 → ℝ) → ℝ) (C Ecap : ℝ)
    (hslice : ∀ t, W ![0, t, 0, 0, 0, 0] = sliceEnergy t)
    (hshift : ∀ q, 0 ≤ W q + C) (hcap : 0 ≤ Ecap) :
    ¬ (1600000 / 9401 : ℝ) * (Ecap + C) ≤ (28 / 5 : ℝ) := by
  exact not_le_of_gt (coarse_budget_exceeds_target C Ecap
    (shift_lower_of_storage_nonnegative W C hslice hshift) hcap)

#print axioms shift_lower_of_slice_nonnegative
#print axioms shift_lower_of_storage_nonnegative
#print axioms coarse_budget_exceeds_target
#print axioms no_coarse_terminal_budget

end RouteBShiftBudgetObstruction
