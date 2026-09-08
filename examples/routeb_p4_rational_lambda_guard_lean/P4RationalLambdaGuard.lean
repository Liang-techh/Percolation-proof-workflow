import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# Route-B P4 rational common-lambda interval guard

Source-independent Lean decomposition of the T-P4-039 common-parameter
algebra and the T-P4-040 implementation-rounding adapter:
`agent_review_inbox/review-T-P4-039-liuguanyi-20260907T1616.md` and
`agent_review_inbox/review-T-P4-040-rational-lambda-guard-kuangmanmozun-20260907T1642.md`.

The sidecar proves the exact quadratic chord identity, endpoint certification
for convex scalar quadratics, a common finite-family interval consumer, a
symmetric rounding guard, coefficient-envelope domination on the positive
`lambda - 1` half-line, and exact counterexamples for the hypotheses that must
not be dropped.

It does not prove any concrete DH/source coefficient, Float64 realization
containment, P8 trajectory/domain coverage, P4/M4 closure, or registry
admission.
-/

set_option autoImplicit false

namespace RouteBP4RationalLambdaGuard

noncomputable section

/-- Checker-facing quadratic in `s = lambda - 1`. -/
def quadratic (P G A s : ℝ) : ℝ :=
  P * s^2 - G * s + A

/-! ### T-P4-039 division-free algebraic leaves

The trusted-facing statements below use `Real`, with rational certificates
instantiated by coercion.  Interval membership is expressed by the two
cross-multiplied inequalities
`G - radius ≤ 2*A*theta` and `2*A*theta ≤ G + radius`; no inverse or
division occurs in any of these four theorem statements.
-/

/-- Completed-square identity for the scalar Young quadratic. -/
theorem young_completed_square_identity
    (A G P theta : ℝ) :
    4 * A * (A * theta^2 - G * theta + P) =
      (2 * A * theta - G)^2 - (G^2 - 4 * A * P) := by
  ring

/-- A division-free rational-radius certificate for one Young row. -/
theorem young_feasible_of_rational_radius
    (A G P theta radius : ℝ)
    (hA : 0 < A) (htheta : 0 < theta) (hradius : 0 ≤ radius)
    (hdisc : radius^2 ≤ G^2 - 4 * A * P)
    (hcenter : (2 * A * theta - G)^2 ≤ radius^2) :
    A * theta^2 - G * theta + P ≤ 0 := by
  have hscale : 0 ≤ 4 * A := by positivity
  have hcompleted :
      4 * A * (A * theta^2 - G * theta + P) ≤ 0 := by
    rw [young_completed_square_identity]
    linarith
  nlinarith

/-- The inner rational interval, written without endpoint divisions. -/
theorem young_inner_interval_feasible
    (A G P theta radius : ℝ)
    (hA : 0 < A) (hG : 0 < G) (hP : 0 ≤ P)
    (htheta : 0 < theta) (hradius : 0 ≤ radius)
    (hdisc : radius^2 ≤ G^2 - 4 * A * P)
    (hlower : G - radius ≤ 2 * A * theta)
    (hupper : 2 * A * theta ≤ G + radius) :
    A * theta^2 - G * theta + P ≤ 0 := by
  have hleft : 0 ≤ radius - (2 * A * theta - G) := by
    linarith
  have hright : 0 ≤ radius + (2 * A * theta - G) := by
    linarith
  have hcenter : (2 * A * theta - G)^2 ≤ radius^2 := by
    nlinarith [mul_nonneg hleft hright]
  exact young_feasible_of_rational_radius
    A G P theta radius hA htheta hradius hdisc hcenter

/-- One shared positive `theta` consumes all supplied inner-bound rows. -/
theorem young_common_parameter_of_inner_bounds
    {ι : Type*}
    (A G P radius : ι → ℝ) (theta : ℝ)
    (hA : ∀ i, 0 < A i) (hG : ∀ i, 0 < G i) (hP : ∀ i, 0 ≤ P i)
    (htheta : 0 < theta)
    (hradius : ∀ i, 0 ≤ radius i)
    (hdisc : ∀ i, (radius i)^2 ≤ (G i)^2 - 4 * A i * P i)
    (hlower : ∀ i, G i - radius i ≤ 2 * A i * theta)
    (hupper : ∀ i, 2 * A i * theta ≤ G i + radius i) :
    ∀ i, A i * theta^2 - G i * theta + P i ≤ 0 := by
  intro i
  exact young_inner_interval_feasible
    (A i) (G i) (P i) theta (radius i)
    (hA i) (hG i) (hP i) htheta (hradius i) (hdisc i)
    (hlower i) (hupper i)

/-- Exact chord identity for a scalar quadratic. -/
theorem quadratic_chord_identity
    (P G A a b t : ℝ) :
    quadratic P G A ((1 - t) * a + t * b) =
      (1 - t) * quadratic P G A a + t * quadratic P G A b -
        P * t * (1 - t) * (b - a)^2 := by
  unfold quadratic
  ring

