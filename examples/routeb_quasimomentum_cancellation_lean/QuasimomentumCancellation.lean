import Mathlib

set_option autoImplicit false

namespace RouteBQuasimomentumCancellation

/-!
Route-B quasi-momentum cancellation as a pure exact-real algebra leaf.

The `v6` coefficient is represented by the finite difference of an affine
profile.  This is deliberately a local algebraic interface: no dynamics,
trajectory, source binding, or numerical implementation is imported.
-/

noncomputable section

def kappa : ℝ := (50000 : ℝ) / 50003

def affineV6 (constant slope : ℝ) : ℝ → ℝ :=
  fun v6 => constant + slope * v6

def quasiMomentum (y p4 p6 : ℝ) : ℝ :=
  p4 - kappa * Real.cos y * p6

def v6Coefficient (profile : ℝ → ℝ) : ℝ :=
  profile 1 - profile 0

def quasiMomentumV6Profile
    (y r4 m46 r6 m66 : ℝ) : ℝ → ℝ :=
  fun v6 =>
    quasiMomentum y (affineV6 r4 m46 v6) (affineV6 r6 m66 v6)

structure OpenInputs where
  /-- The q6-driven contribution, deliberately not set to zero here. -/
  q6Drive : ℝ
  /-- The finite-difference implementation defect, deliberately not bounded here. -/
  fdDefect : ℝ

def routeBResidual
    (y r4 m46 r6 m66 v6 : ℝ) (inputs : OpenInputs) : ℝ :=
  quasiMomentumV6Profile y r4 m46 r6 m66 v6 +
    inputs.q6Drive + inputs.fdDefect

theorem kappa_denominator_nonzero : (50003 : ℝ) ≠ 0 := by
  norm_num

theorem kappa_times_denominator : kappa * (50003 : ℝ) = 50000 := by
  unfold kappa
  field_simp

theorem affineV6_coefficient (constant slope : ℝ) :
    v6Coefficient (affineV6 constant slope) = slope := by
  unfold v6Coefficient affineV6
  ring

theorem quasiMomentumV6Profile_expansion
    (y r4 m46 r6 m66 v6 : ℝ) :
    quasiMomentumV6Profile y r4 m46 r6 m66 v6 =
      (r4 - kappa * Real.cos y * r6) +
        (m46 - kappa * Real.cos y * m66) * v6 := by
  unfold quasiMomentumV6Profile quasiMomentum affineV6
  ring

theorem quasiMomentum_v6_coefficient_cancel
    (y r4 m46 r6 m66 : ℝ)
    (hcoef : m46 = kappa * Real.cos y * m66) :
    v6Coefficient (quasiMomentumV6Profile y r4 m46 r6 m66) = 0 := by
  rw [show v6Coefficient (quasiMomentumV6Profile y r4 m46 r6 m66) =
      m46 - kappa * Real.cos y * m66 by
        unfold v6Coefficient
        rw [quasiMomentumV6Profile_expansion, quasiMomentumV6Profile_expansion]
        ring]
  rw [hcoef]
  ring

theorem quasiMomentum_v6_term_eliminated
    (y r4 m46 r6 m66 : ℝ)
    (hcoef : m46 = kappa * Real.cos y * m66) :
    ∀ v6, quasiMomentumV6Profile y r4 m46 r6 m66 v6 =
      r4 - kappa * Real.cos y * r6 := by
  intro v6
  rw [quasiMomentumV6Profile_expansion, hcoef]
  ring

theorem routeB_v6_coefficient_cancels
    (y r4 r6 : ℝ) :
    v6Coefficient
      (quasiMomentumV6Profile y r4 (50000 * Real.cos y) r6 50003) = 0 := by
  apply quasiMomentum_v6_coefficient_cancel
  unfold kappa
  field_simp

theorem routeB_v6_term_eliminated
    (y r4 r6 v6 : ℝ) :
    quasiMomentumV6Profile y r4 (50000 * Real.cos y) r6 50003 v6 =
      r4 - kappa * Real.cos y * r6 := by
  apply quasiMomentum_v6_term_eliminated
  unfold kappa
  field_simp

theorem routeB_residual_retains_open_inputs
    (y r4 m46 r6 m66 v6 : ℝ) (inputs : OpenInputs) :
    routeBResidual y r4 m46 r6 m66 v6 inputs -
        quasiMomentumV6Profile y r4 m46 r6 m66 v6 =
      inputs.q6Drive + inputs.fdDefect := by
  unfold routeBResidual
  ring

theorem routeB_residual_decomposition
    (y r4 m46 r6 m66 v6 : ℝ) (inputs : OpenInputs) :
    routeBResidual y r4 m46 r6 m66 v6 inputs =
      quasiMomentumV6Profile y r4 m46 r6 m66 v6 +
        inputs.q6Drive + inputs.fdDefect := by
  rfl

#print axioms kappa_denominator_nonzero
#print axioms kappa_times_denominator
#print axioms affineV6_coefficient
#print axioms quasiMomentumV6Profile_expansion
#print axioms quasiMomentum_v6_coefficient_cancel
#print axioms quasiMomentum_v6_term_eliminated
#print axioms routeB_v6_coefficient_cancels
#print axioms routeB_v6_term_eliminated
#print axioms routeB_residual_retains_open_inputs
#print axioms routeB_residual_decomposition

end
end RouteBQuasimomentumCancellation
