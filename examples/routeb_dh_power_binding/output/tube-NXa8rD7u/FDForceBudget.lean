import DHPowerBinding

open scoped BigOperators

namespace RouteBFDForceBudget

noncomputable section

def slope : Fin 6 → ℝ := ![
  257371 / 150416000000000, 257371 / 150416000000000,
  109951 / 150416000000000, 173713 / 300832000000000,
  520451 / 1353744000000000, 1 / 4834800000]

def offset : Fin 6 → ℝ := ![
  0, 68343 / 800000000000000, 21909 / 1000000000000000,
  6867 / 8000000000000000, 6867 / 4000000000000000, 0]

def envelope (cap : ℝ) (i : Fin 6) : ℝ := slope i * cap + offset i

def polynomialBudget (cap : ℝ) : ℝ :=
  ∑ i, envelope cap i ^ 2 / (2 * RouteBSupplyCore.damping i)

theorem exact_polynomial_budget (cap : ℝ) :
    polynomialBudget cap =
      (98881705013075533 / 31867111649569996800000000000000000 : ℝ) * cap ^ 2 +
      (4234629090421 / 27973836800000000000000000000000 : ℝ) * cap +
      (90362741420079 / 25292800000000000000000000000000000 : ℝ) := by
  simp [polynomialBudget, envelope, slope, offset, RouteBSupplyCore.damping, Fin.sum_univ_succ]
  ring

theorem polynomial_budget_upper (cap : ℝ) (hcap : 0 ≤ cap) :
    polynomialBudget cap ≤ (3103 * cap ^ 2 + 152 * cap + 4) / (10 ^ 21 : ℝ) := by
  have ha : (98881705013075533 / 31867111649569996800000000000000000 : ℝ) ≤
      3103 / (10 ^ 21 : ℝ) := by norm_num
  have hb : (4234629090421 / 27973836800000000000000000000000 : ℝ) ≤
      152 / (10 ^ 21 : ℝ) := by norm_num
  have hc : (90362741420079 / 25292800000000000000000000000000000 : ℝ) ≤
      4 / (10 ^ 21 : ℝ) := by norm_num
  have hqa := mul_le_mul_of_nonneg_right ha (sq_nonneg cap)
  have hlb := mul_le_mul_of_nonneg_right hb hcap
  rw [exact_polynomial_budget]
  nlinarith

/- Only conditional admission of the coefficient envelope: the Fourier/DH
   derivation, storage lower bound, and cap invariant are NOT axiomatized here. -/
theorem fd_only_supply_bound (v e : Fin 6 → ℝ) (w cap : ℝ)
    (hcap : 0 ≤ cap) (he : ∀ i, |e i| ≤ envelope cap i) :
    RouteBSupplyCore.supply v w + ∑ i, e i * v i ≤
      (631227 / 1086800 : ℝ) * w ^ 2 +
        (3103 * cap ^ 2 + 152 * cap + 4) / (10 ^ 21 : ℝ) := by
  have hp := RouteBResidualPower.supply_with_squared_force_error v e w
  have he2 := RouteBDHPowerBinding.squared_error_budget_mono e (envelope cap) he
  have hb := polynomial_budget_upper cap hcap
  change (∑ i, e i ^ 2 / (2 * RouteBSupplyCore.damping i)) ≤ polynomialBudget cap at he2
  linarith

/- Keep FD/runtime cross terms: sum(eps+zeta)^2/(2D), not sum eps^2+sum zeta^2. -/
theorem implemented_energy_fd_plus_runtime
    (Ma Mi : RouteBDHPowerBinding.Mat)
    (kp q g0 v a tauI cA cI gA gI efd runtime zeta : RouteBDHPowerBinding.Vec)
    (w dUc dE cap : ℝ)
    (hUc : dUc = ∑ i, (kp i * q i - g0 i) * v i)
    (henergy : dE = (∑ i, v i * (RouteBDHPowerBinding.matVec Ma a i + cA i + gA i)) + dUc)
    (hsplit : ∀ i, RouteBDHPowerBinding.forceError Ma Mi a
      (RouteBDHPowerBinding.controller kp q v g0 w) tauI cA cI gA gI i = efd i + runtime i)
    (hfd : ∀ i, |efd i| ≤ envelope cap i)
    (hruntime : ∀ i, |runtime i| ≤ zeta i) :
    dE ≤ (631227 / 1086800 : ℝ) * w ^ 2 +
      ∑ i, (envelope cap i + zeta i) ^ 2 / (2 * RouteBSupplyCore.damping i) := by
  apply RouteBDHPowerBinding.implemented_energy_bound_of_component_enclosures
    Ma Mi kp q g0 v a tauI cA cI gA gI (fun i => envelope cap i + zeta i)
    w dUc dE hUc henergy
  intro i
  rw [hsplit i]
  exact (abs_add_le (efd i) (runtime i)).trans (add_le_add (hfd i) (hruntime i))

end

#print axioms exact_polynomial_budget
#print axioms polynomial_budget_upper
#print axioms fd_only_supply_bound
#print axioms implemented_energy_fd_plus_runtime

end RouteBFDForceBudget
