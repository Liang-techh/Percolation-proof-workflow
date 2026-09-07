import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# Route-B P5-027 near-sharp exact rational scalar fallback

This is a source-independent algebraic sidecar for
`review-T-P5-027-kuangmanmozun-20260907T1044.md`.  It keeps the four
coordinates `(x4,x5,y4,y5)` and the exact block-(4,5) quadratic from P5-024,
but replaces `144/25` by

`2302494677956489 / 400000000000000`.

The principal-minor theorem is an exact Sylvester certificate for the
weighted gap.  The comparison proof below uses the equivalent exact LDL/SOS
identity, so no matrix API or numerical eigenvalue is needed.  Nothing here
binds a source Jacobian, `K_path`, `ell2_path`, a P8 cell/flowpipe, coverage,
P5/P8/M4 closure, provenance, or registry admission.
-/

set_option autoImplicit false

namespace RouteBP5ScalarFallback

noncomputable section

def qDissipation (x4 x5 y4 y5 : ℝ) : ℝ :=
  (3 / 4 : ℝ) * x4^2 + (29 / 50 : ℝ) * x5^2 - (3 / 200 : ℝ) * x4 * x5 +
  (2049997 / 3000000 : ℝ) * y4^2 + (2399261 / 4000000 : ℝ) * y5^2 +
  (1 / 400 : ℝ) * x4 * y5 - (1 / 400 : ℝ) * x5 * y4

def stateSq (x4 x5 y4 y5 : ℝ) : ℝ :=
  x4^2 + x5^2 + y4^2 + y5^2

def sumSq (x4 x5 y4 y5 : ℝ) : ℝ :=
  (x4 + y4)^2 + (x5 + y5)^2

def alpha : ℝ := 75 / 106
def alphaInv : ℝ := 106 / 75
def comparisonConstant : ℝ := 47984317 / 10000000

/- The entries of H = c P - alpha R - alpha⁻¹ I, in the P5-024 order. -/
def h11 : ℝ := 9399719209 / 6360000000
def h12 : ℝ := -143952951 / 4000000000
def h13 : ℝ := -75 / 106
def h14 : ℝ := 47984317 / 8000000000
def h22 : ℝ := 52645685687 / 79500000000
def h23 : ℝ := -47984317 / 8000000000
def h24 : ℝ := -75 / 106
def h33 : ℝ := 613762804181199 / 530000000000000
def h34 : ℝ := 0
def h44 : ℝ := 4816377161968183 / 6360000000000000

def principalMinor1 : ℝ := h11

def principalMinor2 : ℝ :=
  h11 * h22 - h12^2

def principalMinor3 : ℝ :=
  h11 * h22 * h33 - h11 * h23^2 - h12^2 * h33 +
    2 * h12 * h13 * h23 - h13^2 * h22

def principalMinor4 : ℝ :=
  h11 * h22 * h33 * h44 - h11 * h23^2 * h44 - h11 * h24^2 * h33 -
    h12^2 * h33 * h44 + 2 * h12 * h13 * h23 * h44 +
    2 * h12 * h14 * h24 * h33 - h13^2 * h22 * h44 +
    h13^2 * h24^2 - 2 * h13 * h14 * h23 * h24 -
    h14^2 * h22 * h33 + h14^2 * h23^2

theorem sylvester_principal_minor_values :
    principalMinor1 = 9399719209 / 6360000000 ∧
    principalMinor2 =
      395359846106875447280719 / 404496000000000000000000 ∧
    principalMinor3 =
      359556829343316384950230880641180953 /
        449440000000000000000000000000000000 ∧
    principalMinor4 =
      1337085894390964667090754208081695830761861 /
        17977600000000000000000000000000000000000000000000 := by
  norm_num [principalMinor1, principalMinor2, principalMinor3,
    principalMinor4, h11, h12, h13, h14, h22, h23, h24, h33, h34, h44]

theorem sylvester_principal_minor_positivity :
    0 < principalMinor1 ∧ 0 < principalMinor2 ∧
      0 < principalMinor3 ∧ 0 < principalMinor4 := by
  rcases sylvester_principal_minor_values with ⟨h1, h2, h3, h4⟩
  constructor
  · rw [h1]
    norm_num
  constructor
  · rw [h2]
    norm_num
  constructor
  · rw [h3]
    norm_num
  · rw [h4]
    norm_num

