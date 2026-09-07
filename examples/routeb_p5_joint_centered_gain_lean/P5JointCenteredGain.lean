import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# Route-B P5 joint centered-gain sidecar

Source-independent Lean decomposition of
`review-T-P5-024-kuangmanmozun-20260907T0945.md`.

The file proves the exact rational joint block-(4,5) inequality
`25 U N <= 144 Q^2`, its centered small-gain consumer, exact checker-constant
improvement arithmetic, and the rational regression witness ruling out the
constant `23/4`.  It does not bind Julia/DH/Float64 semantics, prove the
T-P5-023 cell/path premise, prove P8 coverage or ODE continuation, or close
P5/P8/M4.
-/

set_option autoImplicit false

namespace RouteBP5JointCenteredGain

noncomputable section

/-- Exact block-(4,5) dissipation quadratic used by T-P5-019/T-P5-024. -/
def qDissipation (x4 x5 y4 y5 : ℝ) : ℝ :=
  (3/4 : ℝ)*x4^2 + (29/50 : ℝ)*x5^2 - (3/200 : ℝ)*x4*x5 +
  (2049997/3000000 : ℝ)*y4^2 + (2399261/4000000 : ℝ)*y5^2 +
  (1/400 : ℝ)*x4*y5 - (1/400 : ℝ)*x5*y4

/-- `N = ||(x4,x5,y4,y5)||^2`. -/
def stateSq (x4 x5 y4 y5 : ℝ) : ℝ :=
  x4^2 + x5^2 + y4^2 + y5^2

/-- `U = ||(x4+y4,x5+y5)||^2`. -/
def sumSq (x4 x5 y4 y5 : ℝ) : ℝ :=
  (x4+y4)^2 + (x5+y5)^2

/-- Exact rational LDL/SOS certificate for
`(7/10)U + (10/7)N <= (24/5)Q`.

The coefficients are the exact LDL decomposition of the 4x4 rational form
recorded in T-P5-024. -/
theorem joint_quadratic_comparison (x4 x5 y4 y5 : ℝ) :
    (7/10 : ℝ) * sumSq x4 x5 y4 y5 +
        (10/7 : ℝ) * stateSq x4 x5 y4 y5
      ≤ (24/5 : ℝ) * qDissipation x4 x5 y4 y5 := by
  let w1 : ℝ := x4 - (63/2575 : ℝ)*x5 - (49/103 : ℝ)*y4 + (21/5150 : ℝ)*y5
  let w2 : ℝ := x5 - (208425/5899112 : ℝ)*y4 - (6307427/5899112 : ℝ)*y5
  let w3 : ℝ := y4 - (282250198125/10550522799949 : ℝ)*y5
  let w4 : ℝ := y5
  have hdecomp :
      (24/5 : ℝ) * qDissipation x4 x5 y4 y5 -
          (7/10 : ℝ) * sumSq x4 x5 y4 y5 -
          (10/7 : ℝ) * stateSq x4 x5 y4 y5 =
        (103/70 : ℝ) * w1^2 +
        (1474778/2253125 : ℝ) * w2^2 +
        (10550522799949/12904307500000 : ℝ) * w3^2 +
        (302371148712671469/184634148999107500000 : ℝ) * w4^2 := by
    dsimp [w1, w2, w3, w4, qDissipation, sumSq, stateSq]
    ring
  have hnonneg :
      0 ≤ (24/5 : ℝ) * qDissipation x4 x5 y4 y5 -
          (7/10 : ℝ) * sumSq x4 x5 y4 y5 -
          (10/7 : ℝ) * stateSq x4 x5 y4 y5 := by
    rw [hdecomp]
    positivity
  linarith

/-- Weighted AM-GM identity with the exact T-P5-024 weight `alpha=7/10`. -/
theorem weighted_amgm_7_10 (U N : ℝ) :
    4*U*N ≤ ((7/10 : ℝ)*U + (10/7 : ℝ)*N)^2 := by
  nlinarith [sq_nonneg ((7/10 : ℝ)*U - (10/7 : ℝ)*N)]

/-- Positivity of the exact block dissipation follows from the joint quadratic
comparison because the weighted `U,N` combination is nonnegative. -/
theorem qDissipation_nonneg (x4 x5 y4 y5 : ℝ) :
    0 ≤ qDissipation x4 x5 y4 y5 := by
  have hcomp := joint_quadratic_comparison x4 x5 y4 y5
  have hU : 0 ≤ sumSq x4 x5 y4 y5 := by
    simp [sumSq]
    positivity
  have hN : 0 ≤ stateSq x4 x5 y4 y5 := by
    simp [stateSq]
    positivity
  have hS :
      0 ≤ (7/10 : ℝ) * sumSq x4 x5 y4 y5 +
          (10/7 : ℝ) * stateSq x4 x5 y4 y5 := by
    positivity
  nlinarith

