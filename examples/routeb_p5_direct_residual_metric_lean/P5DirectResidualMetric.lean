import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# Route-B P5 direct residual metric sidecar

Source-independent Lean decomposition of the algebraic core of
`review-T-P5-019-honglianmozun-20260907T0702.md`.

The file proves the exact block-(4,5) dissipation lower bound, the direct
`5 ||x+y||^2 <= 17 Q` residual metric, a square-only Young consumer, and the
improved ISS/barrier constants.  It does not bind Julia/DH/Float64 semantics,
prove a source residual enclosure, prove ODE/flowpipe coverage, or close P5/P8/M4.
-/

set_option autoImplicit false

namespace RouteBP5DirectResidualMetric

noncomputable section

/-- Exact rational block constants inherited from the T-P5-016/018 algebra. -/
def m4 : ℝ := 350003 / 3000000
def m5 : ℝ := 200739 / 4000000
def d4 : ℝ := 4 / 5
def d5 : ℝ := 13 / 20
def k44 : ℝ := 3 / 4
def k55 : ℝ := 29 / 50
def k45 : ℝ := -3 / 400

/-- Full positive dissipation quadratic
`yᵀ(D-M)y + xᵀKx - yᵀAx` for the exactized block-(4,5) model. -/
def qDissipation (x4 x5 y4 y5 : ℝ) : ℝ :=
  (d4-m4)*y4^2 + (d5-m5)*y5^2 +
  k44*x4^2 + 2*k45*x4*x5 + k55*x5^2 +
  (1/400 : ℝ)*x4*y5 - (1/400 : ℝ)*x5*y4

/-- The elementary weighted-Young lower bound used by T-P5-019. -/
theorem q_lower_diagonal (x4 x5 y4 y5 : ℝ) :
    (143/200 : ℝ)*x4^2 + (1849/3200 : ℝ)*x5^2 +
      (2034997/3000000 : ℝ)*y4^2 + (2398011/4000000 : ℝ)*y5^2
      ≤ qDissipation x4 x5 y4 y5 := by
  simp [qDissipation, d4, d5, m4, m5, k44, k55, k45]
  nlinarith [sq_nonneg (2*x4 - x5/2),
    sq_nonneg (2*x4 + y5/2),
    sq_nonneg (x5/2 - 2*y4)]

/-- Exact positive scalar gap for coordinate 4. -/
theorem axis4_metric_gap :
    0 < (17 : ℝ)*(143/200)*(2034997/3000000) -
      5*((143/200 : ℝ) + 2034997/3000000) := by
  norm_num

/-- Exact positive scalar gap for coordinate 5. -/
theorem axis5_metric_gap :
    0 < (17 : ℝ)*(1849/3200)*(2398011/4000000) -
      5*((1849/3200 : ℝ) + 2398011/4000000) := by
  norm_num

/-- Coordinate-4 direct metric inequality. -/
theorem axis4_direct_metric (x y : ℝ) :
    5*(x+y)^2 ≤ 17*((143/200 : ℝ)*x^2 + (2034997/3000000 : ℝ)*y^2) := by
  nlinarith [sq_nonneg ((143/200 : ℝ)*x - (2034997/3000000 : ℝ)*y),
    sq_nonneg x, sq_nonneg y, axis4_metric_gap]

/-- Coordinate-5 direct metric inequality. -/
theorem axis5_direct_metric (x y : ℝ) :
    5*(x+y)^2 ≤ 17*((1849/3200 : ℝ)*x^2 + (2398011/4000000 : ℝ)*y^2) := by
  nlinarith [sq_nonneg ((1849/3200 : ℝ)*x - (2398011/4000000 : ℝ)*y),
    sq_nonneg x, sq_nonneg y, axis5_metric_gap]

/-- Main T-P5-019 metric:
`5 ||x+y||² <= 17 Q(x,y)`. -/
theorem block45_direct_metric (x4 x5 y4 y5 : ℝ) :
    5*((x4+y4)^2 + (x5+y5)^2) ≤ 17*qDissipation x4 x5 y4 y5 := by
  have hq := q_lower_diagonal x4 x5 y4 y5
  have h4 := axis4_direct_metric x4 y4
  have h5 := axis5_direct_metric x5 y5
  nlinarith

/-- A reusable ordered-ring bridge: a square comparison against a nonnegative
right-hand side implies the corresponding absolute-value comparison. -/
theorem abs_le_of_sq_le_sq_nonneg
    (z r : ℝ) (hr : 0 ≤ r) (hsq : z^2 ≤ r^2) : |z| ≤ r := by
  apply (abs_le).2
  constructor
  · by_contra h
    have hz1 : z - r < 0 := by linarith
    have hz2 : z + r < 0 := by linarith
    have hp : 0 < (z-r)*(z+r) := mul_pos_of_neg_of_neg hz1 hz2
    nlinarith
  · by_contra h
    have hz1 : 0 < z - r := by linarith
    have hz2 : 0 < z + r := by linarith
    have hp : 0 < (z-r)*(z+r) := mul_pos hz1 hz2
    nlinarith