/-- A convex quadratic whose two endpoints are nonpositive is nonpositive at
any explicit convex combination of those endpoints. -/
theorem convex_quadratic_endpoint_interval
    (P G A a b t : ℝ)
    (hP : 0 ≤ P) (ht0 : 0 ≤ t) (ht1 : t ≤ 1)
    (hqa : quadratic P G A a ≤ 0)
    (hqb : quadratic P G A b ≤ 0) :
    quadratic P G A ((1 - t) * a + t * b) ≤ 0 := by
  have h1t : 0 ≤ 1 - t := by linarith
  have hleft : (1 - t) * quadratic P G A a ≤ 0 :=
    mul_nonpos_of_nonneg_of_nonpos h1t hqa
  have hright : t * quadratic P G A b ≤ 0 :=
    mul_nonpos_of_nonneg_of_nonpos ht0 hqb
  have hpenalty : 0 ≤ P * t * (1 - t) * (b - a)^2 := by
    positivity
  rw [quadratic_chord_identity]
  linarith

/-- Endpoint certification stated directly for every real `s` in `[a,b]`.
The proof constructs the convex-combination parameter only internally. -/
theorem convex_quadratic_on_interval
    (P G A a b s : ℝ)
    (hP : 0 ≤ P) (hab : a ≤ b) (has : a ≤ s) (hsb : s ≤ b)
    (hqa : quadratic P G A a ≤ 0)
    (hqb : quadratic P G A b ≤ 0) :
    quadratic P G A s ≤ 0 := by
  by_cases hEq : a = b
  · have hs : s = a := by linarith
    simpa [hs] using hqa
  · have hlt : a < b := lt_of_le_of_ne hab hEq
    have hden : 0 < b - a := sub_pos.mpr hlt
    let t : ℝ := (s - a) / (b - a)
    have hmul : t * (b - a) = s - a := by
      dsimp [t]
      field_simp [ne_of_gt hden]
    have ht0 : 0 ≤ t := by
      by_contra hnot
      have htneg : t < 0 := lt_of_not_ge hnot
      have hprodneg : t * (b - a) < 0 :=
        mul_neg_of_neg_of_pos htneg hden
      linarith
    have ht1 : t ≤ 1 := by
      by_contra hnot
      have htgt : 1 < t := lt_of_not_ge hnot
      have hpos : 0 < (t - 1) * (b - a) :=
        mul_pos (sub_pos.mpr htgt) hden
      nlinarith [hmul]
    have hrep : s = (1 - t) * a + t * b := by
      nlinarith [hmul]
    have h := convex_quadratic_endpoint_interval
      P G A a b t hP ht0 ht1 hqa hqb
    rw [← hrep] at h
    exact h

/-- One common interval certifies every row in a family.  No finiteness is
needed in the kernel consumer: a finite checker may instantiate `ι` with its
row index type. -/
theorem common_lambda_interval
    {ι : Type*}
    (P G A : ι → ℝ) (a b s : ℝ)
    (hP : ∀ i, 0 ≤ P i)
    (hab : a ≤ b) (has : a ≤ s) (hsb : s ≤ b)
    (hqa : ∀ i, quadratic (P i) (G i) (A i) a ≤ 0)
    (hqb : ∀ i, quadratic (P i) (G i) (A i) b ≤ 0) :
    ∀ i, quadratic (P i) (G i) (A i) s ≤ 0 := by
  intro i
  exact convex_quadratic_on_interval
    (P i) (G i) (A i) a b s (hP i) hab has hsb (hqa i) (hqb i)

/-- Direct `lambda`-facing version of the common interval theorem. -/
theorem common_fixed_lambda_interval
    {ι : Type*}
    (P G A : ι → ℝ) (a b lambda : ℝ)
    (hP : ∀ i, 0 ≤ P i)
    (hab : a ≤ b)
    (hlow : 1 + a ≤ lambda) (hhigh : lambda ≤ 1 + b)
    (hqa : ∀ i, quadratic (P i) (G i) (A i) a ≤ 0)
    (hqb : ∀ i, quadratic (P i) (G i) (A i) b ≤ 0) :
    ∀ i, quadratic (P i) (G i) (A i) (lambda - 1) ≤ 0 := by
  apply common_lambda_interval P G A a b (lambda - 1) hP hab
  · linarith
  · linarith
  · exact hqa
  · exact hqb

/-- Exact right-endpoint expansion around a nominal rational witness. -/
theorem quadratic_center_plus_identity
    (P G A s0 r : ℝ) :
    quadratic P G A (s0 + r) =
      quadratic P G A s0 + (2 * P * s0 - G) * r + P * r^2 := by
  unfold quadratic
  ring

/-- Exact left-endpoint expansion around a nominal rational witness. -/
theorem quadratic_center_minus_identity
    (P G A s0 r : ℝ) :
    quadratic P G A (s0 - r) =
      quadratic P G A s0 - (2 * P * s0 - G) * r + P * r^2 := by
  unfold quadratic
  ring

