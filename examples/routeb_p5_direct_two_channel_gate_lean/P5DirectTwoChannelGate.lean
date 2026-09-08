import Mathlib

noncomputable section

namespace RouteBP5DirectTwoChannelGate

/-- Multiplication by a strictly positive scalar preserves strict negativity. -/
theorem positive_scale_lt_zero_iff
    (k x : ℝ) (hk : 0 < k) :
    k * x < 0 ↔ x < 0 := by
  constructor
  · intro hkx
    by_contra hnot
    have hx : 0 ≤ x := le_of_not_gt hnot
    have hnonneg : 0 ≤ k * x := mul_nonneg (le_of_lt hk) hx
    linarith
  · intro hx
    exact mul_neg_of_pos_of_neg hk hx

/--
Signed one-radical elimination after an arbitrary positive scaling.  The sign
condition on `T` is retained explicitly, so squaring is reversible.
-/
theorem scaled_sqrt_lt_iff_signed_square
    (K X T : ℝ)
    (hK : 0 < K)
    (hX : 0 ≤ X) :
    K * Real.sqrt X < T ↔
      0 < T ∧ K ^ 2 * X < T ^ 2 := by
  have hs0 : 0 ≤ Real.sqrt X := Real.sqrt_nonneg X
  have hz0 : 0 ≤ K * Real.sqrt X :=
    mul_nonneg (le_of_lt hK) hs0
  have hs2 : (Real.sqrt X) ^ 2 = X := Real.sq_sqrt hX
  have hz2 : (K * Real.sqrt X) ^ 2 = K ^ 2 * X := by
    rw [mul_pow, hs2]
  constructor
  · intro hlt
    have hT : 0 < T := lt_of_le_of_lt hz0 hlt
    refine ⟨hT, ?_⟩
    have hdiff : 0 < T - K * Real.sqrt X := sub_pos.mpr hlt
    have hsum : 0 < T + K * Real.sqrt X := by
      nlinarith
    have hprod :
        0 < (T - K * Real.sqrt X) * (T + K * Real.sqrt X) :=
      mul_pos hdiff hsum
    have hid :
        T ^ 2 - (K * Real.sqrt X) ^ 2
          = (T - K * Real.sqrt X) * (T + K * Real.sqrt X) := by
      ring
    nlinarith
  · rintro ⟨hT, hsq⟩
    by_contra hnot
    have hge : T ≤ K * Real.sqrt X := le_of_not_gt hnot
    have hdiff : 0 ≤ K * Real.sqrt X - T := sub_nonneg.mpr hge
    have hsum : 0 < K * Real.sqrt X + T := by
      nlinarith
    have hprod :
        0 ≤ (K * Real.sqrt X - T) * (K * Real.sqrt X + T) :=
      mul_nonneg hdiff (le_of_lt hsum)
    have hid :
        (K * Real.sqrt X) ^ 2 - T ^ 2
          = (K * Real.sqrt X - T) * (K * Real.sqrt X + T) := by
      ring
    nlinarith

/-- Unscaled signed one-radical elimination. -/
theorem sqrt_lt_iff_signed_square
    (X T : ℝ)
    (hX : 0 ≤ X) :
    Real.sqrt X < T ↔ 0 < T ∧ X < T ^ 2 := by
  simpa using scaled_sqrt_lt_iff_signed_square (1 : ℝ) X T (by norm_num) hX

