import ResidualPower
import ControllerPowerCore

open scoped BigOperators

namespace RouteBDHPowerBinding

noncomputable section

abbrev Vec := Fin 6 → ℝ
abbrev Mat := Fin 6 → Fin 6 → ℝ

def matVec (M : Mat) (a : Vec) (i : Fin 6) : ℝ := ∑ j, M i j * a j

/- The residual is defined from the returned acceleration. We do not assume
   that a Float64 linear solve satisfies the real descriptor equation exactly. -/
def solveResidual (Mi : Mat) (a tauI cI gI : Vec) (i : Fin 6) : ℝ :=
  matVec Mi a i - (tauI i - cI i - gI i)

def controller (kp q v g0 : Vec) (w : ℝ) (i : Fin 6) : ℝ :=
  -kp i * q i - RouteBSupplyCore.damping i * v i + g0 i +
    RouteBSupplyCore.disturbance i * w

/- Every discrepancy is charged once, including mass, parameters/controller,
   finite-difference C/G, and the computed linear solve. Analytic and numeric
   quantities are real-valued inputs; their concrete source binding is separate. -/
def forceError (Ma Mi : Mat) (a tauA tauI cA cI gA gI : Vec) (i : Fin 6) : ℝ :=
  (matVec Ma a i - matVec Mi a i) + (tauI i - tauA i) +
    (cA i - cI i) + (gA i - gI i) + solveResidual Mi a tauI cI gI i

theorem implemented_force_identity
    (Ma Mi : Mat) (a tauA tauI cA cI gA gI : Vec) (i : Fin 6) :
    matVec Ma a i + cA i + gA i =
      tauA i + forceError Ma Mi a tauA tauI cA cI gA gI i := by
  unfold forceError solveResidual
  ring

theorem mass_difference_action (Ma Mi : Mat) (a : Vec) (i : Fin 6) :
    matVec Ma a i - matVec Mi a i = ∑ j, (Ma i j - Mi i j) * a j := by
  simp only [matVec, sub_mul, Finset.sum_sub_distrib]

theorem mechanical_power_with_all_errors
    (Ma Mi : Mat) (v a tauA tauI cA cI gA gI : Vec) :
    (∑ i, v i * (matVec Ma a i + cA i + gA i)) =
      (∑ i, v i * tauA i) + ∑ i, forceError Ma Mi a tauA tauI cA cI gA gI i * v i := by
  rw [← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro i _
  rw [implemented_force_identity Ma Mi a tauA tauI cA cI gA gI i]
  ring

/- Reuse the target's existing generic controller-power lemma, compiled from
   its frozen source copy. We do not re-prove or assume its cancellation. -/
theorem implemented_energy_identity
    (Ma Mi : Mat) (kp q g0 v a tauI cA cI gA gI : Vec) (w dUc dE : ℝ)
    (hUc : dUc = ∑ i, (kp i * q i - g0 i) * v i)
    (henergy : dE = (∑ i, v i * (matVec Ma a i + cA i + gA i)) + dUc) :
    dE = RouteBSupplyCore.supply v w +
      ∑ i, forceError Ma Mi a (controller kp q v g0 w) tauI cA cI gA gI i * v i := by
  have hctrl := RobotFormalEnergy.closed_loop_power_identity kp
    RouteBSupplyCore.damping RouteBSupplyCore.disturbance q v
    (controller kp q v g0 w) g0 w dUc (fun _ => rfl) hUc
  have hmech := mechanical_power_with_all_errors Ma Mi v a
    (controller kp q v g0 w) tauI cA cI gA gI
  change (∑ i, v i * controller kp q v g0 w i) + dUc =
    RouteBSupplyCore.supply v w at hctrl
  rw [henergy, hmech]
  linarith

theorem implemented_energy_bound
    (Ma Mi : Mat) (kp q g0 v a tauI cA cI gA gI : Vec) (w dUc dE : ℝ)
    (hUc : dUc = ∑ i, (kp i * q i - g0 i) * v i)
    (henergy : dE = (∑ i, v i * (matVec Ma a i + cA i + gA i)) + dUc) :
    dE ≤ (631227 / 1086800 : ℝ) * w ^ 2 +
      ∑ i, (forceError Ma Mi a (controller kp q v g0 w) tauI cA cI gA gI i) ^ 2 /
        (2 * RouteBSupplyCore.damping i) := by
  rw [implemented_energy_identity Ma Mi kp q g0 v a tauI cA cI gA gI w dUc dE hUc henergy]
  exact RouteBResidualPower.supply_with_squared_force_error v _ w

theorem squared_error_budget_mono (e eps : Vec) (h : ∀ i, |e i| ≤ eps i) :
    (∑ i, e i ^ 2 / (2 * RouteBSupplyCore.damping i)) ≤
      ∑ i, eps i ^ 2 / (2 * RouteBSupplyCore.damping i) := by
  apply Finset.sum_le_sum
  intro i _
  obtain ⟨hl, hu⟩ := abs_le.mp (h i)
  have hm : 0 ≤ (eps i - e i) * (eps i + e i) :=
    mul_nonneg (by linarith) (by linarith)
  have hs : e i ^ 2 ≤ eps i ^ 2 := by nlinarith
  exact div_le_div_of_nonneg_right hs (by have := RouteBSupplyCore.damping_pos i; positivity)

theorem implemented_energy_bound_of_component_enclosures
    (Ma Mi : Mat) (kp q g0 v a tauI cA cI gA gI eps : Vec) (w dUc dE : ℝ)
    (hUc : dUc = ∑ i, (kp i * q i - g0 i) * v i)
    (henergy : dE = (∑ i, v i * (matVec Ma a i + cA i + gA i)) + dUc)
    (herr : ∀ i, |forceError Ma Mi a (controller kp q v g0 w) tauI cA cI gA gI i| ≤ eps i) :
    dE ≤ (631227 / 1086800 : ℝ) * w ^ 2 +
      ∑ i, eps i ^ 2 / (2 * RouteBSupplyCore.damping i) := by
  have hp := implemented_energy_bound Ma Mi kp q g0 v a tauI cA cI gA gI w dUc dE hUc henergy
  have he := squared_error_budget_mono _ eps herr
  linarith

end

#print axioms implemented_force_identity
#print axioms mass_difference_action
#print axioms mechanical_power_with_all_errors
#print axioms implemented_energy_identity
#print axioms implemented_energy_bound
#print axioms squared_error_budget_mono
#print axioms implemented_energy_bound_of_component_enclosures

end RouteBDHPowerBinding
