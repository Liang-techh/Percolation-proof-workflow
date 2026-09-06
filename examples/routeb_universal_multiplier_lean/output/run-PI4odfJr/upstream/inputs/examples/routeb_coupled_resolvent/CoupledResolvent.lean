import DHPowerBinding
import RotationalDual
import LocalEnergyBudget

set_option autoImplicit false
open scoped BigOperators

namespace RouteBCoupledResolvent
noncomputable section
open RouteBDHPowerBinding
open RouteBRotationalDual (dot6 forceMetric lowerMetric)
open RouteBLocalEnergyBudget (m44 m55 residualCost)

def delta (a a0 : Vec) : Vec := fun i => a i-a0 i
def nonlinearForce (M M0 : Mat) (a0 hq c g eta : Vec) : Vec :=
  fun i => matVec M0 a0 i-matVec M a0 i+hq i-g i-c i+eta i

theorem mat_delta (M : Mat) (a a0 : Vec) (i : Fin 6) :
    matVec M (delta a a0) i = matVec M a i-matVec M a0 i := by
  simp only [matVec,delta,mul_sub,Finset.sum_sub_distrib]

/- a0 is computed from the CURRENT full state, not the nominal trajectory.
   eta includes the chosen source/FD/Float64/solve defects exactly once. -/
theorem acceleration_free_resolvent (M M0 : Mat) (a a0 hq c g eta drive : Vec)
    (actual : ∀ i, matVec M a i+c i+g i=drive i+eta i)
    (nominal : ∀ i, matVec M0 a0 i+hq i=drive i) :
    ∀ i, matVec M (delta a a0) i=nonlinearForce M M0 a0 hq c g eta i := by
  intro i
  rw [mat_delta]
  unfold nonlinearForce
  linarith [actual i,nominal i]

theorem residual_energy_identity (M : Mat) (a a0 r : Vec)
    (balance : ∀ i, matVec M (delta a a0) i=r i) :
    dot6 (delta a a0) (matVec M (delta a a0))=dot6 r (delta a a0) := by
  unfold dot6
  apply Finset.sum_congr rfl
  intro i _
  rw [balance]
  ring

theorem correlated_acceleration_energy (v r : Vec) (energy : ℝ)
    (dual : ∀ f, 2*dot6 f v-energy ≤ forceMetric f)
    (balance : energy=dot6 r v) :
    lowerMetric v ≤ forceMetric r := by
  have hl := RouteBRotationalDual.exact_anisotropic_mass_lower v energy dual
  have hu := RouteBRotationalDual.force_balance_bound r v energy (dual r) balance
  rw [← balance] at hu
  exact hl.trans hu

def blockCorrection (v : Vec) : Fin 2 → ℝ := ![m44*v 3,m55*v 4]

theorem correction_cost_from_full_force (v r : Vec) (energy : ℝ)
    (dual : ∀ f, 2*dot6 f v-energy ≤ forceMetric f)
    (balance : energy=dot6 r v) :
    residualCost (blockCorrection v 0) (blockCorrection v 1) ≤
      (3/10 : ℝ)*forceMetric r := by
  have h4 := RouteBRotationalDual.acceleration4_energy v energy dual
  have h5 := RouteBRotationalDual.acceleration5_energy v energy dual
  have hu := RouteBRotationalDual.force_balance_bound r v energy (dual r) balance
  rw [← balance] at hu
  have he : 0 ≤ energy := by nlinarith [sq_nonneg (v 3)]
  norm_num [residualCost,blockCorrection,m44,m55]
  nlinarith

def blockError (a : Vec) (load : Fin 2 → ℝ) : Fin 2 → ℝ :=
  ![m44*a 3+load 0,m55*a 4+load 1]

theorem full_state_error_split (a a0 : Vec) (load : Fin 2 → ℝ) (i : Fin 2) :
    blockError a load i=blockError a0 load i+blockCorrection (delta a a0) i := by
  fin_cases i <;> simp [blockError,blockCorrection,delta] <;> ring

theorem weighted_two_input_bound (x4 x5 y4 y5 : ℝ) :
    residualCost (x4+y4) (x5+y5) ≤
      (3/2 : ℝ)*residualCost x4 x5+3*residualCost y4 y5 := by
  unfold residualCost
  nlinarith [sq_nonneg (x4-2*y4),sq_nonneg (x5-2*y5)]

theorem total_error_from_coupled_residual (a a0 r : Vec) (energy : ℝ)
    (load : Fin 2 → ℝ)
    (dual : ∀ f, 2*dot6 f (delta a a0)-energy ≤ forceMetric f)
    (balance : energy=dot6 r (delta a a0)) :
    residualCost (blockError a load 0) (blockError a load 1) ≤
      (3/2 : ℝ)*residualCost (blockError a0 load 0) (blockError a0 load 1)+
      (9/10 : ℝ)*forceMetric r := by
  have hc := correction_cost_from_full_force (delta a a0) r energy dual balance
  have hs := weighted_two_input_bound (blockError a0 load 0) (blockError a0 load 1)
    (blockCorrection (delta a a0) 0) (blockCorrection (delta a a0) 1)
  rw [full_state_error_split a a0 load 0,full_state_error_split a a0 load 1]
  linarith

/- Algebraic interface for the nominal 12-state linear model: every velocity
   derivative equals its full-state reference acceleration plus the SAME
   coupled correction. No independent sigma input is introduced. -/
theorem state_derivative_split (a a0 : Vec) (i : Fin 6) :
    a i=a0 i+delta a a0 i := by unfold delta; ring

#print axioms acceleration_free_resolvent
#print axioms residual_energy_identity
#print axioms correlated_acceleration_energy
#print axioms correction_cost_from_full_force
#print axioms full_state_error_split
#print axioms total_error_from_coupled_residual
end
end RouteBCoupledResolvent