/--
Signed two-radical elimination.  Both positivity guards survive the two
squarings; the final squared cross condition alone is intentionally not enough.
-/
theorem two_scaled_sqrt_lt_iff_signed_square
    (A B X Y T : ℝ)
    (hA : 0 < A)
    (hB : 0 < B)
    (hX : 0 ≤ X)
    (hY : 0 ≤ Y) :
    A * Real.sqrt X + B * Real.sqrt Y < T ↔
      0 < T
        ∧ 0 < T ^ 2 - A ^ 2 * X - B ^ 2 * Y
        ∧ 4 * A ^ 2 * B ^ 2 * X * Y
            < (T ^ 2 - A ^ 2 * X - B ^ 2 * Y) ^ 2 := by
  let u : ℝ := A * Real.sqrt X
  let v : ℝ := B * Real.sqrt Y
  have hsX0 : 0 ≤ Real.sqrt X := Real.sqrt_nonneg X
  have hsY0 : 0 ≤ Real.sqrt Y := Real.sqrt_nonneg Y
  have hu0 : 0 ≤ u := by
    dsimp [u]
    exact mul_nonneg (le_of_lt hA) hsX0
  have hv0 : 0 ≤ v := by
    dsimp [v]
    exact mul_nonneg (le_of_lt hB) hsY0
  have hu2 : u ^ 2 = A ^ 2 * X := by
    dsimp [u]
    rw [mul_pow, Real.sq_sqrt hX]
  have hv2 : v ^ 2 = B ^ 2 * Y := by
    dsimp [v]
    rw [mul_pow, Real.sq_sqrt hY]
  have hz2 :
      (u + v) ^ 2 = A ^ 2 * X + B ^ 2 * Y + 2 * u * v := by
    calc
      (u + v) ^ 2 = u ^ 2 + v ^ 2 + 2 * u * v := by ring
      _ = A ^ 2 * X + B ^ 2 * Y + 2 * u * v := by rw [hu2, hv2]
  have huv0 : 0 ≤ u * v := mul_nonneg hu0 hv0
  have hw0 : 0 ≤ 2 * u * v := mul_nonneg (by norm_num) huv0
  have hw2 :
      (2 * u * v) ^ 2 = 4 * A ^ 2 * B ^ 2 * X * Y := by
    calc
      (2 * u * v) ^ 2 = 4 * u ^ 2 * v ^ 2 := by ring
      _ = 4 * A ^ 2 * B ^ 2 * X * Y := by rw [hu2, hv2]; ring
  change u + v < T ↔
      0 < T
        ∧ 0 < T ^ 2 - A ^ 2 * X - B ^ 2 * Y
        ∧ 4 * A ^ 2 * B ^ 2 * X * Y
            < (T ^ 2 - A ^ 2 * X - B ^ 2 * Y) ^ 2
  constructor
  · intro hlt
    have hz0 : 0 ≤ u + v := add_nonneg hu0 hv0
    have hT : 0 < T := lt_of_le_of_lt hz0 hlt
    have hdiff : 0 < T - (u + v) := sub_pos.mpr hlt
    have hsum : 0 < T + (u + v) := by nlinarith
    have hprod : 0 < (T - (u + v)) * (T + (u + v)) :=
      mul_pos hdiff hsum
    have hid :
        T ^ 2 - (u + v) ^ 2
          = (T - (u + v)) * (T + (u + v)) := by
      ring
    have hsqsum : (u + v) ^ 2 < T ^ 2 := by
      nlinarith
    have htwocross :
        2 * u * v < T ^ 2 - A ^ 2 * X - B ^ 2 * Y := by
      nlinarith
    have hS : 0 < T ^ 2 - A ^ 2 * X - B ^ 2 * Y :=
      lt_of_le_of_lt hw0 htwocross
    have hdiff2 :
        0 < (T ^ 2 - A ^ 2 * X - B ^ 2 * Y) - 2 * u * v :=
      sub_pos.mpr htwocross
    have hsum2 :
        0 < (T ^ 2 - A ^ 2 * X - B ^ 2 * Y) + 2 * u * v := by
      nlinarith
    have hprod2 :
        0 < ((T ^ 2 - A ^ 2 * X - B ^ 2 * Y) - 2 * u * v)
          * ((T ^ 2 - A ^ 2 * X - B ^ 2 * Y) + 2 * u * v) :=
      mul_pos hdiff2 hsum2
    have hid2 :
        (T ^ 2 - A ^ 2 * X - B ^ 2 * Y) ^ 2 - (2 * u * v) ^ 2
          = ((T ^ 2 - A ^ 2 * X - B ^ 2 * Y) - 2 * u * v)
              * ((T ^ 2 - A ^ 2 * X - B ^ 2 * Y) + 2 * u * v) := by
      ring
    refine ⟨hT, hS, ?_⟩
    nlinarith
  · rintro ⟨hT, hS, hcross⟩
    have hwlt :
        2 * u * v < T ^ 2 - A ^ 2 * X - B ^ 2 * Y := by
      by_contra hnot
      have hge :
          T ^ 2 - A ^ 2 * X - B ^ 2 * Y ≤ 2 * u * v :=
        le_of_not_gt hnot
      have hdiff :
          0 ≤ 2 * u * v - (T ^ 2 - A ^ 2 * X - B ^ 2 * Y) :=
        sub_nonneg.mpr hge
      have hsum :
          0 ≤ 2 * u * v + (T ^ 2 - A ^ 2 * X - B ^ 2 * Y) := by
        nlinarith
      have hprod :
          0 ≤ (2 * u * v - (T ^ 2 - A ^ 2 * X - B ^ 2 * Y))
            * (2 * u * v + (T ^ 2 - A ^ 2 * X - B ^ 2 * Y)) :=
        mul_nonneg hdiff hsum
      have hid :
          (2 * u * v) ^ 2 - (T ^ 2 - A ^ 2 * X - B ^ 2 * Y) ^ 2
            = (2 * u * v - (T ^ 2 - A ^ 2 * X - B ^ 2 * Y))
                * (2 * u * v + (T ^ 2 - A ^ 2 * X - B ^ 2 * Y)) := by
        ring
      nlinarith
    have hsqsum : (u + v) ^ 2 < T ^ 2 := by
      nlinarith
    have hz0 : 0 ≤ u + v := add_nonneg hu0 hv0
    by_contra hnot
    have hge : T ≤ u + v := le_of_not_gt hnot
    have hdiff : 0 ≤ (u + v) - T := sub_nonneg.mpr hge
    have hsum : 0 < (u + v) + T := by nlinarith
    have hprod : 0 ≤ ((u + v) - T) * ((u + v) + T) :=
      mul_nonneg hdiff (le_of_lt hsum)
    have hid :
        (u + v) ^ 2 - T ^ 2 = ((u + v) - T) * ((u + v) + T) := by
      ring
    nlinarith

