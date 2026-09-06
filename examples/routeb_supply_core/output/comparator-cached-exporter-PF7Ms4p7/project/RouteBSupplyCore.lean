import Mathlib.Data.Real.Basic
import Mathlib.Data.Fin.VecNotation
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic

/-!
Exact rational quadratic supply core for the true-DH audit.
No target-repository imports or dynamics assumptions are hidden here.
Fin 6 index 0 corresponds to Julia joint 1. All divisions below are in R.
The coefficients represent the decimal-rational analytic model, not Float64.
-/

open scoped BigOperators

namespace RouteBSupplyCore

noncomputable section

def damping : Fin 6 → ℝ := ![13 / 10, 11 / 10, 19 / 20, 4 / 5, 13 / 20, 1 / 2]

def disturbance : Fin 6 → ℝ := ![1, 1 / 2, 3 / 10, 1 / 5, 1 / 10, 1 / 20]

def centerRate : Fin 6 → ℝ := ![5 / 13, 5 / 22, 3 / 19, 1 / 8, 1 / 13, 1 / 20]

def gamma : ℝ := 631227 / 2173600

def unitMargin : ℝ := 1542373 / 2173600

def supply (v : Fin 6 → ℝ) (w : ℝ) : ℝ :=
  -(∑ i, damping i * v i ^ 2) + ∑ i, disturbance i * v i * w

def completion (v : Fin 6 → ℝ) (w : ℝ) : ℝ :=
  ∑ i, damping i * (v i - centerRate i * w) ^ 2

theorem damping_pos (i : Fin 6) : 0 < damping i := by
  fin_cases i <;> norm_num [damping]

theorem centerRate_exact (i : Fin 6) :
    centerRate i = disturbance i / (2 * damping i) := by
  fin_cases i <;> norm_num [centerRate, disturbance, damping]

theorem gamma_exact :
    (∑ i, disturbance i ^ 2 / (4 * damping i)) = gamma := by
  norm_num [Fin.sum_univ_succ, disturbance, damping, gamma]

theorem gamma_pos : 0 < gamma := by norm_num [gamma]

theorem gamma_lt_one : gamma < 1 := by norm_num [gamma]

theorem unitMargin_exact : 1 - gamma = unitMargin := by
  norm_num [gamma, unitMargin]

theorem unitMargin_pos : 0 < unitMargin := by norm_num [unitMargin]

/- Explicit six weighted squares, preserving rational coefficients. -/
theorem completion_six (v : Fin 6 → ℝ) (w : ℝ) :
    completion v w =
      (13 / 10 : ℝ) * (v 0 - (5 / 13 : ℝ) * w) ^ 2 +
      (11 / 10 : ℝ) * (v 1 - (5 / 22 : ℝ) * w) ^ 2 +
      (19 / 20 : ℝ) * (v 2 - (3 / 19 : ℝ) * w) ^ 2 +
      (4 / 5 : ℝ) * (v 3 - (1 / 8 : ℝ) * w) ^ 2 +
      (13 / 20 : ℝ) * (v 4 - (1 / 13 : ℝ) * w) ^ 2 +
      (1 / 2 : ℝ) * (v 5 - (1 / 20 : ℝ) * w) ^ 2 := by
  simp [completion, Fin.sum_univ_succ, damping, centerRate]
  ring

/- The stronger identity: the supply gap is exactly the six-square completion. -/
theorem vector_completion_identity (v : Fin 6 → ℝ) (w : ℝ) :
    gamma * w ^ 2 - supply v w = completion v w := by
  simp [supply, completion, Fin.sum_univ_succ, damping, disturbance, centerRate, gamma]
  ring

theorem completion_nonneg (v : Fin 6 → ℝ) (w : ℝ) : 0 ≤ completion v w := by
  exact Finset.sum_nonneg fun i _ =>
    mul_nonneg (le_of_lt (damping_pos i)) (sq_nonneg _)

