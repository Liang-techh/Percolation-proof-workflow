import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# Route-B P5 correlated matrix perturbation bridge

Formalizes the source-independent mathematics from
`review-T-P5-054-correlated-matrix-perturbation-liuguanyi-20260908T0013.md`.

The sidecar keeps the signed 2x2 packet correlated.  It proves exact trace and
determinant transport, a sound entry-radius fallback, exact source-variable to
matrix-error identities/radii, two nominal-reserve consumers, and the rank-one
regression showing why the direct correlated determinant-correction lane must
remain available near singularity.

It does not certify a concrete source split, Taylor/trigonometric enclosure,
Float64/outward rounding, physical cell coverage, P8 flowpipe semantics, or
registry admission.
-/

set_option autoImplicit false

namespace RouteBP5CorrelatedMatrixPerturbation

noncomputable section

/-- Determinant of a symmetric 2x2 packet represented by `(a,m,c)`. -/
def det2 (a m c : ℝ) : ℝ := a * c - m ^ 2

/-- Trace of a symmetric 2x2 packet represented by `(a,m,c)`. -/
def trace2 (a c : ℝ) : ℝ := a + c

/-- Exact determinant correction for `[[a,m],[m,c]] + [[e11,e12],[e12,e22]]`. -/
def detCorrection (a m c e11 e12 e22 : ℝ) : ℝ :=
  c * e11 + a * e22 - 2 * m * e12 + e11 * e22 - e12 ^ 2

/-- Sound determinant reserve loss when only independent entry radii are kept. -/
def entryPenalty
    (M11 M12 M22 eta11 eta12 eta22 : ℝ) : ℝ :=
  M22 * eta11 + M11 * eta22 + 2 * M12 * eta12 +
    eta11 * eta22 + eta12 ^ 2

/-- Signed branch-free quadratic energy. -/
def quad (p s sigma x y : ℝ) : ℝ :=
  p * x ^ 2 + sigma * x * y + s * y ^ 2

/-- Signed affine/bias term. -/
def bias (b4 b5 x y : ℝ) : ℝ := b4 * x + b5 * y

/-- First diagonal entry of the branch-free matrix packet. -/
def g11 (kappa p b4 : ℝ) : ℝ := 4 * kappa * p - b4 ^ 2

/-- Signed off-diagonal entry of the branch-free matrix packet. -/
def g12 (kappa sigma b4 b5 : ℝ) : ℝ :=
  2 * kappa * sigma - b4 * b5

/-- Second diagonal entry of the branch-free matrix packet. -/
def g22 (kappa s b5 : ℝ) : ℝ := 4 * kappa * s - b5 ^ 2

/-- Old branch-free trace remainder. -/
def rTrace (kappa p s b4 b5 : ℝ) : ℝ :=
  4 * kappa * (p + s) - (b4 ^ 2 + b5 ^ 2)

/-- Old branch-free determinant remainder in the signed `sigma` convention. -/
def rDet (kappa p s sigma b4 b5 : ℝ) : ℝ :=
  kappa * (4 * p * s - sigma ^ 2) -
    (s * b4 ^ 2 - sigma * b4 * b5 + p * b5 ^ 2)

/-- Exact matrix-packet trace identity. -/
theorem branchfree_packet_trace_identity
    (kappa p s b4 b5 : ℝ) :
    trace2 (g11 kappa p b4) (g22 kappa s b5) =
      rTrace kappa p s b4 b5 := by
  simp [trace2, g11, g22, rTrace]
  ring

/-- Exact cancellation-preserving matrix-packet determinant identity. -/
theorem branchfree_packet_det_identity
    (kappa p s sigma b4 b5 : ℝ) :
    det2 (g11 kappa p b4) (g12 kappa sigma b4 b5) (g22 kappa s b5) =
      4 * kappa * rDet kappa p s sigma b4 b5 := by
  simp [det2, g11, g12, g22, rDet]
  ring

/-- Exact 2x2 determinant update under a correlated symmetric perturbation. -/
theorem det2_add_exact
    (a m c e11 e12 e22 : ℝ) :
    det2 (a + e11) (m + e12) (c + e22) - det2 a m c =
      detCorrection a m c e11 e12 e22 := by
  simp [det2, detCorrection]
  ring

