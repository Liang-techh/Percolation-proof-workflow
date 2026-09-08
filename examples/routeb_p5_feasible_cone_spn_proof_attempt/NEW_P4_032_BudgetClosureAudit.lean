import NEW_P4_032_SchurPMIAbsorption
import NEW_P4_032_ActualRowMissingBase

/-!
OPEN_UNCOMPILED / pending. Bounded audit additions: one additive debit,
sharp target-allocation interfaces and opposite-base scalar witnesses.
No source/matrix/trajectory realization or registry admission is asserted.
-/
set_option autoImplicit false

namespace RouteBP4032BudgetClosureAudit

open RouteBP4032RelativeAdditive RouteBP4032SchurPMIAbsorption
open RouteBP4032ActualRowMissingBase

noncomputable section

/-- The supplied Schur comparison already contains the residual deduction.
The resulting lower bound consumes biasEff once. -/
theorem one_debit_target (p : Parameters) (energy q delta margin target : ℝ)
    (budget : AbsorbedAt p energy q delta)
    (binding : SchurPMIBinding energy q margin)
    (halloc : target + biasEff p ≤ delta * energy) : target ≤ margin := by
  have h := schur_pmi_margin p energy q delta margin budget binding
  linarith

/-- Necessity here is universal over margins known ONLY through this floor;
it is not necessity for a particular source margin that could be larger. -/
theorem lower_floor_target_iff (delta energy bias target : ℝ) :
    (∀ margin : ℝ, delta * energy - bias ≤ margin → target ≤ margin) ↔
      target + bias ≤ delta * energy := by
  constructor
  · intro h
    have hm := h (delta * energy - bias) le_rfl
    linarith
  · intro h margin hm
    linarith

/-- Keeping the additive load is necessary even with strict relative slack.
This tuple is a scalar interface witness, not a Parameters/source instance. -/
theorem missing_bias_counterexample :
    (0 : ℝ) < 1/2 ∧ 1/2 + 1/2 ≤ (1 : ℝ) ∧
    (1 : ℝ) ≤ (1/2)*0 + 1 ∧
    (0 : ℝ) - 1 ≤ -1 ∧
    ¬ ((1/2 : ℝ)*0 ≤ -1) := by norm_num

/-- The single-debit target succeeds; subtracting q a second time rejects
this exact feasible scalar target. Double subtraction is conservative, not
an unsound lower bound; it cannot be claimed equivalent to the original. -/
theorem duplicate_debit_loses_target :
    (1 : ℝ) ≤ (1/2)*2 + 0 ∧
    (2 : ℝ) - 1 ≤ 1 ∧
    (1 : ℝ) + 0 ≤ (1/2)*2 ∧
    (1 : ℝ) ≤ 2 - 1 ∧ ¬ ((1 : ℝ) ≤ 2 - 1 - 1) := by norm_num

/-- Feedback residual numerator rho*base+bias is sharp already in a scalar
equality example. Omitting bias there fails, while charging it twice is slack. -/
theorem feedback_bias_sharp_example :
    (3 : ℝ) = 2 + 1 ∧
    (1 : ℝ) = (1/4)*3 + 1/4 ∧
    (3/4 : ℝ)*3 = 2 + 1/4 ∧
    (3/4 : ℝ)*1 = (1/4)*2 + 1/4 := by norm_num

/-- A uniform base floor is sufficient and necessary for ALL bases above it,
with every residual/metric/Young coefficient fixed. -/
theorem base_floor_target_iff (baseFloor ell metric theta charge target : ℝ) :
    (∀ base : ℝ, baseFloor ≤ base → target ≤ youngMargin base ell metric theta charge) ↔
      target + (1 + theta)*ell^2 + charge*metric ≤ baseFloor := by
  constructor
  · intro h
    exact (target_iff_base_allocation baseFloor ell metric theta charge target).mp
      (h baseFloor le_rfl)
  · intro h base hb
    exact (target_iff_base_allocation base ell metric theta charge target).mpr (h.trans hb)

/-- Opposite target outcomes can be arbitrarily close to the exact threshold.
Only base changes; positive row slack is neither used nor sufficient. -/
theorem opposite_bases_at_threshold (ell metric theta charge target epsilon : ℝ)
    (heps : 0 < epsilon) :
    ¬ target ≤ youngMargin
      (target + (1+theta)*ell^2 + charge*metric - epsilon) ell metric theta charge ∧
    target ≤ youngMargin
      (target + (1+theta)*ell^2 + charge*metric + epsilon) ell metric theta charge := by
  unfold youngMargin
  constructor <;> linarith

end
end RouteBP4032BudgetClosureAudit
