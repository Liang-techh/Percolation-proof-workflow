import Mathlib.Tactic

/-!
  Route-B P5: reusable scalar dissipative residual-power closure.

  This file formalizes the exact algebraic child after an energy identity and
  damping/residual norm estimates have been supplied.  It does not claim those
  estimates for the deployed DH/Float64 source.
-/

set_option autoImplicit false

namespace RouteBP5ResidualPower

theorem global_upper_bound
    (δ ε x y : ℝ)
    (hδ : 0 < δ) (_hε : 0 ≤ ε) (_hx : 0 ≤ x)
    (hy : y ≤ -δ * x ^ 2 + ε * x) :
    4 * δ * y ≤ ε ^ 2 := by
  nlinarith [sq_nonneg (2 * δ * x - ε)]

theorem retained_dissipation
    (δ ε x y : ℝ)
    (hδ : 0 < δ) (_hε : 0 ≤ ε) (_hx : 0 ≤ x)
    (hy : y ≤ -δ * x ^ 2 + ε * x) :
    2 * δ * y ≤ -δ ^ 2 * x ^ 2 + ε ^ 2 := by
  nlinarith [sq_nonneg (δ * x - ε)]

theorem parameterized_young
    (δ η ε x y : ℝ)
    (_hδ : 0 < δ) (hη : 0 < η) (_hηδ : η < δ)
    (_hε : 0 ≤ ε) (_hx : 0 ≤ x)
    (hy : y ≤ -δ * x ^ 2 + ε * x) :
    4 * η * y ≤ -4 * η * (δ - η) * x ^ 2 + ε ^ 2 := by
  nlinarith [sq_nonneg (2 * η * x - ε)]

theorem strict_negativity_above_threshold
    (δ ε x y : ℝ)
    (hδ : 0 < δ) (hε : 0 ≤ ε) (_hx : 0 ≤ x)
    (hy : y ≤ -δ * x ^ 2 + ε * x)
    (hthreshold : ε < δ * x) :
    y < 0 := by
  nlinarith

theorem strict_decay_under_relative_residual
    (δ ρ x y : ℝ)
    (_hδ : 0 < δ) (_hρ : 0 ≤ ρ) (hρδ : ρ < δ)
    (hx : 0 < x)
    (hy : y ≤ -δ * x ^ 2 + (ρ * x) * x) :
    y < 0 := by
  have hgap : 0 < δ - ρ := by linarith
  have hx2 : 0 < x ^ 2 := sq_pos_of_pos hx
  have hterm : -(δ - ρ) * x ^ 2 < 0 := by
    have hprod : 0 < (δ - ρ) * x ^ 2 := mul_pos hgap hx2
    linarith
  have hrewrite : -δ * x ^ 2 + (ρ * x) * x = -(δ - ρ) * x ^ 2 := by
    ring
  rw [hrewrite] at hy
  exact lt_of_le_of_lt hy hterm

#print axioms global_upper_bound
#print axioms retained_dissipation
#print axioms parameterized_young
#print axioms strict_negativity_above_threshold
#print axioms strict_decay_under_relative_residual

end RouteBP5ResidualPower