/-- Exact trace update under the same perturbation. -/
theorem trace2_add_exact
    (a c e11 e22 : ℝ) :
    trace2 (a + e11) (c + e22) - trace2 a c = e11 + e22 := by
  simp [trace2]
  ring

/-- Product interval consequence used by the radius fallback. -/
theorem mul_abs_cap
    (x y X Y : ℝ)
    (hX : 0 ≤ X)
    (hx : |x| ≤ X) (hy : |y| ≤ Y) :
    |x * y| ≤ X * Y := by
  rw [abs_mul]
  exact mul_le_mul hx hy (abs_nonneg y) hX

/-- Determinant lower bound from independent nominal/error entry radii. -/
theorem det2_add_lower_of_abs_bounds
    (a m c e11 e12 e22 M11 M12 M22 eta11 eta12 eta22 : ℝ)
    (hM11 : 0 ≤ M11) (hM12 : 0 ≤ M12) (hM22 : 0 ≤ M22)
    (heta11 : 0 ≤ eta11)
    (ha : |a| ≤ M11) (hm : |m| ≤ M12) (hc : |c| ≤ M22)
    (he11 : |e11| ≤ eta11) (he12 : |e12| ≤ eta12)
    (he22 : |e22| ≤ eta22) :
    det2 a m c - entryPenalty M11 M12 M22 eta11 eta12 eta22 ≤
      det2 (a + e11) (m + e12) (c + e22) := by
  have hceAbs : |c * e11| ≤ M22 * eta11 :=
    mul_abs_cap c e11 M22 eta11 hM22 hc he11
  have haeAbs : |a * e22| ≤ M11 * eta22 :=
    mul_abs_cap a e22 M11 eta22 hM11 ha he22
  have hmeAbs : |m * e12| ≤ M12 * eta12 :=
    mul_abs_cap m e12 M12 eta12 hM12 hm he12
  have heeAbs : |e11 * e22| ≤ eta11 * eta22 :=
    mul_abs_cap e11 e22 eta11 eta22 heta11 he11 he22
  have hceLo : -(M22 * eta11) ≤ c * e11 := (abs_le.mp hceAbs).1
  have haeLo : -(M11 * eta22) ≤ a * e22 := (abs_le.mp haeAbs).1
  have hmeHi : m * e12 ≤ M12 * eta12 := (abs_le.mp hmeAbs).2
  have heeLo : -(eta11 * eta22) ≤ e11 * e22 := (abs_le.mp heeAbs).1
  have he12Bounds := abs_le.mp he12
  have hminus : 0 ≤ eta12 - e12 := by linarith
  have hplus : 0 ≤ eta12 + e12 := by linarith
  have hsquare : e12 ^ 2 ≤ eta12 ^ 2 := by
    nlinarith [mul_nonneg hminus hplus]
  have hid := det2_add_exact a m c e11 e12 e22
  simp [entryPenalty, detCorrection] at hid ⊢
  nlinarith

/-- Trace lower bound from independent diagonal error radii. -/
theorem trace2_add_lower_of_abs_bounds
    (a c e11 e22 eta11 eta22 : ℝ)
    (he11 : |e11| ≤ eta11) (he22 : |e22| ≤ eta22) :
    trace2 a c - (eta11 + eta22) ≤
      trace2 (a + e11) (c + e22) := by
  have h11 := (abs_le.mp he11).1
  have h22 := (abs_le.mp he22).1
  simp [trace2] at *
  linarith

/-- Three-term triangle helper, kept explicit for Lean-4.32 portability. -/
theorem abs_sub_sub_le (u v w : ℝ) :
    |u - v - w| ≤ |u| + |v| + |w| := by
  calc
    |u - v - w| ≤ |u - v| + |w| := by
      simpa [sub_eq_add_neg] using (abs_add_le (u - v) (-w))
    _ ≤ (|u| + |v|) + |w| := by
      exact add_le_add
        (by simpa [sub_eq_add_neg] using (abs_add_le u (-v)))
        (le_refl |w|)
    _ = |u| + |v| + |w| := by ring

