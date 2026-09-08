import Mathlib

namespace RouteBP5TargetDomainObstruction

/-- Minimal typed state needed by the P5-099 broad target-domain witness.  This
sidecar deliberately keeps the physical DH/source graph outside the kernel leaf. -/
structure TargetState where
  q : Fin 6 → ℝ
  v : Fin 6 → ℝ
  w : ℝ

/-- The broad q/v ellipsoid used by the current target-domain sidecar. -/
def fullP (x : TargetState) : ℝ :=
  (3 / 2 : ℝ) * ∑ i, (x.q i) ^ 2 +
    (4 / 5 : ℝ) * ∑ i, (x.v i) ^ 2

/-- Displayed broad coordinate/disturbance caps. -/
def GrowthCaps (x : TargetState) : Prop :=
  (∀ i, |x.q i| ≤ (5 / 2 : ℝ)) ∧
    (∀ i, |x.v i| ≤ (15 : ℝ)) ∧
      |x.w| ≤ (2 : ℝ)

/-- The exact P5-099 obstruction state: q=0, v=0, disturbance=1. -/
def witness : TargetState where
  q := fun _ => 0
  v := fun _ => 0
  w := 1

/-- Broad algebraic target-domain predicate only.  This is not a reachable-set
or ODE-flow predicate. -/
def BroadTarget (x : TargetState) : Prop :=
  fullP x ≤ (28 / 5 : ℝ) ∧ x.w ^ 2 ≤ (3 : ℝ) ∧ GrowthCaps x

/-- Optional ramp algebra used only to show that the displayed relation w=a*t
alone does not exclude w=1. -/
def rampDisturbance (amplitude time : ℝ) : ℝ := amplitude * time

/-- Frozen exact rational direct-target deficit supplied by the upstream
mathematics review.  Binding this number to the deployed DH evaluator remains a
separate source theorem. -/
def gapG : ℝ :=
  (908496145006016245606224697730990370520062591844085847627884168761717525947223 : ℝ) /
    6758722017363098327650876161130774484190251396262627754497272897204629481055540

/-- A witness beta template that makes the q/v-weight boundary explicit. -/
def betaAt
    (pq pv pa pw S : ℝ) (x : TargetState) : ℝ :=
  pq * ∑ i, (x.q i) ^ 2 +
    pv * ∑ i, (x.v i) ^ 2 +
      pa * S + pw * x.w ^ 2

theorem witness_fullP_zero : fullP witness = 0 := by
  simp [fullP, witness]

theorem witness_growth_caps : GrowthCaps witness := by
  norm_num [GrowthCaps, witness]

theorem witness_in_broad_target : BroadTarget witness := by
  constructor
  · rw [witness_fullP_zero]
    norm_num
  constructor
  · norm_num [witness]
  · exact witness_growth_caps

theorem witness_has_strict_displayed_reserve :
    fullP witness < (28 / 5 : ℝ) ∧
      witness.w ^ 2 < (3 : ℝ) ∧
        |witness.w| < (2 : ℝ) := by
  rw [witness_fullP_zero]
  norm_num [witness]

theorem witness_ramp_realization :
    rampDisturbance 1 1 = witness.w ∧
      (1 : ℝ) ^ 2 ≤ 3 ∧
        (0 : ℝ) ≤ 1 ∧ (1 : ℝ) ≤ 1 := by
  norm_num [rampDisturbance, witness]

/-- The exact frozen gap is strictly larger than 11/100. -/
theorem gapG_gt_eleven_percent : (11 / 100 : ℝ) < gapG := by
  norm_num [gapG]

theorem gapG_pos : 0 < gapG := by
  exact lt_trans (by norm_num : (0 : ℝ) < 11 / 100) gapG_gt_eleven_percent

/-- Sharp pointwise repair: if the old target value is exactly -G, adding g
reaches target floor t iff g is at least G+t. -/
theorem beta_increment_iff
    (G g t Pold : ℝ)
    (hP : Pold = -G) :
    Pold + g ≥ t ↔ G + t ≤ g := by
  rw [hP]
  constructor <;> intro h <;> linarith

/-- Exact specialization to the frozen P5-099 rational gap. -/
theorem exact_gap_beta_increment_iff
    (g t Pold : ℝ)
    (hP : Pold = -gapG) :
    Pold + g ≥ t ↔ gapG + t ≤ g := by
  exact beta_increment_iff gapG g t Pold hP

/-- With no added charge, the frozen witness target is strictly negative. -/
theorem exact_gap_target_negative
    (Pold : ℝ)
    (hP : Pold = -gapG) :
    Pold < 0 := by
  rw [hP]
  linarith [gapG_pos]

/-- Equivalent sharp statement for weakening the target floor instead of
increasing beta. -/
theorem floor_weakening_iff
    (G tau Pold : ℝ)
    (hP : Pold = -G) :
    Pold ≥ -tau ↔ G ≤ tau := by
  rw [hP]
  constructor <;> intro h <;> linarith

/-- Division-free coefficient half-space at the witness.  No positivity of S is
needed until one chooses to divide and solve explicitly for pa. -/
theorem witness_beta_coeff_halfspace_iff
    (S h pa pw t : ℝ) :
    pa * S + pw - h ≥ t ↔ h + t ≤ pa * S + pw := by
  constructor <;> intro htarget <;> linarith

/-- q/v beta weights vanish identically at q=v=0, so changing only those
coefficients cannot repair this witness. -/
theorem witness_qv_weights_vanish
    (pq pv pa pw S : ℝ) :
    betaAt pq pv pa pw S witness = pa * S + pw := by
  simp [betaAt, witness]

/-- Exact linear-arithmetic debit for the fixed lambda=2 proof route. -/
theorem witness_lambda2_budget_iff
    (h b d g t : ℝ) :
    b + g ≥ 2 * h + 2 * d + t ↔
      (2 * h - b) + 2 * d + t ≤ g := by
  constructor <;> intro hbudget <;> linarith

/-- Typed obstruction consumer: once a separate source theorem identifies the
witness target with -gapG, universal nonnegativity over the displayed broad
algebraic domain is impossible. -/
theorem broad_target_universal_nonnegative_false
    (P : TargetState → ℝ)
    (hPw : P witness = -gapG) :
    ¬ (∀ x, BroadTarget x → 0 ≤ P x) := by
  intro hall
  have hnonneg : 0 ≤ P witness := hall witness witness_in_broad_target
  have hneg : P witness < 0 := exact_gap_target_negative (P witness) hPw
  linarith

#print axioms witness_fullP_zero
#print axioms witness_growth_caps
#print axioms witness_in_broad_target
#print axioms witness_has_strict_displayed_reserve
#print axioms witness_ramp_realization
#print axioms gapG_gt_eleven_percent
#print axioms gapG_pos
#print axioms beta_increment_iff
#print axioms exact_gap_beta_increment_iff
#print axioms exact_gap_target_negative
#print axioms floor_weakening_iff
#print axioms witness_beta_coeff_halfspace_iff
#print axioms witness_qv_weights_vanish
#print axioms witness_lambda2_budget_iff
#print axioms broad_target_universal_nonnegative_false

end RouteBP5TargetDomainObstruction
