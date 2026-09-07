import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# Route-B P5 physical-gain to parameter-tube sidecar

Source-independent Lean decomposition of
`agent_review_inbox/review-T-P5-031-guyuefangyuan-20260907T1224.md`.

This file formalizes the exact moving-frame endpoint constants, a physical
component-gain transport interface, the four-term centered square aggregation,
the square-only product-slack cross-term bound, the resulting `mu/nu` residual
envelope, and the rational `1/12` tube gate/necessity diagnostic.

It does not supply the physical gain table, bind Julia/DH/Float64 execution
semantics, prove P8 coverage or ODE continuation, or perform final integration.
-/

set_option autoImplicit false

namespace RouteBP5PhysicalGainParameterTube

noncomputable section

def h4 : ℝ := 2340 / 8699
def h5 : ℝ := 1520 / 8699
def r4 : ℝ := -21912800 / 75672601
def r5 : ℝ := -15007200 / 75672601
def A4 : ℝ := 21912800 / 75672601
def A5 : ℝ := 15007200 / 75672601

/-- Exact endpoint bound for the block-4 moving-frame affine factor on `0 <= t <= 1`. -/
theorem moving_frame_a4_endpoint_bound
    (t : ℝ) (ht0 : 0 ≤ t) (ht1 : t ≤ 1) :
    |h4 * t + r4| ≤ A4 := by
  have hnonpos : h4 * t + r4 ≤ 0 := by
    dsimp [h4, r4]
    nlinarith
  rw [abs_of_nonpos hnonpos]
  dsimp [h4, r4, A4]
  nlinarith

/-- Exact endpoint bound for the block-5 moving-frame affine factor on `0 <= t <= 1`. -/
theorem moving_frame_a5_endpoint_bound
    (t : ℝ) (ht0 : 0 ≤ t) (ht1 : t ≤ 1) :
    |h5 * t + r5| ≤ A5 := by
  have hnonpos : h5 * t + r5 ≤ 0 := by
    dsimp [h5, r5]
    nlinarith
  rw [abs_of_nonpos hnonpos]
  dsimp [h5, r5, A5]
  nlinarith

/-- The ramp-time factor itself has unit absolute bound on the current horizon. -/
theorem moving_frame_time_abs_bound
    (t : ℝ) (ht0 : 0 ≤ t) (ht1 : t ≤ 1) : |t| ≤ 1 := by
  rw [abs_of_nonneg ht0]
  exact ht1

/-- Four-term Cauchy bound in a division-free form. -/
theorem four_term_square
    (u1 u2 u3 u4 : ℝ) :
    (u1 + u2 + u3 + u4)^2 ≤ 4 * (u1^2 + u2^2 + u3^2 + u4^2) := by
  nlinarith [sq_nonneg (u1-u2), sq_nonneg (u1-u3), sq_nonneg (u1-u4),
    sq_nonneg (u2-u3), sq_nonneg (u2-u4), sq_nonneg (u3-u4)]

/-- Aggregates four already-typed component square budgets into one centered budget. -/
theorem four_term_component_budget
    (u1 u2 u3 u4 c1 c2 c3 c4 V : ℝ)
    (h1 : u1^2 ≤ c1*V) (h2 : u2^2 ≤ c2*V)
    (h3 : u3^2 ≤ c3*V) (h4b : u4^2 ≤ c4*V) :
    (u1 + u2 + u3 + u4)^2 ≤ 4 * (c1+c2+c3+c4) * V := by
  have hs := four_term_square u1 u2 u3 u4
  have hsum : u1^2 + u2^2 + u3^2 + u4^2 ≤ (c1+c2+c3+c4)*V := by
    nlinarith
  nlinarith

/-- Centered state contribution for one physical residual channel. -/
def centeredPart
    (kq4 kq5 kv4 kv5 X4 X5 Y4 Y5 : ℝ) : ℝ :=
  kq4*|X4| + kq5*|X5| + kv4*|Y4| + kv5*|Y5|

/-- Deterministic parameter contribution induced by the exact moving frame. -/
def parameterGain
    (kq4 kq5 kv4 kv5 kw kc : ℝ) : ℝ :=
  kq4*A4 + kq5*A5 + kv4*h4 + kv5*h5 + kw + kc

