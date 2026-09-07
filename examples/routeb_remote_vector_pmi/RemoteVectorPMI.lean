import Mathlib.Data.Real.Basic
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBRemoteVectorPMI

noncomputable section

/-!
Two-dimensional, division-free Schur/PMI seam for the Route-B remote action.
The remote residual is kept as a vector so the operator bound is charged once
through a squared norm, rather than once per component.
-/

theorem vector_schur_nonnegative
    (p d x1 x2 r1 r2 y : ℝ) (hp : 0 < p)
    (hbudget : r1 ^ 2 + r2 ^ 2 ≤ p * d * y ^ 2) :
    0 ≤ p * (x1 ^ 2 + x2 ^ 2) +
      2 * (x1 * r1 + x2 * r2) + d * y ^ 2 := by
  have hgap : 0 ≤ p * d * y ^ 2 - (r1 ^ 2 + r2 ^ 2) :=
    sub_nonneg.mpr hbudget
  have hsquares : 0 ≤ (p * x1 + r1) ^ 2 + (p * x2 + r2) ^ 2 :=
    add_nonneg (sq_nonneg _) (sq_nonneg _)
  have hmul :
      0 ≤ p * (p * (x1 ^ 2 + x2 ^ 2) +
        2 * (x1 * r1 + x2 * r2) + d * y ^ 2) := by
    calc
      0 ≤ (p * x1 + r1) ^ 2 + (p * x2 + r2) ^ 2 + hgap :=
        add_nonneg hsquares hgap
      _ = p * (p * (x1 ^ 2 + x2 ^ 2) +
          2 * (x1 * r1 + x2 * r2) + d * y ^ 2) := by ring
  exact (mul_nonneg_iff_of_pos_left hp).mp hmul

theorem vector_pmi_nonnegative_of_mass_enclosure
    (p d x1 x2 r1 r2 y k mass beta : ℝ)
    (hp : 0 < p)
    (hk : 0 ≤ k)
    (hremote : r1 ^ 2 + r2 ^ 2 ≤ k * mass)
    (hmass : mass ≤ beta ^ 2 * y ^ 2)
    (hschur : k * beta ^ 2 ≤ p * d) :
    0 ≤ p * (x1 ^ 2 + x2 ^ 2) +
      2 * (x1 * r1 + x2 * r2) + d * y ^ 2 := by
  apply vector_schur_nonnegative p d x1 x2 r1 r2 y hp
  have hscaled : k * mass ≤ k * (beta ^ 2 * y ^ 2) :=
    mul_le_mul_of_nonneg_left hmass hk
  calc
    r1 ^ 2 + r2 ^ 2 ≤ k * mass := hremote
    _ ≤ k * (beta ^ 2 * y ^ 2) := hscaled
    _ ≤ p * d * y ^ 2 := by
      exact mul_le_mul_of_nonneg_right hschur (sq_nonneg y)

#print axioms vector_schur_nonnegative
#print axioms vector_pmi_nonnegative_of_mass_enclosure

end
end RouteBRemoteVectorPMI
