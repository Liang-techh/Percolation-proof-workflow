import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# Abstract joint `p`/`sigma` budget interface

This file is deliberately an algebraic leaf.  It does not import, identify,
or bind to a Denavit--Hartenberg source.  The only trajectory-level premise is
`IntegratedEnergySeam`; that premise is the explicit place where an external
integral/flowpipe argument must enter.
-/

set_option autoImplicit false

namespace RouteBJointPSigmaBudget

noncomputable section

/-! ## Pointwise state and filter contracts -/

def MomentumSplit (m v sigma p : ℝ) : Prop :=
  p = m * v + sigma

def NormalizedState (q p m xq xp : ℝ) : Prop :=
  xq = q ∧ xp = p / m

def JointState (m q p v sigma xq xp : ℝ) : Prop :=
  MomentumSplit m v sigma p ∧ NormalizedState q p m xq xp

def FilterDynamics (kappa lambda xq xp xqDot xpDot forcing : ℝ) : Prop :=
  xqDot = xp ∧ xpDot = -kappa * xq - lambda * xp + forcing

def EnergyDerivative
    (kappa xq xp xqDot xpDot dV : ℝ) : Prop :=
  dV = kappa * xq * xqDot + xp * xpDot

def V (kappa xq xp : ℝ) : ℝ :=
  (kappa / 2) * xq ^ 2 + (1 / 2) * xp ^ 2

theorem normalized_velocity_identity
    (m q p v sigma xq xp : ℝ) (hm : 0 < m)
    (hsplit : MomentumSplit m v sigma p)
    (hnormalized : NormalizedState q p m xq xp) :
    xp = v + sigma / m := by
  calc
    xp = p / m := hnormalized.2
    _ = (m * v + sigma) / m := by rw [hsplit]
    _ = v + sigma / m := by
      field_simp [ne_of_gt hm]

theorem joint_state_normalized_velocity_identity
    (m q p v sigma xq xp : ℝ) (hm : 0 < m)
    (hstate : JointState m q p v sigma xq xp) :
    xp = v + sigma / m :=
  normalized_velocity_identity m q p v sigma xq xp hm hstate.1 hstate.2

theorem filter_energy_derivative_identity
    (kappa lambda xq xp xqDot xpDot forcing dV : ℝ)
    (hdynamics : FilterDynamics kappa lambda xq xp xqDot xpDot forcing)
    (hderivative : EnergyDerivative kappa xq xp xqDot xpDot dV) :
    dV = -lambda * xp ^ 2 + xp * forcing := by
  calc
    dV = kappa * xq * xqDot + xp * xpDot := hderivative
    _ = -lambda * xp ^ 2 + xp * forcing := by
      rw [hdynamics.1, hdynamics.2]
      ring

theorem filter_energy_derivative_bound
    (kappa lambda xq xp xqDot xpDot forcing dV : ℝ)
    (hlambda : 0 < lambda)
    (hdynamics : FilterDynamics kappa lambda xq xp xqDot xpDot forcing)
    (hderivative : EnergyDerivative kappa xq xp xqDot xpDot dV) :
    dV ≤ forcing ^ 2 / (4 * lambda) := by
  have hidentity := filter_energy_derivative_identity kappa lambda xq xp xqDot
    xpDot forcing dV hdynamics hderivative
  have hden : 0 < 4 * lambda := by positivity
  have hsquare :
      0 ≤ (2 * lambda * xp - forcing) ^ 2 / (4 * lambda) := by
    exact div_nonneg (sq_nonneg _) (le_of_lt hden)
  have hcompletion :
      (2 * lambda * xp - forcing) ^ 2 / (4 * lambda) =
        lambda * xp ^ 2 - xp * forcing + forcing ^ 2 / (4 * lambda) := by
    field_simp [ne_of_gt hlambda]
    ring
  have hgap :
      0 ≤ lambda * xp ^ 2 - xp * forcing + forcing ^ 2 / (4 * lambda) := by
    rw [← hcompletion]
    exact hsquare
  calc
    dV = -lambda * xp ^ 2 + xp * forcing := hidentity
    _ ≤ forcing ^ 2 / (4 * lambda) := by linarith

