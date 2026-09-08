import NEW_P4_032_ExactCellLambdaConsumer

/-!
OPEN_UNCOMPILED / pending. Normalization directions and prescribed target.
No Lean/Lake, source reification, physical/PSD claim or registry mutation.
-/
set_option autoImplicit false

namespace RouteBP4032NormalizedTargetGuard

open RouteBP4032SameSourceConsumerPacket RouteBP4032ExactCellLambdaConsumer
open RouteBP4032UniformParameterBridge RouteBP4032ResidualMarginConsumer
open RouteBP4032DualScaleComposition RouteBP4032MinimalResidualBudgetAdapter

noncomputable section

/-- A separately prescribed P4 target must fit the normalized source floor. -/
structure TargetTransfer (nu sourceTarget requestedTarget : ℝ) : Prop where
  positive : 0 < requestedTarget
  fits : requestedTarget ≤ nu * sourceTarget

/-- Sharp information-theoretic gate when the only margin fact is a floor. -/
theorem universal_floor_transfer_iff (floor target : ℝ) :
    (∀ margin : ℝ, floor ≤ margin → target ≤ margin) ↔ target ≤ floor := by
  constructor
  · intro h
    exact h floor (le_refl floor)
  · intro h margin hm
    exact h.trans hm

/-- Keeping the old positive numerical target is valid from this floor
alone exactly when normalization does not shrink it. -/
theorem old_target_fits_iff (nu target : ℝ) (ht : 0 < target) :
    target ≤ nu * target ↔ 1 ≤ nu := by
  constructor
  · intro h
    nlinarith
  · intro h
    nlinarith

/-- Sufficient one-sided alternative to exact normalization identities.
The product gain*beta must be bounded ABOVE, the nominal bounded BELOW.
This scalar lemma does not construct or relax P4's separate sign contracts. -/
theorem conservative_normalization (base q nominal gain beta margin nu target : ℝ)
    (hnu : 0 ≤ nu) (hq : 0 ≤ q) (hf : target ≤ base - q)
    (hnominal : nu * base ≤ nominal) (hproduct : gain * beta ≤ nu)
    (hcomparison : nominal - gain * (beta * q) ≤ margin) :
    nu * target ≤ margin := by
  have hs := mul_le_mul_of_nonneg_left hf hnu
  have hcharge := mul_le_mul_of_nonneg_right hproduct hq
  nlinarith

/-- End-to-end common rational s -> nu*t -> requested P4 target.
No theta=1 Allocation, alpha=beta, or front factor is inferred. -/
theorem common_guard_requested_target {key : SourceKey} {X Z ι : Type*}
    (src : SourceFields key X) (c : RationalCharges ι) (e : SameSourceCharges src c)
    (guard : RationalGuard c) (s : ℚ) (hl : guard.lo ≤ s) (hh : s ≤ guard.hi)
    (f : ParameterField Z) (m : MarginField Z) (scales : ScaleFields Z)
    (embed : X → Z) (nu requested : ℝ) (hnu : 0 < nu)
    (binding : P4Binding src f m scales embed nu)
    (comparison : ScaledComparison f m (residualValues scales))
    (transfer : TargetTransfer nu (c.target : ℝ) requested) :
    ∀ x, src.domain x → 0 < requested ∧ requested ≤ m.margin (embed x) := by
  have hsource := rational_common_source_target src c e guard s hl hh
  have ht : 0 < (c.target : ℝ) := by exact_mod_cast c.target_positive
  have hp4 := source_floor_to_P4 src (c.target : ℝ) ht
    (fun x hx => (hsource x hx).2) f m scales embed nu hnu binding comparison
  intro x hx
  exact ⟨transfer.positive, transfer.fits.trans (hp4 x hx).2⟩

/-- Exact nu=1/2, base=2,q=1,t=1: nu*t is sharp; the old target fails. -/
theorem swallowed_normalization_counterexample :
    (1 : ℝ) ≤ 2 - 1 ∧
    (1 / 2 : ℝ) * 1 ≤ (1 / 2) * 2 - (1 / 2) * 1 ∧
    ¬ (1 : ℝ) ≤ (1 / 2) * 2 - (1 / 2) * 1 := by
  norm_num

/-- gain=nu=1 is insufficient when beta=3 has been omitted. -/
theorem swallowed_beta_counterexample :
    (1 : ℝ) ≤ 2 - 1 ∧
    2 - 1 * (3 * 1) = (-1 : ℝ) ∧
    ¬ (1 : ℝ) * 1 ≤ 2 - 1 * (3 * 1) := by
  norm_num

/-- alpha=1/2 multiplies the base/front side, but gain*beta=1.
Replacing nu by alpha without the residual-product condition is unsound. -/
theorem front_factor_is_not_residual_factor :
    (1 : ℝ) ≤ 2 - 1 ∧
    (1 / 2 : ℝ) * 2 - 1 * (1 * 1) = 0 ∧
    ¬ (1 / 2 : ℝ) * 1 ≤ (1 / 2) * 2 - 1 * (1 * 1) := by
  norm_num

/-- An upper bound on nominal has the wrong direction for a lower margin. -/
theorem nominal_upper_is_insufficient :
    (0 : ℝ) ≤ 1 * 2 ∧ (1 : ℝ) ≤ 2 - 1 ∧
    ¬ (1 : ℝ) * 1 ≤ 0 - 1 * (1 * 1) := by
  norm_num

end
end RouteBP4032NormalizedTargetGuard
