import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# Route-B P4 relative-plus-transverse Schur reserve sidecar

This file formalizes the source-independent inequality core of
`review-T-P4-014-kuangmanmozun-20260907T0247.md`.

It proves a square-root-free transverse Schur budget, composes the two
magnitude envelopes into the P4 quadratic, records a division-free sharpness
witness, and instantiates the exact block-4 rational reserve.

It does not bind Float64 execution remainders to physical coordinates, does
not prove a source/IEEE error bound, and does not close P4/M4.
-/

set_option autoImplicit false

namespace RouteBP4TransverseSchur

noncomputable section

/-- The two residual envelopes compose into a same-coordinate plus transverse
absolute-value envelope. -/
theorem combined_residual_abs
    (c beta gamma y z e b : ℝ)
    (hc : 0 ≤ c) (hbeta : 0 ≤ beta) (hgamma : 0 ≤ gamma)
    (he : |e| ≤ beta * |y|)
    (hb : |b| ≤ gamma * |z|) :
    |c * y + e + b| ≤ (c + beta) * |y| + gamma * |z| := by
  have hce : |c * y + e| ≤ |c * y| + |e| := abs_add (c * y) e
  have hceb : |c * y + e + b| ≤ |c * y + e| + |b| :=
    abs_add (c * y + e) b
  have hcy : |c * y| = c * |y| := by
    rw [abs_mul, abs_of_nonneg hc]
  rw [hcy] at hce
  nlinarith