/-- A physical component gain contract transports to `centeredPart + parameterGain*d`. -/
theorem component_physical_gain_transport
    (Dl dq4 dq5 dv4 dv5 dw X4 X5 Y4 Y5 d : ℝ)
    (kq4 kq5 kv4 kv5 kw kc : ℝ)
    (hkq4 : 0 ≤ kq4) (hkq5 : 0 ≤ kq5)
    (hkv4 : 0 ≤ kv4) (hkv5 : 0 ≤ kv5)
    (hkw : 0 ≤ kw)
    (hq4 : |dq4| ≤ |X4| + A4*d)
    (hq5 : |dq5| ≤ |X5| + A5*d)
    (hv4 : |dv4| ≤ |Y4| + h4*d)
    (hv5 : |dv5| ≤ |Y5| + h5*d)
    (hw : |dw| ≤ d)
    (hcontract : |Dl| ≤
      kq4*|dq4| + kq5*|dq5| + kv4*|dv4| + kv5*|dv5| + kw*|dw| + kc*d) :
    |Dl| ≤ centeredPart kq4 kq5 kv4 kv5 X4 X5 Y4 Y5 +
      parameterGain kq4 kq5 kv4 kv5 kw kc * d := by
  have hq4' := mul_le_mul_of_nonneg_left hq4 hkq4
  have hq5' := mul_le_mul_of_nonneg_left hq5 hkq5
  have hv4' := mul_le_mul_of_nonneg_left hv4 hkv4
  have hv5' := mul_le_mul_of_nonneg_left hv5 hkv5
  have hw' := mul_le_mul_of_nonneg_left hw hkw
  dsimp [centeredPart, parameterGain]
  nlinarith

/-- The exact deterministic parameter gain is nonnegative for nonnegative physical gains. -/
theorem parameterGain_nonneg
    (kq4 kq5 kv4 kv5 kw kc : ℝ)
    (hkq4 : 0 ≤ kq4) (hkq5 : 0 ≤ kq5)
    (hkv4 : 0 ≤ kv4) (hkv5 : 0 ≤ kv5)
    (hkw : 0 ≤ kw) (hkc : 0 ≤ kc) :
    0 ≤ parameterGain kq4 kq5 kv4 kv5 kw kc := by
  dsimp [parameterGain, A4, A5, h4, h5]
  positivity

/-- Two-channel Cauchy identity used by the residual norm-square bridge. -/
theorem two_channel_cauchy
    (S4 S5 G4 G5 : ℝ) :
    (S4*G4 + S5*G5)^2 ≤ (S4^2+S5^2)*(G4^2+G5^2) := by
  nlinarith [sq_nonneg (S4*G5 - S5*G4)]

/-- Converts an absolute-value envelope to a square envelope without relying on `sqrt`. -/
theorem square_le_square_of_abs_le
    (x r : ℝ) (h : |x| ≤ r) : x^2 ≤ r^2 := by
  rcases (abs_le.mp h) with ⟨hlo, hhi⟩
  have h1 : 0 ≤ r-x := by linarith
  have h2 : 0 ≤ r+x := by linarith
  nlinarith [mul_nonneg h1 h2]

/-- Square-only Young/product-slack consumer for the moving-frame cross term. -/
theorem product_slack_cross_bound
    (V d C U W p q : ℝ)
    (hV : 0 ≤ V) (hd : 0 ≤ d) (hC : 0 ≤ C)
    (hp : 0 ≤ p) (hq : 0 ≤ q)
    (hC2 : C^2 ≤ U*W*V)
    (hprod : U*W ≤ p*q) :
    2*d*C ≤ p*V + q*d^2 := by
  have hprodV : U*W*V ≤ p*q*V := by
    exact mul_le_mul_of_nonneg_right hprod hV
  have hc : C^2 ≤ p*q*V := le_trans hC2 hprodV
  have hcd := mul_le_mul_of_nonneg_left hc (sq_nonneg d)
  have hyoung := sq_nonneg (p*V - q*d^2)
  have hlhs : 0 ≤ 2*d*C := by positivity
  have hrhs : 0 ≤ p*V + q*d^2 := by positivity
  have hsq : (2*d*C)^2 ≤ (p*V + q*d^2)^2 := by
    nlinarith
  nlinarith