theorem V_nonneg
    (kappa xq xp : ℝ) (hkappa : 0 ≤ kappa) :
    0 ≤ V kappa xq xp := by
  unfold V
  nlinarith only [hkappa, sq_nonneg xq, sq_nonneg xp]

theorem normalized_velocity_sq_le_two_V
    (kappa xq xp : ℝ) (hkappa : 0 ≤ kappa) :
    xp ^ 2 ≤ 2 * V kappa xq xp := by
  unfold V
  nlinarith only [hkappa, sq_nonneg xq]

/-! ## Explicit external budgets and the conditional integration seam -/

def ForcingBudget (forcingCap accumulatedForcing : ℝ) : Prop :=
  0 ≤ forcingCap ∧ 0 ≤ accumulatedForcing ∧ accumulatedForcing ≤ forcingCap

def SigmaTerminalBound (sigmaCap sigmaTerminal : ℝ) : Prop :=
  0 ≤ sigmaCap ∧ sigmaTerminal ^ 2 ≤ sigmaCap

def IntegratedEnergySeam
    (kappa lambda q0 xp0 qt xpt accumulatedForcing sigmaTerminal : ℝ) : Prop :=
  V kappa qt xpt - V kappa q0 xp0 ≤
    accumulatedForcing / (4 * lambda) + sigmaTerminal ^ 2

def Budget (lambda forcingCap sigmaCap : ℝ) : ℝ :=
  forcingCap / (4 * lambda) + sigmaCap

theorem energy_budget_propagation
    (kappa lambda q0 xp0 qt xpt accumulatedForcing sigmaTerminal
      forcingCap sigmaCap : ℝ)
    (hlambda : 0 < lambda)
    (hforcing : ForcingBudget forcingCap accumulatedForcing)
    (hsigma : SigmaTerminalBound sigmaCap sigmaTerminal)
    (hseam : IntegratedEnergySeam kappa lambda q0 xp0 qt xpt
      accumulatedForcing sigmaTerminal) :
    V kappa qt xpt ≤ V kappa q0 xp0 + Budget lambda forcingCap sigmaCap := by
  have hden : 0 ≤ 4 * lambda := by positivity
  have hforcing_div :
      accumulatedForcing / (4 * lambda) ≤ forcingCap / (4 * lambda) := by
    exact div_le_div_of_nonneg_right hforcing.2.2 hden
  unfold IntegratedEnergySeam at hseam
  unfold Budget
  linarith only [hseam, hforcing_div, hsigma.2]

theorem velocity_sq_of_joint_state
    (m kappa q p v sigma xq xp sigmaCap : ℝ)
    (hm : 0 < m) (hkappa : 0 ≤ kappa)
    (hstate : JointState m q p v sigma xq xp)
    (hsigma : SigmaTerminalBound sigmaCap sigma) :
    v ^ 2 ≤ 4 * V kappa xq xp + 2 * sigmaCap / m ^ 2 := by
  have hnormalized := joint_state_normalized_velocity_identity
    m q p v sigma xq xp hm hstate
  have hsplit :
      v ^ 2 ≤ 2 * xp ^ 2 + 2 * (sigma / m) ^ 2 := by
    have hsq : 0 ≤ (xp + sigma / m) ^ 2 := sq_nonneg _
    have hv : v = xp - sigma / m := by linarith only [hnormalized]
    have hidentity :
        2 * xp ^ 2 + 2 * (sigma / m) ^ 2 - v ^ 2 =
          (xp + sigma / m) ^ 2 := by
      rw [hv]
      ring
    nlinarith only [hsq, hidentity]
  have hxp := normalized_velocity_sq_le_two_V kappa xq xp hkappa
  have hm2 : 0 ≤ m ^ 2 := sq_nonneg m
  have hsigma_div : sigma ^ 2 / m ^ 2 ≤ sigmaCap / m ^ 2 := by
    exact div_le_div_of_nonneg_right hsigma.2 hm2
  have hratio : (sigma / m) ^ 2 = sigma ^ 2 / m ^ 2 := by
    field_simp [ne_of_gt hm]
  rw [hratio] at hsplit
  calc
    v ^ 2 ≤ 2 * xp ^ 2 + 2 * (sigma ^ 2 / m ^ 2) := hsplit
    _ ≤ 4 * V kappa xq xp + 2 * (sigmaCap / m ^ 2) := by
      have hxp_scaled : 2 * xp ^ 2 ≤ 4 * V kappa xq xp := by
        linarith only [hxp]
      have hsigma_scaled :
          2 * (sigma ^ 2 / m ^ 2) ≤ 2 * (sigmaCap / m ^ 2) := by
        exact mul_le_mul_of_nonneg_left hsigma_div (by norm_num)
      linarith only [hxp_scaled, hsigma_scaled]
    _ = 4 * V kappa xq xp + 2 * sigmaCap / m ^ 2 := by ring

