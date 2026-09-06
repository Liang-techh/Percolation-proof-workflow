import FrameRecursion

set_option autoImplicit false

namespace RouteBRealDHStep

noncomputable section

open RouteBB45Fourier
open RouteBB45FrameRecursion

abbrev RealFrame := Matrix (Fin 4) (Fin 4) ℝ

def realDHStep (ct st ca sa a d : ℝ) (i j : Fin 4) : ℝ :=
  match i.1, j.1 with
  | 0, 0 => ct
  | 0, 1 => -st * ca
  | 0, 2 => st * sa
  | 0, 3 => ct * a
  | 1, 0 => st
  | 1, 1 => ct * ca
  | 1, 2 => -ct * sa
  | 1, 3 => st * a
  | 2, 0 => 0
  | 2, 1 => sa
  | 2, 2 => ca
  | 2, 3 => d
  | 3, 0 => 0
  | 3, 1 => 0
  | 3, 2 => 0
  | 3, 3 => 1
  | _, _ => 0

def routeBRealCos (k : Fin 6) (q : ℝ) : ℝ :=
  match k.1 with
  | 0 => Real.cos q
  | 1 => Real.sin q
  | 2 => -Real.sin q
  | 3 => Real.cos q
  | 4 => Real.cos q
  | 5 => Real.cos q
  | _ => 0

def routeBRealSin (k : Fin 6) (q : ℝ) : ℝ :=
  match k.1 with
  | 0 => Real.sin q
  | 1 => -Real.cos q
  | 2 => Real.cos q
  | 3 => Real.sin q
  | 4 => Real.sin q
  | 5 => Real.sin q
  | _ => 0

def routeBRealStepMatrix (k : Fin 6) (q : ℝ) : RealFrame :=
  fun i j => realDHStep (routeBRealCos k q) (routeBRealSin k q)
    (routeBCosAlpha k).re (routeBSinAlpha k).re
    (routeBA k).re (routeBD k).re i j

theorem routeB_real_phase_values (q : ℝ) :
    routeBRealCos 0 q = Real.cos q ∧
    routeBRealCos 1 q = Real.sin q ∧
    routeBRealCos 2 q = -Real.sin q ∧
    routeBRealSin 0 q = Real.sin q ∧
    routeBRealSin 1 q = -Real.cos q ∧
    routeBRealSin 2 q = Real.cos q := by
  simp [routeBRealCos, routeBRealSin]

/-- Exact real/complex bridge for every one of the six Route-B DH steps.

    This is still an ideal-real theorem: Julia's Float64 trigonometric and
    matrix operations are a separate enclosure/source-semantics obligation. -/
theorem routeB_step_complex_eq_ofReal (k : Fin 6) (q : ℝ) :
    routeBStepMatrix k q =
      fun i j => (routeBRealStepMatrix k q i j : ℂ) := by
  have hp := fourier_phase_bridge q
  rcases hp with ⟨h1c, hIc, hmc, h1s, hIs, hms⟩
  funext i j
  fin_cases k <;> fin_cases i <;> fin_cases j <;>
    simp [routeBStepMatrix, routeBRealStepMatrix, realDHStep,
      routeBRealCos, routeBRealSin, fourierDHStep, dhStep,
      routeBOffsetPhase, routeBCosAlpha, routeBSinAlpha, routeBA, routeBD,
      h1c, hIc, hmc, h1s, hIs, hms]

theorem routeB_step_real_entries (k : Fin 6) (q : ℝ) (i j : Fin 4) :
    (routeBStepMatrix k q i j).re = routeBRealStepMatrix k q i j := by
  have h := congrFun (congrFun (routeB_step_complex_eq_ofReal k q) i) j
  rw [h]
  simp

#print axioms routeB_real_phase_values
#print axioms routeB_step_complex_eq_ofReal
#print axioms routeB_step_real_entries

end
end RouteBRealDHStep
