import StorageObstruction

open scoped BigOperators

namespace RouteBPotentialSlice

/- Canonical cosine encoding of the 17 CSV rows, in their original order.
   Both conjugates are retained. No physical-DH identification is asserted. -/
structure FourierRow where
  frequency : Fin 6 → ℤ
  realNum : ℤ
  realDen : ℕ
  imagNum : ℤ
  imagDen : ℕ

def rows : Fin 17 → FourierRow := ![
  ⟨![0, -1, -1, -1, -1, 0], 20601, 3200000, 0, 1⟩,
  ⟨![0, -1, -1, -1, 1, 0], -20601, 3200000, 0, 1⟩,
  ⟨![0, -1, -1, 0, -1, 0], 20601, 1600000, 0, 1⟩,
  ⟨![0, -1, -1, 0, 0, 0], 242307, 400000, 0, 1⟩,
  ⟨![0, -1, -1, 0, 1, 0], 20601, 1600000, 0, 1⟩,
  ⟨![0, -1, -1, 1, -1, 0], 20601, 3200000, 0, 1⟩,
  ⟨![0, -1, -1, 1, 1, 0], -20601, 3200000, 0, 1⟩,
  ⟨![0, -1, 0, 0, 0, 0], 762237, 400000, 0, 1⟩,
  ⟨![0, 0, 0, 0, 0, 0], 10791, 4000, 0, 1⟩,
  ⟨![0, 1, 0, 0, 0, 0], 762237, 400000, 0, 1⟩,
  ⟨![0, 1, 1, -1, -1, 0], -20601, 3200000, 0, 1⟩,
  ⟨![0, 1, 1, -1, 1, 0], 20601, 3200000, 0, 1⟩,
  ⟨![0, 1, 1, 0, -1, 0], 20601, 1600000, 0, 1⟩,
  ⟨![0, 1, 1, 0, 0, 0], 242307, 400000, 0, 1⟩,
  ⟨![0, 1, 1, 0, 1, 0], 20601, 1600000, 0, 1⟩,
  ⟨![0, 1, 1, 1, -1, 0], -20601, 3200000, 0, 1⟩,
  ⟨![0, 1, 1, 1, 1, 0], 20601, 3200000, 0, 1⟩]

def Kp : Fin 6 → ℚ := ![1, 4/5, 7/10, 3/5, 1/2, 2/5]

theorem row_count : Fintype.card (Fin 17) = 17 := by decide

theorem all_imaginary_parts_zero : ∀ i, (rows i).imagNum = 0 := by
  intro i
  fin_cases i <;> norm_num [rows]

theorem all_denominators_positive :
    ∀ i, 0 < (rows i).realDen ∧ 0 < (rows i).imagDen := by
  intro i
  fin_cases i <;> norm_num [rows]

noncomputable def coefficient (r : FourierRow) : ℝ :=
  (r.realNum : ℝ) / (r.realDen : ℝ)

noncomputable def phase (r : FourierRow) (q : Fin 6 → ℝ) : ℝ :=
  ∑ k, (r.frequency k : ℝ) * q k

noncomputable def potential (q : Fin 6 → ℝ) : ℝ :=
  ∑ i : Fin 17, coefficient (rows i) * Real.cos (phase (rows i) q)

noncomputable def proportionalEnergy (q : Fin 6 → ℝ) : ℝ :=
  (1 / 2 : ℝ) * ∑ k, (Kp k : ℝ) * q k ^ 2

noncomputable def W (q : Fin 6 → ℝ) : ℝ :=
  potential q - potential ![0, 0, 0, 0, 0, 0] + proportionalEnergy q

theorem potential_on_slice (t : ℝ) :
    potential ![0, t, 0, 0, 0, 0] =
      (10791 / 4000 : ℝ) + (2029689 / 400000 : ℝ) * Real.cos t := by
  norm_num [potential, rows, coefficient, phase, Fin.sum_univ_succ, Real.cos_neg]
  ring

theorem potential_at_zero :
    potential ![0, 0, 0, 0, 0, 0] = (3108789 / 400000 : ℝ) := by
  have h := potential_on_slice (0 : ℝ)
  norm_num at h ⊢
  exact h

theorem proportional_energy_on_slice (t : ℝ) :
    proportionalEnergy ![0, t, 0, 0, 0, 0] = (2 / 5 : ℝ) * t ^ 2 := by
  norm_num [proportionalEnergy, Kp, Fin.sum_univ_succ]
  ring

theorem W_on_slice (t : ℝ) :
    W ![0, t, 0, 0, 0, 0] = RouteBStorageObstruction.sliceEnergy t := by
  rw [W, potential_on_slice, potential_at_zero, proportional_energy_on_slice]
  unfold RouteBStorageObstruction.sliceEnergy
  ring

theorem no_global_nonnegative_W : ¬ ∀ q, 0 ≤ W q :=
  RouteBStorageObstruction.no_nonnegative_storage_of_slice W W_on_slice

theorem rational_configuration_negative : W ![0, (1 / 10 : ℝ), 0, 0, 0, 0] < 0 := by
  rw [W_on_slice]
  exact RouteBStorageObstruction.rational_configuration_negative

#print axioms row_count
#print axioms all_imaginary_parts_zero
#print axioms all_denominators_positive
#print axioms potential_on_slice
#print axioms potential_at_zero
#print axioms proportional_energy_on_slice
#print axioms W_on_slice
#print axioms no_global_nonnegative_W
#print axioms rational_configuration_negative

end RouteBPotentialSlice
