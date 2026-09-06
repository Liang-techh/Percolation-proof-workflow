import ShiftedStorage
import PotentialSlice

open scoped BigOperators

namespace RouteBActualShift

open RouteBPotentialSlice RouteBShiftedStorage

noncomputable section

def actualKp (i : Fin 6) : ℝ := (Kp i : ℝ)

/-- Row 8 is constant and cancels from potential q - potential 0. -/
def a (i : Fin 17) : ℝ := if i = 8 then 0 else coefficient (rows i)

def phases (q : Fin 6 → ℝ) (i : Fin 17) : ℝ := phase (rows i) q

theorem constant_row_phase (q : Fin 6 → ℝ) : phases q 8 = 0 := by
  change (∑ k : Fin 6, ((![0, 0, 0, 0, 0, 0] : Fin 6 → ℤ) k : ℝ) * q k) = 0
  simp [Fin.sum_univ_succ]

theorem potential_zero_eq_sum :
    potential ![0, 0, 0, 0, 0, 0] = ∑ i : Fin 17, coefficient (rows i) := by
  unfold potential
  apply Finset.sum_congr rfl
  intro i _
  have hz : phase (rows i) ![0, 0, 0, 0, 0, 0] = 0 := by
    simp [phase, Fin.sum_univ_succ]
  rw [hz, Real.cos_zero, mul_one]

/-- Exact identity for the imported 17-row W, with the constant row removed. -/
theorem actual_W_eq_storage (q : Fin 6 → ℝ) :
    W q = storage actualKp q a (phases q) := by
  calc
    W q = proportionalEnergy q +
        ∑ i : Fin 17, (coefficient (rows i) * Real.cos (phases q i) -
          coefficient (rows i)) := by
      unfold W
      rw [potential_zero_eq_sum]
      unfold potential phases
      rw [← Finset.sum_sub_distrib]
      exact add_comm _ _
    _ = storage actualKp q a (phases q) := by
      change proportionalEnergy q + _ = proportionalEnergy q + _
      congr 1
      apply Finset.sum_congr rfl
      intro i _
      by_cases hi : i = 8
      · subst i
        simp [a, constant_row_phase]
      · simp only [a, if_neg hi]
        ring

/-- Exact rational shift: both conjugate rows counted once, row 8 excluded. -/
theorem actual_shift_exact : shift a = (4079979 / 400000 : ℝ) := by
  norm_num [shift, a, coefficient, rows, Fin.sum_univ_succ, Fin.ext_iff]

theorem actualKp_lower (i : Fin 6) : (2 / 5 : ℝ) ≤ actualKp i := by
  fin_cases i <;> norm_num [actualKp, Kp]

theorem actual_shifted_storage_chain (q : Fin 6 → ℝ) :
    proportionalEnergy q ≤ W q + (4079979 / 400000 : ℝ) ∧
      (1 / 5 : ℝ) * (∑ i, q i ^ 2) ≤ proportionalEnergy q := by
  have h := shifted_storage_chain actualKp q a (phases q) actualKp_lower
  rw [← actual_W_eq_storage q, actual_shift_exact] at h
  exact h

/-- Global coercivity for the imported exact-real Fourier storage, no premises. -/
theorem actual_W_shifted_coercivity (q : Fin 6 → ℝ) :
    (∑ i, q i ^ 2) / 5 ≤ W q + (4079979 / 400000 : ℝ) := by
  have h := actual_shifted_storage_chain q
  linarith [h.2.trans h.1]

/-- Optional composition: the only remaining assumptions are mass lower bound
and E = kinetic + the imported W. No physical mass identification is asserted. -/
theorem actual_p45_bound (q v : Fin 6 → ℝ) (M : Fin 6 → Fin 6 → ℝ) (E : ℝ)
    (hmass : (9401 / 1000000 : ℝ) * (∑ i, v i ^ 2) ≤
      ∑ i, v i * (∑ j, M i j * v j))
    (hE : E = kinetic M v + W q) :
    p45 q v ≤ (1600000 / 9401 : ℝ) * (E + (4079979 / 400000 : ℝ)) := by
  rw [actual_W_eq_storage q] at hE
  have h := fourier_p45_bound actualKp q v a (phases q) M E actualKp_lower hmass hE
  rw [actual_shift_exact] at h
  exact h

end

#print axioms constant_row_phase
#print axioms potential_zero_eq_sum
#print axioms actual_W_eq_storage
#print axioms actual_shift_exact
#print axioms actualKp_lower
#print axioms actual_shifted_storage_chain
#print axioms actual_W_shifted_coercivity
#print axioms actual_p45_bound

end RouteBActualShift