/-- Four-term triangle helper. -/
theorem abs_sub_sub_sub_le (u v w z : ℝ) :
    |u - v - w - z| ≤ |u| + |v| + |w| + |z| := by
  calc
    |u - v - w - z| ≤ |u - v - w| + |z| := by
      simpa [sub_eq_add_neg] using (abs_add_le (u - v - w) (-z))
    _ ≤ (|u| + |v| + |w|) + |z| := by
      exact add_le_add (abs_sub_sub_le u v w) (le_refl |z|)
    _ = |u| + |v| + |w| + |z| := by ring

/-- Exact source-variable to packet-error entries. -/
theorem branchfree_packet_error_entries
    (kappa phat shat sigmahat b4hat b5hat ep es esigma e4 e5 : ℝ) :
    g11 kappa (phat + ep) (b4hat + e4) - g11 kappa phat b4hat =
        4 * kappa * ep - 2 * b4hat * e4 - e4 ^ 2 ∧
    g22 kappa (shat + es) (b5hat + e5) - g22 kappa shat b5hat =
        4 * kappa * es - 2 * b5hat * e5 - e5 ^ 2 ∧
    g12 kappa (sigmahat + esigma) (b4hat + e4) (b5hat + e5) -
        g12 kappa sigmahat b4hat b5hat =
        2 * kappa * esigma - b4hat * e5 - b5hat * e4 - e4 * e5 := by
  simp [g11, g12, g22]
  constructor
  · ring
  constructor <;> ring

/-- Exact rational entry radii induced from signed source-variable error radii. -/
theorem branchfree_packet_error_abs_bounds
    (kappa b4hat b5hat ep es esigma e4 e5 dp ds dsigma d4 d5 B4 B5 : ℝ)
    (hkappa : 0 ≤ kappa)
    (hd4 : 0 ≤ d4) (hd5 : 0 ≤ d5)
    (hB4 : 0 ≤ B4) (hB5 : 0 ≤ B5)
    (hep : |ep| ≤ dp) (hes : |es| ≤ ds) (hesigma : |esigma| ≤ dsigma)
    (he4 : |e4| ≤ d4) (he5 : |e5| ≤ d5)
    (hb4 : |b4hat| ≤ B4) (hb5 : |b5hat| ≤ B5) :
    |4 * kappa * ep - 2 * b4hat * e4 - e4 ^ 2| ≤
        4 * kappa * dp + 2 * B4 * d4 + d4 ^ 2 ∧
    |4 * kappa * es - 2 * b5hat * e5 - e5 ^ 2| ≤
        4 * kappa * ds + 2 * B5 * d5 + d5 ^ 2 ∧
    |2 * kappa * esigma - b4hat * e5 - b5hat * e4 - e4 * e5| ≤
        2 * kappa * dsigma + B4 * d5 + B5 * d4 + d4 * d5 := by
  have hk4 : 0 ≤ 4 * kappa := by positivity
  have hk2 : 0 ≤ 2 * kappa := by positivity
  have h4ep : |4 * kappa * ep| ≤ 4 * kappa * dp := by
    calc
      |4 * kappa * ep| = (4 * kappa) * |ep| := by
        rw [abs_mul, abs_of_nonneg hk4]
      _ ≤ (4 * kappa) * dp := mul_le_mul_of_nonneg_left hep hk4
  have h4es : |4 * kappa * es| ≤ 4 * kappa * ds := by
    calc
      |4 * kappa * es| = (4 * kappa) * |es| := by
        rw [abs_mul, abs_of_nonneg hk4]
      _ ≤ (4 * kappa) * ds := mul_le_mul_of_nonneg_left hes hk4
  have h2esigma : |2 * kappa * esigma| ≤ 2 * kappa * dsigma := by
    calc
      |2 * kappa * esigma| = (2 * kappa) * |esigma| := by
        rw [abs_mul, abs_of_nonneg hk2]
      _ ≤ (2 * kappa) * dsigma := mul_le_mul_of_nonneg_left hesigma hk2
  have hb4e4 : |b4hat * e4| ≤ B4 * d4 :=
    mul_abs_cap b4hat e4 B4 d4 hB4 hb4 he4
  have hb5e5 : |b5hat * e5| ≤ B5 * d5 :=
    mul_abs_cap b5hat e5 B5 d5 hB5 hb5 he5
  have hb4e5 : |b4hat * e5| ≤ B4 * d5 :=
    mul_abs_cap b4hat e5 B4 d5 hB4 hb4 he5
  have hb5e4 : |b5hat * e4| ≤ B5 * d4 :=
    mul_abs_cap b5hat e4 B5 d4 hB5 hb5 he4
  have he4e5 : |e4 * e5| ≤ d4 * d5 :=
    mul_abs_cap e4 e5 d4 d5 hd4 he4 he5
  have h2b4e4 : |2 * b4hat * e4| ≤ 2 * B4 * d4 := by
    calc
      |2 * b4hat * e4| = 2 * |b4hat * e4| := by
        simp [abs_mul, mul_assoc]
      _ ≤ 2 * (B4 * d4) := mul_le_mul_of_nonneg_left hb4e4 (by norm_num)
      _ = 2 * B4 * d4 := by ring
  have h2b5e5 : |2 * b5hat * e5| ≤ 2 * B5 * d5 := by
    calc
      |2 * b5hat * e5| = 2 * |b5hat * e5| := by
        simp [abs_mul, mul_assoc]
      _ ≤ 2 * (B5 * d5) := mul_le_mul_of_nonneg_left hb5e5 (by norm_num)
      _ = 2 * B5 * d5 := by ring
  have he4sq : |e4 ^ 2| ≤ d4 ^ 2 := by
    have hprod := mul_le_mul he4 he4 (abs_nonneg e4) hd4
    simpa [pow_two, abs_mul] using hprod
  have he5sq : |e5 ^ 2| ≤ d5 ^ 2 := by
    have hprod := mul_le_mul he5 he5 (abs_nonneg e5) hd5
    simpa [pow_two, abs_mul] using hprod
  constructor
  · calc
      |4 * kappa * ep - 2 * b4hat * e4 - e4 ^ 2| ≤
          |4 * kappa * ep| + |2 * b4hat * e4| + |e4 ^ 2| :=
        abs_sub_sub_le _ _ _
      _ ≤ 4 * kappa * dp + 2 * B4 * d4 + d4 ^ 2 := by linarith
  constructor
  · calc
      |4 * kappa * es - 2 * b5hat * e5 - e5 ^ 2| ≤
          |4 * kappa * es| + |2 * b5hat * e5| + |e5 ^ 2| :=
        abs_sub_sub_le _ _ _
      _ ≤ 4 * kappa * ds + 2 * B5 * d5 + d5 ^ 2 := by linarith
  · calc
      |2 * kappa * esigma - b4hat * e5 - b5hat * e4 - e4 * e5| ≤
          |2 * kappa * esigma| + |b4hat * e5| + |b5hat * e4| + |e4 * e5| :=
        abs_sub_sub_sub_le _ _ _ _
      _ ≤ 2 * kappa * dsigma + B4 * d5 + B5 * d4 + d4 * d5 := by linarith

