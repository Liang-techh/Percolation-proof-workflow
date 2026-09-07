import Mathlib.Data.Real.Basic
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBP4NextChild

noncomputable section

/-! A small exact-real leaf for the P4 block-4 Schur/PMI channel.

The decimal M0[4,4] snapshot is written as the exact rational
116667666666667 / 10^15.  No DH, Float64, coverage, or trajectory premise is
introduced here: those remain source-binding obligations outside this child.
-/

def p : ℝ := 3 / 5
def ell : ℝ := 1 / 100
def d : ℝ := 116667666666667 / 1000000000000000

def quadratic (x y : ℝ) : ℝ := p * x ^ 2 + 2 * ell * x * y + d * y ^ 2

theorem p_pos : 0 < p := by
  norm_num [p]

theorem d_pos : 0 < d := by
  norm_num [d]

theorem exact_schur_margin : 0 < p * d - ell ^ 2 := by
  norm_num [p, ell, d]

theorem exact_schur_nonnegative (x y : ℝ) : 0 ≤ quadratic x y := by
  have hp : 0 < p := p_pos
  have hratio : ell ^ 2 / p ≤ d := by
    have hmargin := exact_schur_margin
    exact (div_le_iff₀ hp).2 (by linarith)
  have hm : 0 ≤ d - ell ^ 2 / p := sub_nonneg.mpr hratio
  have hsq : 0 ≤ (p * x + ell * y) ^ 2 := sq_nonneg _
  unfold quadratic
  have hid :
      p * x ^ 2 + 2 * ell * x * y + d * y ^ 2 =
        (p * x + ell * y) ^ 2 / p + (d - ell ^ 2 / p) * y ^ 2 := by
    field_simp [ne_of_gt hp]
    ring
  rw [hid]
  exact add_nonneg
    (div_nonneg hsq hp.le)
    (mul_nonneg hm (sq_nonneg y))

/- The residual envelope is the exact rational beta=1/100 channel.  Young's
   parameter epsilon=1/100 leaves both diagonal budgets nonnegative. -/
theorem residual_absorption
    (x y residual : ℝ)
    (hresidual : residual ^ 2 ≤ ell ^ 2 * y ^ 2) :
    0 ≤ p * x ^ 2 + 2 * x * residual + d * y ^ 2 := by
  have he : (0 : ℝ) < 1 / 100 := by norm_num
  have hp : (1 / 100 : ℝ) ≤ p := by norm_num [p]
  have hd : ell ^ 2 / (1 / 100 : ℝ) ≤ d := by
    norm_num [ell, d]
  have hsq : 0 ≤ ((1 / 100 : ℝ) * x + residual) ^ 2 := sq_nonneg _
  have hgap : 0 ≤ ell ^ 2 * y ^ 2 - residual ^ 2 :=
    sub_nonneg.mpr hresidual
  have hyoung :
      -(1 / 100 : ℝ) * x ^ 2 - ell ^ 2 / (1 / 100 : ℝ) * y ^ 2 ≤
        2 * x * residual := by
    have hscaled :
        0 ≤ (1 / 100 : ℝ) *
          ((1 / 100 : ℝ) * x ^ 2 + 2 * x * residual +
            ell ^ 2 / (1 / 100 : ℝ) * y ^ 2) := by
      calc
        0 ≤ ((1 / 100 : ℝ) * x + residual) ^ 2 +
            (ell ^ 2 * y ^ 2 - residual ^ 2) := add_nonneg hsq hgap
        _ = (1 / 100 : ℝ) *
            ((1 / 100 : ℝ) * x ^ 2 + 2 * x * residual +
              ell ^ 2 / (1 / 100 : ℝ) * y ^ 2) := by
          field_simp
          ring
    have hcore :
        0 ≤ (1 / 100 : ℝ) * x ^ 2 + 2 * x * residual +
          ell ^ 2 / (1 / 100 : ℝ) * y ^ 2 := by
      exact (mul_nonneg_iff_of_pos_left he).mp hscaled
    linarith
  have hx : 0 ≤ (p - (1 / 100 : ℝ)) * x ^ 2 :=
    mul_nonneg (sub_nonneg.mpr hp) (sq_nonneg x)
  have hy : 0 ≤ (d - ell ^ 2 / (1 / 100 : ℝ)) * y ^ 2 :=
    mul_nonneg (sub_nonneg.mpr hd) (sq_nonneg y)
  linarith

#print axioms exact_schur_margin
#print axioms exact_schur_nonnegative
#print axioms residual_absorption

end
end RouteBP4NextChild
