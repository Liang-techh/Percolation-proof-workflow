import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-!
Local PD/reference kinetic storage, with exact rational coefficients.
The residual e is the TOTAL reference-block force mismatch: mass error,
remote coupling acceleration, gravity, and FD/Float64 effects. There is no
gravitational potential in VB and no assertion that the residual budget holds.
The derivative is an explicitly supplied algebraic expression; this file does
not assert differentiability or identify any external robot implementation.
-/

open scoped BigOperators

namespace RouteBLocalEnergyBudget

noncomputable section

def m44 : ℝ := 350003 / 3000000
def m55 : ℝ := 200739 / 4000000

def VB (q4 q5 v4 v5 : ℝ) : ℝ :=
  (1 / 2) * m44 * v4^2 + (1 / 2) * m55 * v5^2 +
    (3 / 10) * q4^2 + (1 / 4) * q5^2

/-- Explicit chain-rule expression for constant reference masses. -/
def derivativeExpr (q4 q5 v4 v5 a4 a5 : ℝ) : ℝ :=
  m44 * v4 * a4 + m55 * v5 * a5 + (3 / 5) * q4 * v4 + (1 / 2) * q5 * v5

def blockNormSq (q4 q5 v4 v5 : ℝ) : ℝ := q4^2 + q5^2 + v4^2 + v5^2

def p (q4 q5 v4 v5 : ℝ) : ℝ :=
  (3 / 2) * (q4^2 + q5^2) + (4 / 5) * (v4^2 + v5^2)

def qterminal (q4 q5 v4 v5 : ℝ) : ℝ :=
  3 * (q4^2 + q5^2) + 2 * (v4^2 + v5^2)

def residualCost (e4 e5 : ℝ) : ℝ := e4^2 / (8 / 5) + e5^2 / (13 / 10)

def cap : ℝ := 27 / 4000 + 17 / 520 + 1 / 10

/-- Zero-centered full state ball; ordering is q1..q6,v1..v6 (zero-based Fin). -/
def full12Ball (x : Fin 12 → ℝ) : Prop := ∑ i, (x i)^2 ≤ 9 / 400

theorem derivative_identity (q4 q5 v4 v5 a4 a5 w e4 e5 : ℝ)
    (h4 : m44 * a4 = -(3 / 5) * q4 - (4 / 5) * v4 + (1 / 5) * w + e4)
    (h5 : m55 * a5 = -(1 / 2) * q5 - (13 / 20) * v5 + (1 / 10) * w + e5) :
    derivativeExpr q4 q5 v4 v5 a4 a5 =
      -(4 / 5) * v4^2 - (13 / 20) * v5^2 +
        (1 / 5) * v4 * w + (1 / 10) * v5 * w + v4 * e4 + v5 * e5 := by
  calc
    derivativeExpr q4 q5 v4 v5 a4 a5 =
        v4 * (m44 * a4 + (3 / 5) * q4) +
          v5 * (m55 * a5 + (1 / 2) * q5) := by unfold derivativeExpr; ring
    _ = _ := by rw [h4, h5]; ring

/-- Each axis assigns half its damping to input and half to total residual.
This exact four-square remainder exposes every sign and Young coefficient. -/
theorem half_damping_identity (v4 v5 w e4 e5 : ℝ) :
    (17 / 520) * w^2 + residualCost e4 e5 -
      (-(4 / 5) * v4^2 - (13 / 20) * v5^2 +
        (1 / 5) * v4 * w + (1 / 10) * v5 * w + v4 * e4 + v5 * e5) =
      (2 / 5) * (v4 - w / 4)^2 + (2 / 5) * (v4 - (5 / 4) * e4)^2 +
        (13 / 40) * (v5 - (2 / 13) * w)^2 +
        (13 / 40) * (v5 - (20 / 13) * e5)^2 := by
  unfold residualCost
  ring

/-- Budget for any supplied derivative value satisfying the explicit expression. -/
theorem derivative_budget (q4 q5 v4 v5 a4 a5 w e4 e5 dVB : ℝ)
    (hd : dVB = derivativeExpr q4 q5 v4 v5 a4 a5)
    (h4 : m44 * a4 = -(3 / 5) * q4 - (4 / 5) * v4 + (1 / 5) * w + e4)
    (h5 : m55 * a5 = -(1 / 2) * q5 - (13 / 20) * v5 + (1 / 10) * w + e5) :
    dVB ≤ (17 / 520) * w^2 + e4^2 / (8 / 5) + e5^2 / (13 / 10) := by
  rw [hd, derivative_identity q4 q5 v4 v5 a4 a5 w e4 e5 h4 h5]
  have hc := half_damping_identity v4 v5 w e4 e5
  unfold residualCost at hc
  nlinarith only [hc, sq_nonneg (v4 - w / 4), sq_nonneg (v4 - (5 / 4) * e4),
    sq_nonneg (v5 - (2 / 13) * w), sq_nonneg (v5 - (20 / 13) * e5)]