/-- Division-free square completion for a scaled symmetric quadratic form. -/
theorem sym2_scaled_qf_completion_identity
    (a m c x y : ℝ) :
    4 * a * (a * x ^ 2 + m * x * y + c * y ^ 2) =
      (2 * a * x + m * y) ^ 2 + (4 * a * c - m ^ 2) * y ^ 2 := by
  ring

/-- Matrix-free 2x2 PSD consumer from trace and scaled determinant. -/
theorem sym2_scaled_qf_nonneg_of_trace_det4
    (a m c x y : ℝ)
    (htrace : 0 ≤ a + c)
    (hdet : 0 ≤ 4 * a * c - m ^ 2) :
    0 ≤ a * x ^ 2 + m * x * y + c * y ^ 2 := by
  by_cases ha0 : a = 0
  · subst a
    have hm0 : m = 0 := by nlinarith [sq_nonneg m]
    subst m
    have hc0 : 0 ≤ c := by simpa using htrace
    simpa using mul_nonneg hc0 (sq_nonneg y)
  · rcases le_or_gt a 0 with ha_nonpos | ha_pos
    · have ha_neg : a < 0 := lt_of_le_of_ne ha_nonpos ha0
      have hac : 0 ≤ a * c := by nlinarith [sq_nonneg m]
      have hc_nonpos : c ≤ 0 := by
        by_contra hc
        have hc_pos : 0 < c := lt_of_not_ge hc
        have hneg : a * c < 0 := mul_neg_of_neg_of_pos ha_neg hc_pos
        linarith
      nlinarith
    · have hid := sym2_scaled_qf_completion_identity a m c x y
      have htail : 0 ≤ (4 * a * c - m ^ 2) * y ^ 2 :=
        mul_nonneg hdet (sq_nonneg y)
      have hmul : 0 ≤ 4 * a * (a * x ^ 2 + m * x * y + c * y ^ 2) := by
        rw [hid]
        exact add_nonneg (sq_nonneg (2 * a * x + m * y)) htail
      have h4a : 0 < 4 * a := by nlinarith
      by_contra hq
      have hqneg : a * x ^ 2 + m * x * y + c * y ^ 2 < 0 := lt_of_not_ge hq
      have hprodneg : 4 * a * (a * x ^ 2 + m * x * y + c * y ^ 2) < 0 :=
        mul_neg_of_pos_of_neg h4a hqneg
      linarith