/-- Division-free form of the exact two-coordinate Schur identity.  If the
same-coordinate term leaves strict reserve `p*d-a^2>0`, then a transverse
coefficient `gamma` is affordable precisely when
`d*gamma^2 ≤ (p*d-a^2)*h`. -/
theorem transverse_square_budget
    (p d a gamma h Y Z : ℝ)
    (hp : 0 < p)
    (hDelta : 0 < p * d - a ^ 2)
    (hreserve : d * gamma ^ 2 ≤ (p * d - a ^ 2) * h) :
    0 ≤ p * d * Y ^ 2 + p * h * Z ^ 2 - (a * Y + gamma * Z) ^ 2 := by
  let Delta : ℝ := p * d - a ^ 2
  have hDelta' : 0 < Delta := by
    simpa [Delta] using hDelta
  have hreserve' : 0 ≤ Delta * h - d * gamma ^ 2 := by
    simpa [Delta] using (sub_nonneg.mpr hreserve)
  have hsquare : 0 ≤ (Delta * Y - a * gamma * Z) ^ 2 :=
    sq_nonneg (Delta * Y - a * gamma * Z)
  have hzsq : 0 ≤ Z ^ 2 := sq_nonneg Z
  have hsecond : 0 ≤ p * (Delta * h - d * gamma ^ 2) * Z ^ 2 := by
    exact mul_nonneg (mul_nonneg (le_of_lt hp) hreserve') hzsq
  have hid :
      Delta * (p * d * Y ^ 2 + p * h * Z ^ 2 -
        (a * Y + gamma * Z) ^ 2) =
        (Delta * Y - a * gamma * Z) ^ 2 +
          p * (Delta * h - d * gamma ^ 2) * Z ^ 2 := by
    dsimp [Delta]
    ring
  have hprod :
      0 ≤ Delta * (p * d * Y ^ 2 + p * h * Z ^ 2 -
        (a * Y + gamma * Z) ^ 2) := by
    rw [hid]
    exact add_nonneg hsquare hsecond
  nlinarith

/-- Convert the absolute-value residual envelope and the transverse reserve
into the exact square budget consumed by the final Schur completion. -/
theorem residual_square_budget
    (p d a gamma h r y z : ℝ)
    (hp : 0 < p)
    (ha : 0 ≤ a) (hgamma : 0 ≤ gamma)
    (hDelta : 0 < p * d - a ^ 2)
    (hr : |r| ≤ a * |y| + gamma * |z|)
    (hreserve : d * gamma ^ 2 ≤ (p * d - a ^ 2) * h) :
    r ^ 2 ≤ p * (d * y ^ 2 + h * z ^ 2) := by
  have hR : 0 ≤ a * |y| + gamma * |z| :=
    add_nonneg (mul_nonneg ha (abs_nonneg y))
      (mul_nonneg hgamma (abs_nonneg z))
  have hrsq : |r| ^ 2 ≤ (a * |y| + gamma * |z|) ^ 2 := by
    nlinarith [abs_nonneg r]
  have hquad := transverse_square_budget p d a gamma h |y| |z|
    hp hDelta hreserve
  rw [sq_abs r] at hrsq
  rw [sq_abs y, sq_abs z] at hquad
  nlinarith

/-- Main source-independent P4 consumer.  The theorem is square-root-free and
never divides by `p` or by the Schur reserve. -/
theorem relative_plus_transverse_schur
    (p d c beta gamma h x y z e b : ℝ)
    (hp : 0 < p)
    (hc : 0 ≤ c) (hbeta : 0 ≤ beta) (hgamma : 0 ≤ gamma)
    (hDelta : 0 < p * d - (c + beta) ^ 2)
    (he : |e| ≤ beta * |y|)
    (hb : |b| ≤ gamma * |z|)
    (hreserve : d * gamma ^ 2 ≤ (p * d - (c + beta) ^ 2) * h) :
    0 ≤ p * x ^ 2 + 2 * x * (c * y + e + b) + d * y ^ 2 + h * z ^ 2 := by
  have hrabs := combined_residual_abs c beta gamma y z e b
    hc hbeta hgamma he hb
  have hrsq := residual_square_budget p d (c + beta) gamma h
    (c * y + e + b) y z hp (add_nonneg hc hbeta) hgamma hDelta hrabs hreserve
  have hsquare : 0 ≤ (p * x + (c * y + e + b)) ^ 2 :=
    sq_nonneg (p * x + (c * y + e + b))
  have hpQ :
      0 ≤ p * (p * x ^ 2 + 2 * x * (c * y + e + b) +
        d * y ^ 2 + h * z ^ 2) := by
    nlinarith
  nlinarith

/-- A uniform additive bias is the special case `z=1`: it needs its own
explicit positive scalar slack. -/
theorem additive_bias_with_slack
    (p d c beta B sigma x y e b : ℝ)
    (hp : 0 < p)
    (hc : 0 ≤ c) (hbeta : 0 ≤ beta) (hB : 0 ≤ B)
    (hDelta : 0 < p * d - (c + beta) ^ 2)
    (he : |e| ≤ beta * |y|)
    (hb : |b| ≤ B)
    (hreserve : d * B ^ 2 ≤ (p * d - (c + beta) ^ 2) * sigma) :
    0 ≤ p * x ^ 2 + 2 * x * (c * y + e + b) + d * y ^ 2 + sigma := by
  have hb' : |b| ≤ B * |(1 : ℝ)| := by
    simpa using hb
  simpa using relative_plus_transverse_schur
    p d c beta B sigma x y (1 : ℝ) e b hp hc hbeta hB hDelta he hb' hreserve

/-- Polynomial sharpness witness for the transverse reserve.  It avoids all
division: if `Delta*h < d*gamma^2`, the homogeneous witness
`z=p*Delta`, `y=a*gamma*p`, `x=-gamma*p*d` makes the completed quadratic
strictly negative. -/
theorem transverse_reserve_failure_witness
    (p d a gamma h : ℝ)
    (hp : 0 < p)
    (hDelta : 0 < p * d - a ^ 2)
    (hfail : (p * d - a ^ 2) * h < d * gamma ^ 2) :
    p * (-gamma * p * d) ^ 2 +
        2 * (-gamma * p * d) *
          (a * (a * gamma * p) + gamma * (p * (p * d - a ^ 2))) +
        d * (a * gamma * p) ^ 2 +
        h * (p * (p * d - a ^ 2)) ^ 2 < 0 := by
  have hp2 : 0 < p ^ 2 := sq_pos_of_pos hp
  have hneg : (p * d - a ^ 2) * h - d * gamma ^ 2 < 0 := by
    linarith
  have hpos : 0 < p ^ 2 * (p * d - a ^ 2) :=
    mul_pos hp2 hDelta
  have hid :
      p * (-gamma * p * d) ^ 2 +
          2 * (-gamma * p * d) *
            (a * (a * gamma * p) + gamma * (p * (p * d - a ^ 2))) +
          d * (a * gamma * p) ^ 2 +
          h * (p * (p * d - a ^ 2)) ^ 2 =
        p ^ 2 * (p * d - a ^ 2) *
          ((p * d - a ^ 2) * h - d * gamma ^ 2) := by
    ring
  rw [hid]
  exact mul_neg_of_pos_of_neg hpos hneg

/-- Exact block-4 positive coefficient used by the Route-B PMI. -/
def p4 : ℝ := 3 / 5

/-- Exact block-4 cross-coordinate coefficient from the Route-B PMI. -/
def d4 : ℝ := 116667666666667 / 1000000000000000

/-- Exact unused squared Schur reserve after the corrected quarter envelope. -/
def Delta4 : ℝ := 37503000000001 / 5000000000000000

theorem block4_delta_identity :
    p4 * d4 - ((1 / 100 : ℝ) + 6 / 25) ^ 2 = Delta4 := by
  norm_num [p4, d4, Delta4]

theorem block4_delta_pos : 0 < Delta4 := by
  norm_num [Delta4]

/-- Exact division-free form of the block-4 transverse reserve budget. -/
theorem block4_reserve_from_integer_budget
    (gamma h : ℝ)
    (hbudget :
      (583338333333335 : ℝ) * gamma ^ 2 ≤ 37503000000001 * h) :
    d4 * gamma ^ 2 ≤
      (p4 * d4 - ((1 / 100 : ℝ) + 6 / 25) ^ 2) * h := by
  rw [block4_delta_identity]
  norm_num [d4, Delta4] at ⊢
  nlinarith

/-- Concrete block-4 quarter-envelope plus transverse-reserve consumer. -/
theorem block4_quarter_plus_transverse
    (gamma h x y z e b : ℝ)
    (hgamma : 0 ≤ gamma)
    (he : |e| ≤ (6 / 25 : ℝ) * |y|)
    (hb : |b| ≤ gamma * |z|)
    (hbudget :
      (583338333333335 : ℝ) * gamma ^ 2 ≤ 37503000000001 * h) :
    0 ≤ p4 * x ^ 2 +
      2 * x * ((1 / 100 : ℝ) * y + e + b) + d4 * y ^ 2 + h * z ^ 2 := by
  have hp : 0 < p4 := by norm_num [p4]
  have hDelta :
      0 < p4 * d4 - ((1 / 100 : ℝ) + 6 / 25) ^ 2 := by
    rw [block4_delta_identity]
    exact block4_delta_pos
  have hreserve := block4_reserve_from_integer_budget gamma h hbudget
  exact relative_plus_transverse_schur
    p4 d4 (1 / 100) (6 / 25) gamma h x y z e b
    hp (by norm_num) (by norm_num) hgamma hDelta he hb hreserve

#print axioms combined_residual_abs
#print axioms transverse_square_budget
#print axioms residual_square_budget
#print axioms relative_plus_transverse_schur
#print axioms additive_bias_with_slack
#print axioms transverse_reserve_failure_witness
#print axioms block4_delta_identity
#print axioms block4_delta_pos
#print axioms block4_reserve_from_integer_budget
#print axioms block4_quarter_plus_transverse

end

end RouteBP4TransverseSchur
