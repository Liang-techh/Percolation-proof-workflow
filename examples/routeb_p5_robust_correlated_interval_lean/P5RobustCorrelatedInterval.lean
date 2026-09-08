import Mathlib

noncomputable section

namespace RouteBP5RobustCorrelatedInterval

/-- Scaled determinant of the symmetric two-channel reserve. -/
def scaledDet (p s sigma : ℝ) : ℝ := 4 * p * s - sigma ^ 2

/-- Scaled adjugate bias seen by the correlated Lyapunov completion. -/
def scaledBias (p s sigma b4 b5 : ℝ) : ℝ :=
  s * b4 ^ 2 - sigma * b4 * b5 + p * b5 ^ 2

/-- Cellwise rational lower determinant certificate. -/
def detLower (pL sL Q : ℝ) : ℝ := 4 * pL * sL - Q ^ 2

/-- Independent component-box upper bound for the scaled adjugate bias. -/
def boxBias (pU sU Q beta4 beta5 : ℝ) : ℝ :=
  sU * beta4 ^ 2 + Q * beta4 * beta5 + pU * beta5 ^ 2

/--
The source-facing scaled coordinates are exactly the unscaled `q = sigma/2`
coordinates of T-P5-044, but with all `/2` and `/4` factors cleared.
-/
theorem scaled_correlated_invariants
    (p s sigma b4 b5 : ℝ) :
    4 * (p * s - (sigma / 2) ^ 2) = scaledDet p s sigma ∧
      s * b4 ^ 2 - 2 * (sigma / 2) * b4 * b5 + p * b5 ^ 2 =
        scaledBias p s sigma b4 b5 := by
  constructor <;> dsimp [scaledDet, scaledBias] <;> ring

/--
A signed interval enclosure of `sigma` and one positive lower determinant are
enough to certify positivity of both diagonal reserves and the pointwise scaled
determinant.  No separate `sL > 0` premise is required.
-/
theorem scaled_symmetric_det_lower_of_interval
    (pL sL Q p s sigma : ℝ)
    (hpL : 0 < pL)
    (hDmin : 0 < detLower pL sL Q)
    (hp : pL ≤ p)
    (hs : sL ≤ s)
    (hsigmaL : -Q ≤ sigma)
    (hsigmaU : sigma ≤ Q) :
    0 < p ∧ 0 < s ∧ detLower pL sL Q ≤ scaledDet p s sigma := by
  have hQ : 0 ≤ Q := by linarith
  have hsLpos : 0 < sL := by
    by_contra hnot
    have hsLnonpos : sL ≤ 0 := le_of_not_gt hnot
    have hmul : pL * sL ≤ 0 :=
      mul_nonpos_of_nonneg_of_nonpos (le_of_lt hpL) hsLnonpos
    dsimp [detLower] at hDmin
    nlinarith [sq_nonneg Q]
  have hppos : 0 < p := lt_of_lt_of_le hpL hp
  have hspos : 0 < s := lt_of_lt_of_le hsLpos hs
  have hps : pL * sL ≤ p * s :=
    mul_le_mul hp hs (le_of_lt hsLpos) (le_of_lt hppos)
  have hleft : 0 ≤ Q - sigma := sub_nonneg.mpr hsigmaU
  have hright : 0 ≤ Q + sigma := by linarith
  have hprod : 0 ≤ (Q - sigma) * (Q + sigma) := mul_nonneg hleft hright
  have hsigmaSq : sigma ^ 2 ≤ Q ^ 2 := by nlinarith
  constructor
  · exact hppos
  constructor
  · exact hspos
  · dsimp [detLower, scaledDet]
    nlinarith