/-- Exact denominator-cleared E/E branch gate. -/
theorem ee_direct_gate_iff
    (N4 N5 P4 P5 L : ℝ)
    (hP4 : 0 < P4)
    (hP5 : 0 < P5) :
    N4 / P4 + N5 / P5 < L ↔
      N4 * P5 + N5 * P4 < L * P4 * P5 := by
  have hP4ne : P4 ≠ 0 := ne_of_gt hP4
  have hP5ne : P5 ≠ 0 := ne_of_gt hP5
  have hprod : 0 < P4 * P5 := mul_pos hP4 hP5
  have hid :
      (P4 * P5) * (N4 / P4 + N5 / P5 - L)
        = N4 * P5 + N5 * P4 - L * P4 * P5 := by
    field_simp [hP4ne, hP5ne]
    <;> ring
  constructor
  · intro hcost
    have hdiff : N4 / P4 + N5 / P5 - L < 0 := by linarith
    have hmul :
        (P4 * P5) * (N4 / P4 + N5 / P5 - L) < 0 :=
      mul_neg_of_pos_of_neg hprod hdiff
    rw [hid] at hmul
    linarith
  · intro hgate
    have hmul :
        (P4 * P5) * (N4 / P4 + N5 / P5 - L) < 0 := by
      rw [hid]
      linarith
    have hdiff : N4 / P4 + N5 / P5 - L < 0 :=
      (positive_scale_lt_zero_iff (P4 * P5)
        (N4 / P4 + N5 / P5 - L) hprod).mp hmul
    linarith

