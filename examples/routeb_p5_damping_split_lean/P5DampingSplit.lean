import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# Route-B P5 damping-split sidecar

This file formalizes the source-independent scalar algebra from
`review-T-P5-015-guyuefangyuan-20260907T0438.md`.

It proves the generic division-free damping-split certificate implies the
corresponding headroom inequality, the exact rational `2/3 : 1/3`
specialization, its dominance over the previous `1/2 : 1/2` split, the current
C-FD integer reduction, and the calculus-free stationary polynomial identity.

It deliberately does not prove source binding, IEEE/solve error bounds,
weighted-dual source construction, ODE existence/continuation, P8 coverage, or
P5/M4 admission.
-/

set_option autoImplicit false

namespace RouteBP5DampingSplit

noncomputable section

/-- Dimensionless scalar split objective `H_e(alpha)`. -/
def splitObjective (e alpha : ℝ) : ℝ :=
  (1 - alpha) * (alpha ^ 2 - e)

/-- Exact calculus-free identity at a stationary witness
`e = 3*s^2 - 2*s`. -/
theorem split_objective_stationary_identity
    (e s alpha : ℝ)
    (hs : e = 3 * s ^ 2 - 2 * s) :
    splitObjective e s - splitObjective e alpha =
      (alpha - s) ^ 2 * (2 * s + alpha - 1) := by
  simp only [splitObjective]
  rw [hs]
  ring

/-- A stationary witness at or above `2/3` maximizes the scalar split objective
against every nonnegative comparison split.  This is the algebraic optimizer
comparison and uses no calculus or square root. -/
theorem stationary_witness_maximizes
    (e s alpha : ℝ)
    (hs : e = 3 * s ^ 2 - 2 * s)
    (hs23 : (2 : ℝ) / 3 ≤ s)
    (ha0 : 0 ≤ alpha) :
    splitObjective e alpha ≤ splitObjective e s := by
  have hlin : 0 ≤ 2 * s + alpha - 1 := by
    linarith
  have hprod :
      0 ≤ (alpha - s) ^ 2 * (2 * s + alpha - 1) :=
    mul_nonneg (sq_nonneg (alpha - s)) hlin
  have hid := split_objective_stationary_identity e s alpha hs
  linarith

/-- At a stationary witness the objective has the simplified exact value
`2*s*(1-s)^2`. -/
theorem stationary_objective_value
    (e s : ℝ)
    (hs : e = 3 * s ^ 2 - 2 * s) :
    splitObjective e s = 2 * s * (1 - s) ^ 2 := by
  simp only [splitObjective]
  rw [hs]
  ring

/-- The division-free checker certificate is sufficient for the original
headroom inequality.  Only positivity needed to clear the two denominators is
assumed; nonnegativity of the load variables is not needed for this algebraic
implication itself. -/
theorem damping_split_certificate
    (Q g0 E T Rbar alpha : ℝ)
    (hQ : 0 < Q)
    (hg0 : 0 < g0)
    (ha1 : alpha < 1)
    (hcert :
      4 * Q * (1 - alpha) * g0 * E + Q * T * Rbar <
        4 * alpha ^ 2 * (1 - alpha) * g0 ^ 3) :
    E + T * (Rbar / (4 * ((1 - alpha) * g0))) <
      alpha ^ 2 * g0 ^ 2 / Q := by
  have hOne : 0 < 1 - alpha := sub_pos.mpr ha1
  have hden : 0 < 4 * ((1 - alpha) * g0) := by
    positivity
  have hden_ne : 4 * ((1 - alpha) * g0) ≠ 0 := ne_of_gt hden
  apply (lt_div_iff₀ hQ).2
  have hscaled :
      (4 * ((1 - alpha) * g0)) *
          ((E + T * (Rbar / (4 * ((1 - alpha) * g0)))) * Q) <
        (4 * ((1 - alpha) * g0)) * (alpha ^ 2 * g0 ^ 2) := by
    calc
      (4 * ((1 - alpha) * g0)) *
          ((E + T * (Rbar / (4 * ((1 - alpha) * g0)))) * Q) =
          4 * Q * (1 - alpha) * g0 * E + Q * T * Rbar := by
            field_simp [hden_ne]
            <;> ring
      _ < 4 * alpha ^ 2 * (1 - alpha) * g0 ^ 3 := hcert
      _ = (4 * ((1 - alpha) * g0)) * (alpha ^ 2 * g0 ^ 2) := by
        ring
  by_contra hnot
  have hrev :
      alpha ^ 2 * g0 ^ 2 ≤
        (E + T * (Rbar / (4 * ((1 - alpha) * g0)))) * Q :=
    le_of_not_gt hnot
  have hmul := mul_le_mul_of_nonneg_left hrev (le_of_lt hden)
  exact (not_lt_of_ge hmul) hscaled

/-- The exact `alpha = 2/3` checker inequality is precisely strong enough to
instantiate the generic division-free certificate. -/
theorem two_thirds_checker_to_generic
    (Q g0 E T Rbar : ℝ)
    (hcert :
      36 * Q * g0 * E + 27 * Q * T * Rbar < 16 * g0 ^ 3) :
    4 * Q * (1 - (2 : ℝ) / 3) * g0 * E + Q * T * Rbar <
      4 * ((2 : ℝ) / 3) ^ 2 * (1 - (2 : ℝ) / 3) * g0 ^ 3 := by
  nlinarith

