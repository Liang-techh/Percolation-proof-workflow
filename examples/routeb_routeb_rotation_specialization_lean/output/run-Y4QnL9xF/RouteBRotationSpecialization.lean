import DHRotationOrthogonality
import RealDHStep

set_option autoImplicit false

namespace RouteBRotationSpecialization

noncomputable section

open RouteBDHRotationOrthogonality
open RouteBRealDHStep
open RouteBB45Fourier

theorem routeB_real_step_rotation_rows_orthogonal
    (k : Fin 6) (q : ℝ) :
    ∀ i j : Fin 3, ∑ a : Fin 3,
      dhRotation (routeBRealCos k q) (routeBRealSin k q)
        (routeBCosAlpha k).re (routeBSinAlpha k).re i a *
      dhRotation (routeBRealCos k q) (routeBRealSin k q)
        (routeBCosAlpha k).re (routeBSinAlpha k).re j a =
      if i = j then 1 else 0 := by
  apply dh_rotation_rows_orthogonal
  · fin_cases k <;>
      simp [routeBRealCos, routeBRealSin] <;>
      nlinarith [Real.sin_sq_add_cos_sq q]
  · fin_cases k <;>
      norm_num [routeBCosAlpha, routeBSinAlpha]

#print axioms routeB_real_step_rotation_rows_orthogonal

end
end RouteBRotationSpecialization