/- Universally pointwise: no bound on v or w and no circle/domain premise. -/
theorem pointwise_supply_bound (v : Fin 6 → ℝ) (w : ℝ) :
    supply v w ≤ (631227 / 2173600 : ℝ) * w ^ 2 := by
  have hid := vector_completion_identity v w
  have hnonneg := completion_nonneg v w
  change supply v w ≤ gamma * w ^ 2
  linarith

theorem unit_supply_gap_identity (v : Fin 6 → ℝ) (w : ℝ) :
    w ^ 2 - supply v w = unitMargin * w ^ 2 + completion v w := by
  have hid := vector_completion_identity v w
  have hm := unitMargin_exact
  nlinarith

theorem unit_supply_bound (v : Fin 6 → ℝ) (w : ℝ) : supply v w ≤ w ^ 2 := by
  have hgap := unit_supply_gap_identity v w
  have hnonneg := completion_nonneg v w
  have hm := mul_nonneg (le_of_lt unitMargin_pos) (sq_nonneg w)
  linarith

/- The maximizing vector also witnesses sharpness of this quadratic bound.
This is not a claim of an optimal trajectory or full DH certificate. -/
theorem supply_at_center (w : ℝ) :
    supply (fun i => centerRate i * w) w = gamma * w ^ 2 := by
  have hid := vector_completion_identity (fun i => centerRate i * w) w
  have hz : completion (fun i => centerRate i * w) w = 0 := by
    simp [completion]
  rw [hz] at hid
  linarith

theorem uniform_supply_coefficient_iff (beta : ℝ) :
    (∀ (v : Fin 6 → ℝ) (w : ℝ), supply v w ≤ beta * w ^ 2) ↔ gamma ≤ beta := by
  constructor
  · intro h
    have hb := h (fun i => centerRate i * 1) 1
    rw [supply_at_center] at hb
    simpa using hb
  · intro h v w
    exact (pointwise_supply_bound v w).trans
      (mul_le_mul_of_nonneg_right h (sq_nonneg w))

/- Explicit interface for externally established power and residual facts. -/
theorem power_bound_with_remainder
    (v : Fin 6 → ℝ) (w dE remainder defect : ℝ)
    (hpower : dE = supply v w + remainder) (hrem : remainder ≤ defect) :
    dE ≤ (631227 / 2173600 : ℝ) * w ^ 2 + defect := by
  have hbound := pointwise_supply_bound v w
  linarith

/- Full completion credit is available for residual absorption. -/
theorem unit_supply_of_power_identity
    (v : Fin 6 → ℝ) (w dE remainder : ℝ)
    (hpower : dE = supply v w + remainder)
    (hrem : remainder ≤ unitMargin * w ^ 2 + completion v w) :
    dE ≤ w ^ 2 := by
  have hid := unit_supply_gap_identity v w
  linarith

/- A convenient sufficient condition using only the rational scalar margin. -/
theorem unit_supply_of_margin_bound
    (v : Fin 6 → ℝ) (w dE remainder : ℝ)
    (hpower : dE = supply v w + remainder)
    (hrem : remainder ≤ (1542373 / 2173600 : ℝ) * w ^ 2) :
    dE ≤ w ^ 2 := by
  apply unit_supply_of_power_identity v w dE remainder hpower
  have hc := completion_nonneg v w
  change remainder ≤ unitMargin * w ^ 2 at hrem
  linarith

end

#print axioms damping_pos
#print axioms centerRate_exact
#print axioms gamma_exact
#print axioms gamma_pos
#print axioms gamma_lt_one
#print axioms unitMargin_exact
#print axioms unitMargin_pos
#print axioms completion_six
#print axioms vector_completion_identity
#print axioms completion_nonneg
#print axioms pointwise_supply_bound
#print axioms unit_supply_gap_identity
#print axioms unit_supply_bound
#print axioms supply_at_center
#print axioms uniform_supply_coefficient_iff
#print axioms power_bound_with_remainder
#print axioms unit_supply_of_power_identity
#print axioms unit_supply_of_margin_bound

end RouteBSupplyCore