theorem weighted_amgm_75_106 (U N : ℝ) :
    4 * U * N ≤ (alpha * U + alphaInv * N)^2 := by
  dsimp [alpha, alphaInv]
  nlinarith [sq_nonneg ((75 / 106 : ℝ) * U - (106 / 75 : ℝ) * N)]

def weightedGap (x4 x5 y4 y5 : ℝ) : ℝ :=
  comparisonConstant * qDissipation x4 x5 y4 y5 -
    alpha * sumSq x4 x5 y4 y5 - alphaInv * stateSq x4 x5 y4 y5

theorem weighted_gap_ldl_identity (x4 x5 y4 y5 : ℝ) :
    weightedGap x4 x5 y4 y5 =
      (9399719209 / 6360000000 : ℝ) *
          (x4 - (22888519209 / 939971920900 : ℝ) * x5 -
            (4500000000 / 9399719209 : ℝ) * y4 +
            (7629506403 / 1879943841800 : ℝ) * y5)^2 +
      (395359846106875447280719 / 597822141692400000000000 : ℝ) *
          (x5 -
            (13885594538623379761350 /
              395359846106875447280719 : ℝ) * y4 -
            (845800100706139746004773 /
              790719692213750894561438 : ℝ) * y5)^2 +
      (3236011464089847464552077925770628577 /
        3953598461068754472807190000000000000 : ℝ) *
          (y4 -
            (3217560789628848699300752572801875 /
              119852276447772128316743626880393651 : ℝ) * y5)^2 +
      (1337085894390964667090754208081695830761861 /
        14382273173732655398009235225647238120000000000000 : ℝ) * y5^2 := by
  dsimp [weightedGap, comparisonConstant, alpha, alphaInv,
    qDissipation, sumSq, stateSq]
  ring

theorem weighted_gap_nonneg (x4 x5 y4 y5 : ℝ) :
    0 ≤ weightedGap x4 x5 y4 y5 := by
  rw [weighted_gap_ldl_identity]
  positivity

theorem weighted_joint_quadratic_bound (x4 x5 y4 y5 : ℝ) :
    alpha * sumSq x4 x5 y4 y5 + alphaInv * stateSq x4 x5 y4 y5 ≤
      comparisonConstant * qDissipation x4 x5 y4 y5 := by
  have hgap := weighted_gap_nonneg x4 x5 y4 y5
  dsimp [weightedGap] at hgap
  linarith

theorem qDissipation_nonneg (x4 x5 y4 y5 : ℝ) :
    0 ≤ qDissipation x4 x5 y4 y5 := by
  have hcomp := weighted_joint_quadratic_bound x4 x5 y4 y5
  have hU : 0 ≤ sumSq x4 x5 y4 y5 := by
    simp [sumSq]
    positivity
  have hN : 0 ≤ stateSq x4 x5 y4 y5 := by
    simp [stateSq]
    positivity
  have hS : 0 ≤ alpha * sumSq x4 x5 y4 y5 + alphaInv * stateSq x4 x5 y4 y5 := by
    dsimp [alpha, alphaInv]
    positivity
  dsimp [comparisonConstant] at hcomp
  nlinarith

theorem near_sharp_joint_centered_gain (x4 x5 y4 y5 : ℝ) :
    400000000000000 * sumSq x4 x5 y4 y5 * stateSq x4 x5 y4 y5 ≤
      2302494677956489 * (qDissipation x4 x5 y4 y5)^2 := by
  let U : ℝ := sumSq x4 x5 y4 y5
  let N : ℝ := stateSq x4 x5 y4 y5
  let Q : ℝ := qDissipation x4 x5 y4 y5
  let S : ℝ := alpha * U + alphaInv * N
  let T : ℝ := comparisonConstant * Q
  have hU : 0 ≤ U := by
    dsimp [U, sumSq]
    positivity
  have hN : 0 ≤ N := by
    dsimp [N, stateSq]
    positivity
  have hS : 0 ≤ S := by
    dsimp [S, alpha, alphaInv]
    positivity
  have hcomp : S ≤ T := by
    dsimp [S, T, U, N, Q]
    exact weighted_joint_quadratic_bound x4 x5 y4 y5
  have hT : 0 ≤ T := le_trans hS hcomp
  have hsq : S^2 ≤ T^2 := by
    have hminus : 0 ≤ T - S := sub_nonneg.mpr hcomp
    have hplus : 0 ≤ T + S := add_nonneg hT hS
    have hprod : 0 ≤ (T - S) * (T + S) := mul_nonneg hminus hplus
    nlinarith
  have hamgm : 4 * U * N ≤ S^2 := by
    dsimp [S]
    exact weighted_amgm_75_106 U N
  have hchain : 4 * U * N ≤ T^2 := le_trans hamgm hsq
  dsimp [T, comparisonConstant] at hchain
  dsimp [U, N, Q]
  nlinarith