/--
Box bound for the correlated adjugate bias.  The crucial cross premise is a
single signed-sum cap `|sigma| ≤ Q`; no separate absolute bounds on `k45` and
`k54` occur in this theorem.
-/
theorem scaled_adjugate_bias_le_box
    (p s sigma b4 b5 pU sU Q beta4 beta5 : ℝ)
    (hp0 : 0 ≤ p)
    (hs0 : 0 ≤ s)
    (hpU : p ≤ pU)
    (hsU : s ≤ sU)
    (hsigma : |sigma| ≤ Q)
    (hb4 : |b4| ≤ beta4)
    (hb5 : |b5| ≤ beta5)
    (hbeta4 : 0 ≤ beta4) :
    scaledBias p s sigma b4 b5 ≤ boxBias pU sU Q beta4 beta5 := by
  have hQ : 0 ≤ Q := le_trans (abs_nonneg sigma) hsigma
  have hpU0 : 0 ≤ pU := le_trans hp0 hpU
  have hsU0 : 0 ≤ sU := le_trans hs0 hsU

  have hb4parts := abs_le.mp hb4
  have hb4prod : 0 ≤ (beta4 - b4) * (beta4 + b4) := by
    apply mul_nonneg
    · exact sub_nonneg.mpr hb4parts.2
    · linarith [hb4parts.1]
  have hb4sq : b4 ^ 2 ≤ beta4 ^ 2 := by nlinarith

  have hb5parts := abs_le.mp hb5
  have hb5prod : 0 ≤ (beta5 - b5) * (beta5 + b5) := by
    apply mul_nonneg
    · exact sub_nonneg.mpr hb5parts.2
    · linarith [hb5parts.1]
  have hb5sq : b5 ^ 2 ≤ beta5 ^ 2 := by nlinarith

  have hdiag4a : s * b4 ^ 2 ≤ sU * b4 ^ 2 :=
    mul_le_mul_of_nonneg_right hsU (sq_nonneg b4)
  have hdiag4b : sU * b4 ^ 2 ≤ sU * beta4 ^ 2 :=
    mul_le_mul_of_nonneg_left hb4sq hsU0
  have hdiag4 : s * b4 ^ 2 ≤ sU * beta4 ^ 2 := le_trans hdiag4a hdiag4b

  have hdiag5a : p * b5 ^ 2 ≤ pU * b5 ^ 2 :=
    mul_le_mul_of_nonneg_right hpU (sq_nonneg b5)
  have hdiag5b : pU * b5 ^ 2 ≤ pU * beta5 ^ 2 :=
    mul_le_mul_of_nonneg_left hb5sq hpU0
  have hdiag5 : p * b5 ^ 2 ≤ pU * beta5 ^ 2 := le_trans hdiag5a hdiag5b

  have hsigmaB4 : |sigma| * |b4| ≤ Q * beta4 :=
    mul_le_mul hsigma hb4 (abs_nonneg b4) hQ
  have hsigmaB4B5 : |sigma| * |b4| * |b5| ≤ Q * beta4 * beta5 :=
    mul_le_mul hsigmaB4 hb5 (abs_nonneg b5) (mul_nonneg hQ hbeta4)
  have hcross : -sigma * b4 * b5 ≤ Q * beta4 * beta5 := by
    calc
      -sigma * b4 * b5 = -(sigma * b4 * b5) := by ring
      _ ≤ |sigma * b4 * b5| := neg_le_abs (sigma * b4 * b5)
      _ = |sigma| * |b4| * |b5| := by simp [abs_mul]
      _ ≤ Q * beta4 * beta5 := hsigmaB4B5

  dsimp [scaledBias, boxBias]
  linarith

