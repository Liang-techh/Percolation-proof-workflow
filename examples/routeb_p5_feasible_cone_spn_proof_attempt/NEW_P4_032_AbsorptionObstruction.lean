import NEW_P4_032_SchurPMIAbsorption

/-!
UNCOMPILED, source-independent negative branch for scalar absorption.
Exact real witnesses only; no source realization or verification claim.
Does not repeat the positive absorption, weighted, or Schur identities.
-/

set_option autoImplicit false

namespace RouteBP4032AbsorptionObstruction

open RouteBP4032RelativeAdditive
open RouteBP4032SchurPMIAbsorption

noncomputable section

theorem no_positive_slack (rho : ℝ) (hlarge : 1 ≤ rho) :
    ¬ ∃ delta : ℝ, 0 < delta ∧ rho + delta ≤ 1 := by
  rintro ⟨delta, hpos, halloc⟩
  linarith

/-- The negative gate uses exactly the preceding sidecar's Slack type. -/
theorem no_effective_slack (p : Parameters) (hlarge : 1 ≤ rhoEff p) :
    ¬ ∃ delta : ℝ, Slack p delta := by
  rintro ⟨delta, hs⟩
  exact no_positive_slack (rhoEff p) hlarge
    ⟨delta, hs.positive, hs.allocation⟩

/-- Only the scalar information available from a residual upper budget.
This does not assert a realizable force/accel or matrix/source instance. -/
structure ResidualFeasible (rho bias energy q : ℝ) : Prop where
  energy_nonnegative : 0 ≤ energy
  residual_nonnegative : 0 ≤ q
  upper : q ≤ rho * energy + bias

/-- An explicit real exceeding any proposed finite real cap. -/
def beyond (cap : ℝ) : ℝ := max 0 cap + 1

theorem beyond_nonnegative (cap : ℝ) : 0 ≤ beyond cap := by
  have h := le_max_left (0 : ℝ) cap
  unfold beyond
  linarith

theorem beyond_gt (cap : ℝ) : cap < beyond cap := by
  have h := le_max_right (0 : ℝ) cap
  unfold beyond
  linarith

/-- q=0 allows every nonnegative E, even when rho<1. Thus residual-only
information cannot imply any finite uniform energy cap. -/
theorem residual_only_counterexample (rho bias cap : ℝ)
    (hrho : 0 ≤ rho) (hbias : 0 ≤ bias) :
    ResidualFeasible rho bias (beyond cap) 0 ∧ cap < beyond cap := by
  refine ⟨⟨beyond_nonnegative cap, le_rfl, ?_⟩, beyond_gt cap⟩
  exact add_nonneg (mul_nonneg hrho (beyond_nonnegative cap)) hbias

theorem no_residual_only_cap (rho bias : ℝ)
    (hrho : 0 ≤ rho) (hbias : 0 ≤ bias) :
    ¬ ∃ cap : ℝ, ∀ energy q : ℝ,
      ResidualFeasible rho bias energy q → energy ≤ cap := by
  rintro ⟨cap, hcap⟩
  have hw := residual_only_counterexample rho bias cap hrho hbias
  exact (not_le_of_gt hw.2) (hcap (beyond cap) 0 hw.1)

/-- In particular, any affine expression in a fixed external base fails.
The candidate coefficients/base are nonnegative, finite real constants. -/
theorem residual_only_affine_counterexample (rho bias base a b : ℝ)
    (hrho : 0 ≤ rho) (hbias : 0 ≤ bias)
    (hbase : 0 ≤ base) (ha : 0 ≤ a) (hb : 0 ≤ b) :
    ∃ energy q : ℝ, ResidualFeasible rho bias energy q ∧
      a * base + b < energy := by
  exact ⟨beyond (a * base + b), 0,
    residual_only_counterexample rho bias (a * base + b) hrho hbias⟩

/-- The effective parameter packet inherits the same obstruction; small
rhoEff alone does not supply the missing feedback closure. -/
theorem effective_residual_only_counterexample (p : Parameters) (cap : ℝ) :
    ResidualFeasible (rhoEff p) (biasEff p) (beyond cap) 0 ∧
      cap < beyond cap := by
  have hc := effective_coefficients_nonnegative p
  exact residual_only_counterexample (rhoEff p) (biasEff p) cap hc.1 hc.2

/-- Stronger negative branch: when rho>=1, q=E gives arbitrarily large
energy even WITH the old FeedbackBinding E<=base+q. -/
theorem feedback_counterexample (rho bias base cap : ℝ)
    (hrho : 1 ≤ rho) (hbias : 0 ≤ bias) (hbase : 0 ≤ base) :
    ResidualFeasible rho bias (beyond cap) (beyond cap) ∧
      FeedbackBinding (beyond cap) (beyond cap) base ∧ cap < beyond cap := by
  have hE := beyond_nonnegative cap
  have hscaled := mul_le_mul_of_nonneg_right hrho hE
  refine ⟨⟨hE, hE, ?_⟩, ⟨hbase, ?_⟩, beyond_gt cap⟩ <;> nlinarith

/-- Boundary rho=1 is already obstructed with zero additive and base
budgets: every t>=0 gives E=q=t and satisfies feedback exactly. -/
theorem unit_feedback_ray (t : ℝ) (ht : 0 ≤ t) :
    ResidualFeasible 1 0 t t ∧ FeedbackBinding t t 0 := by
  refine ⟨⟨ht, ht, ?_⟩, ⟨le_rfl, ?_⟩⟩ <;> simp

theorem no_feedback_cap (rho bias base : ℝ)
    (hrho : 1 ≤ rho) (hbias : 0 ≤ bias) (hbase : 0 ≤ base) :
    ¬ ∃ cap : ℝ, ∀ energy q : ℝ,
      ResidualFeasible rho bias energy q →
      FeedbackBinding energy q base → energy ≤ cap := by
  rintro ⟨cap, hcap⟩
  have hw := feedback_counterexample rho bias base cap hrho hbias hbase
  exact (not_le_of_gt hw.2.2)
    (hcap (beyond cap) (beyond cap) hw.1 hw.2.1)

/-- Necessity concerns a bound over ALL scalar feasible points. Additional
source restrictions could bound a smaller class even when rho>=1. -/
theorem uniform_feedback_cap_requires_strict (rho bias base : ℝ)
    (hbias : 0 ≤ bias) (hbase : 0 ≤ base)
    (hcap : ∃ cap : ℝ, ∀ energy q : ℝ,
      ResidualFeasible rho bias energy q →
      FeedbackBinding energy q base → energy ≤ cap) : rho < 1 := by
  by_contra hnot
  exact no_feedback_cap rho bias base (le_of_not_gt hnot) hbias hbase hcap

end

-- Future audit commands only; NOT executed in this round.
#print axioms no_positive_slack
#print axioms no_effective_slack
#print axioms residual_only_counterexample
#print axioms no_residual_only_cap
#print axioms residual_only_affine_counterexample
#print axioms effective_residual_only_counterexample
#print axioms feedback_counterexample
#print axioms unit_feedback_ray
#print axioms no_feedback_cap
#print axioms uniform_feedback_cap_requires_strict

end RouteBP4032AbsorptionObstruction