/-- Exact affine completion using the branch-free packet entries. -/
theorem affine_packet_identity
    (kappa p s sigma b4 b5 x y : ℝ) :
    4 * kappa * (quad p s sigma x y + bias b4 b5 x y + kappa) =
      g11 kappa p b4 * x ^ 2 +
      (2 * g12 kappa sigma b4 b5) * x * y +
      g22 kappa s b5 * y ^ 2 +
      (bias b4 b5 x y + 2 * kappa) ^ 2 := by
  simp [quad, bias, g11, g12, g22]
  ring

/-- Consume nonnegative trace/determinant of the actual packet. -/
theorem affine_energy_le_of_packet_trace_det
    (kappa p s sigma b4 b5 x y : ℝ)
    (hkappa : 0 < kappa)
    (htrace : 0 ≤ trace2 (g11 kappa p b4) (g22 kappa s b5))
    (hdet : 0 ≤ det2 (g11 kappa p b4) (g12 kappa sigma b4 b5) (g22 kappa s b5)) :
    -quad p s sigma x y - bias b4 b5 x y ≤ kappa := by
  have htrace' : 0 ≤ g11 kappa p b4 + g22 kappa s b5 := by
    simpa [trace2] using htrace
  have hdet4 :
      0 ≤ 4 * g11 kappa p b4 * g22 kappa s b5 -
        (2 * g12 kappa sigma b4 b5) ^ 2 := by
    simp [det2] at hdet
    nlinarith
  have hG :=
    sym2_scaled_qf_nonneg_of_trace_det4
      (g11 kappa p b4) (2 * g12 kappa sigma b4 b5) (g22 kappa s b5)
      x y htrace' hdet4
  have hid := affine_packet_identity kappa p s sigma b4 b5 x y
  have hmul : 0 ≤ 4 * kappa * (quad p s sigma x y + bias b4 b5 x y + kappa) := by
    rw [hid]
    exact add_nonneg hG (sq_nonneg (bias b4 b5 x y + 2 * kappa))
  have h4k : 0 < 4 * kappa := by nlinarith
  by_contra hgoal
  have hsumneg : quad p s sigma x y + bias b4 b5 x y + kappa < 0 := by
    nlinarith
  have hprodneg : 4 * kappa * (quad p s sigma x y + bias b4 b5 x y + kappa) < 0 :=
    mul_neg_of_pos_of_neg h4k hsumneg
  linarith

/-- Preferred correlated reserve consumer.  All nominal/error data are composed
at one call site, so the caller cannot mix different source/cell keys. -/
theorem branchfree_of_nominal_correlated_reserve
    (kappa p s sigma b4 b5 a m c e11 e12 e22
      Treserve Dreserve Tloss Dloss x y : ℝ)
    (hkappa : 0 < kappa)
    (hg11 : g11 kappa p b4 = a + e11)
    (hg12 : g12 kappa sigma b4 b5 = m + e12)
    (hg22 : g22 kappa s b5 = c + e22)
    (hNomTrace : Treserve ≤ trace2 a c)
    (hNomDet : Dreserve ≤ det2 a m c)
    (hTraceCorrection : -Tloss ≤ e11 + e22)
    (hDetCorrection : -Dloss ≤ detCorrection a m c e11 e12 e22)
    (hTraceReserve : Tloss ≤ Treserve)
    (hDetReserve : Dloss ≤ Dreserve) :
    -quad p s sigma x y - bias b4 b5 x y ≤ kappa := by
  have hActualTrace0 : 0 ≤ trace2 (a + e11) (c + e22) := by
    simp [trace2] at *
    linarith
  have hid := det2_add_exact a m c e11 e12 e22
  have hActualDet0 : 0 ≤ det2 (a + e11) (m + e12) (c + e22) := by
    nlinarith
  apply affine_energy_le_of_packet_trace_det kappa p s sigma b4 b5 x y hkappa
  · rw [hg11, hg22]
    exact hActualTrace0
  · rw [hg11, hg12, hg22]
    exact hActualDet0