/--
Tighter bias theorem for a source that can certify the correlated cross term
directly instead of falling back to `Q * beta4 * beta5`.
-/
theorem scaled_adjugate_bias_le_cross_cap
    (p s sigma b4 b5 pU sU beta4 beta5 chi : ℝ)
    (hp0 : 0 ≤ p)
    (hs0 : 0 ≤ s)
    (hpU : p ≤ pU)
    (hsU : s ≤ sU)
    (hb4 : |b4| ≤ beta4)
    (hb5 : |b5| ≤ beta5)
    (hcross : -sigma * b4 * b5 ≤ chi) :
    scaledBias p s sigma b4 b5 ≤
      sU * beta4 ^ 2 + chi + pU * beta5 ^ 2 := by
  have hpU0 : 0 ≤ pU := le_trans hp0 hpU
  have hsU0 : 0 ≤ sU := le_trans hs0 hsU

  have hb4parts := abs_le.mp hb4
  have hb4prod : 0 ≤ (beta4 - b4) * (beta4 + b4) := by
    apply mul_nonneg
    · exact sub_nonneg.mpr hb4parts.2
    · linarith [hb4parts.1]
  have hb4sq : b4 ^ 2 ≤ beta4 ^ 2 := by nlinarith

  have hb5parts := abs_le.mp hb5
  have hb5prod : 0 ≤ (beta5 - b5) * (beta5 + b5) := by
    apply mul_nonneg
    · exact sub_nonneg.mpr hb5parts.2
    · linarith [hb5parts.1]
  have hb5sq : b5 ^ 2 ≤ beta5 ^ 2 := by nlinarith

  have hdiag4a : s * b4 ^ 2 ≤ sU * b4 ^ 2 :=
    mul_le_mul_of_nonneg_right hsU (sq_nonneg b4)
  have hdiag4b : sU * b4 ^ 2 ≤ sU * beta4 ^ 2 :=
    mul_le_mul_of_nonneg_left hb4sq hsU0
  have hdiag4 : s * b4 ^ 2 ≤ sU * beta4 ^ 2 := le_trans hdiag4a hdiag4b

  have hdiag5a : p * b5 ^ 2 ≤ pU * b5 ^ 2 :=
    mul_le_mul_of_nonneg_right hpU (sq_nonneg b5)
  have hdiag5b : pU * b5 ^ 2 ≤ pU * beta5 ^ 2 :=
    mul_le_mul_of_nonneg_left hb5sq hpU0
  have hdiag5 : p * b5 ^ 2 ≤ pU * beta5 ^ 2 := le_trans hdiag5a hdiag5b

  dsimp [scaledBias]
  linarith

/--
Transport a robust cellwise determinant/bias certificate into the exact
T-P5-044 quarter-barrier gate.
-/
theorem correlated_quarter_gate_of_interval_box
    (r rU B Ebox D4 Dmin : ℝ)
    (hB : B ≤ Ebox)
    (hD : Dmin ≤ D4)
    (hDpos : 0 < Dmin)
    (hr : r ≤ rU)
    (hrU : rU < 109)
    (hgate : 800 * Ebox < (109 - rU) * Dmin) :
    800 * B < (109 - r) * D4 := by
  have hcoef : 109 - rU ≤ 109 - r := by linarith
  have hcoefNonneg : 0 ≤ 109 - r := by linarith
  have hstep1 : (109 - rU) * Dmin ≤ (109 - r) * Dmin :=
    mul_le_mul_of_nonneg_right hcoef (le_of_lt hDpos)
  have hstep2 : (109 - r) * Dmin ≤ (109 - r) * D4 :=
    mul_le_mul_of_nonneg_left hD hcoefNonneg
  nlinarith

/-- Same interval transport for the one-twelfth parameter/incremental tube gate. -/
theorem correlated_one_twelfth_parameter_gate_of_interval_box
    (r rU G Eg D4 Dmin : ℝ)
    (hG : G ≤ Eg)
    (hD : Dmin ≤ D4)
    (hDpos : 0 < Dmin)
    (hr : r ≤ rU)
    (hrU : rU < 109)
    (hgate : 2400 * Eg < (109 - rU) * Dmin) :
    2400 * G < (109 - r) * D4 := by
  have hcoef : 109 - rU ≤ 109 - r := by linarith
  have hcoefNonneg : 0 ≤ 109 - r := by linarith
  have hstep1 : (109 - rU) * Dmin ≤ (109 - r) * Dmin :=
    mul_le_mul_of_nonneg_right hcoef (le_of_lt hDpos)
  have hstep2 : (109 - r) * Dmin ≤ (109 - r) * D4 :=
    mul_le_mul_of_nonneg_left hD hcoefNonneg
  nlinarith