/-- Main source-independent bridge from two physical channel envelopes to the `mu/nu` norm-square envelope. -/
theorem physical_gain_to_mu_nu_envelope
    (Dl4 Dl5 S4 S5 G4 G5 U V d p q : ℝ)
    (hS4 : 0 ≤ S4) (hS5 : 0 ≤ S5)
    (hG4 : 0 ≤ G4) (hG5 : 0 ≤ G5)
    (hV : 0 ≤ V) (hd : 0 ≤ d)
    (hp : 0 ≤ p) (hq : 0 ≤ q)
    (hDl4 : |Dl4| ≤ S4 + G4*d)
    (hDl5 : |Dl5| ≤ S5 + G5*d)
    (hcentered : S4^2 + S5^2 ≤ U*V)
    (hprod : U*(G4^2+G5^2) ≤ p*q) :
    Dl4^2 + Dl5^2 ≤
      (U+p)*V + ((G4^2+G5^2)+q)*d^2 := by
  let C : ℝ := S4*G4 + S5*G5
  have hC : 0 ≤ C := by
    dsimp [C]
    positivity
  have hcauchy : C^2 ≤ (S4^2+S5^2)*(G4^2+G5^2) := by
    dsimp [C]
    exact two_channel_cauchy S4 S5 G4 G5
  have hGsq : 0 ≤ G4^2+G5^2 := by positivity
  have hmul :
      (S4^2+S5^2)*(G4^2+G5^2) ≤ (U*V)*(G4^2+G5^2) :=
    mul_le_mul_of_nonneg_right hcentered hGsq
  have hC2 : C^2 ≤ U*(G4^2+G5^2)*V := by
    have hchain := le_trans hcauchy hmul
    nlinarith
  have hcross : 2*d*C ≤ p*V + q*d^2 := by
    exact product_slack_cross_bound V d C U (G4^2+G5^2) p q
      hV hd hC hp hq hC2 hprod
  have hsq4 := square_le_square_of_abs_le Dl4 (S4+G4*d) hDl4
  have hsq5 := square_le_square_of_abs_le Dl5 (S5+G5*d) hDl5
  dsimp [C] at hcross
  nlinarith

/-- Checker-facing assignment `mu=U+p`, `nu=W+q` for the existing T-P5-030 tube ledger. -/
theorem parameter_tube_gain_gate
    (U W p q : ℝ)
    (hU : 0 ≤ U) (hW : 0 ≤ W) (hp : 0 ≤ p) (hq : 0 ≤ q)
    (hprod : U*W ≤ p*q)
    (hgate : 11424*(U+p) + 137088*(W+q) < 2285) :
    0 ≤ U+p ∧ 0 ≤ W+q ∧ U*W ≤ p*q ∧
      11424*(U+p) + 137088*(W+q) < 2285 := by
  constructor
  · positivity
  constructor
  · positivity
  constructor
  · exact hprod
  · exact hgate

/-- Necessity diagnostic for any nonnegative slack pair passing the rational tube cost. -/
theorem slack_feasibility_necessity
    (U W p q R : ℝ)
    (hp : 0 ≤ p) (hq : 0 ≤ q)
    (hprod : U*W ≤ p*q)
    (hcost : 11424*p + 137088*q < R) :
    0 < R ∧ 6264373248*U*W < R^2 := by
  have hcost0 : 0 ≤ 11424*p + 137088*q := by positivity
  have hR : 0 < R := lt_of_le_of_lt hcost0 hcost
  have hamgm : 6264373248*p*q ≤ (11424*p + 137088*q)^2 := by
    nlinarith [sq_nonneg (11424*p - 137088*q)]
  have hscaled : 6264373248*U*W ≤ 6264373248*p*q := by
    nlinarith
  have hcostsq : (11424*p + 137088*q)^2 < R^2 := by
    nlinarith
  constructor
  · exact hR
  · nlinarith

/-- Freezes the exact integer factor `4*11424*137088`. -/
theorem exact_feasibility_factor :
    (4:ℤ) * 11424 * 137088 = 6264373248 := by
  norm_num

#print axioms moving_frame_a4_endpoint_bound
#print axioms moving_frame_a5_endpoint_bound
#print axioms moving_frame_time_abs_bound
#print axioms four_term_square
#print axioms four_term_component_budget
#print axioms component_physical_gain_transport
#print axioms parameterGain_nonneg
#print axioms two_channel_cauchy
#print axioms square_le_square_of_abs_le
#print axioms product_slack_cross_bound
#print axioms physical_gain_to_mu_nu_envelope
#print axioms parameter_tube_gain_gate
#print axioms slack_feasibility_necessity
#print axioms exact_feasibility_factor

end

end RouteBP5PhysicalGainParameterTube
