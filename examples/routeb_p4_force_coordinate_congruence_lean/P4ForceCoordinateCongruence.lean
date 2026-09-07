import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# Route-B P4 nominal-to-force coordinate congruence sidecar

This file formalizes the source-independent interface mathematics from
`review-T-P4-018-liuguanyi-20260907T0522.md`.

The PMI nominal/acceleration-style coordinate is transported to the current
P4 generalized-force residual by `I_B = diag(1/5,1/10)`.  The file records the
exact `kc` normalization, a division-free scalar Schur congruence theorem, a
mixed-coordinate residual envelope with an extremizer, and exact channel-4
rational corollaries.

It does not authenticate Julia/Float64 source semantics, does not replace the
generic Schur sidecars, and does not close P4/M4.
-/

set_option autoImplicit false

namespace RouteBP4ForceCoordinateCongruence

noncomputable section

/-- The literal nominal `kc=(q5/20,q4/20)` becomes
`(q5/100,q4/200)` in the generalized-force residual after applying
`I_B=diag(1/5,1/10)`. -/
theorem kc_force_normalization (q4 q5 : ℝ) :
    ((1 / 5 : ℝ) * (q5 / 20), (1 / 10 : ℝ) * (q4 / 20)) =
      (q5 / 100, q4 / 200) := by
  ext <;> ring

/-- Division-free scalar coordinate congruence.  If the residual, Schur
auxiliary variable, and positive quadratic coefficient are all transported by
the same scalar normalization, the quadratic form is exactly unchanged. -/
theorem schur_coordinate_congruence
    (j pF pA d xF xA rF rA y : ℝ)
    (hx : xA = j * xF)
    (hr : rF = j * rA)
    (hp : pF = j ^ 2 * pA) :
    pF * xF ^ 2 + 2 * xF * rF + d * y ^ 2 =
      pA * xA ^ 2 + 2 * xA * rA + d * y ^ 2 := by
  rw [hx, hr, hp]
  ring

/-- Transport an acceleration-style relative envelope and a native force-side
envelope into one generalized-force envelope.  No sign condition on the beta
coefficients is needed beyond the stated envelope hypotheses; only the scale
`j` and nominal coefficient `c` need be nonnegative to remove their absolute
values. -/
theorem mixed_normalization_residual_bound
    (j c betaA betaF y eA eF : ℝ)
    (hj : 0 ≤ j)
    (hc : 0 ≤ c)
    (heA : |eA| ≤ betaA * |y|)
    (heF : |eF| ≤ betaF * |y|) :
    |j * (c * y + eA) + eF| ≤
      (j * (c + betaA) + betaF) * |y| := by
  have hinner0 : |c * y + eA| ≤ |c * y| + |eA| :=
    abs_add_le (c * y) eA
  have hcy : |c * y| = c * |y| := by
    rw [abs_mul, abs_of_nonneg hc]
  rw [hcy] at hinner0
  have hinner : |c * y + eA| ≤ (c + betaA) * |y| := by
    nlinarith
  have hjinner :
      j * |c * y + eA| ≤ j * ((c + betaA) * |y|) :=
    mul_le_mul_of_nonneg_left hinner hj
  have houter :
      |j * (c * y + eA) + eF| ≤ |j * (c * y + eA)| + |eF| :=
    abs_add_le (j * (c * y + eA)) eF
  have hjabs : |j * (c * y + eA)| = j * |c * y + eA| := by
    rw [abs_mul, abs_of_nonneg hj]
  rw [hjabs] at houter
  nlinarith

/-- The mixed-coordinate coefficient is attained by aligned independent
remainders at `y=1`; hence the coefficient in
`mixed_normalization_residual_bound` cannot be lowered using only those
independent magnitude envelopes. -/
theorem mixed_normalization_extremizer
    (j c betaA betaF : ℝ)
    (hj : 0 ≤ j)
    (hc : 0 ≤ c)
    (hA : 0 ≤ betaA)
    (hF : 0 ≤ betaF) :
    |betaA| = betaA * |(1 : ℝ)| ∧
      |betaF| = betaF * |(1 : ℝ)| ∧
      |j * (c * (1 : ℝ) + betaA) + betaF| =
        (j * (c + betaA) + betaF) * |(1 : ℝ)| := by
  have hsum : 0 ≤ j * (c + betaA) + betaF := by
    exact add_nonneg
      (mul_nonneg hj (add_nonneg hc hA)) hF
  constructor
  · rw [abs_of_nonneg hA, abs_one, mul_one]
  constructor
  · rw [abs_of_nonneg hF, abs_one, mul_one]
  · rw [abs_one, mul_one]
    convert abs_of_nonneg hsum using 1 <;> ring

