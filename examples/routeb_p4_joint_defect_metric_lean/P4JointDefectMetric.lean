import Mathlib.Data.Real.Basic
import Mathlib.Analysis.Normed.Group.Basic
import Mathlib.Tactic

/-!
# Route-B P4 joint defect metric bridge

Source-independent Lean decomposition of
`agent_review_inbox/review-T-P4-033-joint-defect-metric-liuguanyi-20260907T1422.md`.

The sidecar formalizes the exact weighted scalar pushforward used after a typed
source adapter has produced a transfer image `u = T d`, plus the force/O1 sign
flip and the singular-metric kernel obstruction.  It deliberately stops before
concrete matrix/source/interval/coverage/provenance/admission claims.
-/

set_option autoImplicit false

namespace RouteBP4JointDefectMetric

noncomputable section

/-- The exact square identity behind the optimal two-block scalar metric
pushforward.  It is purely algebraic and requires no positivity hypotheses. -/
theorem weighted_square_identity (alpha beta tau x y : ℝ) :
    (beta * tau^2 + alpha) * (alpha * x^2 + beta * y^2) -
        alpha * beta * (tau * x + y)^2 =
      (alpha * x - beta * tau * y)^2 := by
  ring

/-- Division-free scalar weighted-square inequality. -/
theorem scalar_weighted_square_le (alpha beta tau x y : ℝ) :
    alpha * beta * (tau * x + y)^2 ≤
      (beta * tau^2 + alpha) * (alpha * x^2 + beta * y^2) := by
  nlinarith [sq_nonneg (alpha * x - beta * tau * y)]

/-- Abstract normed-space pushforward for the `+ T d + b` convention.
The source adapter supplies `u = T d` indirectly through the norm bound `hu`.
No linear-map or matrix semantics are assumed here. -/
theorem weighted_defect_pushforward_add
    {B : Type*} [NormedAddCommGroup B]
    (alpha beta tau x E : ℝ) (u b : B)
    (hAlpha : 0 ≤ alpha) (hBeta : 0 ≤ beta)
    (hTau : 0 ≤ tau) (hX : 0 ≤ x)
    (hu : ‖u‖ ≤ tau * x)
    (hSource : alpha * x^2 + beta * ‖b‖^2 ≤ E) :
    alpha * beta * ‖u + b‖^2 ≤ (beta * tau^2 + alpha) * E := by
  have hTri : ‖u + b‖ ≤ tau * x + ‖b‖ := by
    calc
      ‖u + b‖ ≤ ‖u‖ + ‖b‖ := norm_add_le u b
      _ ≤ tau * x + ‖b‖ := add_le_add hu (le_refl ‖b‖)
  have hSum : 0 ≤ tau * x + ‖b‖ :=
    add_nonneg (mul_nonneg hTau hX) (norm_nonneg b)
  have hSq : ‖u + b‖^2 ≤ (tau * x + ‖b‖)^2 := by
    nlinarith [norm_nonneg (u + b)]
  have hScaled :
      alpha * beta * ‖u + b‖^2 ≤
        alpha * beta * (tau * x + ‖b‖)^2 :=
    mul_le_mul_of_nonneg_left hSq (mul_nonneg hAlpha hBeta)
  have hScalar := scalar_weighted_square_le alpha beta tau x ‖b‖
  have hCoef : 0 ≤ beta * tau^2 + alpha :=
    add_nonneg (mul_nonneg hBeta (sq_nonneg tau)) hAlpha
  have hBudget :
      (beta * tau^2 + alpha) * (alpha * x^2 + beta * ‖b‖^2) ≤
        (beta * tau^2 + alpha) * E :=
    mul_le_mul_of_nonneg_left hSource hCoef
  exact hScaled.trans (hScalar.trans hBudget)

