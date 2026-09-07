import Mathlib

/-!
OPEN_UNCOMPILED. Decimal-text arithmetic and a missing-premise counterexample.
Selected CSV: routeB_compact_external_budget_ledger.csv, physical line 9.
eta=5.6, theta=1.0, mass_regularizer=1e-6. No other row is used.
The rationals below model printed decimal tokens, NOT Float64 execution,
directed interval bounds, source reification or a descriptor-feasible state.
No Lean/Lake execution or admission/physical-certificate claim.
-/
set_option autoImplicit false

namespace RouteBP4032ActualRowMissingBase

noncomputable section

def candidateGamma : ℝ := 1 / 5
def candidateCharge : ℝ := 15698624457194343 / 100000000000000000
def printedMargin : ℝ := 4301375542805658 / 100000000000000000
def printedRhoSquared : ℝ := 7849312228597172 / 100000000000000000

theorem exact_decimal_external_slack :
    candidateGamma - candidateCharge = 4301375542805657 / 100000000000000000 := by
  norm_num [candidateGamma, candidateCharge]

theorem external_slack_positive : candidateCharge < candidateGamma := by
  norm_num [candidateGamma, candidateCharge]

/-- CSV decimal fields cannot all be identified as exact rational operations. -/
theorem printed_subtraction_discrepancy :
    printedMargin - (candidateGamma - candidateCharge) = 1 / 100000000000000000 := by
  norm_num [printedMargin, candidateGamma, candidateCharge]

theorem printed_young_discrepancy :
    2 * printedRhoSquared - candidateCharge = 1 / 100000000000000000 := by
  norm_num [printedRhoSquared, candidateCharge]

/-- The generator's full conservative scalar expression, with ell=||l_base||.
This definition alone does not identify it with a physical Schur margin. -/
def youngMargin (base ell metric theta charge : ℝ) : ℝ :=
  base - (1 + theta) * ell ^ 2 - charge * metric

/-- Exact minimal pointwise allocation obligation for this expression. -/
theorem target_iff_base_allocation (base ell metric theta charge target : ℝ) :
    target ≤ youngMargin base ell metric theta charge ↔
      target + (1 + theta) * ell ^ 2 + charge * metric ≤ base := by
  unfold youngMargin
  constructor <;> intro h <;> linarith

/-- A larger external cap helps only AFTER the base allocation is supplied. -/
theorem consume_base_allocation (base ell metric theta charge gamma target : ℝ)
    (hmetric : 0 ≤ metric) (hcap : charge ≤ gamma)
    (hbase : target + (1 + theta) * ell ^ 2 + gamma * metric ≤ base) :
    target ≤ youngMargin base ell metric theta charge := by
  apply (target_iff_base_allocation base ell metric theta charge target).mpr
  have hmul : charge * metric ≤ gamma * metric := mul_le_mul_of_nonneg_right hcap hmetric
  linarith

/-- Consumes only explicitly bound functions on ONE domain. Source identity,
normalization and domain coverage are still external prerequisites. -/
theorem same_domain_consumer {X : Type*} (D : X → Prop)
    (base ell metric margin : X → ℝ) (theta charge gamma target : ℝ)
    (hmetric : ∀ x, D x → 0 ≤ metric x) (hcap : charge ≤ gamma)
    (hbase : ∀ x, D x →
      target + (1 + theta) * ell x ^ 2 + gamma * metric x ≤ base x)
    (hcomparison : ∀ x, D x →
      youngMargin (base x) (ell x) (metric x) theta charge ≤ margin x) :
    ∀ x, D x → target ≤ margin x := by
  intro x hx
  exact (consume_base_allocation (base x) (ell x) (metric x) theta charge gamma target
    (hmetric x hx) hcap (hbase x hx)).trans (hcomparison x hx)

/-- Exact interface assignment: same-row positive external slack, but a
negative full expression once the missing base residual is included.
Not claimed to satisfy the physical descriptor manifold. -/
theorem row_slack_does_not_close_full_budget :
    candidateCharge < candidateGamma ∧
    youngMargin candidateGamma 1 1 1 candidateCharge =
      -(195698624457194343 / 100000000000000000) ∧
    youngMargin candidateGamma 1 1 1 candidateCharge < 0 := by
  norm_num [candidateCharge, candidateGamma, youngMargin]

theorem row_counterexample_blocks_every_positive_target (target : ℝ) (hp : 0 < target) :
    ¬ target ≤ youngMargin candidateGamma 1 1 1 candidateCharge := by
  have hn := row_slack_does_not_close_full_budget.2.2
  linarith

/-- Keep ALL selected coefficients, ell, metric and target fixed. Changing
only the unrecorded base term reverses prescribed-target feasibility. -/
theorem same_coefficients_opposite_target_results :
    (0 : ℝ) < 1 / 100 ∧
    ¬ (1 / 100 ≤ youngMargin candidateGamma 1 1 1 candidateCharge) ∧
    1 / 100 ≤ youngMargin (candidateGamma + 2) 1 1 1 candidateCharge := by
  norm_num [candidateGamma, candidateCharge, youngMargin]

/-- Even a perfect base allocation with zero baseline may yield only a
homogeneous margin. A zero metric point prevents a positive CONSTANT floor. -/
theorem zero_metric_no_positive_floor (gamma charge target : ℝ) (hp : 0 < target) :
    ¬ target ≤ (gamma - charge) * 0 := by
  simp only [mul_zero]
  exact not_le_of_gt hp

end
end RouteBP4032ActualRowMissingBase