theorem velocity_sq_downstream_bound
    (m kappa q p v sigma xq xp sigmaCap V0 B : ℝ)
    (hm : 0 < m) (hkappa : 0 ≤ kappa)
    (hstate : JointState m q p v sigma xq xp)
    (hsigma : SigmaTerminalBound sigmaCap sigma)
    (henergy : V kappa xq xp ≤ V0 + B) :
    v ^ 2 ≤ 4 * (V0 + B) + 2 * sigmaCap / m ^ 2 := by
  have hpoint := velocity_sq_of_joint_state m kappa q p v sigma xq xp
    sigmaCap hm hkappa hstate hsigma
  have hratio : 4 * V kappa xq xp + 2 * sigmaCap / m ^ 2 ≤
      4 * (V0 + B) + 2 * sigmaCap / m ^ 2 := by
    linarith
  exact hpoint.trans hratio

/-! The main combined theorem: the seam gives `V(t) ≤ V(0)+B`, then the
pointwise joint state gives the requested `v^2` downstream bound. -/

theorem joint_budget_and_velocity_bound
    (m kappa lambda q0 xp0 qt pt vt sigmaT xt xpt
      accumulatedForcing forcingCap sigmaCap : ℝ)
    (hm : 0 < m) (hkappa : 0 ≤ kappa) (hlambda : 0 < lambda)
    (hstate : JointState m qt pt vt sigmaT xt xpt)
    (hforcing : ForcingBudget forcingCap accumulatedForcing)
    (hsigma : SigmaTerminalBound sigmaCap sigmaT)
    (hseam : IntegratedEnergySeam kappa lambda q0 xp0 xt xpt
      accumulatedForcing sigmaT) :
    V kappa xt xpt ≤ V kappa q0 xp0 + Budget lambda forcingCap sigmaCap ∧
      vt ^ 2 ≤ 4 * (V kappa q0 xp0 + Budget lambda forcingCap sigmaCap) +
        2 * sigmaCap / m ^ 2 := by
  have henergy := energy_budget_propagation kappa lambda q0 xp0 xt xpt
    accumulatedForcing sigmaT forcingCap sigmaCap hlambda hforcing hsigma hseam
  constructor
  · exact henergy
  · exact velocity_sq_downstream_bound m kappa qt pt vt sigmaT xt xpt sigmaCap
      (V kappa q0 xp0) (Budget lambda forcingCap sigmaCap)
      hm hkappa hstate hsigma henergy

#print axioms normalized_velocity_identity
#print axioms joint_state_normalized_velocity_identity
#print axioms filter_energy_derivative_identity
#print axioms filter_energy_derivative_bound
#print axioms V_nonneg
#print axioms normalized_velocity_sq_le_two_V
#print axioms energy_budget_propagation
#print axioms velocity_sq_of_joint_state
#print axioms velocity_sq_downstream_bound
#print axioms joint_budget_and_velocity_bound

end
end RouteBJointPSigmaBudget