/-- The force-side `- T d + b` convention has the same block-diagonal scalar
metric bound. -/
theorem weighted_defect_pushforward_sub
    {B : Type*} [NormedAddCommGroup B]
    (alpha beta tau x E : ℝ) (u b : B)
    (hAlpha : 0 ≤ alpha) (hBeta : 0 ≤ beta)
    (hTau : 0 ≤ tau) (hX : 0 ≤ x)
    (hu : ‖u‖ ≤ tau * x)
    (hSource : alpha * x^2 + beta * ‖b‖^2 ≤ E) :
    alpha * beta * ‖-u + b‖^2 ≤ (beta * tau^2 + alpha) * E := by
  have huNeg : ‖-u‖ ≤ tau * x := by simpa using hu
  exact weighted_defect_pushforward_add
    alpha beta tau x E (-u) b hAlpha hBeta hTau hX huNeg hSource

/-- Relative-plus-additive source budgets preserve the same split after the
joint weighted pushforward. -/
theorem weighted_defect_relative_additive
    {B : Type*} [NormedAddCommGroup B]
    (alpha beta tau x kappa A B0 : ℝ) (u b : B)
    (hAlpha : 0 ≤ alpha) (hBeta : 0 ≤ beta)
    (hTau : 0 ≤ tau) (hX : 0 ≤ x)
    (hu : ‖u‖ ≤ tau * x)
    (hSource : alpha * x^2 + beta * ‖b‖^2 ≤ kappa * A + B0) :
    alpha * beta * ‖u + b‖^2 ≤
      (beta * tau^2 + alpha) * (kappa * A + B0) := by
  exact weighted_defect_pushforward_add
    alpha beta tau x (kappa * A + B0) u b
      hAlpha hBeta hTau hX hu hSource

/-- Universal quadratic domination is preserved by coordinate pullback.  This
is the function-level core of the congruence rule; a concrete matrix adapter
may instantiate `q` and `c` by quadratic forms and `P` by its coordinate map. -/
theorem quadratic_domination_pullback
    {Z Z' : Type*} (q c : Z → ℝ) (P : Z' → Z) (mu : ℝ)
    (hDom : ∀ z, c z ≤ mu * q z) :
    ∀ z', c (P z') ≤ mu * q (P z') := by
  intro z'
  exact hDom (P z')

/-- If a source metric vanishes on a direction that carries strictly positive
physical correction energy, no finite universal multiplicative coefficient can
exist. -/
theorem singular_metric_kernel_obstruction
    {Z : Type*} (q c : Z → ℝ) (z : Z)
    (hMetricZero : q z = 0) (hCorrectionPositive : 0 < c z) :
    ¬ ∃ mu : ℝ, ∀ x, c x ≤ mu * q x := by
  rintro ⟨mu, hDom⟩
  have hz := hDom z
  rw [hMetricZero, mul_zero] at hz
  linarith

/-- Scalar two-block model of a correlated joint metric. -/
def jointMetric (a cross c d b : ℝ) : ℝ :=
  a * d^2 + 2 * cross * d * b + c * b^2

/-- Under the force/O1 coordinate flip `d_O = -d_F`, the cross coefficient
must flip sign in order to represent the same quadratic source assumption. -/
theorem joint_metric_sign_flip (a cross c d b : ℝ) :
    jointMetric a (-cross) c (-d) b = jointMetric a cross c d b := by
  simp [jointMetric]

/-- The same coordinate flip converts `+ tau*d + b` into `- tau*d + b`. -/
theorem correction_sign_flip (tau d b : ℝ) :
    tau * (-d) + b = -tau * d + b := by
  ring

/-- If the joint metric has no distal/port cross term, the metric itself is
sign-convention invariant. -/
theorem block_diagonal_metric_sign_invariant (a c d b : ℝ) :
    jointMetric a 0 c (-d) b = jointMetric a 0 c d b := by
  simp [jointMetric]

#print axioms weighted_square_identity
#print axioms scalar_weighted_square_le
#print axioms weighted_defect_pushforward_add
#print axioms weighted_defect_pushforward_sub
#print axioms weighted_defect_relative_additive
#print axioms quadratic_domination_pullback
#print axioms singular_metric_kernel_obstruction
#print axioms joint_metric_sign_flip
#print axioms correction_sign_flip
#print axioms block_diagonal_metric_sign_invariant

end

end RouteBP4JointDefectMetric
