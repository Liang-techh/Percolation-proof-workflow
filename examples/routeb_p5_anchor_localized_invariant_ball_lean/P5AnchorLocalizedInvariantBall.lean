import Mathlib

noncomputable section

namespace RouteBP5AnchorLocalizedInvariantBall

/-- Division-free scalar consumer for the anchor-residual localization argument.
    `V0` is the weighted squared distance, `ip` the weighted monotonicity pairing,
    and `qFc` the weighted squared anchor residual. -/
theorem anchor_root_localization_division_free
    (mu V0 ip qFc B0 : ℝ)
    (hmu : 0 < mu)
    (hV0 : 0 ≤ V0)
    (hqFc : 0 ≤ qFc)
    (hmon : mu * V0 ≤ ip)
    (hcauchy : ip ^ 2 ≤ qFc * V0)
    (hbudget : qFc ≤ B0) :
    mu ^ 2 * V0 ≤ B0 := by
  by_cases hz : V0 = 0
  · have hB0 : 0 ≤ B0 := le_trans hqFc hbudget
    simpa [hz] using hB0
  have hVpos : 0 < V0 := lt_of_le_of_ne hV0 (Ne.symm hz)
  have hmuV : 0 ≤ mu * V0 := by positivity
  have hip : 0 ≤ ip := le_trans hmuV hmon
  have hsq : (mu * V0) ^ 2 ≤ ip ^ 2 := by
    nlinarith [sq_nonneg (ip - mu * V0)]
  have hq : qFc * V0 ≤ B0 * V0 :=
    mul_le_mul_of_nonneg_right hbudget hV0
  nlinarith [hsq, hcauchy, hq]

/-- Once localization is known, the same division-free budget initializes a chosen sublevel. -/
theorem anchor_inside_sublevel_of_budget
    (mu V0 B0 Vstar : ℝ)
    (hmu : 0 < mu)
    (hloc : mu ^ 2 * V0 ≤ B0)
    (hbudget : B0 ≤ mu ^ 2 * Vstar) :
    V0 ≤ Vstar := by
  have hmu2 : 0 < mu ^ 2 := by positivity
  nlinarith

/-- Radical-free two-square envelope. It is the polynomial form of
    `sqrt A + sqrt C <= sqrt T`, but requires no square root in the checker.
    Nonnegativity of `C` is derivable from `hb` and `K > 0`, so it is not
    duplicated as a theorem hypothesis. -/
theorem scaled_two_square_sum_gate
    (K A C T a b : ℝ)
    (hK : 0 < K)
    (hA : 0 ≤ A)
    (ha : K * a ^ 2 ≤ A)
    (hb : K * b ^ 2 ≤ C)
    (hreserve : 0 ≤ T - A - C)
    (hcross : 4 * A * C ≤ (T - A - C) ^ 2) :
    K * (a + b) ^ 2 ≤ T := by
  have hKb : 0 ≤ K * b ^ 2 := mul_nonneg (le_of_lt hK) (sq_nonneg b)
  have hprod : (K * a ^ 2) * (K * b ^ 2) ≤ A * C :=
    mul_le_mul ha hb hKb hA
  have hcrosssq : (2 * K * a * b) ^ 2 ≤ (T - A - C) ^ 2 := by
    nlinarith [hprod, hcross]
  have hlinear : 2 * K * a * b ≤ T - A - C := by
    nlinarith [hcrosssq, sq_nonneg (2 * K * a * b + (T - A - C))]
  calc
    K * (a + b) ^ 2 = K * a ^ 2 + K * b ^ 2 + 2 * K * a * b := by ring
    _ ≤ A + C + (T - A - C) := by nlinarith
    _ = T := by ring

/-- Strict radical-free two-square envelope. -/
theorem scaled_two_square_sum_gate_strict
    (K A C T a b : ℝ)
    (hK : 0 < K)
    (hA : 0 ≤ A)
    (ha : K * a ^ 2 ≤ A)
    (hb : K * b ^ 2 ≤ C)
    (hreserve : 0 < T - A - C)
    (hcross : 4 * A * C < (T - A - C) ^ 2) :
    K * (a + b) ^ 2 < T := by
  have hKb : 0 ≤ K * b ^ 2 := mul_nonneg (le_of_lt hK) (sq_nonneg b)
  have hprod : (K * a ^ 2) * (K * b ^ 2) ≤ A * C :=
    mul_le_mul ha hb hKb hA
  have hcrosssq : (2 * K * a * b) ^ 2 < (T - A - C) ^ 2 := by
    nlinarith [hprod, hcross]
  have hlinear : 2 * K * a * b < T - A - C := by
    nlinarith [hcrosssq, sq_nonneg (2 * K * a * b + (T - A - C))]
  calc
    K * (a + b) ^ 2 = K * a ^ 2 + K * b ^ 2 + 2 * K * a * b := by ring
    _ < A + C + (T - A - C) := by nlinarith
    _ = T := by ring

/-- One coordinate of the root-centered Lyapunov sublevel stays inside the
    anchor-centered source interval under the radical-free gate. -/
