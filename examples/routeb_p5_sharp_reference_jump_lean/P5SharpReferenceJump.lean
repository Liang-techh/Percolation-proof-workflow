import Mathlib

namespace RouteBP5SharpReferenceJump

noncomputable section

/-- Four scalar slots for the block-expanded storage/action seam.  This keeps the
T-P5-109 coefficient identity independent of a particular Matrix API while
still exposing every component that a later source-binding theorem must match. -/
structure Four where
  x0 : ℝ
  x1 : ℝ
  x2 : ℝ
  x3 : ℝ

/-- Exact T-P5-106 reference direction. -/
def a0 : ℝ := 2340 / 8699
def a1 : ℝ := 1520 / 8699

/-- The jump observable as written from `((K+D)a, M a)`. -/
def jumpObservable : Four where
  x0 := ((3 / 4 : ℝ) + 4 / 5) * a0 + (-3 / 400 : ℝ) * a1
  x1 := (-3 / 400 : ℝ) * a0 + ((29 / 50 : ℝ) + 13 / 20) * a1
  x2 := (350003 / 3000000 : ℝ) * a0
  x3 := (200739 / 4000000 : ℝ) * a1

/-- The same covector obtained by explicitly expanding the block product `P e`
for `P=[[K+D,M],[M,M]]` and `e=(a,0)`. -/
def storageBlockMulDirection : Four where
  x0 := (31 / 20 : ℝ) * a0 + (-3 / 400 : ℝ) * a1
  x1 := (-3 / 400 : ℝ) * a0 + (123 / 100 : ℝ) * a1
  x2 := (350003 / 3000000 : ℝ) * a0
  x3 := (200739 / 4000000 : ℝ) * a1

/-- Exact componentwise representer identity from T-P5-109 section 1.  The
physical/source claim that these are the deployed packet remains outside this
sidecar. -/
theorem reference_jump_observable_eq_storage_mul_direction :
    jumpObservable = storageBlockMulDirection := by
  ext <;> norm_num [jumpObservable, storageBlockMulDirection, a0, a1]

/-- Numerator and denominator of `A=eᵀPe`. -/
def nA : ℝ := 11275620
def dA : ℝ := 75672601

/-- Block-expanded value of `eᵀPe=aᵀ(K+D)a`. -/
def directionEnergy : ℝ :=
  a0 * ((31 / 20 : ℝ) * a0 + (-3 / 400 : ℝ) * a1) +
    a1 * ((-3 / 400 : ℝ) * a0 + (123 / 100 : ℝ) * a1)

theorem reference_jump_direction_energy_exact :
    directionEnergy = nA / dA := by
  norm_num [directionEnergy, a0, a1, nA, dA]

theorem current_nA_nonneg : 0 ≤ nA := by
  norm_num [nA]

theorem current_dA_pos : 0 < dA := by
  norm_num [dA]

/-- The sharp coefficient `2A` is strictly smaller than the old `63/8`
envelope. -/
theorem current_sharp_coefficient_strictly_better_than_old :
    (22551240 / 75672601 : ℝ) < 63 / 8 := by
  norm_num

/-- Exact integer coefficient in the denominator-cleared quadratic gate. -/
theorem current_eight_n_d_exact :
    8 * nA * dA = 6826043946300960 := by
  norm_num [nA, dA]

/-- Algebraic last step of the completed-square representer proof.  A previous
leaf only needs to establish the nonnegativity of
`n * (2*n*V - d*s^2)` from the P-metric square. -/
theorem storage_representer_observable_sq_le
    (n d V s : ℝ)
    (hn : 0 < n)
    (hsquare : 0 ≤ n * (2 * n * V - d * s ^ 2)) :
    d * s ^ 2 ≤ 2 * n * V := by
  nlinarith

