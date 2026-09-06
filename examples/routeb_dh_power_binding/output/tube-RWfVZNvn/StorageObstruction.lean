import Mathlib

namespace RouteBStorageObstruction

noncomputable def sliceEnergy (t : ℝ) : ℝ :=
  (2029689 / 400000 : ℝ) * (Real.cos t - 1) + (2 / 5 : ℝ) * t ^ 2

/- A deliberately simple rigorous bound; it suffices for strict negativity.
   The coefficient audit also has a sharper fourth-order Taylor estimate. -/
theorem cos_upper_on_unit (t : ℝ) (ht : |t| ≤ 1) :
    Real.cos t ≤ 1 - t ^ 2 / 8 := by
  have hp := Real.pi_pos
  have hp4 := Real.pi_lt_four
  have hp1 : (1 : ℝ) ≤ Real.pi := by linarith [Real.two_le_pi]
  have hcos := Real.cos_le_one_sub_mul_cos_sq (ht.trans hp1)
  have hp2 : 0 < Real.pi ^ 2 := sq_pos_of_pos hp
  have hcoef : (1 / 8 : ℝ) ≤ 2 / Real.pi ^ 2 := by
    apply (le_div_iff₀ hp2).2
    nlinarith
  have hm := mul_le_mul_of_nonneg_right hcoef (sq_nonneg t)
  nlinarith

theorem slice_energy_upper (t : ℝ) (ht : |t| ≤ 1) :
    sliceEnergy t ≤ -(749689 / 3200000 : ℝ) * t ^ 2 := by
  have hc := cos_upper_on_unit t ht
  unfold sliceEnergy
  linarith

theorem slice_energy_negative (t : ℝ) (ht : |t| ≤ 1) (hne : t ≠ 0) :
    sliceEnergy t < 0 := by
  have hu := slice_energy_upper t ht
  have hs := sq_pos_of_ne_zero hne
  nlinarith

theorem rational_configuration_negative : sliceEnergy (1 / 10 : ℝ) < 0 := by
  apply slice_energy_negative <;> norm_num

/- The coefficient/source seam remains visible: proving hslice for the full
   DH potential will transfer this obstruction without any numerical test. -/
theorem no_nonnegative_storage_of_slice
    (W : (Fin 6 → ℝ) → ℝ)
    (hslice : ∀ t, W ![0, t, 0, 0, 0, 0] = sliceEnergy t) :
    ¬ ∀ q, 0 ≤ W q := by
  intro hnonneg
  have h := hnonneg ![0, (1 / 10 : ℝ), 0, 0, 0, 0]
  rw [hslice] at h
  exact (not_lt_of_ge h) rational_configuration_negative

#print axioms cos_upper_on_unit
#print axioms slice_energy_upper
#print axioms slice_energy_negative
#print axioms rational_configuration_negative
#print axioms no_nonnegative_storage_of_slice

end RouteBStorageObstruction