/-- Source-facing `2/3 : 1/3` headroom consequence, with the generic split
substituted exactly.  Keeping the conclusion in this form avoids introducing
any extra normalization convention. -/
theorem two_thirds_split_certificate
    (Q g0 E T Rbar : ℝ)
    (hQ : 0 < Q)
    (hg0 : 0 < g0)
    (hcert :
      36 * Q * g0 * E + 27 * Q * T * Rbar < 16 * g0 ^ 3) :
    E + T * (Rbar / (4 * ((1 - (2 : ℝ) / 3) * g0))) <
      ((2 : ℝ) / 3) ^ 2 * g0 ^ 2 / Q := by
  apply damping_split_certificate Q g0 E T Rbar ((2 : ℝ) / 3) hQ hg0
  · norm_num
  · exact two_thirds_checker_to_generic Q g0 E T Rbar hcert

/-- On nonnegative loads, every instance certified by the old `1/2 : 1/2`
criterion is also certified by the `2/3 : 1/3` criterion. -/
theorem two_thirds_dominates_half
    (Q g0 E T Rbar : ℝ)
    (hQ : 0 ≤ Q)
    (hg0 : 0 ≤ g0)
    (hE : 0 ≤ E)
    (hT : 0 ≤ T)
    (hR : 0 ≤ Rbar)
    (hhalf :
      4 * Q * g0 * E + 2 * Q * T * Rbar < g0 ^ 3) :
    36 * Q * g0 * E + 27 * Q * T * Rbar < 16 * g0 ^ 3 := by
  have hA : 0 ≤ Q * g0 * E :=
    mul_nonneg (mul_nonneg hQ hg0) hE
  have hB : 0 ≤ Q * T * Rbar :=
    mul_nonneg (mul_nonneg hQ hT) hR
  have hscaled :
      64 * Q * g0 * E + 32 * Q * T * Rbar < 16 * g0 ^ 3 := by
    nlinarith
  have hle :
      36 * Q * g0 * E + 27 * Q * T * Rbar ≤
        64 * Q * g0 * E + 32 * Q * T * Rbar := by
    nlinarith
  exact lt_of_le_of_lt hle hscaled

/-- Exact normalized comparison: for every `e >= 0`, the `2/3` split has
strictly larger scalar objective than the `1/2` split. -/
theorem two_thirds_strictly_better_than_half
    (e : ℝ)
    (he : 0 ≤ e) :
    splitObjective e ((1 : ℝ) / 2) <
      splitObjective e ((2 : ℝ) / 3) := by
  simp only [splitObjective]
  norm_num
  linarith

/-- Kernel-checked rational witness that the old half split can reject a
nonnegative normalized instance admitted by the `2/3` split. -/
theorem half_rejects_two_thirds_accepts_counterexample :
    ¬ ((7 : ℝ) / 50 < splitObjective 0 ((1 : ℝ) / 2)) ∧
      ((7 : ℝ) / 50 < splitObjective 0 ((2 : ℝ) / 3)) := by
  norm_num [splitObjective]

/-- The current C-FD specialization
`Q = 13*SF / 72000000000000000` reduces the `2/3` checker condition to the
integer certificate from T-P5-015. -/
theorem cfd_integer_certificate_implies_two_thirds
    (SF g0 E T Rbar : ℝ)
    (hcert :
      52 * SF * g0 * E + 39 * SF * T * Rbar <
        128000000000000000 * g0 ^ 3) :
    36 * (13 * SF / 72000000000000000) * g0 * E +
        27 * (13 * SF / 72000000000000000) * T * Rbar <
      16 * g0 ^ 3 := by
  nlinarith

/-- Exact `T=1`, `E=Z0+Hbar` source/checker-facing integer certificate. -/
theorem t1_cfd_two_thirds_certificate
    (SF g0 Z0 Hbar Rbar : ℝ)
    (hcert :
      52 * SF * g0 * (Z0 + Hbar) + 39 * SF * Rbar <
        128000000000000000 * g0 ^ 3) :
    36 * (13 * SF / 72000000000000000) * g0 * (Z0 + Hbar) +
        27 * (13 * SF / 72000000000000000) * 1 * Rbar <
      16 * g0 ^ 3 := by
  apply cfd_integer_certificate_implies_two_thirds SF g0 (Z0 + Hbar) 1 Rbar
  simpa using hcert

#print axioms split_objective_stationary_identity
#print axioms stationary_witness_maximizes
#print axioms stationary_objective_value
#print axioms damping_split_certificate
#print axioms two_thirds_checker_to_generic
#print axioms two_thirds_split_certificate
#print axioms two_thirds_dominates_half
#print axioms two_thirds_strictly_better_than_half
#print axioms half_rejects_two_thirds_accepts_counterexample
#print axioms cfd_integer_certificate_implies_two_thirds
#print axioms t1_cfd_two_thirds_certificate

end

end RouteBP5DampingSplit
