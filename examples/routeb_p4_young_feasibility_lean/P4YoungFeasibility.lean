import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# Route-B P4 exact scalar Young-feasibility sidecar

Source-independent Lean decomposition of
`agent_review_inbox/review-T-P4-038-guyuefangyuan-20260907T1521.md`.

The sidecar proves the division-free quadratic form of one sign-robust scalar
Young budget, the sharp discriminant necessity, constructive rational `theta`
and `lambda` witnesses, exact reserve identities, a strict-reserve consumer,
and two exact rational sanity examples.

It does not prove any concrete P4 source value for `A`, `P`, `D`, or `m`; it
does not prove a shared-parameter multi-row intersection, true-DH/Float64
semantics, trajectory/domain coverage, registry admission, or final P4/M4
integration.
-/

set_option autoImplicit false

namespace RouteBP4YoungFeasibility

noncomputable section

/-- Scalar sign-robust Young charge from T-P4-037/T-P4-038. -/
def youngCost (theta A P : ℝ) : ℝ :=
  (1 + theta) * A + (1 + 1 / theta) * P

/-- Exact multiplication identity behind the division-free quadratic seam. -/
theorem young_gap_mul_identity
    (A P D theta : ℝ) (htheta0 : theta ≠ 0) :
    theta * (D - youngCost theta A P) =
      (D - A - P) * theta - A * theta^2 - P := by
  unfold youngCost
  field_simp [htheta0]
  ring

/-- For `theta>0`, the Young budget is equivalent to one polynomial quadratic
inequality, with no division remaining in the checker-facing condition. -/
theorem young_scalar_budget_mul_iff
    (A P D theta : ℝ) (htheta : 0 < theta) :
    youngCost theta A P ≤ D ↔
      A * theta^2 - (D - A - P) * theta + P ≤ 0 := by
  have hid := young_gap_mul_identity A P D theta (ne_of_gt htheta)
  constructor
  · intro hbudget
    have hgap : 0 ≤ D - youngCost theta A P := by linarith
    have hmul : 0 ≤ theta * (D - youngCost theta A P) :=
      mul_nonneg (le_of_lt htheta) hgap
    rw [hid] at hmul
    linarith
  · intro hquad
    have hmul : 0 ≤ theta * (D - youngCost theta A P) := by
      rw [hid]
      linarith
    have hgap : 0 ≤ D - youngCost theta A P := by
      by_contra hnot
      have hneg : D - youngCost theta A P < 0 := lt_of_not_ge hnot
      have hprodneg : theta * (D - youngCost theta A P) < 0 :=
        mul_neg_of_pos_of_neg htheta hneg
      linarith
    linarith

/-- A feasible positive Young parameter forces both positive slack
`G=D-A-P` and the sharp discriminant gate `4AP ≤ G²`. -/
theorem young_scalar_discriminant_necessary
    (A P D theta : ℝ)
    (hA : 0 < A) (hP : 0 ≤ P) (htheta : 0 < theta)
    (hbudget : youngCost theta A P ≤ D) :
    0 < D - A - P ∧ 4 * A * P ≤ (D - A - P)^2 := by
  let G : ℝ := D - A - P
  have hquad0 := (young_scalar_budget_mul_iff A P D theta htheta).mp hbudget
  have hquad : A * theta^2 - G * theta + P ≤ 0 := by
    simpa [G] using hquad0
  have htheta2 : 0 < theta^2 := by
    simpa [pow_two] using mul_pos htheta htheta
  have hAterm : 0 < A * theta^2 := mul_pos hA htheta2
  have hsumpos : 0 < A * theta^2 + P := by linarith
  have hGt_ge : A * theta^2 + P ≤ G * theta := by linarith
  have hGt_pos : 0 < G * theta := lt_of_lt_of_le hsumpos hGt_ge
  have hG : 0 < G := by
    by_contra hnot
    have hGle : G ≤ 0 := le_of_not_gt hnot
    have hprodle : G * theta ≤ 0 :=
      mul_nonpos_of_nonpos_of_nonneg hGle (le_of_lt htheta)
    linarith

  let X : ℝ := A * theta^2 + P
  have hX_nonneg : 0 ≤ X := by
    dsimp [X]
    linarith
  have hGt_nonneg : 0 ≤ G * theta := le_of_lt hGt_pos
  have hminus_nonneg : 0 ≤ G * theta - X := by
    dsimp [X]
    linarith
  have hplus_nonneg : 0 ≤ G * theta + X := add_nonneg hGt_nonneg hX_nonneg
  have hprod : 0 ≤ (G * theta - X) * (G * theta + X) :=
    mul_nonneg hminus_nonneg hplus_nonneg
  have hsq_cmp : X^2 ≤ (G * theta)^2 := by
    nlinarith [hprod]
  have hamgm : 4 * A * P * theta^2 ≤ X^2 := by
    dsimp [X]
    nlinarith [sq_nonneg (A * theta^2 - P)]
  have hscaled : (4 * A * P) * theta^2 ≤ G^2 * theta^2 := by
    calc
      (4 * A * P) * theta^2 = 4 * A * P * theta^2 := by ring
      _ ≤ X^2 := hamgm
      _ ≤ (G * theta)^2 := hsq_cmp
      _ = G^2 * theta^2 := by ring
  have hdisc : 4 * A * P ≤ G^2 := by
    by_contra hnot
    have hlt : G^2 < 4 * A * P := lt_of_not_ge hnot
    have hscaled_strict : G^2 * theta^2 < (4 * A * P) * theta^2 :=
      mul_lt_mul_of_pos_right hlt htheta2
    linarith
  constructor
  · simpa [G] using hG
  · simpa [G] using hdisc

