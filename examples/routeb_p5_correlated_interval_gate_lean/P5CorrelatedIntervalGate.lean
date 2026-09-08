import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# Route-B P5 signed-symmetric correlated interval gate sidecar

Source-independent Lean decomposition of
`agent_review_inbox/review-T-P5-045-liuguanyi-20260907T2108.md`.

The file formalizes the scaled signed-symmetric invariants used by the correlated
2x2 residual route, transports signed entry intervals to a bound on
`sigma = k45 + k54`, proves a robust determinant lower bound, proves both the
independent component-box and direct correlated-cross-cap adjugate-bias bounds,
and exposes the strict quarter-barrier / one-twelfth parameter arithmetic seams.

It intentionally does not bind source Jacobians, Float64/libm/FD/controller
semantics, P8 trajectory/domain coverage, provenance/admission, registry state,
or final integration.
-/

set_option autoImplicit false

namespace RouteBP5CorrelatedIntervalGate

noncomputable section

/-- Exact scaled identities connecting the T-P5-044 half-cross coordinate
`q = sigma/2` to the division-free determinant and adjugate-bias forms. -/
theorem scaled_correlated_invariants
    (p s sigma b4 b5 : ℝ) :
    4 * (p*s - (sigma/2)^2) = 4*p*s - sigma^2 ∧
      s*b4^2 - 2*(sigma/2)*b4*b5 + p*b5^2 =
        s*b4^2 - sigma*b4*b5 + p*b5^2 := by
  constructor <;> ring

/-- Signed interval addition must occur before absolute scalarization.  Entrywise
signed intervals and an endpoint cap on their sum transport directly to the
pointwise symmetric cross coordinate. -/
theorem signed_sum_interval_transport
    (k45 k54 k45L k45U k54L k54U Q : ℝ)
    (h45L : k45L ≤ k45) (h45U : k45 ≤ k45U)
    (h54L : k54L ≤ k54) (h54U : k54 ≤ k54U)
    (hQL : -Q ≤ k45L + k54L)
    (hQU : k45U + k54U ≤ Q) :
    -Q ≤ k45 + k54 ∧ k45 + k54 ≤ Q := by
  constructor <;> linarith

/-- A reusable square bound extracted from a component absolute-value cap. -/
theorem square_le_square_of_abs_le
    (x beta : ℝ) (h : |x| ≤ beta) : x^2 ≤ beta^2 := by
  rcases (abs_le.mp h) with ⟨hlo, hhi⟩
  have hdiff : 0 ≤ beta - x := sub_nonneg.mpr hhi
  have hsum : 0 ≤ beta + x := by
    linarith
  have hprod : 0 ≤ (beta - x) * (beta + x) := mul_nonneg hdiff hsum
  nlinarith

/-- Robust lower determinant certificate.  No separate `sL > 0` hypothesis is
needed: it follows from `pL > 0` and the strict determinant lower bound. -/
theorem scaled_symmetric_det_lower_of_interval
    (pL sL Q p s sigma Dmin : ℝ)
    (hpL : 0 < pL)
    (hDminDef : Dmin = 4*pL*sL - Q^2)
    (hDminPos : 0 < Dmin)
    (hp : pL ≤ p)
    (hs : sL ≤ s)
    (hsigmaL : -Q ≤ sigma)
    (hsigmaU : sigma ≤ Q) :
    0 < p ∧ 0 < s ∧ Dmin ≤ 4*p*s - sigma^2 := by
  have hsL : 0 < sL := by
    by_contra hnot
    have hsLnonpos : sL ≤ 0 := le_of_not_gt hnot
    have hprodNonpos : pL*sL ≤ 0 :=
      mul_nonpos_of_nonneg_of_nonpos (le_of_lt hpL) hsLnonpos
    have hQsq : 0 ≤ Q^2 := sq_nonneg Q
    nlinarith
  have hpPos : 0 < p := lt_of_lt_of_le hpL hp
  have hsPos : 0 < s := lt_of_lt_of_le hsL hs
  have hQminus : 0 ≤ Q - sigma := sub_nonneg.mpr hsigmaU
  have hQplus : 0 ≤ Q + sigma := by
    linarith
  have hsigmaSq : sigma^2 ≤ Q^2 := by
    have hprod : 0 ≤ (Q - sigma) * (Q + sigma) := mul_nonneg hQminus hQplus
    nlinarith
  have hps1 : pL*sL ≤ p*sL :=
    mul_le_mul_of_nonneg_right hp (le_of_lt hsL)
  have hps2 : p*sL ≤ p*s :=
    mul_le_mul_of_nonneg_left hs (le_of_lt hpPos)
  have hps : pL*sL ≤ p*s := le_trans hps1 hps2
  constructor
  · exact hpPos
  · constructor
    · exact hsPos
    · nlinarith