/-- If `B≥0` and `t²≤B²`, then `t≤B`.  Keeping this leaf explicit prevents a
squared certificate from silently being interpreted as a signed one. -/
theorem le_of_sq_le_sq_of_nonneg_right
    (t B : ℝ) (hB : 0 ≤ B) (hsq : t ^ 2 ≤ B ^ 2) :
    t ≤ B := by
  by_contra hnot
  have hgt : B < t := lt_of_not_ge hnot
  have hsum : 0 < t + B := by
    nlinarith
  have hprod : 0 < (t - B) * (t + B) :=
    mul_pos (sub_pos.mpr hgt) hsum
  have hid : (t - B) * (t + B) = t ^ 2 - B ^ 2 := by
    ring
  rw [hid] at hprod
  nlinarith

/-- T-P5-109 section 4, sufficient direction, entirely denominator-cleared.
`hobs` is the sharp representer bound and `hjump` is the scaled exact
translation identity.  The two scalar gate hypotheses are exactly (4.5)-(4.6). -/
theorem quadratic_translation_ball_inclusion_sq_gate
    (n d Rin Rout Vin Vplus s Delta : ℝ)
    (hn : 0 ≤ n) (hd : 0 < d)
    (hVinRin : Vin ≤ Rin)
    (hobs : d * s ^ 2 ≤ 2 * n * Vin)
    (hjump :
      2 * d * Vplus =
        2 * d * Vin - 2 * d * Delta * s + n * Delta ^ 2)
    (hB : 0 ≤ 2 * d * (Rout - Rin) - n * Delta ^ 2)
    (hBsq :
      8 * n * d * Rin * Delta ^ 2 ≤
        (2 * d * (Rout - Rin) - n * Delta ^ 2) ^ 2) :
    Vplus ≤ Rout := by
  have h2n : 0 ≤ 2 * n := by
    nlinarith
  have hnr : 2 * n * Vin ≤ 2 * n * Rin := by
    exact mul_le_mul_of_nonneg_left hVinRin h2n
  have hobsR : d * s ^ 2 ≤ 2 * n * Rin := le_trans hobs hnr
  have hd0 : 0 ≤ d := le_of_lt hd
  have hscale : 0 ≤ 4 * d * Delta ^ 2 := by
    exact mul_nonneg (mul_nonneg (by norm_num) hd0) (sq_nonneg Delta)
  have hmul := mul_le_mul_of_nonneg_right hobsR hscale
  have hcross :
      (-2 * d * Delta * s) ^ 2 ≤ 8 * n * d * Rin * Delta ^ 2 := by
    calc
      (-2 * d * Delta * s) ^ 2 =
          (d * s ^ 2) * (4 * d * Delta ^ 2) := by ring
      _ ≤ (2 * n * Rin) * (4 * d * Delta ^ 2) := hmul
      _ = 8 * n * d * Rin * Delta ^ 2 := by ring
  have hcrossB :
      (-2 * d * Delta * s) ^ 2 ≤
        (2 * d * (Rout - Rin) - n * Delta ^ 2) ^ 2 :=
    le_trans hcross hBsq
  have hsigned :
      -2 * d * Delta * s ≤ 2 * d * (Rout - Rin) - n * Delta ^ 2 :=
    le_of_sq_le_sq_of_nonneg_right
      (-2 * d * Delta * s)
      (2 * d * (Rout - Rin) - n * Delta ^ 2) hB hcrossB
  have h2d : 0 ≤ 2 * d := by
    positivity
  have hVinScaled : 2 * d * Vin ≤ 2 * d * Rin := by
    exact mul_le_mul_of_nonneg_left hVinRin h2d
  have hscaled : 2 * d * Vplus ≤ 2 * d * Rout := by
    nlinarith [hjump, hsigned, hVinScaled]
  have hfactor : 0 < 2 * d := by
    positivity
  exact (mul_le_mul_left hfactor).mp hscaled

