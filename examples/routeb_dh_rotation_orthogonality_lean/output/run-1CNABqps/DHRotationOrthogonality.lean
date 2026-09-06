import Mathlib

set_option autoImplicit false

namespace RouteBDHRotationOrthogonality

noncomputable section

abbrev V := Fin 3
abbrev Mat3 := Matrix V V ℝ

def dhRotation (ct st ca sa : ℝ) : Mat3 := fun i j =>
  match i.val, j.val with
  | 0, 0 => ct
  | 0, 1 => -st * ca
  | 0, 2 => st * sa
  | 1, 0 => st
  | 1, 1 => ct * ca
  | 1, 2 => -ct * sa
  | 2, 0 => 0
  | 2, 1 => sa
  | 2, 2 => ca
  | _, _ => 0

theorem dh_rotation_rows_orthogonal
    (ct st ca sa : ℝ)
    (hct : ct * ct + st * st = 1)
    (hca : ca * ca + sa * sa = 1) :
    ∀ i k : V, ∑ a : V, dhRotation ct st ca sa i a *
      dhRotation ct st ca sa k a = if i = k then 1 else 0 := by
  intro i k
  fin_cases i <;> fin_cases k <;>
    simp [dhRotation, Fin.sum_univ_succ] <;>
    ring_nf at * <;>
    first
    | ring
    | linear_combination hct + st ^ 2 * hca
    | linear_combination hct + ct ^ 2 * hca
    | linear_combination hca
    | linear_combination (ct * st) * hca

#print axioms dh_rotation_rows_orthogonal

end
end RouteBDHRotationOrthogonality
