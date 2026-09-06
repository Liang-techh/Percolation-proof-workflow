import MatrixOrthogonalityClosure

set_option autoImplicit false

namespace RouteBRotationPrefixOrthogonality

noncomputable section

open RouteBMatrixOrthogonalityClosure

abbrev V := Fin 3
abbrev Mat3 := Matrix V V ℝ

def prefixAt (s : Fin 6 → Mat3) (i : Fin 7) : Mat3 :=
  match i.val with
  | 0 => 1
  | 1 => 1 * s 0
  | 2 => (1 * s 0) * s 1
  | 3 => ((1 * s 0) * s 1) * s 2
  | 4 => (((1 * s 0) * s 1) * s 2) * s 3
  | 5 => ((((1 * s 0) * s 1) * s 2) * s 3) * s 4
  | 6 => (((((1 * s 0) * s 1) * s 2) * s 3) * s 4) * s 5
  | _ => 1

theorem rowOrtho_one : rowOrtho (1 : Mat3) := by
  apply (rowOrtho_iff_gram (1 : Mat3)).mpr
  simp

theorem prefixAt_rowOrtho
    (s : Fin 6 → Mat3) (hs : ∀ k, rowOrtho (s k)) :
    ∀ i : Fin 7, rowOrtho (prefixAt s i) := by
  intro i
  fin_cases i
  · exact rowOrtho_one
  · simpa [prefixAt] using rowOrtho_mul rowOrtho_one (hs 0)
  · simpa [prefixAt] using
      rowOrtho_mul (rowOrtho_mul rowOrtho_one (hs 0)) (hs 1)
  · simpa [prefixAt] using
      rowOrtho_mul (rowOrtho_mul (rowOrtho_mul rowOrtho_one (hs 0)) (hs 1)) (hs 2)
  · simpa [prefixAt] using
      rowOrtho_mul
        (rowOrtho_mul (rowOrtho_mul (rowOrtho_mul rowOrtho_one (hs 0)) (hs 1)) (hs 2))
        (hs 3)
  · simpa [prefixAt] using
      rowOrtho_mul
        (rowOrtho_mul
          (rowOrtho_mul (rowOrtho_mul (rowOrtho_mul rowOrtho_one (hs 0)) (hs 1)) (hs 2))
          (hs 3))
        (hs 4)
  · simpa [prefixAt] using
      rowOrtho_mul
        (rowOrtho_mul
          (rowOrtho_mul
            (rowOrtho_mul (rowOrtho_mul (rowOrtho_mul rowOrtho_one (hs 0)) (hs 1)) (hs 2))
            (hs 3))
          (hs 4))
        (hs 5)

#print axioms rowOrtho_one
#print axioms prefixAt_rowOrtho

end
end RouteBRotationPrefixOrthogonality