/-- Current exact-rational specialization of the section-4 consumer. -/
theorem current_reference_jump_gate
    (Rin Rout Vin Vplus s Delta : ℝ)
    (hVinRin : Vin ≤ Rin)
    (hobs : dA * s ^ 2 ≤ 2 * nA * Vin)
    (hjump :
      2 * dA * Vplus =
        2 * dA * Vin - 2 * dA * Delta * s + nA * Delta ^ 2)
    (hB : 0 ≤ 2 * dA * (Rout - Rin) - nA * Delta ^ 2)
    (hBsq :
      8 * nA * dA * Rin * Delta ^ 2 ≤
        (2 * dA * (Rout - Rin) - nA * Delta ^ 2) ^ 2) :
    Vplus ≤ Rout := by
  exact quadratic_translation_ball_inclusion_sq_gate
    nA dA Rin Rout Vin Vplus s Delta
    current_nA_nonneg current_dA_pos hVinRin hobs hjump hB hBsq

/-- T-P5-109 section 5, direct dwell-then-jump composition with a rational decay
factor represented by `U/Vden`.  `hpre` is already denominator-cleared, so the
trusted consumer performs no division or square-root operation. -/
theorem reference_dwell_jump_direct_gate
    (n d U Vden R0 H Vin Vplus s Delta : ℝ)
    (hn : 0 ≤ n) (hd : 0 < d) (hVden : 0 < Vden)
    (hpre : Vden * Vin ≤ Vden * R0 + U * H)
    (hobs : d * s ^ 2 ≤ 2 * n * Vin)
    (hjump :
      2 * d * Vplus =
        2 * d * Vin - 2 * d * Delta * s + n * Delta ^ 2)
    (hB :
      0 ≤ 2 * d * (Vden - U) * H - n * Vden * Delta ^ 2)
    (hBsq :
      8 * n * d * Vden * Delta ^ 2 * (Vden * R0 + U * H) ≤
        (2 * d * (Vden - U) * H - n * Vden * Delta ^ 2) ^ 2) :
    Vplus ≤ R0 + H := by
  have hV0 : 0 ≤ Vden := le_of_lt hVden
  have hobsVraw := mul_le_mul_of_nonneg_left hobs hV0
  have hobsV : d * Vden * s ^ 2 ≤ 2 * n * (Vden * Vin) := by
    calc
      d * Vden * s ^ 2 = Vden * (d * s ^ 2) := by ring
      _ ≤ Vden * (2 * n * Vin) := hobsVraw
      _ = 2 * n * (Vden * Vin) := by ring
  have h2n : 0 ≤ 2 * n := by
    nlinarith
  have hpreN := mul_le_mul_of_nonneg_left hpre h2n
  have hobsPre :
      d * Vden * s ^ 2 ≤ 2 * n * (Vden * R0 + U * H) :=
    le_trans hobsV hpreN
  have hd0 : 0 ≤ d := le_of_lt hd
  have hscale : 0 ≤ 4 * d * Vden * Delta ^ 2 := by
    exact mul_nonneg
      (mul_nonneg (mul_nonneg (by norm_num) hd0) hV0)
      (sq_nonneg Delta)
  have hmul := mul_le_mul_of_nonneg_right hobsPre hscale
  have hcross :
      (-2 * d * Vden * Delta * s) ^ 2 ≤
        8 * n * d * Vden * Delta ^ 2 * (Vden * R0 + U * H) := by
    calc
      (-2 * d * Vden * Delta * s) ^ 2 =
          (d * Vden * s ^ 2) * (4 * d * Vden * Delta ^ 2) := by ring
      _ ≤ (2 * n * (Vden * R0 + U * H)) *
          (4 * d * Vden * Delta ^ 2) := hmul
      _ = 8 * n * d * Vden * Delta ^ 2 * (Vden * R0 + U * H) := by ring
  have hcrossB :
      (-2 * d * Vden * Delta * s) ^ 2 ≤
        (2 * d * (Vden - U) * H - n * Vden * Delta ^ 2) ^ 2 :=
    le_trans hcross hBsq
  have hsigned :
      -2 * d * Vden * Delta * s ≤
        2 * d * (Vden - U) * H - n * Vden * Delta ^ 2 :=
    le_of_sq_le_sq_of_nonneg_right
      (-2 * d * Vden * Delta * s)
      (2 * d * (Vden - U) * H - n * Vden * Delta ^ 2) hB hcrossB
  have hjumpV :
      2 * d * Vden * Vplus =
        2 * d * Vden * Vin - 2 * d * Vden * Delta * s +
          n * Vden * Delta ^ 2 := by
    calc
      2 * d * Vden * Vplus = Vden * (2 * d * Vplus) := by ring
      _ = Vden *
          (2 * d * Vin - 2 * d * Delta * s + n * Delta ^ 2) := by
            rw [hjump]
      _ = 2 * d * Vden * Vin - 2 * d * Vden * Delta * s +
          n * Vden * Delta ^ 2 := by ring
  have h2d : 0 ≤ 2 * d := by
    positivity
  have hpre2d := mul_le_mul_of_nonneg_left hpre h2d
  have hscaled :
      2 * d * Vden * Vplus ≤ 2 * d * Vden * (R0 + H) := by
    nlinarith [hjumpV, hsigned, hpre2d]
  have hfactor : 0 < 2 * d * Vden := by
    positivity
  exact (mul_le_mul_left hfactor).mp hscaled