/-- Independent component-box fallback for the scaled correlated adjugate bias.
The explicit nonnegativity of `p` and `s` is the typed boundary needed to
transport component square caps through the diagonal coefficients. -/
theorem scaled_adjugate_bias_le_box
    (p s sigma pU sU Q b4 b5 beta4 beta5 : ℝ)
    (hp0 : 0 ≤ p) (hs0 : 0 ≤ s)
    (hpU : p ≤ pU) (hsU : s ≤ sU)
    (hQ : |sigma| ≤ Q)
    (hb4 : |b4| ≤ beta4) (hb5 : |b5| ≤ beta5) :
    s*b4^2 - sigma*b4*b5 + p*b5^2 ≤
      sU*beta4^2 + Q*beta4*beta5 + pU*beta5^2 := by
  have hb4sq : b4^2 ≤ beta4^2 := square_le_square_of_abs_le b4 beta4 hb4
  have hb5sq : b5^2 ≤ beta5^2 := square_le_square_of_abs_le b5 beta5 hb5
  have hsdiag1 : s*b4^2 ≤ s*beta4^2 :=
    mul_le_mul_of_nonneg_left hb4sq hs0
  have hsdiag2 : s*beta4^2 ≤ sU*beta4^2 :=
    mul_le_mul_of_nonneg_right hsU (sq_nonneg beta4)
  have hsdiag : s*b4^2 ≤ sU*beta4^2 := le_trans hsdiag1 hsdiag2
  have hpdiag1 : p*b5^2 ≤ p*beta5^2 :=
    mul_le_mul_of_nonneg_left hb5sq hp0
  have hpdiag2 : p*beta5^2 ≤ pU*beta5^2 :=
    mul_le_mul_of_nonneg_right hpU (sq_nonneg beta5)
  have hpdiag : p*b5^2 ≤ pU*beta5^2 := le_trans hpdiag1 hpdiag2
  have hQ0 : 0 ≤ Q := le_trans (abs_nonneg sigma) hQ
  have hbeta4 : 0 ≤ beta4 := le_trans (abs_nonneg b4) hb4
  have hsb1 : |sigma| * |b4| ≤ Q * beta4 := by
    exact mul_le_mul hQ hb4 (abs_nonneg b4) hQ0
  have hQbeta4 : 0 ≤ Q*beta4 := mul_nonneg hQ0 hbeta4
  have hsb2 : |sigma| * |b4| * |b5| ≤ Q*beta4*beta5 := by
    exact mul_le_mul hsb1 hb5 (abs_nonneg b5) hQbeta4
  have hcrossAbs : -sigma*b4*b5 ≤ |sigma*b4*b5| := by
    have h := neg_le_abs (sigma*b4*b5)
    nlinarith
  have habsProduct : |sigma*b4*b5| = |sigma|*|b4|*|b5| := by
    rw [abs_mul, abs_mul]
  have hcross : -sigma*b4*b5 ≤ Q*beta4*beta5 := by
    calc
      -sigma*b4*b5 ≤ |sigma*b4*b5| := hcrossAbs
      _ = |sigma|*|b4|*|b5| := habsProduct
      _ ≤ Q*beta4*beta5 := hsb2
  linarith

/-- Tighter optional interface when the source lane supplies a correlated direct
cross cap instead of the independent `Q*beta4*beta5` fallback. -/
theorem scaled_adjugate_bias_le_cross_cap
    (p s sigma pU sU b4 b5 beta4 beta5 chi : ℝ)
    (hp0 : 0 ≤ p) (hs0 : 0 ≤ s)
    (hpU : p ≤ pU) (hsU : s ≤ sU)
    (hb4 : |b4| ≤ beta4) (hb5 : |b5| ≤ beta5)
    (hcross : -sigma*b4*b5 ≤ chi) :
    s*b4^2 - sigma*b4*b5 + p*b5^2 ≤
      sU*beta4^2 + chi + pU*beta5^2 := by
  have hb4sq : b4^2 ≤ beta4^2 := square_le_square_of_abs_le b4 beta4 hb4
  have hb5sq : b5^2 ≤ beta5^2 := square_le_square_of_abs_le b5 beta5 hb5
  have hsdiag1 : s*b4^2 ≤ s*beta4^2 :=
    mul_le_mul_of_nonneg_left hb4sq hs0
  have hsdiag2 : s*beta4^2 ≤ sU*beta4^2 :=
    mul_le_mul_of_nonneg_right hsU (sq_nonneg beta4)
  have hsdiag : s*b4^2 ≤ sU*beta4^2 := le_trans hsdiag1 hsdiag2
  have hpdiag1 : p*b5^2 ≤ p*beta5^2 :=
    mul_le_mul_of_nonneg_left hb5sq hp0
  have hpdiag2 : p*beta5^2 ≤ pU*beta5^2 :=
    mul_le_mul_of_nonneg_right hpU (sq_nonneg beta5)
  have hpdiag : p*b5^2 ≤ pU*beta5^2 := le_trans hpdiag1 hpdiag2
  linarith