/-- Main T-P5-024 joint residual metric:
`25 * ||x+y||^2 * ||(x,y)||^2 <= 144 * Q^2`. -/
theorem block45_joint_residual_metric (x4 x5 y4 y5 : ℝ) :
    25 * sumSq x4 x5 y4 y5 * stateSq x4 x5 y4 y5
      ≤ 144 * (qDissipation x4 x5 y4 y5)^2 := by
  let U : ℝ := sumSq x4 x5 y4 y5
  let N : ℝ := stateSq x4 x5 y4 y5
  let Q : ℝ := qDissipation x4 x5 y4 y5
  let S : ℝ := (7/10 : ℝ)*U + (10/7 : ℝ)*N
  let T : ℝ := (24/5 : ℝ)*Q
  have hU : 0 ≤ U := by
    dsimp [U, sumSq]
    positivity
  have hN : 0 ≤ N := by
    dsimp [N, stateSq]
    positivity
  have hS : 0 ≤ S := by
    dsimp [S]
    positivity
  have hcomp : S ≤ T := by
    dsimp [S, T, U, N, Q]
    exact joint_quadratic_comparison x4 x5 y4 y5
  have hT : 0 ≤ T := le_trans hS hcomp
  have hsq : S^2 ≤ T^2 := by
    have hminus : 0 ≤ T-S := sub_nonneg.mpr hcomp
    have hplus : 0 ≤ T+S := add_nonneg hT hS
    have hprod : 0 ≤ (T-S)*(T+S) := mul_nonneg hminus hplus
    nlinarith
  have hamgm : 4*U*N ≤ S^2 := by
    dsimp [S]
    exact weighted_amgm_7_10 U N
  have hchain : 4*U*N ≤ T^2 := le_trans hamgm hsq
  have hfinal : 25*U*N ≤ 144*Q^2 := by
    dsimp [T] at hchain
    nlinarith
  simpa [U, N, Q] using hfinal

/-- Reusable square-to-absolute-value bridge. -/
theorem abs_le_of_sq_le_sq_nonneg
    (z r : ℝ) (hr : 0 ≤ r) (hsq : z^2 ≤ r^2) : |z| ≤ r := by
  apply (abs_le).2
  constructor
  · by_contra h
    have hz1 : z-r < 0 := by linarith
    have hz2 : z+r < 0 := by linarith
    have hp : 0 < (z-r)*(z+r) := mul_pos_of_neg_of_neg hz1 hz2
    nlinarith
  · by_contra h
    have hz1 : 0 < z-r := by linarith
    have hz2 : 0 < z+r := by linarith
    have hp : 0 < (z-r)*(z+r) := mul_pos hz1 hz2
    nlinarith

/-- Generic centered-small-gain consumer.  It deliberately accepts the joint
metric as a premise so source/path geometry remains separate from this algebra. -/
theorem centered_small_gain_joint
    (U N Q rcSq coupling ell2 mu : ℝ)
    (hU : 0 ≤ U) (hQ : 0 ≤ Q)
    (hell2 : 0 ≤ ell2) (hmu : 0 ≤ mu)
    (hrc : rcSq ≤ ell2*N)
    (hcoupling : coupling^2 ≤ U*rcSq)
    (hjoint : 25*U*N ≤ 144*Q^2)
    (hgain : 144*ell2 ≤ 25*mu^2) :
    |coupling| ≤ mu*Q := by
  have hrcU : U*rcSq ≤ U*(ell2*N) :=
    mul_le_mul_of_nonneg_left hrc hU
  have hc1 : coupling^2 ≤ ell2*U*N := by
    nlinarith
  have hjmul : ell2*(25*U*N) ≤ ell2*(144*Q^2) :=
    mul_le_mul_of_nonneg_left hjoint hell2
  have hc2 : 25*coupling^2 ≤ 144*ell2*Q^2 := by
    nlinarith
  have hgmul : (144*ell2)*(Q^2) ≤ (25*mu^2)*(Q^2) :=
    mul_le_mul_of_nonneg_right hgain (sq_nonneg Q)
  have hsquare : coupling^2 ≤ (mu*Q)^2 := by
    nlinarith
  have hrhs : 0 ≤ mu*Q := mul_nonneg hmu hQ
  exact abs_le_of_sq_le_sq_nonneg coupling (mu*Q) hrhs hsquare