/-- Square-only Young consumer recommended by T-P5-019. -/
theorem residual_square_absorption
    (z Q R2 : ℝ)
    (hQ : 0 ≤ Q) (hR : 0 ≤ R2)
    (hz : z^2 ≤ (17/5 : ℝ)*Q*R2) :
    |z| ≤ (1/2 : ℝ)*Q + (17/10 : ℝ)*R2 := by
  let rhs : ℝ := (1/2 : ℝ)*Q + (17/10 : ℝ)*R2
  have hrhs : 0 ≤ rhs := by
    dsimp [rhs]
    positivity
  have hsquare : z^2 ≤ rhs^2 := by
    have hcomp := sq_nonneg ((1/2 : ℝ)*Q - (17/10 : ℝ)*R2)
    dsimp [rhs]
    nlinarith
  exact abs_le_of_sq_le_sq_nonneg z rhs hrhs hsquare

/-- Absorb the residual power into half of the dissipation quadratic. -/
theorem derivative_after_residual_absorption
    (Vdot Q R2 z : ℝ)
    (hQ : 0 ≤ Q) (hR : 0 ≤ R2)
    (hz : z^2 ≤ (17/5 : ℝ)*Q*R2)
    (hdot : Vdot ≤ -Q + |z|) :
    Vdot ≤ -(1/2 : ℝ)*Q + (17/10 : ℝ)*R2 := by
  have hab := residual_square_absorption z Q R2 hQ hR hz
  linarith

/-- Convert `Q >= (457/672)V` to the improved T-P5-019 ISS inequality. -/
theorem iss_direct_metric_refinement
    (V Vdot Q R2 : ℝ)
    (hQV : (457/672 : ℝ)*V ≤ Q)
    (hdot : Vdot ≤ -(1/2 : ℝ)*Q + (17/10 : ℝ)*R2) :
    Vdot ≤ -(457/1344 : ℝ)*V + (17/10 : ℝ)*R2 := by
  nlinarith

/-- Exact ultimate-gain arithmetic `(17/10)/(457/1344)=11424/2285 < 5`. -/
theorem ultimate_gain_constants :
    (17/10 : ℝ) / (457/1344 : ℝ) = 11424/2285 ∧
      (11424/2285 : ℝ) < 5 := by
  constructor <;> norm_num

/-- Division-free inward-pointing barrier for the improved residual consumer. -/
theorem direct_metric_barrier_inward
    (Vstar L2 Vdot : ℝ)
    (hbar : 2285*Vstar > 11424*L2)
    (hdot : Vdot ≤ -(457/1344 : ℝ)*Vstar + (17/10 : ℝ)*L2) :
    Vdot < 0 := by
  nlinarith

/-- Quarter-barrier specialization: `45696 L2 < 2285`. -/
theorem quarter_barrier_inward
    (L2 Vdot : ℝ)
    (hbar : 45696*L2 < 2285)
    (hdot : Vdot ≤ -(457/1344 : ℝ)*(1/4 : ℝ) + (17/10 : ℝ)*L2) :
    Vdot < 0 := by
  nlinarith

/-- Common physical-margin specialization from `Vstar=(117/4880)s²`. -/
theorem common_margin_barrier_inward
    (s L2 Vdot : ℝ)
    (hbar : 17823*s^2 > 3716608*L2)
    (hdot : Vdot ≤ -(457/1344 : ℝ)*((117/4880 : ℝ)*s^2) +
      (17/10 : ℝ)*L2) :
    Vdot < 0 := by
  nlinarith

/-- Integer/rational identities behind the two barrier specializations. -/
theorem barrier_constant_checks :
    (11424 : ℤ)*4 = 45696 ∧
    (2285 : ℤ)*117 = 267345 ∧
    (11424 : ℤ)*4880 = 55749120 ∧
    (267345 : ℤ) = 15*17823 ∧
    (55749120 : ℤ) = 15*3716608 := by
  norm_num

#print axioms q_lower_diagonal
#print axioms axis4_metric_gap
#print axioms axis5_metric_gap
#print axioms axis4_direct_metric
#print axioms axis5_direct_metric
#print axioms block45_direct_metric
#print axioms abs_le_of_sq_le_sq_nonneg
#print axioms residual_square_absorption
#print axioms derivative_after_residual_absorption
#print axioms iss_direct_metric_refinement
#print axioms ultimate_gain_constants
#print axioms direct_metric_barrier_inward
#print axioms quarter_barrier_inward
#print axioms common_margin_barrier_inward
#print axioms barrier_constant_checks

end

end RouteBP5DirectResidualMetric
