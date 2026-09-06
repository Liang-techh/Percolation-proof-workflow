import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/- Trusted, self-contained statement: no imports of Solution or the supply core.
An independent elementary proof keeps even the Challenge free of proof holes.
Fin 6 indices 0,...,5 correspond to Julia joints 1,...,6. -/
namespace RouteBSupplyComparison

theorem explicit_supply_bound (v : Fin 6 → ℝ) (w : ℝ) :
    -((13 / 10 : ℝ) * v 0 ^ 2 + (11 / 10 : ℝ) * v 1 ^ 2 +
      (19 / 20 : ℝ) * v 2 ^ 2 + (4 / 5 : ℝ) * v 3 ^ 2 +
      (13 / 20 : ℝ) * v 4 ^ 2 + (1 / 2 : ℝ) * v 5 ^ 2) +
    (v 0 * w + (1 / 2 : ℝ) * v 1 * w + (3 / 10 : ℝ) * v 2 * w +
      (1 / 5 : ℝ) * v 3 * w + (1 / 10 : ℝ) * v 4 * w +
      (1 / 20 : ℝ) * v 5 * w) ≤ (631227 / 2173600 : ℝ) * w ^ 2 := by
  nlinarith [sq_nonneg (v 0 - (5 / 13 : ℝ) * w),
    sq_nonneg (v 1 - (5 / 22 : ℝ) * w),
    sq_nonneg (v 2 - (3 / 19 : ℝ) * w),
    sq_nonneg (v 3 - (1 / 8 : ℝ) * w),
    sq_nonneg (v 4 - (1 / 13 : ℝ) * w),
    sq_nonneg (v 5 - (1 / 20 : ℝ) * w)]

end RouteBSupplyComparison

#print axioms RouteBSupplyComparison.explicit_supply_bound