/-- Algebraic I/E cost-to-scaled-radical bridge. -/
theorem ie_cost_scaled_iff
    (m d D N P L : ℝ)
    (hm : 0 < m)
    (hP : 0 < P) :
    (2 / m) * (Real.sqrt D - d) + N / P < L ↔
      2 * P * Real.sqrt D < 2 * P * d + m * (L * P - N) := by
  have hmne : m ≠ 0 := ne_of_gt hm
  have hPne : P ≠ 0 := ne_of_gt hP
  have hprod : 0 < m * P := mul_pos hm hP
  have hid :
      (m * P) * ((2 / m) * (Real.sqrt D - d) + N / P - L)
        = 2 * P * Real.sqrt D - (2 * P * d + m * (L * P - N)) := by
    field_simp [hmne, hPne]
    <;> ring
  constructor
  · intro hcost
    have hdiff : (2 / m) * (Real.sqrt D - d) + N / P - L < 0 := by
      linarith
    have hmul :
        (m * P) * ((2 / m) * (Real.sqrt D - d) + N / P - L) < 0 :=
      mul_neg_of_pos_of_neg hprod hdiff
    rw [hid] at hmul
    linarith
  · intro hscaled
    have hmul :
        (m * P) * ((2 / m) * (Real.sqrt D - d) + N / P - L) < 0 := by
      rw [hid]
      linarith
    have hdiff : (2 / m) * (Real.sqrt D - d) + N / P - L < 0 :=
      (positive_scale_lt_zero_iff (m * P)
        ((2 / m) * (Real.sqrt D - d) + N / P - L) hprod).mp hmul
    linarith

/-- Algebraic E/I cost-to-scaled-radical bridge. -/
theorem ei_cost_scaled_iff
    (N P m d D L : ℝ)
    (hP : 0 < P)
    (hm : 0 < m) :
    N / P + (2 / m) * (Real.sqrt D - d) < L ↔
      2 * P * Real.sqrt D < 2 * P * d + m * (L * P - N) := by
  simpa [add_comm] using ie_cost_scaled_iff m d D N P L hm hP

/-- Algebraic I/I cost-to-scaled-two-radical bridge. -/
theorem ii_cost_scaled_iff
    (m4 m5 d4 d5 D4 D5 L : ℝ)
    (hm4 : 0 < m4)
    (hm5 : 0 < m5) :
    (2 / m4) * (Real.sqrt D4 - d4)
        + (2 / m5) * (Real.sqrt D5 - d5) < L ↔
      2 * m5 * Real.sqrt D4 + 2 * m4 * Real.sqrt D5
        < L * m4 * m5 + 2 * m5 * d4 + 2 * m4 * d5 := by
  have hm4ne : m4 ≠ 0 := ne_of_gt hm4
  have hm5ne : m5 ≠ 0 := ne_of_gt hm5
  have hprod : 0 < m4 * m5 := mul_pos hm4 hm5
  have hid :
      (m4 * m5)
          * ((2 / m4) * (Real.sqrt D4 - d4)
            + (2 / m5) * (Real.sqrt D5 - d5) - L)
        = 2 * m5 * Real.sqrt D4 + 2 * m4 * Real.sqrt D5
          - (L * m4 * m5 + 2 * m5 * d4 + 2 * m4 * d5) := by
    field_simp [hm4ne, hm5ne]
    <;> ring
  constructor
  · intro hcost
    have hdiff :
        (2 / m4) * (Real.sqrt D4 - d4)
            + (2 / m5) * (Real.sqrt D5 - d5) - L < 0 := by
      linarith
    have hmul :
        (m4 * m5)
            * ((2 / m4) * (Real.sqrt D4 - d4)
              + (2 / m5) * (Real.sqrt D5 - d5) - L) < 0 :=
      mul_neg_of_pos_of_neg hprod hdiff
    rw [hid] at hmul
    linarith
  · intro hscaled
    have hmul :
        (m4 * m5)
            * ((2 / m4) * (Real.sqrt D4 - d4)
              + (2 / m5) * (Real.sqrt D5 - d5) - L) < 0 := by
      rw [hid]
      linarith
    have hdiff :
        (2 / m4) * (Real.sqrt D4 - d4)
            + (2 / m5) * (Real.sqrt D5 - d5) - L < 0 :=
      (positive_scale_lt_zero_iff (m4 * m5)
        ((2 / m4) * (Real.sqrt D4 - d4)
          + (2 / m5) * (Real.sqrt D5 - d5) - L) hprod).mp hmul
    linarith

