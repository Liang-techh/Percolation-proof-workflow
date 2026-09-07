import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# Route-B P5 near-sharp scalar centered-gain sidecar

Source-independent Lean decomposition of
`review-T-P5-027-kuangmanmozun-20260907T1044.md`, with the arithmetic correction
from `companion-T-P5-027-kuangmanmozun-20260907T1048.md`.

The file proves the exact rational weighted block-(4,5) comparison, the
near-sharp scalar `U*N/Q^2` bound, a square-only centered residual consumer,
and an exact rational lower witness.  It does not bind Julia/DH/Float64 source
semantics, a concrete P8 path/cell chain, ODE coverage, provenance/admission,
or final P5/P8/M4 integration.
-/

set_option autoImplicit false

namespace RouteBP5NearSharpCenteredGain

noncomputable section

/-- Exact block-(4,5) dissipation quadratic used by T-P5-019/T-P5-024/T-P5-027. -/
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
`(75/106) U + (106/75) N <= (47984317/10000000) Q`.

The coefficients below are an exact LDL decomposition of the rational matrix
`c*P - alpha*L^T*L - alpha^{-1} I` from T-P5-027. -/
theorem weighted_joint_quadratic_bound_block45 (x4 x5 y4 y5 : ℝ) :
    (75/106 : ℝ) * sumSq x4 x5 y4 y5 +
        (106/75 : ℝ) * stateSq x4 x5 y4 y5
      ≤ (47984317/10000000 : ℝ) * qDissipation x4 x5 y4 y5 := by
  let w1 : ℝ :=
    x4 - (22888519209/939971920900 : ℝ)*x5
       - (4500000000/9399719209 : ℝ)*y4
       + (7629506403/1879943841800 : ℝ)*y5
  let w2 : ℝ :=
    x5 - (13885594538623379761350/395359846106875447280719 : ℝ)*y4
       - (845800100706139746004773/790719692213750894561438 : ℝ)*y5
  let w3 : ℝ :=
    y4 - (3217560789628848699300752572801875/
      119852276447772128316743626880393651 : ℝ)*y5
  let w4 : ℝ := y5
  have hdecomp :
      (47984317/10000000 : ℝ) * qDissipation x4 x5 y4 y5 -
          (75/106 : ℝ) * sumSq x4 x5 y4 y5 -
          (106/75 : ℝ) * stateSq x4 x5 y4 y5 =
        (9399719209/6360000000 : ℝ) * w1^2 +
        (395359846106875447280719/597822141692400000000000 : ℝ) * w2^2 +
        (3236011464089847464552077925770628577/
          3953598461068754472807190000000000000 : ℝ) * w3^2 +
        (1337085894390964667090754208081695830761861/
          14382273173732655398009235225647238120000000000000 : ℝ) * w4^2 := by
    dsimp [w1, w2, w3, w4, qDissipation, sumSq, stateSq]
    ring
  have hnonneg :
      0 ≤ (47984317/10000000 : ℝ) * qDissipation x4 x5 y4 y5 -
          (75/106 : ℝ) * sumSq x4 x5 y4 y5 -
          (106/75 : ℝ) * stateSq x4 x5 y4 y5 := by
    rw [hdecomp]
    positivity
  linarith

/-- Weighted AM-GM identity at the near-optimal rational weight `75/106`. -/
theorem weighted_amgm_75_106 (U N : ℝ) :
    4*U*N ≤ ((75/106 : ℝ)*U + (106/75 : ℝ)*N)^2 := by
  nlinarith [sq_nonneg ((75/106 : ℝ)*U - (106/75 : ℝ)*N)]

/-- Nonnegativity of the exact dissipation follows from the weighted comparison. -/
theorem qDissipation_nonneg (x4 x5 y4 y5 : ℝ) :
    0 ≤ qDissipation x4 x5 y4 y5 := by
  have hcomp := weighted_joint_quadratic_bound_block45 x4 x5 y4 y5
  have hU : 0 ≤ sumSq x4 x5 y4 y5 := by
    simp [sumSq]
    positivity
  have hN : 0 ≤ stateSq x4 x5 y4 y5 := by
    simp [stateSq]
    positivity
  have hS :
      0 ≤ (75/106 : ℝ) * sumSq x4 x5 y4 y5 +
          (106/75 : ℝ) * stateSq x4 x5 y4 y5 := by
    positivity
  nlinarith

/-- Near-sharp scalar block-(4,5) metric from T-P5-027. -/
theorem near_sharp_joint_centered_gain (x4 x5 y4 y5 : ℝ) :
    400000000000000 * sumSq x4 x5 y4 y5 * stateSq x4 x5 y4 y5
      ≤ 2302494677956489 * (qDissipation x4 x5 y4 y5)^2 := by
  let U : ℝ := sumSq x4 x5 y4 y5
  let N : ℝ := stateSq x4 x5 y4 y5
  let Q : ℝ := qDissipation x4 x5 y4 y5
  let S : ℝ := (75/106 : ℝ)*U + (106/75 : ℝ)*N
  let T : ℝ := (47984317/10000000 : ℝ)*Q
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
    exact weighted_joint_quadratic_bound_block45 x4 x5 y4 y5
  have hT : 0 ≤ T := le_trans hS hcomp
  have hsq : S^2 ≤ T^2 := by
    have hminus : 0 ≤ T-S := sub_nonneg.mpr hcomp
    have hplus : 0 ≤ T+S := add_nonneg hT hS
    have hprod : 0 ≤ (T-S)*(T+S) := mul_nonneg hminus hplus
    nlinarith
  have hamgm : 4*U*N ≤ S^2 := by
    dsimp [S]
    exact weighted_amgm_75_106 U N
  have hchain : 4*U*N ≤ T^2 := le_trans hamgm hsq
  have hfinal :
      400000000000000*U*N ≤ 2302494677956489*Q^2 := by
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