/-- The concrete rational packet from T-P5-109 section 6 passes the direct
contracted-ellipsoid square gate.  This is arithmetic regression evidence only. -/
theorem direct_contracted_packet_strict_margin :
    let delta : ℝ := 31 / 50
    let B : ℝ := dA - nA * delta ^ 2
    0 < B ∧ 12 * nA * dA * delta ^ 2 < B ^ 2 := by
  norm_num [nA, dA]

/-- The same jump fails the sharp outer-collar prebudget test.  Thus the direct
flow-then-jump composition is strictly stronger on this exact rational packet. -/
theorem outer_collar_prebudget_fails_same_packet :
    let delta : ℝ := 31 / 50
    let B : ℝ := dA - nA * delta ^ 2
    B ^ 2 < 16 * nA * dA * delta ^ 2 := by
  norm_num [nA, dA]

/-- Equality of the scalar gate is boundary-only, not strict inward reserve. -/
theorem boundary_gate_equality_regression :
    let n : ℝ := 1
    let d : ℝ := 1
    let Rin : ℝ := 1 / 2
    let Rout : ℝ := 2
    let Vin : ℝ := 1 / 2
    let Vplus : ℝ := 2
    let s : ℝ := -1
    let Delta : ℝ := 1
    d * s ^ 2 = 2 * n * Vin ∧
      2 * d * Vplus =
        2 * d * Vin - 2 * d * Delta * s + n * Delta ^ 2 ∧
      (2 * d * (Rout - Rin) - n * Delta ^ 2) ^ 2 =
        8 * n * d * Rin * Delta ^ 2 ∧
      Vplus = Rout := by
  norm_num

#print axioms reference_jump_observable_eq_storage_mul_direction
#print axioms reference_jump_direction_energy_exact
#print axioms current_sharp_coefficient_strictly_better_than_old
#print axioms current_eight_n_d_exact
#print axioms storage_representer_observable_sq_le
#print axioms le_of_sq_le_sq_of_nonneg_right
#print axioms quadratic_translation_ball_inclusion_sq_gate
#print axioms current_reference_jump_gate
#print axioms reference_dwell_jump_direct_gate
#print axioms direct_contracted_packet_strict_margin
#print axioms outer_collar_prebudget_fails_same_packet
#print axioms boundary_gate_equality_regression

end

end RouteBP5SharpReferenceJump
