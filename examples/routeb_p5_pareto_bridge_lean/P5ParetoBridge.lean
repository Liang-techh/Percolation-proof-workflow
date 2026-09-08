import Mathlib

noncomputable section

namespace RouteBP5ParetoBridge

/--
Convex interpolation of the two already-derived block-(4,5) endpoint
certificates.  `r = 0` is the scalar/isotropic T-P5-037 endpoint, while
`r = 1` is the anisotropic T-P5-036 endpoint.
-/
theorem block45_joint_pareto_of_two_certificates
    (Q V u4 u5 r : ℝ)
    (hr0 : 0 ≤ r)
    (hr1 : r ≤ 1)
    (hScalar :
      (109 / 200 : ℝ) * V + (1 / 6 : ℝ) * u4 ^ 2 + (1 / 6 : ℝ) * u5 ^ 2 ≤ Q)
    (hAniso :
      (27 / 50 : ℝ) * V + (101 / 500 : ℝ) * u4 ^ 2 + (1 / 6 : ℝ) * u5 ^ 2 ≤ Q) :
    ((109 - r) / 200) * V
        + ((250 + 53 * r) / 1500) * u4 ^ 2
        + (1 / 6 : ℝ) * u5 ^ 2 ≤ Q := by
  have hB := mul_le_mul_of_nonneg_left hAniso hr0
  have hA := mul_le_mul_of_nonneg_left hScalar (sub_nonneg.mpr hr1)
  nlinarith

/-- The convex-family coefficients remain strictly positive on `0 ≤ r ≤ 1`. -/
theorem pareto_coefficients_positive
    (r : ℝ) (hr0 : 0 ≤ r) (hr1 : r ≤ 1) :
    0 < (109 - r) / 200 ∧ 0 < (250 + 53 * r) / 1500 := by
  constructor <;> nlinarith

/-- `r = 0` reduces exactly to the T-P5-037 scalar endpoint. -/
theorem pareto_r0_identity (V u4 u5 : ℝ) :
    ((109 - (0 : ℝ)) / 200) * V
        + ((250 + 53 * (0 : ℝ)) / 1500) * u4 ^ 2
        + (1 / 6 : ℝ) * u5 ^ 2
      = (109 / 200 : ℝ) * V
        + (1 / 6 : ℝ) * u4 ^ 2
        + (1 / 6 : ℝ) * u5 ^ 2 := by
  ring

/-- `r = 1` reduces exactly to the T-P5-036 anisotropic endpoint. -/
theorem pareto_r1_identity (V u4 u5 : ℝ) :
    ((109 - (1 : ℝ)) / 200) * V
        + ((250 + 53 * (1 : ℝ)) / 1500) * u4 ^ 2
        + (1 / 6 : ℝ) * u5 ^ 2
      = (27 / 50 : ℝ) * V
        + (101 / 500 : ℝ) * u4 ^ 2
        + (1 / 6 : ℝ) * u5 ^ 2 := by
  ring

/--
The quarter-barrier cleared checker at `r = 0` is exactly the scalar gate
`1200 (E4+E5) < 109`.
-/
theorem quarter_checker_r0_reduces (E4 E5 : ℝ) :
    300000 * E4 + 1200 * (250 + 53 * (0 : ℝ)) * E5
        < (109 - (0 : ℝ)) * (250 + 53 * (0 : ℝ))
      ↔ 1200 * (E4 + E5) < 109 := by
  constructor <;> intro h <;> norm_num at h ⊢ <;> nlinarith

/--
The quarter-barrier cleared checker at `r = 1` is exactly the anisotropic gate
`25000 E4 + 30300 E5 < 2727`.
-/
theorem quarter_checker_r1_reduces (E4 E5 : ℝ) :
    300000 * E4 + 1200 * (250 + 53 * (1 : ℝ)) * E5
        < (109 - (1 : ℝ)) * (250 + 53 * (1 : ℝ))
      ↔ 25000 * E4 + 30300 * E5 < 2727 := by
  constructor <;> intro h <;> norm_num at h ⊢ <;> nlinarith