/--
End-to-end source-facing quarter gate: signed interval determinant plus the
independent component-box bias cap imply the pointwise correlated gate.
-/
theorem correlated_quarter_gate_from_cell_box
    (r rU pL sL Q p s sigma pU sU b4 b5 beta4 beta5 : ℝ)
    (hpL : 0 < pL)
    (hDmin : 0 < detLower pL sL Q)
    (hpLpoint : pL ≤ p)
    (hsLpoint : sL ≤ s)
    (hsigmaL : -Q ≤ sigma)
    (hsigmaU : sigma ≤ Q)
    (hpU : p ≤ pU)
    (hsU : s ≤ sU)
    (hb4 : |b4| ≤ beta4)
    (hb5 : |b5| ≤ beta5)
    (hbeta4 : 0 ≤ beta4)
    (hr : r ≤ rU)
    (hrU : rU < 109)
    (hgate :
      800 * boxBias pU sU Q beta4 beta5 <
        (109 - rU) * detLower pL sL Q) :
    800 * scaledBias p s sigma b4 b5 <
      (109 - r) * scaledDet p s sigma := by
  obtain ⟨hppos, hspos, hdet⟩ :=
    scaled_symmetric_det_lower_of_interval pL sL Q p s sigma
      hpL hDmin hpLpoint hsLpoint hsigmaL hsigmaU
  have hsigmaAbs : |sigma| ≤ Q := abs_le.mpr ⟨hsigmaL, hsigmaU⟩
  have hbias :=
    scaled_adjugate_bias_le_box p s sigma b4 b5 pU sU Q beta4 beta5
      (le_of_lt hppos) (le_of_lt hspos) hpU hsU hsigmaAbs hb4 hb5 hbeta4
  exact correlated_quarter_gate_of_interval_box
    r rU (scaledBias p s sigma b4 b5) (boxBias pU sU Q beta4 beta5)
      (scaledDet p s sigma) (detLower pL sL Q)
      hbias hdet hDmin hr hrU hgate

/-- Global `r ∈ (-∞,1]` simplification of the quarter gate: `200 E < 27 Dmin`. -/
theorem correlated_quarter_gate_global_r
    (r B Ebox D4 Dmin : ℝ)
    (hB : B ≤ Ebox)
    (hD : Dmin ≤ D4)
    (hDpos : 0 < Dmin)
    (hr : r ≤ 1)
    (hgate : 200 * Ebox < 27 * Dmin) :
    800 * B < (109 - r) * D4 := by
  have hscaled : 800 * Ebox < (109 - (1 : ℝ)) * Dmin := by
    norm_num
    nlinarith
  exact correlated_quarter_gate_of_interval_box
    r 1 B Ebox D4 Dmin hB hD hDpos hr (by norm_num) hscaled

/-- Global `r ∈ (-∞,1]` simplification of the one-twelfth gate: `200 E < 9 Dmin`. -/
theorem correlated_one_twelfth_parameter_gate_global_r
    (r G Eg D4 Dmin : ℝ)
    (hG : G ≤ Eg)
    (hD : Dmin ≤ D4)
    (hDpos : 0 < Dmin)
    (hr : r ≤ 1)
    (hgate : 200 * Eg < 9 * Dmin) :
    2400 * G < (109 - r) * D4 := by
  have hscaled : 2400 * Eg < (109 - (1 : ℝ)) * Dmin := by
    norm_num
    nlinarith
  exact correlated_one_twelfth_parameter_gate_of_interval_box
    r 1 G Eg D4 Dmin hG hD hDpos hr (by norm_num) hscaled

/-- Exact skew family: the antisymmetric off-diagonal part disappears before enclosure. -/
theorem skew_family_scaled_det_independent
    (p s M : ℝ) : scaledDet p s (M + (-M)) = 4 * p * s := by
  dsimp [scaledDet]
  ring

#print axioms scaled_correlated_invariants
#print axioms scaled_symmetric_det_lower_of_interval
#print axioms scaled_adjugate_bias_le_box
#print axioms scaled_adjugate_bias_le_cross_cap
#print axioms correlated_quarter_gate_of_interval_box
#print axioms correlated_one_twelfth_parameter_gate_of_interval_box
#print axioms correlated_quarter_gate_from_cell_box
#print axioms correlated_quarter_gate_global_r
#print axioms correlated_one_twelfth_parameter_gate_global_r
#print axioms skew_family_scaled_det_independent

end RouteBP5RobustCorrelatedInterval