theorem full12Ball_block_bound (x : Fin 12 → ℝ) (hx : full12Ball x) :
    blockNormSq (x 3) (x 4) (x 9) (x 10) ≤ 9 / 400 := by
  have hs : (∑ i ∈ ({3, 4, 9, 10} : Finset (Fin 12)), (x i)^2) ≤
      ∑ i : Fin 12, (x i)^2 :=
    Finset.sum_le_sum_of_subset_of_nonneg (Finset.subset_univ _)
      (fun i _ _ => sq_nonneg (x i))
  norm_num [Finset.sum_insert, Finset.sum_singleton, Finset.mem_insert,
    Finset.mem_singleton] at hs
  dsimp [blockNormSq]
  dsimp [full12Ball] at hx
  linarith only [hs, hx]

theorem VB_nonneg (q4 q5 v4 v5 : ℝ) : 0 ≤ VB q4 q5 v4 v5 := by
  unfold VB m44 m55
  nlinarith only [sq_nonneg q4, sq_nonneg q5, sq_nonneg v4, sq_nonneg v5]

theorem VB_le_blockNormSq (q4 q5 v4 v5 : ℝ) :
    VB q4 q5 v4 v5 ≤ (3 / 10) * blockNormSq q4 q5 v4 v5 := by
  unfold VB m44 m55 blockNormSq
  nlinarith only [sq_nonneg q5, sq_nonneg v4, sq_nonneg v5]

theorem initial_VB_bound (q4 q5 v4 v5 : ℝ)
    (hblock : blockNormSq q4 q5 v4 v5 ≤ 9 / 400) :
    VB q4 q5 v4 v5 ≤ 27 / 4000 := by
  have hv := VB_le_blockNormSq q4 q5 v4 v5
  linarith only [hblock, hv]

theorem full12Ball_initial_VB (x : Fin 12 → ℝ) (hx : full12Ball x) :
    VB (x 3) (x 4) (x 9) (x 10) ≤ 27 / 4000 :=
  initial_VB_bound _ _ _ _ (full12Ball_block_bound x hx)

theorem p_le_VB (q4 q5 v4 v5 : ℝ) :
    p q4 q5 v4 v5 ≤ (6400000 / 200739) * VB q4 q5 v4 v5 := by
  unfold p VB m44 m55
  nlinarith only [sq_nonneg q4, sq_nonneg q5, sq_nonneg v4, sq_nonneg v5]

theorem qterminal_le_VB (q4 q5 v4 v5 : ℝ) :
    qterminal q4 q5 v4 v5 ≤ (16000000 / 200739) * VB q4 q5 v4 v5 := by
  unfold qterminal VB m44 m55
  nlinarith only [sq_nonneg q4, sq_nonneg q5, sq_nonneg v4, sq_nonneg v5]

/-- Exact arithmetic, including strict margins for both outputs. -/
theorem cap_arithmetic :
    cap = (7251 / 52000 : ℝ) ∧
    (6400000 / 200739 : ℝ) * cap = 3867200 / 869869 ∧
    (16000000 / 200739 : ℝ) * cap = 9668000 / 869869 ∧
    (6400000 / 200739 : ℝ) * cap < 28 / 5 ∧
    (16000000 / 200739 : ℝ) * cap < 12 := by
  norm_num [cap]

theorem outputs_of_cap (q4 q5 v4 v5 : ℝ) (hcap : VB q4 q5 v4 v5 ≤ cap) :
    p q4 q5 v4 v5 < 28 / 5 ∧ qterminal q4 q5 v4 v5 < 12 := by
  have hp := p_le_VB q4 q5 v4 v5
  have hq := qterminal_le_VB q4 q5 v4 v5
  have hc := cap_arithmetic
  constructor <;> linarith only [hp, hq, hcap, hc.2.2.2.1, hc.2.2.2.2]

/-- A conditional ledger interface, NOT a proof of the integrated energy bound.
`inputEnergy` and `residualEnergy` must be identified and bounded externally. -/
theorem cap_of_energy_ledger (q4 q5 v4 v5 V0 inputEnergy residualEnergy : ℝ)
    (henergy : VB q4 q5 v4 v5 ≤ V0 + (17 / 520) * inputEnergy + residualEnergy)
    (h0 : V0 ≤ 27 / 4000) (hw : inputEnergy ≤ 1) (he : residualEnergy ≤ 1 / 10) :
    VB q4 q5 v4 v5 ≤ cap := by
  unfold cap
  linarith only [henergy, h0, hw, he]

end

#print axioms derivative_identity
#print axioms half_damping_identity
#print axioms derivative_budget
#print axioms full12Ball_block_bound
#print axioms VB_nonneg
#print axioms VB_le_blockNormSq
#print axioms initial_VB_bound
#print axioms full12Ball_initial_VB
#print axioms p_le_VB
#print axioms qterminal_le_VB
#print axioms cap_arithmetic
#print axioms outputs_of_cap
#print axioms cap_of_energy_ledger

end RouteBLocalEnergyBudget
