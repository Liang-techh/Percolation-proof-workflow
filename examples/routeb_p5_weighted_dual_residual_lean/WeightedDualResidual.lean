import Mathlib.Data.Fin.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic

/-!
Route-B P5: source-independent damping-weighted residual closure.

This sidecar formalizes only the abstract finite-dimensional inequality behind
T-P5-007.  It does not bind any deployed DH/Float64 source and does not close
P5/M4.
-/

open scoped BigOperators

set_option autoImplicit false

namespace RouteBP5WeightedDualResidual

noncomputable section

abbrev Vec6 := Fin 6 → ℝ

def dampedSq (d v : Vec6) : ℝ := ∑ i, d i * v i ^ 2

def dualSq (d r : Vec6) : ℝ := ∑ i, r i ^ 2 / d i

def dot (r v : Vec6) : ℝ := ∑ i, r i * v i

lemma weighted_young_component
    (d κ r v : ℝ) (hd : 0 < d) :
    2 * κ * (r * v) ≤ κ ^ 2 * (d * v ^ 2) + r ^ 2 / d := by
  have hsq : 0 ≤ (κ * d * v - r) ^ 2 / d := by
    exact div_nonneg (sq_nonneg _) (le_of_lt hd)
  field_simp [ne_of_gt hd] at hsq ⊢
  nlinarith [hsq]

theorem weighted_dot_le_of_dualSq
    (d r v : Vec6) (κ : ℝ)
    (hd : ∀ i, 0 < d i)
    (hκ : 0 < κ)
    (hdual : dualSq d r ≤ κ ^ 2 * dampedSq d v) :
    dot r v ≤ κ * dampedSq d v := by
  have hsum :
      2 * κ * dot r v ≤ κ ^ 2 * dampedSq d v + dualSq d r := by
    unfold dot dampedSq dualSq
    calc
      2 * κ * (∑ i, r i * v i)
          = ∑ i, 2 * κ * (r i * v i) := by
              rw [Finset.mul_sum]
      _ ≤ ∑ i, (κ ^ 2 * (d i * v i ^ 2) + r i ^ 2 / d i) := by
              exact Finset.sum_le_sum fun i _ => weighted_young_component (d i) κ (r i) (v i) (hd i)
      _ = κ ^ 2 * (∑ i, d i * v i ^ 2) + ∑ i, r i ^ 2 / d i := by
              rw [Finset.sum_add_distrib, Finset.mul_sum]
  have h2 : 2 * κ * dot r v ≤ 2 * κ ^ 2 * dampedSq d v := by
    linarith
  nlinarith

theorem weighted_residual_decay
    (d r v : Vec6) (κ dE : ℝ)
    (hd : ∀ i, 0 < d i)
    (hκ0 : 0 < κ) (hκ1 : κ < 1)
    (hdual : dualSq d r ≤ κ ^ 2 * dampedSq d v)
    (henergy : dE ≤ -dampedSq d v + dot r v) :
    dE ≤ -(1 - κ) * dampedSq d v := by
  have hdot := weighted_dot_le_of_dualSq d r v κ hd hκ0 hdual
  linarith

lemma dualSq_nonneg (d r : Vec6) (hd : ∀ i, 0 < d i) :
    0 ≤ dualSq d r := by
  unfold dualSq
  exact Finset.sum_nonneg fun i _ => div_nonneg (sq_nonneg _) (le_of_lt (hd i))

lemma dualSq_eq_zero_forces_component_zero
    (d r : Vec6) (hd : ∀ i, 0 < d i)
    (hzero : dualSq d r = 0) :
    ∀ i, r i = 0 := by
  intro i
  have hterm_nonneg : ∀ j ∈ (Finset.univ : Finset (Fin 6)), 0 ≤ r j ^ 2 / d j := by
    intro j _
    exact div_nonneg (sq_nonneg _) (le_of_lt (hd j))
  have hterm : r i ^ 2 / d i = 0 := by
    have hsum : ∑ j : Fin 6, r j ^ 2 / d j = 0 := by
      simpa [dualSq] using hzero
    exact (Finset.sum_eq_zero_iff_of_nonneg hterm_nonneg).mp hsum i (Finset.mem_univ i)
  have hsquare : r i ^ 2 = 0 := by
    apply (div_eq_zero_iff).mp at hterm
    exact hterm.1
  nlinarith

theorem weighted_residual_decay_kappa_zero
    (d r v : Vec6) (dE : ℝ)
    (hd : ∀ i, 0 < d i)
    (hdual : dualSq d r ≤ 0)
    (henergy : dE ≤ -dampedSq d v + dot r v) :
    dE ≤ -dampedSq d v := by
  have hnonneg := dualSq_nonneg d r hd
  have hz : dualSq d r = 0 := le_antisymm hdual hnonneg
  have hr : ∀ i, r i = 0 := dualSq_eq_zero_forces_component_zero d r hd hz
  have hdot : dot r v = 0 := by
    simp [dot, hr]
  linarith

/- A small algebraic counterexample capturing the current generic force-error
interface obstruction: an additive gravity mismatch can remain nonzero while
velocity is exactly zero. -/
def genericForceError
    (mass tau coriolis gravity solve : Vec6) (i : Fin 6) : ℝ :=
  mass i + tau i + coriolis i + gravity i + solve i

theorem generic_force_error_not_velocity_relative (ρ : ℝ) :
    ∃ (mass tau coriolis gravity solve v : Vec6) (i : Fin 6),
      v i = 0 ∧
      |genericForceError mass tau coriolis gravity solve i| > ρ * |v i| := by
  let z : Vec6 := fun _ => 0
  let g : Vec6 := fun j => if j = (0 : Fin 6) then 1 else 0
  refine ⟨z, z, z, g, z, z, 0, ?_, ?_⟩
  · rfl
  · simp [genericForceError, z, g]

#print axioms weighted_young_component
#print axioms weighted_dot_le_of_dualSq
#print axioms weighted_residual_decay
#print axioms dualSq_nonneg
#print axioms dualSq_eq_zero_forces_component_zero
#print axioms weighted_residual_decay_kappa_zero
#print axioms generic_force_error_not_velocity_relative

end

end RouteBP5WeightedDualResidual