/-- Exact gap of the constructive rational `theta = G/(2A)`. -/
theorem young_theta_gap_identity
    (A P G : ℝ) (hA0 : A ≠ 0) (hG0 : G ≠ 0) :
    A + P + G - youngCost (G / (2 * A)) A P =
      (G^2 - 4 * A * P) / (2 * G) := by
  unfold youngCost
  field_simp [hA0, hG0]
  ring

/-- Sharp constructive sufficiency.  Notably, `P≥0` is unnecessary once the
positive-slack and discriminant premises are supplied. -/
theorem young_scalar_discriminant_constructive
    (A P G : ℝ)
    (hA : 0 < A) (hG : 0 < G)
    (hdisc : 4 * A * P ≤ G^2) :
    0 < G / (2 * A) ∧
    youngCost (G / (2 * A)) A P ≤ A + P + G ∧
    A + P + G - youngCost (G / (2 * A)) A P =
      (G^2 - 4 * A * P) / (2 * G) := by
  have htheta : 0 < G / (2 * A) := by positivity
  have hgap := young_theta_gap_identity A P G (ne_of_gt hA) (ne_of_gt hG)
  have hgap_nonneg : 0 ≤ A + P + G - youngCost (G / (2 * A)) A P := by
    rw [hgap]
    exact div_nonneg (sub_nonneg.mpr hdisc) (by positivity)
  exact ⟨htheta, by linarith, hgap⟩

/-- Exact gap for the historical `lambda = 1 + 2A/G` parameterization. -/
theorem young_lambda_gap_identity
    (A P G : ℝ) (hA0 : A ≠ 0) (hG0 : G ≠ 0) :
    A + P + G -
      (((1 + 2 * A / G) / ((1 + 2 * A / G) - 1)) * A +
        (1 + 2 * A / G) * P) =
      (G^2 - 4 * A * P) / (2 * G) := by
  field_simp [hA0, hG0]
  ring

/-- Constructive rational `lambda>1` consumer for the combined-Schur ledger. -/
theorem young_scalar_lambda_constructive
    (A P G : ℝ)
    (hA : 0 < A) (hG : 0 < G)
    (hdisc : 4 * A * P ≤ G^2) :
    1 < 1 + 2 * A / G ∧
    ((1 + 2 * A / G) / ((1 + 2 * A / G) - 1)) * A +
        (1 + 2 * A / G) * P ≤ A + P + G ∧
    A + P + G -
      (((1 + 2 * A / G) / ((1 + 2 * A / G) - 1)) * A +
        (1 + 2 * A / G) * P) =
      (G^2 - 4 * A * P) / (2 * G) := by
  have hfrac : 0 < 2 * A / G := by
    exact div_pos (mul_pos (by norm_num) hA) hG
  have hlambda : 1 < 1 + 2 * A / G := by linarith
  have hgap := young_lambda_gap_identity A P G (ne_of_gt hA) (ne_of_gt hG)
  have hgap_nonneg :
      0 ≤ A + P + G -
        (((1 + 2 * A / G) / ((1 + 2 * A / G) - 1)) * A +
          (1 + 2 * A / G) * P) := by
    rw [hgap]
    exact div_nonneg (sub_nonneg.mpr hdisc) (by positivity)
  exact ⟨hlambda, by linarith, hgap⟩