/-- Checker-facing specialization using the exact block-(4,5) `Q,U,N`. -/
theorem block45_centered_small_gain
    (x4 x5 y4 y5 rcSq coupling ell2 mu : ℝ)
    (hell2 : 0 ≤ ell2) (hmu : 0 ≤ mu)
    (hrc : rcSq ≤ ell2 * stateSq x4 x5 y4 y5)
    (hcoupling : coupling^2 ≤ sumSq x4 x5 y4 y5 * rcSq)
    (hgain : 144*ell2 ≤ 25*mu^2) :
    |coupling| ≤ mu * qDissipation x4 x5 y4 y5 := by
  apply centered_small_gain_joint
      (U := sumSq x4 x5 y4 y5)
      (N := stateSq x4 x5 y4 y5)
      (Q := qDissipation x4 x5 y4 y5)
      (rcSq := rcSq) (coupling := coupling) (ell2 := ell2) (mu := mu)
  · simp [sumSq]
    positivity
  · exact qDissipation_nonneg x4 x5 y4 y5
  · exact hell2
  · exact hmu
  · exact hrc
  · exact hcoupling
  · exact block45_joint_residual_metric x4 x5 y4 y5
  · exact hgain

/-- With no anchor bias, the centered residual leaves `(1-mu)Q` of dissipation. -/
theorem centered_no_bias_decay
    (Vdot Q coupling mu : ℝ)
    (hcoupling : |coupling| ≤ mu*Q)
    (hdot : Vdot ≤ -Q + |coupling|) :
    Vdot ≤ -(1-mu)*Q := by
  linarith

/-- Strict no-bias decay when `mu<1` and the dissipation quadratic is positive. -/
theorem centered_no_bias_strict_decay
    (Vdot Q coupling mu : ℝ)
    (hmu : mu < 1) (hQ : 0 < Q)
    (hcoupling : |coupling| ≤ mu*Q)
    (hdot : Vdot ≤ -Q + |coupling|) :
    Vdot < 0 := by
  have hle := centered_no_bias_decay Vdot Q coupling mu hcoupling hdot
  have hneg : -(1-mu)*Q < 0 := by
    nlinarith
  linarith

/-- Exact 3.33% checker-constant improvement over the product-of-bounds route. -/
theorem gain_improvement_exact :
    ((25/144 : ℝ) / (457/2720 : ℝ) = 4250/4113) ∧
    ((1 : ℝ) < 4250/4113) ∧
    ((25/144 : ℝ) - 457/2720 = 137/24480) := by
  norm_num

/-- `mu=1/2` checker specializations: old `10880 ell2 <= 457`, new
`576 ell2 <= 25`. -/
theorem half_gain_checker_constants (ell2 : ℝ) :
    (2720*ell2 ≤ 457*(1/2 : ℝ)^2 ↔ 10880*ell2 ≤ 457) ∧
    (144*ell2 ≤ 25*(1/2 : ℝ)^2 ↔ 576*ell2 ≤ 25) := by
  constructor
  · constructor
    · intro h
      nlinarith
    · intro h
      nlinarith
  · constructor
    · intro h
      nlinarith
    · intro h
      nlinarith

/-- Exact rational state `(x4,x5,y4,y5)=(0,15,0,14)` disproves the stronger
universal constant `23/4`. -/
theorem counterexample_23_quarter :
    stateSq 0 15 0 14 = 421 ∧
    sumSq 0 15 0 14 = 841 ∧
    qDissipation 0 15 0 14 = 248063789/1000000 ∧
    4 * sumSq 0 15 0 14 * stateSq 0 15 0 14 -
        23 * (qDissipation 0 15 0 14)^2 =
      924201500160017/1000000000000 ∧
    (0 : ℝ) < 924201500160017/1000000000000 := by
  norm_num [stateSq, sumSq, qDissipation]

#print axioms joint_quadratic_comparison
#print axioms weighted_amgm_7_10
#print axioms qDissipation_nonneg
#print axioms block45_joint_residual_metric
#print axioms abs_le_of_sq_le_sq_nonneg
#print axioms centered_small_gain_joint
#print axioms block45_centered_small_gain
#print axioms centered_no_bias_decay
#print axioms centered_no_bias_strict_decay
#print axioms gain_improvement_exact
#print axioms half_gain_checker_constants
#print axioms counterexample_23_quarter

end

end RouteBP5JointCenteredGain
