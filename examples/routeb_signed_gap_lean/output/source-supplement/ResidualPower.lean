import RouteBSupplyCore

open scoped BigOperators

namespace RouteBResidualPower

noncomputable section

theorem scalar_completion (d b x : ℝ) (hd : 0 < d) :
    b ^ 2 / (4 * d) - (-d * x ^ 2 + b * x) =
      d * (x - b / (2 * d)) ^ 2 := by
  field_simp
  nlinarith [sq_nonneg (d * x)]

theorem scalar_power_bound (d b x : ℝ) (hd : 0 < d) :
    -d * x ^ 2 + b * x ≤ b ^ 2 / (4 * d) := by
  have hid := scalar_completion d b x hd
  have hn := mul_nonneg hd.le (sq_nonneg (x - b / (2 * d)))
  linarith

theorem scalar_at_center (d b : ℝ) (hd : 0 < d) :
    -d * (b / (2 * d)) ^ 2 + b * (b / (2 * d)) = b ^ 2 / (4 * d) := by
  have h := scalar_completion d b (b / (2 * d)) hd
  simp only [sub_self, zero_pow (by decide : 2 ≠ 0), mul_zero] at h
  linarith

/- Exact obstruction, not a counterexample to the full DH target: a nonzero
   velocity-linear defect cannot have zero supply budget uniformly in velocity. -/
theorem zero_input_obstruction (d e : ℝ) (hd : 0 < d) (he : e ≠ 0) :
    ∃ v : ℝ, 0 < -d * v ^ 2 + e * v := by
  refine ⟨e / (2 * d), ?_⟩
  rw [scalar_at_center d e hd]
  exact div_pos (sq_pos_of_ne_zero he) (by positivity)

theorem scalar_required_budget_iff (d e budget : ℝ) (hd : 0 < d) :
    (∀ v : ℝ, -d * v ^ 2 + e * v ≤ budget) ↔ e ^ 2 / (4 * d) ≤ budget := by
  constructor
  · intro h
    simpa only [scalar_at_center d e hd] using h (e / (2 * d))
  · intro h v
    exact (scalar_power_bound d e v hd).trans h

def power (d b v : Fin 6 → ℝ) : ℝ := ∑ i, (-d i * v i ^ 2 + b i * v i)

def budget (d b : Fin 6 → ℝ) : ℝ := ∑ i, b i ^ 2 / (4 * d i)

theorem vector_power_bound (d b v : Fin 6 → ℝ) (hd : ∀ i, 0 < d i) :
    power d b v ≤ budget d b := by
  exact Finset.sum_le_sum fun i _ => scalar_power_bound (d i) (b i) (v i) (hd i)

theorem perturbed_supply_identity (v e : Fin 6 → ℝ) (w : ℝ) :
    power RouteBSupplyCore.damping (fun i => RouteBSupplyCore.disturbance i * w + e i) v =
      RouteBSupplyCore.supply v w + ∑ i, e i * v i := by
  unfold power RouteBSupplyCore.supply
  simp only [Fin.sum_univ_succ, RouteBSupplyCore.damping, RouteBSupplyCore.disturbance]
  ring

theorem perturbed_supply_bound (v e : Fin 6 → ℝ) (w : ℝ) :
    RouteBSupplyCore.supply v w + ∑ i, e i * v i ≤
      budget RouteBSupplyCore.damping (fun i => RouteBSupplyCore.disturbance i * w + e i) := by
  rw [← perturbed_supply_identity]
  exact vector_power_bound _ _ _ RouteBSupplyCore.damping_pos

theorem split_square_budget (d a b : ℝ) (hd : 0 < d) :
    (a + b) ^ 2 / (4 * d) ≤ a ^ 2 / (2 * d) + b ^ 2 / (2 * d) := by
  apply (div_le_iff₀ (by positivity : 0 < 4 * d)).2
  have hid : (a ^ 2 / (2 * d) + b ^ 2 / (2 * d)) * (4 * d) =
      2 * a ^ 2 + 2 * b ^ 2 := by
    field_simp
    ring
  rw [hid]
  nlinarith [sq_nonneg (a - b)]

/- An additive squared-force error budget survives at w=0. This is suitable
   for integrating a rigorously bounded residual without pretending it vanishes. -/
theorem supply_with_squared_force_error (v e : Fin 6 → ℝ) (w : ℝ) :
    RouteBSupplyCore.supply v w + ∑ i, e i * v i ≤
      (631227 / 1086800 : ℝ) * w ^ 2 +
        ∑ i, e i ^ 2 / (2 * RouteBSupplyCore.damping i) := by
  have h := perturbed_supply_bound v e w
  have hs : budget RouteBSupplyCore.damping
      (fun i => RouteBSupplyCore.disturbance i * w + e i) ≤
      (∑ i, (RouteBSupplyCore.disturbance i * w) ^ 2 / (2 * RouteBSupplyCore.damping i)) +
        ∑ i, e i ^ 2 / (2 * RouteBSupplyCore.damping i) := by
    rw [← Finset.sum_add_distrib]
    exact Finset.sum_le_sum fun i _ => split_square_budget _ _ _ (RouteBSupplyCore.damping_pos i)
  have hc : (∑ i, (RouteBSupplyCore.disturbance i * w) ^ 2 /
      (2 * RouteBSupplyCore.damping i)) = (631227 / 1086800 : ℝ) * w ^ 2 := by
    simp [Fin.sum_univ_succ, RouteBSupplyCore.damping, RouteBSupplyCore.disturbance]
    ring
  rw [hc] at hs
  exact h.trans hs

end

#print axioms scalar_completion
#print axioms scalar_power_bound
#print axioms scalar_at_center
#print axioms zero_input_obstruction
#print axioms scalar_required_budget_iff
#print axioms vector_power_bound
#print axioms perturbed_supply_identity
#print axioms perturbed_supply_bound
#print axioms split_square_budget
#print axioms supply_with_squared_force_error

end RouteBResidualPower