/-- Fallback reserve consumer using only independent entry radii. -/
theorem branchfree_of_nominal_entry_radius_reserve
    (kappa p s sigma b4 b5 a m c e11 e12 e22
      Treserve Dreserve M11 M12 M22 eta11 eta12 eta22 x y : ℝ)
    (hkappa : 0 < kappa)
    (hg11 : g11 kappa p b4 = a + e11)
    (hg12 : g12 kappa sigma b4 b5 = m + e12)
    (hg22 : g22 kappa s b5 = c + e22)
    (hNomTrace : Treserve ≤ trace2 a c)
    (hNomDet : Dreserve ≤ det2 a m c)
    (hM11 : 0 ≤ M11) (hM12 : 0 ≤ M12) (hM22 : 0 ≤ M22)
    (heta11 : 0 ≤ eta11)
    (ha : |a| ≤ M11) (hm : |m| ≤ M12) (hc : |c| ≤ M22)
    (he11 : |e11| ≤ eta11) (he12 : |e12| ≤ eta12)
    (he22 : |e22| ≤ eta22)
    (hTraceReserve : eta11 + eta22 ≤ Treserve)
    (hDetReserve : entryPenalty M11 M12 M22 eta11 eta12 eta22 ≤ Dreserve) :
    -quad p s sigma x y - bias b4 b5 x y ≤ kappa := by
  have htr := trace2_add_lower_of_abs_bounds a c e11 e22 eta11 eta22 he11 he22
  have hActualTrace0 : 0 ≤ trace2 (a + e11) (c + e22) := by linarith
  have hdet :=
    det2_add_lower_of_abs_bounds
      a m c e11 e12 e22 M11 M12 M22 eta11 eta12 eta22
      hM11 hM12 hM22 heta11 ha hm hc he11 he12 he22
  have hActualDet0 : 0 ≤ det2 (a + e11) (m + e12) (c + e22) := by linarith
  apply affine_energy_le_of_packet_trace_det kappa p s sigma b4 b5 x y hkappa
  · rw [hg11, hg22]
    exact hActualTrace0
  · rw [hg11, hg12, hg22]
    exact hActualDet0

/-- Rank-one family: the exact correlated determinant correction is identically zero. -/
theorem rank_one_correlated_error_regression
    (t : ℝ) :
    det2 1 t (t ^ 2) = 0 ∧
    detCorrection 1 0 0 0 t (t ^ 2) = 0 := by
  simp [det2, detCorrection]

/-- Independent entry radii lose `2*eps^2` determinant reserve on the same family. -/
theorem rank_one_entry_radius_penalty
    (eps : ℝ) :
    entryPenalty 1 0 0 0 eps (eps ^ 2) = 2 * eps ^ 2 := by
  simp [entryPenalty]
  ring

#print axioms branchfree_packet_trace_identity
#print axioms branchfree_packet_det_identity
#print axioms det2_add_exact
#print axioms trace2_add_exact
#print axioms mul_abs_cap
#print axioms det2_add_lower_of_abs_bounds
#print axioms trace2_add_lower_of_abs_bounds
#print axioms abs_sub_sub_le
#print axioms abs_sub_sub_sub_le
#print axioms branchfree_packet_error_entries
#print axioms branchfree_packet_error_abs_bounds
#print axioms sym2_scaled_qf_completion_identity
#print axioms sym2_scaled_qf_nonneg_of_trace_det4
#print axioms affine_packet_identity
#print axioms affine_energy_le_of_packet_trace_det
#print axioms branchfree_of_nominal_correlated_reserve
#print axioms branchfree_of_nominal_entry_radius_reserve
#print axioms rank_one_correlated_error_regression
#print axioms rank_one_entry_radius_penalty

end

end RouteBP5CorrelatedMatrixPerturbation