/-- Strict-reserve consumer: set `Gm = D-m-A-P` and use the same rational
`lambda`.  No sign assumption on `m` is algebraically needed here. -/
theorem young_scalar_strict_margin_constructive
    (A P D m : ℝ)
    (hA : 0 < A)
    (hGm : 0 < D - m - A - P)
    (hdisc : 4 * A * P ≤ (D - m - A - P)^2) :
    1 < 1 + 2 * A / (D - m - A - P) ∧
    ((1 + 2 * A / (D - m - A - P)) /
        ((1 + 2 * A / (D - m - A - P)) - 1)) * A +
        (1 + 2 * A / (D - m - A - P)) * P ≤ D - m ∧
    D - m -
      (((1 + 2 * A / (D - m - A - P)) /
          ((1 + 2 * A / (D - m - A - P)) - 1)) * A +
        (1 + 2 * A / (D - m - A - P)) * P) =
      (((D - m - A - P)^2 - 4 * A * P) /
        (2 * (D - m - A - P))) := by
  have h := young_scalar_lambda_constructive
    A P (D - m - A - P) hA hGm hdisc
  rcases h with ⟨hlambda, hcost, hgap⟩
  refine ⟨hlambda, ?_, ?_⟩
  · nlinarith
  · nlinarith [hgap]

/-- A strict discriminant gives a strictly positive reserve beyond `m`. -/
theorem young_scalar_strict_extra_reserve
    (A P D m : ℝ)
    (hA : 0 < A)
    (hGm : 0 < D - m - A - P)
    (hdisc : 4 * A * P < (D - m - A - P)^2) :
    0 < D - m -
      (((1 + 2 * A / (D - m - A - P)) /
          ((1 + 2 * A / (D - m - A - P)) - 1)) * A +
        (1 + 2 * A / (D - m - A - P)) * P) := by
  have hgap := young_lambda_gap_identity
    A P (D - m - A - P) (ne_of_gt hA) (ne_of_gt hGm)
  have hrhs :
      0 < (((D - m - A - P)^2 - 4 * A * P) /
        (2 * (D - m - A - P))) := by
    exact div_pos (sub_pos.mpr hdisc) (by positivity)
  nlinarith [hgap]

/-- Exact rational example from T-P4-038 showing the constructive parameter can
succeed when the fixed `theta=1` charge fails. -/
theorem rational_example_sharp_vs_theta_one :
    youngCost (3/25 : ℝ) 1 (1/100) = 91/75 ∧
    youngCost (3/25 : ℝ) 1 (1/100) < 5/4 ∧
    youngCost 1 1 (1/100) = 101/50 ∧
    (5/4 : ℝ) < youngCost 1 1 (1/100) := by
  norm_num [youngCost]

/-- Exact obstruction example: `A=P=1, D=3` cannot admit any positive scalar
Young parameter. -/
theorem obstruction_example_no_theta
    (theta : ℝ) (htheta : 0 < theta) :
    ¬ youngCost theta 1 1 ≤ 3 := by
  intro hbudget
  have hdisc := young_scalar_discriminant_necessary
    1 1 3 theta (by norm_num) (by norm_num) htheta hbudget
  norm_num at hdisc

#print axioms young_gap_mul_identity
#print axioms young_scalar_budget_mul_iff
#print axioms young_scalar_discriminant_necessary
#print axioms young_theta_gap_identity
#print axioms young_scalar_discriminant_constructive
#print axioms young_lambda_gap_identity
#print axioms young_scalar_lambda_constructive
#print axioms young_scalar_strict_margin_constructive
#print axioms young_scalar_strict_extra_reserve
#print axioms rational_example_sharp_vs_theta_one
#print axioms obstruction_example_no_theta

end

end RouteBP4YoungFeasibility