/-- Exact channel-4 force scaling of the literal `1/20` nominal coefficient. -/
theorem channel4_kc_force :
    (1 / 5 : ℝ) * (1 / 20) = 1 / 100 := by
  norm_num

/-- Exact channel-5 force scaling of the literal `1/20` nominal coefficient. -/
theorem channel5_kc_force :
    (1 / 10 : ℝ) * (1 / 20) = 1 / 200 := by
  norm_num

/-- Channel 4 uses `pA=15` after congruently pulling the force-side
`pF=3/5` back through `j=1/5`. -/
theorem channel4_positive_coefficient_transport :
    (3 / 5 : ℝ) = (1 / 5) ^ 2 * 15 := by
  norm_num

/-- Exact block-4 cross-coordinate coefficient from the Route-B PMI. -/
def d4 : ℝ := 116667666666667 / 1000000000000000

/-- Exact force-coordinate Schur margin for the isolated normalized `kc` term. -/
theorem channel4_force_margin :
    (3 / 5 : ℝ) * d4 - (1 / 100 : ℝ) ^ 2 =
      349503000000001 / 5000000000000000 := by
  norm_num [d4]

/-- The congruent acceleration-style margin is exactly twenty-five times the
force-coordinate margin. -/
theorem channel4_margin_congruence :
    (15 : ℝ) * d4 - (1 / 20 : ℝ) ^ 2 =
      25 * ((3 / 5 : ℝ) * d4 - (1 / 100 : ℝ) ^ 2) := by
  norm_num [d4]

/-- The exact force-coordinate margin is strictly positive. -/
theorem channel4_force_margin_pos :
    0 < (3 / 5 : ℝ) * d4 - (1 / 100 : ℝ) ^ 2 := by
  rw [channel4_force_margin]
  norm_num

/-- Source-facing channel-4 mixed budget.  An acceleration-style remainder
with slope `betaA` costs only `1/5*betaA` after transport, while a native force
remainder with slope `betaF` costs `betaF`.  The existing force-side quarter
consumer is respected whenever that combined remainder uses at most `6/25`. -/
theorem channel4_mixed_quarter_envelope
    (betaA betaF y eA eF : ℝ)
    (heA : |eA| ≤ betaA * |y|)
    (heF : |eF| ≤ betaF * |y|)
    (hbudget : (1 / 5 : ℝ) * betaA + betaF ≤ 6 / 25) :
    |(1 / 5 : ℝ) * ((1 / 20 : ℝ) * y + eA) + eF| ≤
      (1 / 4 : ℝ) * |y| := by
  have hmix := mixed_normalization_residual_bound
    (1 / 5 : ℝ) (1 / 20 : ℝ) betaA betaF y eA eF
    (by norm_num) (by norm_num) heA heF
  have hcoef :
      (1 / 5 : ℝ) * ((1 / 20 : ℝ) + betaA) + betaF ≤ 1 / 4 := by
    nlinarith
  calc
    |(1 / 5 : ℝ) * ((1 / 20 : ℝ) * y + eA) + eF|
        ≤ ((1 / 5 : ℝ) * ((1 / 20 : ℝ) + betaA) + betaF) * |y| := hmix
    _ ≤ (1 / 4 : ℝ) * |y| :=
      mul_le_mul_of_nonneg_right hcoef (abs_nonneg y)

#print axioms kc_force_normalization
#print axioms schur_coordinate_congruence
#print axioms mixed_normalization_residual_bound
#print axioms mixed_normalization_extremizer
#print axioms channel4_kc_force
#print axioms channel5_kc_force
#print axioms channel4_positive_coefficient_transport
#print axioms channel4_force_margin
#print axioms channel4_margin_congruence
#print axioms channel4_force_margin_pos
#print axioms channel4_mixed_quarter_envelope

end

end RouteBP4ForceCoordinateCongruence
