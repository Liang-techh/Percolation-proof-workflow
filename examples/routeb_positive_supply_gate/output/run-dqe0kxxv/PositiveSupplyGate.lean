import Mathlib.Data.Real.Basic
import Mathlib.Tactic

set_option autoImplicit false
open scoped BigOperators

namespace RouteBPositiveSupplyGate
noncomputable section

/-- The exact first-order terminal expression after the eta work term is
    retained.  `E` is the assembled fixed-Z source cost, `W` is W0 on the
    selected slice, and `D` is the positive damping contribution. -/
def firstOrderTotal (E W D rho eta a1 tau : ℝ) : ℝ :=
  E - a1 * (W + tau * (D * rho ^ 2 - rho * eta))

/-- A finite nonnegative supply polynomial in `tau = 1-t`. -/
def polynomialSupply {n : ℕ} (beta : Fin n → ℝ) (tau : ℝ) : ℝ :=
  ∑ k, beta k * tau ^ k.val

/-- If the exact first-order gate is below `b`, a positive denominator forces
    the displayed finite lower bound on `a1`. -/
theorem first_order_supply_lower_bound
    (E W D rho eta a1 tau b : ℝ)
    (hden : 0 < W + tau * (D * rho ^ 2 - rho * eta))
    (hgate : firstOrderTotal E W D rho eta a1 tau ≤ b)
    (_hfloor : b < E) :
    (E - b) / (W + tau * (D * rho ^ 2 - rho * eta)) ≤ a1 := by
  apply (div_le_iff₀ hden).2
  unfold firstOrderTotal at hgate
  linarith

/-- Zero supply cannot hide a strictly positive residual when the first-order
    storage coefficient is zero. -/
theorem zero_supply_requires_positive_first_order
    (E W D rho eta a1 tau : ℝ)
    (hE : 0 < E)
    (hden : 0 < W + tau * (D * rho ^ 2 - rho * eta))
    (hgate : firstOrderTotal E W D rho eta a1 tau ≤ 0) :
    0 < a1 := by
  have hbound := first_order_supply_lower_bound E W D rho eta a1 tau 0
    hden hgate (by linarith)
  have hbound' : E / (W + tau * (D * rho ^ 2 - rho * eta)) ≤ a1 := by
    simpa using hbound
  have hpositive : 0 <
      E / (W + tau * (D * rho ^ 2 - rho * eta)) :=
    div_pos hE hden
  exact lt_of_lt_of_le hpositive hbound'

/-- The finite coefficient budget is an exact arithmetic implication.  The
    polynomial's integral interpretation is deliberately left as a separate
    FTC/regularity obligation. -/
def coefficientBudget {n : ℕ} (v0 betaUpper : ℝ) (beta : Fin n → ℝ) : ℝ :=
  v0 + ∑ k, beta k / ((k.val + 1 : ℕ) : ℝ)

theorem finite_coefficient_budget
    {n : ℕ} (v0 _betaUpper : ℝ) (beta : Fin n → ℝ)
    (hv0 : v0 ≤ betaUpper)
    (hbudget : betaUpper +
      ∑ k, beta k / ((k.val + 1 : ℕ) : ℝ) < 1) :
    coefficientBudget v0 betaUpper beta < 1 := by
  unfold coefficientBudget
  linarith

theorem polynomialSupply_nonnegative
    {n : ℕ} (beta : Fin n → ℝ) (tau : ℝ)
    (hbeta : ∀ k, 0 ≤ beta k) (htau : 0 ≤ tau) :
    0 ≤ polynomialSupply beta tau := by
  unfold polynomialSupply
  exact Finset.sum_nonneg (fun k _ =>
    mul_nonneg (hbeta k) (pow_nonneg htau _))

#print axioms first_order_supply_lower_bound
#print axioms zero_supply_requires_positive_first_order
#print axioms finite_coefficient_budget
#print axioms polynomialSupply_nonnegative

end
end RouteBPositiveSupplyGate