/-- Strict quarter-barrier arithmetic seam.  `B <= Ebox`, `Dmin <= D4`, and a
single upper radius endpoint are enough to transport the checker gate to every
point in the same cell. -/
theorem correlated_quarter_gate_of_interval_box
    (B Ebox Dmin D4 r rU : ℝ)
    (hB : B ≤ Ebox)
    (hD : Dmin ≤ D4)
    (hDminPos : 0 < Dmin)
    (hr : r ≤ rU)
    (hrU : rU ≤ 1)
    (hgate : 800*Ebox < (109-rU)*Dmin) :
    800*B < (109-r)*D4 := by
  have hcoef0 : 0 ≤ 109-rU := by
    linarith
  have hcoef : 109-rU ≤ 109-r := by
    linarith
  have hD40 : 0 ≤ D4 := le_trans (le_of_lt hDminPos) hD
  have hleft : (109-rU)*Dmin ≤ (109-rU)*D4 :=
    mul_le_mul_of_nonneg_left hD hcoef0
  have hright : (109-rU)*D4 ≤ (109-r)*D4 :=
    mul_le_mul_of_nonneg_right hcoef hD40
  have hBscaled : 800*B ≤ 800*Ebox := by
    nlinarith
  linarith

/-- The identical interval transport for the T-P5-044 one-twelfth incremental
parameter tube, with scaled coefficient `2400`. -/
theorem correlated_one_twelfth_parameter_gate_of_interval_box
    (G Eg Dmin D4 r rU : ℝ)
    (hG : G ≤ Eg)
    (hD : Dmin ≤ D4)
    (hDminPos : 0 < Dmin)
    (hr : r ≤ rU)
    (hrU : rU ≤ 1)
    (hgate : 2400*Eg < (109-rU)*Dmin) :
    2400*G < (109-r)*D4 := by
  have hcoef0 : 0 ≤ 109-rU := by
    linarith
  have hcoef : 109-rU ≤ 109-r := by
    linarith
  have hD40 : 0 ≤ D4 := le_trans (le_of_lt hDminPos) hD
  have hleft : (109-rU)*Dmin ≤ (109-rU)*D4 :=
    mul_le_mul_of_nonneg_left hD hcoef0
  have hright : (109-rU)*D4 ≤ (109-r)*D4 :=
    mul_le_mul_of_nonneg_right hcoef hD40
  have hGscaled : 2400*G ≤ 2400*Eg := by
    nlinarith
  linarith

/-- Whole-range `r in [0,1]` exact integer simplification for the quarter gate. -/
theorem whole_cell_quarter_integer_gate_iff (E D : ℝ) :
    800*E < 108*D ↔ 200*E < 27*D := by
  constructor <;> nlinarith

/-- Whole-range exact integer simplification for the one-twelfth parameter gate. -/
theorem whole_cell_one_twelfth_integer_gate_iff (E D : ℝ) :
    2400*E < 108*D ↔ 200*E < 9*D := by
  constructor <;> nlinarith

#print axioms scaled_correlated_invariants
#print axioms signed_sum_interval_transport
#print axioms square_le_square_of_abs_le
#print axioms scaled_symmetric_det_lower_of_interval
#print axioms scaled_adjugate_bias_le_box
#print axioms scaled_adjugate_bias_le_cross_cap
#print axioms correlated_quarter_gate_of_interval_box
#print axioms correlated_one_twelfth_parameter_gate_of_interval_box
#print axioms whole_cell_quarter_integer_gate_iff
#print axioms whole_cell_one_twelfth_integer_gate_iff

end

end RouteBP5CorrelatedIntervalGate