/-- Review-form I/E gate, with the sign condition that makes squaring reversible. -/
theorem ie_direct_gate_iff
    (m d D N P L : ℝ)
    (hm : 0 < m)
    (hP : 0 < P)
    (hD : 0 ≤ D) :
    (2 / m) * (Real.sqrt D - d) + N / P < L ↔
      0 < 2 * P * d + m * (L * P - N)
        ∧ 4 * P ^ 2 * D < (2 * P * d + m * (L * P - N)) ^ 2 := by
  rw [ie_cost_scaled_iff m d D N P L hm hP]
  constructor
  · intro hscaled
    have hrad :=
      (scaled_sqrt_lt_iff_signed_square
        (2 * P) D (2 * P * d + m * (L * P - N)) (by nlinarith) hD).mp hscaled
    rcases hrad with ⟨hT, hsq⟩
    refine ⟨hT, ?_⟩
    nlinarith
  · rintro ⟨hT, hsq⟩
    apply (scaled_sqrt_lt_iff_signed_square
      (2 * P) D (2 * P * d + m * (L * P - N)) (by nlinarith) hD).mpr
    refine ⟨hT, ?_⟩
    nlinarith

/-- Review-form E/I gate. -/
theorem ei_direct_gate_iff
    (N P m d D L : ℝ)
    (hP : 0 < P)
    (hm : 0 < m)
    (hD : 0 ≤ D) :
    N / P + (2 / m) * (Real.sqrt D - d) < L ↔
      0 < 2 * P * d + m * (L * P - N)
        ∧ 4 * P ^ 2 * D < (2 * P * d + m * (L * P - N)) ^ 2 := by
  rw [ei_cost_scaled_iff N P m d D L hP hm]
  constructor
  · intro hscaled
    have hrad :=
      (scaled_sqrt_lt_iff_signed_square
        (2 * P) D (2 * P * d + m * (L * P - N)) (by nlinarith) hD).mp hscaled
    rcases hrad with ⟨hT, hsq⟩
    refine ⟨hT, ?_⟩
    nlinarith
  · rintro ⟨hT, hsq⟩
    apply (scaled_sqrt_lt_iff_signed_square
      (2 * P) D (2 * P * d + m * (L * P - N)) (by nlinarith) hD).mpr
    refine ⟨hT, ?_⟩
    nlinarith

/--
Review-form I/I gate.  `T>0`, `S>0`, and the strict cross-square condition are
all retained; none may be dropped.
-/
theorem ii_direct_gate_iff
    (m4 m5 d4 d5 D4 D5 L : ℝ)
    (hm4 : 0 < m4)
    (hm5 : 0 < m5)
    (hD4 : 0 ≤ D4)
    (hD5 : 0 ≤ D5) :
    (2 / m4) * (Real.sqrt D4 - d4)
        + (2 / m5) * (Real.sqrt D5 - d5) < L ↔
      0 < L * m4 * m5 + 2 * m5 * d4 + 2 * m4 * d5
        ∧ 0 <
          (L * m4 * m5 + 2 * m5 * d4 + 2 * m4 * d5) ^ 2
            - 4 * m5 ^ 2 * D4 - 4 * m4 ^ 2 * D5
        ∧ 64 * m4 ^ 2 * m5 ^ 2 * D4 * D5
          < ((L * m4 * m5 + 2 * m5 * d4 + 2 * m4 * d5) ^ 2
              - 4 * m5 ^ 2 * D4 - 4 * m4 ^ 2 * D5) ^ 2 := by
  rw [ii_cost_scaled_iff m4 m5 d4 d5 D4 D5 L hm4 hm5]
  let T : ℝ := L * m4 * m5 + 2 * m5 * d4 + 2 * m4 * d5
  change 2 * m5 * Real.sqrt D4 + 2 * m4 * Real.sqrt D5 < T ↔
      0 < T
        ∧ 0 < T ^ 2 - 4 * m5 ^ 2 * D4 - 4 * m4 ^ 2 * D5
        ∧ 64 * m4 ^ 2 * m5 ^ 2 * D4 * D5
          < (T ^ 2 - 4 * m5 ^ 2 * D4 - 4 * m4 ^ 2 * D5) ^ 2
  constructor
  · intro hscaled
    have hraw :=
      (two_scaled_sqrt_lt_iff_signed_square
        (2 * m5) (2 * m4) D4 D5 T (by nlinarith) (by nlinarith) hD4 hD5).mp hscaled
    rcases hraw with ⟨hT, hS, hcross⟩
    refine ⟨hT, ?_, ?_⟩
    · ring_nf at hS ⊢
      exact hS
    · ring_nf at hcross ⊢
      exact hcross
  · rintro ⟨hT, hS, hcross⟩
    apply (two_scaled_sqrt_lt_iff_signed_square
      (2 * m5) (2 * m4) D4 D5 T (by nlinarith) (by nlinarith) hD4 hD5).mpr
    refine ⟨hT, ?_, ?_⟩
    · ring_nf at hS ⊢
      exact hS
    · ring_nf at hcross ⊢
      exact hcross