theorem abs_le_of_sq_le_sq_nonneg (z r : ℝ) (hr : 0 ≤ r)
    (hsq : z^2 ≤ r^2) : |z| ≤ r := by
  apply (abs_le).2
  constructor
  · by_contra h
    have hz1 : z - r < 0 := by linarith
    have hz2 : z + r < 0 := by linarith
    have hp : 0 < (z - r) * (z + r) := mul_pos_of_neg_of_neg hz1 hz2
    nlinarith
  · by_contra h
    have hz1 : 0 < z - r := by linarith
    have hz2 : 0 < z + r := by linarith
    have hp : 0 < (z - r) * (z + r) := mul_pos hz1 hz2
    nlinarith

theorem near_sharp_scalar_residual_consumer
    (U N Q rcSq coupling ell2 mu : ℝ)
    (hU : 0 ≤ U) (hQ : 0 ≤ Q) (hell2 : 0 ≤ ell2) (hmu : 0 ≤ mu)
    (hrc : rcSq ≤ ell2 * N)
    (hcoupling : coupling^2 ≤ U * rcSq)
    (hjoint : 400000000000000 * U * N ≤ 2302494677956489 * Q^2)
    (hgain : 2302494677956489 * ell2 ≤ 400000000000000 * mu^2) :
    |coupling| ≤ mu * Q := by
  have hrcU : U * rcSq ≤ U * (ell2 * N) :=
    mul_le_mul_of_nonneg_left hrc hU
  have hc1 : coupling^2 ≤ ell2 * U * N := by
    nlinarith
  have hjmul : 400000000000000 * ell2 * (U * N) ≤
      2302494677956489 * ell2 * Q^2 := by
    nlinarith [mul_le_mul_of_nonneg_left hjoint hell2]
  have hc2 : 400000000000000 * coupling^2 ≤
      2302494677956489 * ell2 * Q^2 := by
    nlinarith
  have hgmul : 2302494677956489 * ell2 * Q^2 ≤
      400000000000000 * mu^2 * Q^2 := by
    nlinarith [mul_le_mul_of_nonneg_right hgain (sq_nonneg Q)]
  have hsquare : coupling^2 ≤ (mu * Q)^2 := by
    nlinarith
  have hrhs : 0 ≤ mu * Q := mul_nonneg hmu hQ
  exact abs_le_of_sq_le_sq_nonneg coupling (mu * Q) hrhs hsquare

theorem lower_witness_rejects_57562365_over_1e7 :
    stateSq 2379 73046 1832 68229 = 9999930422 ∧
    sumSq 2379 73046 1832 68229 = 19976358146 ∧
    qDissipation 2379 73046 1832 68229 =
      14138344959005123 / 2400000 ∧
    10000000 * (19976358146 : ℝ) * 9999930422 * 2400000^2 -
        57562365 * (14138344959005123 : ℝ)^2 =
      23290832775682489880381695029915 ∧
    (0 : ℝ) < 23290832775682489880381695029915 := by
  norm_num [stateSq, sumSq, qDissipation]

theorem exact_constant_arithmetic :
    (comparisonConstant^2 / 4 =
      2302494677956489 / 400000000000000) ∧
    ((144 / 25 : ℝ) -
      2302494677956489 / 400000000000000 =
      1505322043511 / 400000000000000) ∧
    (2302494677956489 / 400000000000000 -
      11512473 / 2000000 =
      77956489 / 400000000000000) := by
  norm_num [comparisonConstant]

#print axioms weighted_amgm_75_106
#print axioms sylvester_principal_minor_values
#print axioms sylvester_principal_minor_positivity
#print axioms weighted_joint_quadratic_bound
#print axioms near_sharp_joint_centered_gain
#print axioms near_sharp_scalar_residual_consumer
#print axioms lower_witness_rejects_57562365_over_1e7
#print axioms exact_constant_arithmetic

end

end RouteBP5ScalarFallback