/-- Generic square-only centered residual consumer for the T-P5-027 constant. -/
theorem near_sharp_scalar_residual_consumer
    (U N Q rcSq coupling ell2 mu : ℝ)
    (hU : 0 ≤ U) (hQ : 0 ≤ Q)
    (hell2 : 0 ≤ ell2) (hmu : 0 ≤ mu)
    (hrc : rcSq ≤ ell2*N)
    (hcoupling : coupling^2 ≤ U*rcSq)
    (hjoint : 400000000000000*U*N ≤ 2302494677956489*Q^2)
    (hgain : 2302494677956489*ell2 ≤ 400000000000000*mu^2) :
    |coupling| ≤ mu*Q := by
  have hrcU : U*rcSq ≤ U*(ell2*N) :=
    mul_le_mul_of_nonneg_left hrc hU
  have hc1 : coupling^2 ≤ ell2*U*N := by
    nlinarith
  have hjmul :
      ell2*(400000000000000*U*N) ≤
        ell2*(2302494677956489*Q^2) :=
    mul_le_mul_of_nonneg_left hjoint hell2
  have hc2 :
      400000000000000*coupling^2 ≤
        2302494677956489*ell2*Q^2 := by
    nlinarith
  have hgmul :
      (2302494677956489*ell2)*(Q^2) ≤
        (400000000000000*mu^2)*(Q^2) :=
    mul_le_mul_of_nonneg_right hgain (sq_nonneg Q)
  have hsquare : coupling^2 ≤ (mu*Q)^2 := by
    nlinarith
  have hrhs : 0 ≤ mu*Q := mul_nonneg hmu hQ
  exact abs_le_of_sq_le_sq_nonneg coupling (mu*Q) hrhs hsquare

/-- Checker-facing block-(4,5) specialization. -/
theorem block45_near_sharp_scalar_residual_consumer
    (x4 x5 y4 y5 rcSq coupling ell2 mu : ℝ)
    (hell2 : 0 ≤ ell2) (hmu : 0 ≤ mu)
    (hrc : rcSq ≤ ell2 * stateSq x4 x5 y4 y5)
    (hcoupling : coupling^2 ≤ sumSq x4 x5 y4 y5 * rcSq)
    (hgain : 2302494677956489*ell2 ≤ 400000000000000*mu^2) :
    |coupling| ≤ mu * qDissipation x4 x5 y4 y5 := by
  apply near_sharp_scalar_residual_consumer
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
  · exact near_sharp_joint_centered_gain x4 x5 y4 y5
  · exact hgain

/-- Corrected exact improvement over the old `144/25` scalar constant. -/
theorem old_minus_new_constant_corrected :
    (144/25 : ℝ) -
        (2302494677956489/400000000000000 : ℝ) =
      1505322043511/400000000000000 ∧
    (0 : ℝ) < 1505322043511/400000000000000 := by
  norm_num

/-- Exact width of the rational sharpness bracket from T-P5-027. -/
theorem sharpness_bracket_width :
    (2302494677956489/400000000000000 : ℝ) -
        11512473/2000000 =
      77956489/400000000000000 ∧
    (0 : ℝ) < 77956489/400000000000000 := by
  norm_num

/-- Exact rational lower witness.  This rejects every claimed universal scalar
constant at or below `11512473/2000000`. -/
theorem lower_witness_rejects_57562365_over_1e7 :
    stateSq 2379 73046 1832 68229 = 9999930422 ∧
    sumSq 2379 73046 1832 68229 = 19976358146 ∧
    qDissipation 2379 73046 1832 68229 =
      14138344959005123/2400000 ∧
    10000000 * sumSq 2379 73046 1832 68229 *
        stateSq 2379 73046 1832 68229 * 2400000^2 -
      57562365 * 14138344959005123^2 =
        23290832775682489880381695029915 ∧
    (0 : ℝ) < 23290832775682489880381695029915 := by
  norm_num [stateSq, sumSq, qDissipation]

#print axioms weighted_joint_quadratic_bound_block45
#print axioms weighted_amgm_75_106
#print axioms qDissipation_nonneg
#print axioms near_sharp_joint_centered_gain
#print axioms abs_le_of_sq_le_sq_nonneg
#print axioms near_sharp_scalar_residual_consumer
#print axioms block45_near_sharp_scalar_residual_consumer
#print axioms old_minus_new_constant_corrected
#print axioms sharpness_bracket_width
#print axioms lower_witness_rejects_57562365_over_1e7

end

end RouteBP5NearSharpCenteredGain
