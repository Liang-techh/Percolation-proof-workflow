import Mathlib.Data.Real.Basic
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBRemotePMIComposition

noncomputable section

/-!
Composition seam for the P4 remote-action repair.  The two physical/source
premises are intentionally parameters: this file proves only that a bound on
the remote action in a full-state mass budget and a mass-to-PMI-scale bound
compose into the scalar Schur envelope consumed by P4.
-/

theorem residual_sq_le_of_mass_and_scale
    (residual kappa mass beta y : ℝ)
    (hremote : residual ^ 2 ≤ kappa ^ 2 * mass)
    (hmass : mass ≤ beta ^ 2 * y ^ 2) :
    residual ^ 2 ≤ (kappa * beta) ^ 2 * y ^ 2 := by
  have hk : 0 ≤ kappa ^ 2 := sq_nonneg kappa
  have hscaled : kappa ^ 2 * mass ≤ kappa ^ 2 * (beta ^ 2 * y ^ 2) :=
    mul_le_mul_of_nonneg_left hmass hk
  calc
    residual ^ 2 ≤ kappa ^ 2 * mass := hremote
    _ ≤ kappa ^ 2 * (beta ^ 2 * y ^ 2) := hscaled
    _ = (kappa * beta) ^ 2 * y ^ 2 := by ring

theorem pmi_nonnegative_of_mass_scaled_enclosure
    (p d epsilon residual x y kappa mass beta : ℝ)
    (hepsilon : 0 < epsilon)
    (hremote : residual ^ 2 ≤ kappa ^ 2 * mass)
    (hmass : mass ≤ beta ^ 2 * y ^ 2)
    (hprefix : epsilon ≤ p)
    (hschur : (kappa * beta) ^ 2 / epsilon ≤ d) :
    0 ≤ p * x ^ 2 + 2 * x * residual + d * y ^ 2 := by
  have hresidual := residual_sq_le_of_mass_and_scale
    residual kappa mass beta y hremote hmass
  have hgap : 0 ≤ (kappa * beta) ^ 2 * y ^ 2 - residual ^ 2 :=
    sub_nonneg.mpr hresidual
  have hsquare : 0 ≤ (epsilon * x + residual) ^ 2 := sq_nonneg _
  have hscaled :
      0 ≤ epsilon *
        (epsilon * x ^ 2 + 2 * x * residual +
          (kappa * beta) ^ 2 / epsilon * y ^ 2) := by
    calc
      0 ≤ (epsilon * x + residual) ^ 2 +
          ((kappa * beta) ^ 2 * y ^ 2 - residual ^ 2) :=
        add_nonneg hsquare hgap
      _ = epsilon *
          (epsilon * x ^ 2 + 2 * x * residual +
            (kappa * beta) ^ 2 / epsilon * y ^ 2) := by
        field_simp [ne_of_gt hepsilon]
        ring
  have hcore :
      0 ≤ epsilon * x ^ 2 + 2 * x * residual +
        (kappa * beta) ^ 2 / epsilon * y ^ 2 :=
    (mul_nonneg_iff_of_pos_left hepsilon).mp hscaled
  have hx : 0 ≤ (p - epsilon) * x ^ 2 :=
    mul_nonneg (sub_nonneg.mpr hprefix) (sq_nonneg x)
  have hy : 0 ≤ (d - (kappa * beta) ^ 2 / epsilon) * y ^ 2 :=
    mul_nonneg (sub_nonneg.mpr hschur) (sq_nonneg y)
  linarith

#print axioms residual_sq_le_of_mass_and_scale
#print axioms pmi_nonnegative_of_mass_scaled_enclosure

end
end RouteBRemotePMIComposition