/-- Exact symmetric rounding guard: endpoint checks certify every realized
`s` whose real error from `s0` is at most `r`. -/
theorem symmetric_rounding_guard
    (P G A s0 r s : ℝ)
    (hP : 0 ≤ P) (hr : 0 ≤ r)
    (hdist : |s - s0| ≤ r)
    (hleft : quadratic P G A (s0 - r) ≤ 0)
    (hright : quadratic P G A (s0 + r) ≤ 0) :
    quadratic P G A s ≤ 0 := by
  rcases abs_le.mp hdist with ⟨hlower, hupper⟩
  apply convex_quadratic_on_interval P G A (s0 - r) (s0 + r) s hP
  · linarith
  · linarith
  · linarith
  · exact hleft
  · exact hright

/-- If the certified rounding radius lies strictly inside the positive nominal
shift, every realized shift remains positive, hence `lambda = 1+s > 1`. -/
theorem rounding_preserves_lambda_gt_one
    (s0 r s : ℝ)
    (hrlt : r < s0)
    (hdist : |s - s0| ≤ r) :
    1 < 1 + s := by
  rcases abs_le.mp hdist with ⟨hlower, _⟩
  linarith

/-- One-sided coefficient envelopes dominate the true quadratic on `s ≥ 0`.
The true leading coefficient need not itself be nonnegative. -/
theorem source_envelope_quadratic_le
    (P G A Pup Glow Aup s : ℝ)
    (hs : 0 ≤ s)
    (hP : P ≤ Pup) (hG : Glow ≤ G) (hA : A ≤ Aup) :
    quadratic P G A s ≤ quadratic Pup Glow Aup s := by
  have hp : 0 ≤ (Pup - P) * s^2 :=
    mul_nonneg (sub_nonneg.mpr hP) (sq_nonneg s)
  have hg : 0 ≤ (G - Glow) * s :=
    mul_nonneg (sub_nonneg.mpr hG) hs
  unfold quadratic
  nlinarith

/-- A convex upper-envelope interval certifies every allowed row realization.
This is the source-widening consumer from T-P4-040. -/
theorem source_envelope_common_lambda_interval
    {ι : Type*}
    (P G A Pup Glow Aup : ι → ℝ) (a b s : ℝ)
    (ha0 : 0 ≤ a) (hab : a ≤ b) (has : a ≤ s) (hsb : s ≤ b)
    (hPup : ∀ i, 0 ≤ Pup i)
    (hP : ∀ i, P i ≤ Pup i)
    (hG : ∀ i, Glow i ≤ G i)
    (hA : ∀ i, A i ≤ Aup i)
    (hleft : ∀ i, quadratic (Pup i) (Glow i) (Aup i) a ≤ 0)
    (hright : ∀ i, quadratic (Pup i) (Glow i) (Aup i) b ≤ 0) :
    ∀ i, quadratic (P i) (G i) (A i) s ≤ 0 := by
  intro i
  have hs0 : 0 ≤ s := le_trans ha0 has
  have hup : quadratic (Pup i) (Glow i) (Aup i) s ≤ 0 :=
    convex_quadratic_on_interval
      (Pup i) (Glow i) (Aup i) a b s (hPup i) hab has hsb
      (hleft i) (hright i)
  have hdom :
      quadratic (P i) (G i) (A i) s ≤
        quadratic (Pup i) (Glow i) (Aup i) s :=
    source_envelope_quadratic_le
      (P i) (G i) (A i) (Pup i) (Glow i) (Aup i) s
      hs0 (hP i) (hG i) (hA i)
  exact le_trans hdom hup

/-- Convexity cannot be dropped from endpoint-only certification. -/
theorem concave_endpoint_failure :
    quadratic (-1) (-4) (-3) 1 = 0 ∧
    quadratic (-1) (-4) (-3) 3 = 0 ∧
    0 < quadratic (-1) (-4) (-3) 2 := by
  norm_num [quadratic]

/-- A good nominal midpoint alone does not certify an arbitrary rounding
radius. -/
theorem midpoint_margin_not_global :
    quadratic 1 4 3 2 = -1 ∧
    0 < quadratic 1 4 3 (1 / 2) ∧
    0 < quadratic 1 4 3 (7 / 2) := by
  norm_num [quadratic]

/-- The sign restriction `s ≥ 0` is essential for the `Glow ≤ G` envelope
direction. -/
theorem negative_shift_envelope_failure :
    ¬ quadratic 0 2 0 (-1) ≤ quadratic 0 1 0 (-1) := by
  norm_num [quadratic]

#print axioms quadratic_chord_identity
#print axioms convex_quadratic_endpoint_interval
#print axioms convex_quadratic_on_interval
#print axioms common_lambda_interval
#print axioms common_fixed_lambda_interval
#print axioms quadratic_center_plus_identity
#print axioms quadratic_center_minus_identity
#print axioms symmetric_rounding_guard
#print axioms rounding_preserves_lambda_gt_one
#print axioms source_envelope_quadratic_le
#print axioms source_envelope_common_lambda_interval
#print axioms concave_endpoint_failure
#print axioms midpoint_margin_not_global
#print axioms negative_shift_envelope_failure

#print axioms young_completed_square_identity
#print axioms young_feasible_of_rational_radius
#print axioms young_inner_interval_feasible
#print axioms young_common_parameter_of_inner_bounds

end

end RouteBP4RationalLambdaGuard
