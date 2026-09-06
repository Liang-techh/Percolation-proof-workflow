import Mathlib

set_option autoImplicit false

namespace RouteBMatrixOrthogonalityClosure

noncomputable section

abbrev V := Fin 3
abbrev Mat3 := Matrix V V ℝ

def rowOrtho (R : Mat3) : Prop :=
  ∀ i k : V, ∑ a : V, R i a * R k a = if i = k then 1 else 0

theorem rowOrtho_iff_gram (R : Mat3) :
    rowOrtho R ↔ R * R.transpose = (1 : Mat3) := by
  constructor
  · intro h
    funext i k
    simpa [Matrix.mul_apply, Matrix.transpose_apply] using h i k
  · intro h i k
    have hik := congrFun (congrFun h i) k
    simpa [Matrix.mul_apply, Matrix.transpose_apply] using hik

theorem rowOrtho_mul {R S : Mat3}
    (hR : rowOrtho R) (hS : rowOrtho S) :
    rowOrtho (R * S) := by
  rw [rowOrtho_iff_gram]
  have hRgram : R * R.transpose = (1 : Mat3) :=
    (rowOrtho_iff_gram R).mp hR
  have hSgram : S * S.transpose = (1 : Mat3) :=
    (rowOrtho_iff_gram S).mp hS
  calc
    (R * S) * (R * S).transpose =
        R * (S * S.transpose) * R.transpose := by
      rw [Matrix.transpose_mul]
      simp only [Matrix.mul_assoc]
    _ = R * (1 : Mat3) * R.transpose := by rw [hSgram]
    _ = R * R.transpose := by simp
    _ = (1 : Mat3) := hRgram

#print axioms rowOrtho_iff_gram
#print axioms rowOrtho_mul

end
end RouteBMatrixOrthogonalityClosure
