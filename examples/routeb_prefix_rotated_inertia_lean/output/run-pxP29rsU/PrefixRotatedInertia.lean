import IsotropicInertia
import RotationPrefixOrthogonality

set_option autoImplicit false

namespace RouteBPrefixRotatedInertia

noncomputable section

open RouteBIsotropicInertia
open RouteBMatrixOrthogonalityClosure
open RouteBRotationPrefixOrthogonality

abbrev V := Fin 3
abbrev Mat3 := Matrix V V ℝ

theorem prefix_rotated_isotropic_eq
    (s : Fin 6 → Mat3) (hs : ∀ k, rowOrtho (s k))
    (i : Fin 7) (scalar : ℝ) :
    rotatedIsotropic (prefixAt s i) scalar = scalarIdentity scalar := by
  apply rotated_isotropic_eq
  exact prefixAt_rowOrtho s hs i

theorem prefix_rotated_isotropic_entry
    (s : Fin 6 → Mat3) (hs : ∀ k, rowOrtho (s k))
    (i : Fin 7) (scalar : ℝ) (a b : V) :
    rotatedIsotropic (prefixAt s i) scalar a b =
      if a = b then scalar else 0 := by
  rw [prefix_rotated_isotropic_eq s hs i scalar]
  rfl

#print axioms prefix_rotated_isotropic_eq
#print axioms prefix_rotated_isotropic_entry

end
end RouteBPrefixRotatedInertia
