import RouteBSupplyCore

/- Separately elaborated counterpart of Challenge; never import Challenge. -/
namespace RouteBSupplyComparison

theorem explicit_supply_bound (v : Fin 6 → ℝ) (w : ℝ) :
    -((13 / 10 : ℝ) * v 0 ^ 2 + (11 / 10 : ℝ) * v 1 ^ 2 +
      (19 / 20 : ℝ) * v 2 ^ 2 + (4 / 5 : ℝ) * v 3 ^ 2 +
      (13 / 20 : ℝ) * v 4 ^ 2 + (1 / 2 : ℝ) * v 5 ^ 2) +
    (v 0 * w + (1 / 2 : ℝ) * v 1 * w + (3 / 10 : ℝ) * v 2 * w +
      (1 / 5 : ℝ) * v 3 * w + (1 / 10 : ℝ) * v 4 * w +
      (1 / 20 : ℝ) * v 5 * w) ≤ (631227 / 2173600 : ℝ) * w ^ 2 := by
  simpa [RouteBSupplyCore.supply, RouteBSupplyCore.damping,
    RouteBSupplyCore.disturbance, Fin.sum_univ_succ, add_assoc] using
    RouteBSupplyCore.pointwise_supply_bound v w

end RouteBSupplyComparison

#print axioms RouteBSupplyComparison.explicit_supply_bound
