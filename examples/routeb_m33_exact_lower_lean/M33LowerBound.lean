import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# Exact M33 lower-bound seam

This sidecar consumes the exact M33 Fourier formula extracted from the
canonical Route-B DH source.  It proves the rational global lower bound after
the trigonometric substitution `u = cos(q5)`, `x = cos(2*q4)`, and
`cos(2*q5) = 2*u^2 - 1`.

The source/parser equality, Float64/libm rounding, and the remaining mass
matrix entries are separate obligations.  This file is only the exact
algebraic lower-bound child.
-/

set_option autoImplicit false

namespace RouteBM33ExactLower

def m33 (u x : ℝ) : ℝ :=
  (12159703 : ℝ) / 48000000
    + (399 : ℝ) / 200000 * u
    + (147 : ℝ) / 3200000 * (x + (2 * u ^ 2 - 1) - x * (2 * u ^ 2 - 1))

/-- The exact M33 Fourier expression is uniformly positive on the cosine box. -/
theorem m33_lower_bound
    (u x : ℝ)
    (hu : -1 ≤ u ∧ u ≤ 1)
    (hx : -1 ≤ x ∧ x ≤ 1) :
    (3016537 : ℝ) / 12000000 ≤ m33 u x := by
  have hu_nonneg : 0 ≤ 1 - u := by linarith [hu.2]
  have hx_nonneg : 0 ≤ 1 - x := by linarith [hx.2]
  have hx_cap : 1 - x ≤ 2 := by linarith [hx.1]
  have hu_cap : 1 - u ≤ 2 := by linarith [hu.1]
  have hprod_step : (1 - u) * (1 - x) ≤ 2 * (1 - u) :=
    mul_le_mul_of_nonneg_left hx_cap hu_nonneg
  have hprod_cap : 2 * (1 - u) ≤ 4 := by linarith
  have hprod : (1 - u) * (1 - x) ≤ 4 := by linarith
  have hinner :
      0 ≤ (399 : ℝ) / 200000
        - 2 * ((147 : ℝ) / 3200000) * ((1 - u) * (1 - x)) := by
    nlinarith [hprod]
  have hfactor :
      0 ≤ (u + 1) *
        ((399 : ℝ) / 200000
          - 2 * ((147 : ℝ) / 3200000) * ((1 - u) * (1 - x))) :=
    mul_nonneg (by linarith [hu.1]) hinner
  have hidentity :
      m33 u x - (3016537 : ℝ) / 12000000 =
        (u + 1) *
          ((399 : ℝ) / 200000
            - 2 * ((147 : ℝ) / 3200000) * ((1 - u) * (1 - x))) := by
    dsimp [m33]
    ring
  nlinarith [hfactor, hidentity]

#print axioms m33_lower_bound

end RouteBM33ExactLower