/-- A failed I/I polynomial gate blocks the corresponding strict branch-cost inequality. -/
theorem ii_gate_fail_blocks_branch_cost
    (m4 m5 d4 d5 D4 D5 L : ℝ)
    (hm4 : 0 < m4)
    (hm5 : 0 < m5)
    (hD4 : 0 ≤ D4)
    (hD5 : 0 ≤ D5)
    (hfail : ¬(
      0 < L * m4 * m5 + 2 * m5 * d4 + 2 * m4 * d5
        ∧ 0 <
          (L * m4 * m5 + 2 * m5 * d4 + 2 * m4 * d5) ^ 2
            - 4 * m5 ^ 2 * D4 - 4 * m4 ^ 2 * D5
        ∧ 64 * m4 ^ 2 * m5 ^ 2 * D4 * D5
          < ((L * m4 * m5 + 2 * m5 * d4 + 2 * m4 * d5) ^ 2
              - 4 * m5 ^ 2 * D4 - 4 * m4 ^ 2 * D5) ^ 2)) :
    ¬((2 / m4) * (Real.sqrt D4 - d4)
        + (2 / m5) * (Real.sqrt D5 - d5) < L) := by
  intro hcost
  apply hfail
  exact (ii_direct_gate_iff m4 m5 d4 d5 D4 D5 L hm4 hm5 hD4 hD5).mp hcost

/-- Exact strict I/I regression from T-P5-043. -/
theorem ii_strict_success_regression :
    let D : ℝ := 13 / 50
    let T : ℝ := 41 / 20
    let S : ℝ := 849 / 400
    0 < T
      ∧ 0 < S
      ∧ 64 * D * D < S ^ 2
      ∧ S ^ 2 - 64 * D * D = 28577 / 160000 := by
  norm_num

/-- Exact boundary-only I/I regression: the final strict gate becomes equality. -/
theorem ii_boundary_regression :
    let D : ℝ := 9 / 25
    let T : ℝ := 12 / 5
    let S : ℝ := 72 / 25
    0 < T
      ∧ 0 < S
      ∧ S ^ 2 = 64 * D * D
      ∧ S ^ 2 = 5184 / 625 := by
  norm_num

/-- Final-square PASS can coexist with `T<0`; the first sign guard is essential. -/
theorem omit_T_positive_guard_counterexample :
    let T : ℝ := -3
    let S : ℝ := T ^ 2 - 1 - 1
    0 < S ∧ 4 < S ^ 2 ∧ ¬ 0 < T := by
  norm_num

/-- Final-square PASS can coexist with `S<0`; the second sign guard is essential. -/
theorem omit_S_positive_guard_counterexample :
    let T : ℝ := 1
    let S : ℝ := T ^ 2 - 100 - 1
    0 < T ∧ 400 < S ^ 2 ∧ ¬ 0 < S := by
  norm_num

#print axioms positive_scale_lt_zero_iff
#print axioms scaled_sqrt_lt_iff_signed_square
#print axioms sqrt_lt_iff_signed_square
#print axioms two_scaled_sqrt_lt_iff_signed_square
#print axioms ee_direct_gate_iff
#print axioms ie_cost_scaled_iff
#print axioms ei_cost_scaled_iff
#print axioms ii_cost_scaled_iff
#print axioms ie_direct_gate_iff
#print axioms ei_direct_gate_iff
#print axioms ii_direct_gate_iff
#print axioms ii_gate_fail_blocks_branch_cost
#print axioms ii_strict_success_regression
#print axioms ii_boundary_regression
#print axioms omit_T_positive_guard_counterexample
#print axioms omit_S_positive_guard_counterexample

end RouteBP5DirectTwoChannelGate