/--
Exact comparison of the two endpoint inward margins.  The anisotropic endpoint
wins exactly when the component-4 squared residual budget crosses the stated
threshold; the component-5 budget cancels out.
-/
theorem anisotropic_margin_beats_scalar_iff
    (Vstar E4 E5 : ℝ) :
    (27 / 50 : ℝ) * Vstar - (125 / 101 : ℝ) * E4 - (3 / 2 : ℝ) * E5
        > (109 / 200 : ℝ) * Vstar - (3 / 2 : ℝ) * (E4 + E5)
      ↔ E4 > (101 / 5300 : ℝ) * Vstar := by
  constructor <;> intro h <;> nlinarith

/--
A fully division-free first-exit consumer for the Pareto family.  It assumes
only the abstract Pareto certificate, the exact derivative identity, and
same-domain componentwise squared residual caps.  No source or trajectory
coverage is asserted here.
-/
theorem quarter_first_exit_inward_of_pareto
    (Q V Vdot u4 u5 l4 l5 E4 E5 r : ℝ)
    (hr0 : 0 ≤ r)
    (hr1 : r ≤ 1)
    (hPareto :
      ((109 - r) / 200) * V
          + ((250 + 53 * r) / 1500) * u4 ^ 2
          + (1 / 6 : ℝ) * u5 ^ 2 ≤ Q)
    (hDerivative : Vdot = -Q - u4 * l4 - u5 * l5)
    (hBoundary : V = 1 / 4)
    (hE4 : l4 ^ 2 ≤ E4)
    (hE5 : l5 ^ 2 ≤ E5)
    (hGate :
      300000 * E4 + 1200 * (250 + 53 * r) * E5
        < (109 - r) * (250 + 53 * r)) :
    Vdot < 0 := by
  have hd : 0 < 250 + 53 * r := by
    nlinarith
  have hParetoScaled := mul_le_mul_of_nonneg_left hPareto (le_of_lt hd)
  have hs4 : 0 ≤ ((250 + 53 * r) * u4 + 750 * l4) ^ 2 := sq_nonneg _
  have hy4 :
      -(375 : ℝ) * l4 ^ 2 ≤
        (250 + 53 * r) *
          (((250 + 53 * r) / 1500) * u4 ^ 2 + u4 * l4) := by
    nlinarith [hs4]
  have hs5 : 0 ≤ (u5 + 3 * l5) ^ 2 := sq_nonneg _
  have hy5base :
      0 ≤ (1 / 6 : ℝ) * u5 ^ 2 + u5 * l5 + (3 / 2 : ℝ) * l5 ^ 2 := by
    nlinarith [hs5]
  have hy5 := mul_nonneg (le_of_lt hd) hy5base
  have hE5Scaled := mul_le_mul_of_nonneg_left hE5 (le_of_lt hd)
  have hposScaled :
      0 < (250 + 53 * r) * (Q + u4 * l4 + u5 * l5) := by
    nlinarith [hParetoScaled, hy4, hy5, hE4, hE5Scaled]
  have hcore : 0 < Q + u4 * l4 + u5 * l5 := by
    by_contra hnot
    have hnonpos : Q + u4 * l4 + u5 * l5 ≤ 0 := le_of_not_gt hnot
    have hmulnonpos := mul_nonpos_of_nonneg_of_nonpos (le_of_lt hd) hnonpos
    linarith
  nlinarith [hDerivative]

#print axioms block45_joint_pareto_of_two_certificates
#print axioms pareto_coefficients_positive
#print axioms pareto_r0_identity
#print axioms pareto_r1_identity
#print axioms quarter_checker_r0_reduces
#print axioms quarter_checker_r1_reduces
#print axioms anisotropic_margin_beats_scalar_iff
#print axioms quarter_first_exit_inward_of_pareto

end RouteBP5ParetoBridge
