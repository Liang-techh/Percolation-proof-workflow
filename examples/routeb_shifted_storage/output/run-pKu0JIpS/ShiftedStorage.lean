import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-! Finite Fourier storage with an explicit constant shift.
All coefficient/phase and mass identifications remain explicit parameters.
No coefficient table, target module, or numerical certificate is imported. -/

open scoped BigOperators

namespace RouteBShiftedStorage

noncomputable section

variable {ι ν : Type*} [Fintype ι] [Fintype ν]

def quadraticStorage (kp q : ι → ℝ) : ℝ :=
  (1 / 2 : ℝ) * ∑ i, kp i * q i ^ 2

def storage (kp q : ι → ℝ) (a phase : ν → ℝ) : ℝ :=
  quadraticStorage kp q + ∑ n, a n * (Real.cos (phase n) - 1)

def shift (a : ν → ℝ) : ℝ := 2 * ∑ n, max (a n) 0

/-- A negative Fourier coefficient needs no downward-offset budget. -/
theorem shifted_cos_term_nonneg (a phase : ℝ) :
    0 ≤ a * (Real.cos phase - 1) + 2 * max a 0 := by
  have hlo := Real.neg_one_le_cos phase
  have hhi := Real.cos_le_one phase
  by_cases ha : 0 ≤ a
  · rw [max_eq_left ha]
    nlinarith [mul_nonneg ha (show 0 ≤ Real.cos phase + 1 by linarith)]
  · have ha' : a ≤ 0 := le_of_not_ge ha
    rw [max_eq_right ha']
    nlinarith [mul_nonneg (neg_nonneg.mpr ha')
      (show 0 ≤ 1 - Real.cos phase by linarith)]

theorem shift_nonneg (a : ν → ℝ) : 0 ≤ shift a := by
  unfold shift
  exact mul_nonneg (by norm_num) (Finset.sum_nonneg fun n _ => le_max_right (a n) 0)

/-- The first bound holds for arbitrary gains, even negative gains. -/
theorem quadratic_le_shifted_storage (kp q : ι → ℝ) (a phase : ν → ℝ) :
    quadraticStorage kp q ≤ storage kp q a phase + shift a := by
  have h := Finset.sum_nonneg (s := Finset.univ)
    (fun n _ => shifted_cos_term_nonneg (a n) (phase n))
  simp only [Finset.sum_add_distrib, ← Finset.mul_sum] at h
  unfold storage shift
  linarith

theorem quadratic_coercivity (kp q : ι → ℝ)
    (hkp : ∀ i, (2 / 5 : ℝ) ≤ kp i) :
    (1 / 5 : ℝ) * (∑ i, q i ^ 2) ≤ quadraticStorage kp q := by
  have h := Finset.sum_le_sum (s := Finset.univ)
    (fun i _ => mul_le_mul_of_nonneg_right (hkp i) (sq_nonneg (q i)))
  rw [← Finset.mul_sum] at h
  unfold quadraticStorage
  linarith

/-- Both links in the requested inequality, with no assumption on phases. -/
theorem shifted_storage_chain (kp q : ι → ℝ) (a phase : ν → ℝ)
    (hkp : ∀ i, (2 / 5 : ℝ) ≤ kp i) :
    quadraticStorage kp q ≤ storage kp q a phase + shift a ∧
      (1 / 5 : ℝ) * (∑ i, q i ^ 2) ≤ quadraticStorage kp q :=
  ⟨quadratic_le_shifted_storage kp q a phase, quadratic_coercivity kp q hkp⟩

theorem shifted_storage_coercivity (kp q : ι → ℝ) (a phase : ν → ℝ)
    (hkp : ∀ i, (2 / 5 : ℝ) ≤ kp i) :
    (1 / 5 : ℝ) * (∑ i, q i ^ 2) ≤ storage kp q a phase + shift a :=
  (quadratic_coercivity kp q hkp).trans (quadratic_le_shifted_storage kp q a phase)

def kinetic (M : ι → ι → ℝ) (v : ι → ℝ) : ℝ :=
  (1 / 2 : ℝ) * ∑ i, v i * (∑ j, M i j * v j)

/-- Pointwise mass lower bound and energy decomposition are explicit premises.
Symmetry of M is not needed for this algebraic implication. -/
theorem shifted_energy_lower (kp q v : ι → ℝ) (a phase : ν → ℝ)
    (M : ι → ι → ℝ) (E μ : ℝ)
    (hkp : ∀ i, (2 / 5 : ℝ) ≤ kp i)
    (hmass : μ * (∑ i, v i ^ 2) ≤ ∑ i, v i * (∑ j, M i j * v j))
    (hE : E = kinetic M v + storage kp q a phase) :
    (μ / 2) * (∑ i, v i ^ 2) + (1 / 5 : ℝ) * (∑ i, q i ^ 2) ≤
      E + shift a := by
  have hW := shifted_storage_coercivity kp q a phase hkp
  unfold kinetic at hE
  linarith

/-- Joint numbers 4 and 5 are Lean indices 3 and 4. Exact target weights:
3/2 for configuration squares, 4/5 for velocity squares. -/
def p45 (q v : Fin 6 → ℝ) : ℝ :=
  (3 / 2 : ℝ) * (q 3 ^ 2 + q 4 ^ 2) + (4 / 5 : ℝ) * (v 3 ^ 2 + v 4 ^ 2)

theorem block45_sq_le_total (x : Fin 6 → ℝ) :
    x 3 ^ 2 + x 4 ^ 2 ≤ ∑ i, x i ^ 2 := by
  have h := Finset.sum_le_sum_of_subset_of_nonneg (f := fun i => x i ^ 2)
    (Finset.subset_univ ({3, 4} : Finset (Fin 6))) (fun i _ _ => sq_nonneg (x i))
  simpa using h

/-- Exact block comparison conditional on the displayed shifted energy bound. -/
theorem p45_le_shifted_energy (q v : Fin 6 → ℝ) (E B : ℝ)
    (hlower : (9401 / 2000000 : ℝ) * (∑ i, v i ^ 2) +
      (1 / 5 : ℝ) * (∑ i, q i ^ 2) ≤ E + B) :
    p45 q v ≤ (1600000 / 9401 : ℝ) * (E + B) := by
  have hq := block45_sq_le_total q
  have hv := block45_sq_le_total v
  have hqn : 0 ≤ ∑ i, q i ^ 2 := Finset.sum_nonneg fun i _ => sq_nonneg (q i)
  unfold p45
  nlinarith

/-- The full optional composition, retaining the actual mass/source seams. -/
theorem fourier_p45_bound (kp q v : Fin 6 → ℝ) (a phase : ν → ℝ)
    (M : Fin 6 → Fin 6 → ℝ) (E : ℝ)
    (hkp : ∀ i, (2 / 5 : ℝ) ≤ kp i)
    (hmass : (9401 / 1000000 : ℝ) * (∑ i, v i ^ 2) ≤
      ∑ i, v i * (∑ j, M i j * v j))
    (hE : E = kinetic M v + storage kp q a phase) :
    p45 q v ≤ (1600000 / 9401 : ℝ) * (E + shift a) := by
  apply p45_le_shifted_energy
  have h := shifted_energy_lower kp q v a phase M E (9401 / 1000000) hkp hmass hE
  norm_num at h ⊢
  exact h

end

#print axioms shifted_cos_term_nonneg
#print axioms shift_nonneg
#print axioms quadratic_le_shifted_storage
#print axioms quadratic_coercivity
#print axioms shifted_storage_chain
#print axioms shifted_storage_coercivity
#print axioms shifted_energy_lower
#print axioms block45_sq_le_total
#print axioms p45_le_shifted_energy
#print axioms fourier_p45_bound

end RouteBShiftedStorage