theorem coordinate_source_interval_of_radical_free_gate
    (mu w H Vstar B0 x xstar c : ℝ)
    (hmu : 0 < mu)
    (hw : 0 < w)
    (hH : 0 ≤ H)
    (hVstar : 0 ≤ Vstar)
    (hstate : w * (x - xstar) ^ 2 ≤ Vstar)
    (hroot : mu ^ 2 * w * (xstar - c) ^ 2 ≤ B0)
    (hreserve : 0 ≤ mu ^ 2 * w * H ^ 2 - mu ^ 2 * Vstar - B0)
    (hcross : 4 * (mu ^ 2 * Vstar) * B0 ≤
      (mu ^ 2 * w * H ^ 2 - mu ^ 2 * Vstar - B0) ^ 2) :
    |x - c| ≤ H := by
  have hmu2 : 0 ≤ mu ^ 2 := sq_nonneg mu
  have hK : 0 < mu ^ 2 * w := by positivity
  have ha : (mu ^ 2 * w) * (x - xstar) ^ 2 ≤ mu ^ 2 * Vstar := by
    have h := mul_le_mul_of_nonneg_left hstate hmu2
    nlinarith
  have hsum := scaled_two_square_sum_gate
    (K := mu ^ 2 * w)
    (A := mu ^ 2 * Vstar)
    (C := B0)
    (T := mu ^ 2 * w * H ^ 2)
    (a := x - xstar)
    (b := xstar - c)
    hK (mul_nonneg hmu2 hVstar) ha hroot hreserve hcross
  have hscaled : (mu ^ 2 * w) * (x - c) ^ 2 ≤ (mu ^ 2 * w) * H ^ 2 := by
    nlinarith [hsum]
  have hsq : (x - c) ^ 2 ≤ H ^ 2 := by
    by_contra hnot
    have hgt : H ^ 2 < (x - c) ^ 2 := lt_of_not_ge hnot
    have hmulgt :
        (mu ^ 2 * w) * H ^ 2 < (mu ^ 2 * w) * (x - c) ^ 2 :=
      mul_lt_mul_of_pos_left hgt hK
    exact (not_lt_of_ge hscaled) hmulgt
  have hupper : x - c ≤ H := by nlinarith
  have hlower : -H ≤ x - c := by nlinarith
  exact (abs_le).2 ⟨hlower, hupper⟩

/-- Finite typed consumer: if every coordinate carries the same-weight state/root
    square packets and passes the rational gate, the whole state is in the box. -/
theorem finite_source_box_containment
    {n : ℕ}
    (mu Vstar B0 : ℝ)
    (w H x xstar c : Fin n → ℝ)
    (hmu : 0 < mu)
    (hw : ∀ i, 0 < w i)
    (hH : ∀ i, 0 ≤ H i)
    (hVstar : 0 ≤ Vstar)
    (hstate : ∀ i, w i * (x i - xstar i) ^ 2 ≤ Vstar)
    (hroot : ∀ i, mu ^ 2 * w i * (xstar i - c i) ^ 2 ≤ B0)
    (hreserve : ∀ i, 0 ≤ mu ^ 2 * w i * H i ^ 2 - mu ^ 2 * Vstar - B0)
    (hcross : ∀ i, 4 * (mu ^ 2 * Vstar) * B0 ≤
      (mu ^ 2 * w i * H i ^ 2 - mu ^ 2 * Vstar - B0) ^ 2) :
    ∀ i, |x i - c i| ≤ H i := by
  intro i
  exact coordinate_source_interval_of_radical_free_gate
    mu (w i) (H i) Vstar B0 (x i) (xstar i) (c i)
    hmu (hw i) (hH i) hVstar
    (hstate i) (hroot i) (hreserve i) (hcross i)

/-- Boundary equality gives zero reserve: it is containment at best, not a strict-interior certificate. -/
theorem reserve_equality_is_not_strict
    (A C T : ℝ)
    (h : T = A + C) :
    T - A - C = 0 := by
  linarith

/-- Exact counterexample: the naive `A+C <= T` gate passes while the root-centered
    sublevel leaves the anchor-centered source interval because the cross term was dropped. -/
theorem naive_additive_gate_counterexample :
    ((1 / 4 : ℝ) + 1 / 4 ≤ 9 / 16) ∧
    (((1 : ℝ) - 1 / 2) ^ 2 ≤ 1 / 4) ∧
    (((1 / 2 : ℝ) - 0) ^ 2 ≤ 1 / 4) ∧
    ¬ |(1 : ℝ) - 0| ≤ 3 / 4 := by
  norm_num

#print axioms anchor_root_localization_division_free
#print axioms anchor_inside_sublevel_of_budget
#print axioms scaled_two_square_sum_gate
#print axioms scaled_two_square_sum_gate_strict
#print axioms coordinate_source_interval_of_radical_free_gate
#print axioms finite_source_box_containment
#print axioms reserve_equality_is_not_strict
#print axioms naive_additive_gate_counterexample

end RouteBP5AnchorLocalizedInvariantBall
