import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
UNCOMPILED bounded exact-real contraction interface.
No division/sqrt in declarations or proofs; no Schur/PMI reconstruction.
The caller supplies the scalar closure on its own energy and domain.
Sign failures are distinguished from failure of an upper bound.
-/

set_option autoImplicit false

namespace RouteBP4032DivisionFreeContraction

noncomputable section

/-- Rearrangement is unconditional: no sign or strict-contraction premise
is needed merely to move rho*energy to the left. -/
theorem closure_iff_scaled (energy bias rho : ℝ) :
    energy ≤ bias + rho * energy ↔ (1 - rho) * energy ≤ bias := by
  constructor <;> intro h <;> nlinarith

/-- Requested nonnegative-energy contract. The signs and strict gate are
retained for consumers; the underlying rearrangement is stronger. -/
theorem division_free_contraction (energy bias rho : ℝ)
    (hE : 0 ≤ energy) (hB : 0 ≤ bias) (hrho : rho < 1)
    (hclosure : energy ≤ bias + rho * energy) :
    (1 - rho) * energy ≤ bias :=
  (closure_iff_scaled energy bias rho).mp hclosure

/-- A proposed finite real cap can be checked without division. E and B
may have either sign: positivity of 1-rho is the cancellation condition. -/
theorem allocated_upper_bound (energy bias rho cap : ℝ)
    (hrho : rho < 1) (hclosure : energy ≤ bias + rho * energy)
    (hcap : bias ≤ (1 - rho) * cap) : energy ≤ cap := by
  have hs := (closure_iff_scaled energy bias rho).mp hclosure
  exact (mul_le_mul_left (sub_pos.mpr hrho)).mp (hs.trans hcap)

/-- B>=0 is a consequence of a feasible nonnegative E when rho<=1,
not an additional prerequisite for real upper-bound cancellation. -/
theorem feasible_nonnegative_energy_requires_nonnegative_bias
    (energy bias rho : ℝ) (hE : 0 ≤ energy) (hrho : rho ≤ 1)
    (hclosure : energy ≤ bias + rho * energy) : 0 ≤ bias := by
  have hs := (closure_iff_scaled energy bias rho).mp hclosure
  exact (mul_nonneg (sub_nonneg.mpr hrho) hE).trans hs

/-- Negative B with E>=0 and rho<1 is inconsistent, rather than an
unbounded feasible energy family. -/
theorem negative_bias_inconsistent (energy bias rho : ℝ)
    (hE : 0 ≤ energy) (hB : bias < 0) (hrho : rho < 1)
    (hclosure : energy ≤ bias + rho * energy) : False := by
  have hnonneg := feasible_nonnegative_energy_requires_nonnegative_bias
    energy bias rho hE hrho.le hclosure
  linarith

/-- At rho=1 the closure is independent of energy. -/
theorem critical_closure_iff (energy bias : ℝ) :
    energy ≤ bias + 1 * energy ↔ 0 ≤ bias := by
  constructor <;> intro h <;> linarith

/-- For rho>1 this is a lower constraint on E, not an upper constraint.
The algebraic equivalence itself does not require a sign assumption. -/
theorem closure_iff_lower_form (energy bias rho : ℝ) :
    energy ≤ bias + rho * energy ↔ -bias ≤ (rho - 1) * energy := by
  constructor <;> intro h <;> nlinarith

/-- Exact ray exceeding any proposed finite cap for rho>=1 and B>=0. -/
theorem noncontractive_counterexample (rho bias cap : ℝ)
    (hrho : 1 ≤ rho) (hB : 0 ≤ bias) :
    ∃ energy : ℝ, 0 ≤ energy ∧ energy ≤ bias + rho * energy ∧ cap < energy := by
  let energy : ℝ := max 0 cap + 1
  have hzero := le_max_left (0 : ℝ) cap
  have hcap := le_max_right (0 : ℝ) cap
  have hE : 0 ≤ energy := by dsimp [energy]; linarith
  have hscaled := mul_le_mul_of_nonneg_right hrho hE
  refine ⟨energy, hE, ?_, ?_⟩
  · nlinarith
  · dsimp [energy]
    linarith

theorem no_noncontractive_uniform_cap (rho bias : ℝ)
    (hrho : 1 ≤ rho) (hB : 0 ≤ bias) :
    ¬ ∃ cap : ℝ, ∀ energy : ℝ,
      0 ≤ energy → energy ≤ bias + rho * energy → energy ≤ cap := by
  rintro ⟨cap, hcap⟩
  obtain ⟨energy, hE, hclosure, hlarge⟩ :=
    noncontractive_counterexample rho bias cap hrho hB
  exact (not_le_of_gt hlarge) (hcap energy hE hclosure)

/-- A negative E and B still admit a finite upper bound when rho=0.
This refutes treating either missing sign as an upper-bound obstruction. -/
theorem negative_bias_signed_witness :
    (-1 : ℝ) ≤ -1 + 0 * (-1) ∧
      ∀ energy : ℝ, energy ≤ -1 + 0 * energy → energy ≤ -1 := by
  constructor
  · norm_num
  · intro energy h
    simpa using h

/-- Without E>=0, even rho=B=0 permits arbitrarily negative E.
The upper bound E<=0 remains valid; nonnegativity and a uniform lower
bound (and hence a two-sided magnitude bound) are what are lost. -/
theorem missing_energy_sign_no_lower_bound (lower : ℝ) :
    ∃ energy : ℝ, energy ≤ 0 + 0 * energy ∧ energy < 0 ∧ energy < lower := by
  refine ⟨min 0 lower - 1, ?_, ?_, ?_⟩
  all_goals
    have hzero := min_le_left (0 : ℝ) lower
    have hlower := min_le_right (0 : ℝ) lower
    nlinarith

end

-- Future audit commands only; NOT executed in this round.
#print axioms closure_iff_scaled
#print axioms division_free_contraction
#print axioms allocated_upper_bound
#print axioms feasible_nonnegative_energy_requires_nonnegative_bias
#print axioms negative_bias_inconsistent
#print axioms critical_closure_iff
#print axioms closure_iff_lower_form
#print axioms noncontractive_counterexample
#print axioms no_noncontractive_uniform_cap
#print axioms negative_bias_signed_witness
#print axioms missing_energy_sign_no_lower_bound

end RouteBP4032DivisionFreeContraction
