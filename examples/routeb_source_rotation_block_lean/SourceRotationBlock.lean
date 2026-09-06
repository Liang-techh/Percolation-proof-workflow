import RouteBRotationSpecialization

set_option autoImplicit false

namespace RouteBSourceRotationBlock

noncomputable section

open RouteBDHRotationOrthogonality
open RouteBRotationSpecialization
open RouteBRealDHStep
open RouteBB45Fourier

abbrev Mat3 := Matrix (Fin 3) (Fin 3) ℝ

def embed3 (i : Fin 3) : Fin 4 :=
  ⟨i.val, by omega⟩

def sourceRotationBlock (k : Fin 6) (q : ℝ) : Mat3 :=
  fun i j => routeBRealStepMatrix k q (embed3 i) (embed3 j)

theorem source_rotation_block_eq_dhRotation (k : Fin 6) (q : ℝ) :
    sourceRotationBlock k q =
      dhRotation (routeBRealCos k q) (routeBRealSin k q)
        (routeBCosAlpha k).re (routeBSinAlpha k).re := by
  funext i j
  fin_cases k <;> fin_cases i <;> fin_cases j <;>
    simp [sourceRotationBlock, embed3, routeBRealStepMatrix,
      realDHStep, dhRotation]

theorem source_rotation_block_rows_orthogonal (k : Fin 6) (q : ℝ) :
    ∀ i j : Fin 3, ∑ a : Fin 3,
      sourceRotationBlock k q i a * sourceRotationBlock k q j a =
      if i = j then 1 else 0 := by
  rw [source_rotation_block_eq_dhRotation k q]
  exact routeB_real_step_rotation_rows_orthogonal k q

#print axioms source_rotation_block_eq_dhRotation
#print axioms source_rotation_block_rows_orthogonal

end
end RouteBSourceRotationBlock
